import requests
import json
import subprocess
import time
from typing import ClassVar
from abc import ABC
from dataclasses import dataclass, field

from ciocore import conductor_submit
from ciocore import api_client

from ceon_render.render_provider import (
    RenderProvider,
    RenderProviderAppHandler,
)
from ceon_render.render_provider import RenderProviderConfig
from ceon_render import render_app
from ceon_render import JobProgress

from .app_handlers import RenderProviderConductorAppHandlerHou

# from . import ffmpeg


@dataclass
class RenderProviderConductorConfig(RenderProviderConfig):
    batch_size: int  # Num frames to run per instance
    # Files to upload. Paths can be folders.
    upload_paths: list[str] = field(default_factory=list)
    job_title: str = ""


class RenderProviderConductor(RenderProvider):
    name = "conductor"
    app_handlers = {"hou": RenderProviderConductorAppHandlerHou()}
    default_config = RenderProviderConductorConfig(
        batch_size=5
    )  # Default config

    def __init__(self):
        pass

    def submit_job(
        self,
        # job_uuid: str,
        app_render_job: render_app.AppRenderJob,
        render_provider_config: RenderProviderConductorConfig | None = None,
    ) -> str:
        print("SUBMITING via conductor render provider...")
        if not render_provider_config:
            render_provider_config = self.default_config

        # Prepare payload
        app_handler = self.app_handlers[app_render_job.app_type]
        print(f"Got app handler: {app_handler}")
        payload = app_handler.create_payload(
            app_render_job, render_provider_config=render_provider_config
        )
        print("Created payload:")
        print(json.dumps(payload, indent=2))

        # Submit to Conductor
        submission = conductor_submit.Submit(payload)
        response, response_code = submission.main()
        print(response_code)
        print(json.dumps(response))
        job_id = response["jobid"]
        return job_id

    def get_job_progress(self, job_id: int | str) -> JobProgress:
        """Fetch the job progress from Conductor and return a JobProgress instance"""
        print(f"Fetching job progress for conductor job: {job_id}")
        res = api_client.get_jobs(job_id)
        # print(json.dumps(res, indent=2))
        if not res:
            raise Exception(f"Did not find job for Conductor job id: {job_id}")

        status = res[0]["status"]
        # List of job statuses which indicate that the job has ended (regardless of outcome)
        ended_statuses = [
            "success",
            "downloaded",
            "reviewed",
            "killed",
            "failed",
        ]
        # Other job statuses, for reference.
        running_statuses = ["sync_pending", "syncing", "pending", "running"]

        # Total number of tasks for this job.
        num_tasks = int(res[0]["tasks"])

        num_running = int(res[0]["running"])
        num_holding = int(res[0]["holding"])
        num_pending = int(res[0]["pending"])

        # Will preempted be marked as failed by conductor?
        num_preempted = int(res[0]["preempted"])
        num_downloaded = int(res[0]["downloaded"])
        num_reviewed = int(res[0]["reviewed"])

        num_success = int(res[0]["success"])
        num_failed = int(res[0]["failed"])
        num_killed = int(res[0]["killed"])

        is_ended = status in ended_statuses

        print(f"{status=}")
        print(f"{num_tasks=}")
        print(f"{num_running=}")
        print(f"{num_success=}")
        print(f"{num_failed=}")
        print(f"{num_killed=}")
        print(f"{num_preempted=}")

        is_success = num_tasks == num_success
        is_failed = is_ended and not is_success

        return JobProgress(
            ended=is_ended, failed=is_failed, success=is_success
        )

    def wait_for_job_completion(self, job_id: str, poll_interval_seconds=30):
        """
        A blocking method that waits for a render to complete.
        job_id: The job_id of the Conductor job.
        poll_interval: The number of seconds between checks
        """
        job_status = self.get_job_progress(job_id)
        while not job_status.ended:
            time.sleep(poll_interval_seconds)
            job_status = self.get_job_progress(job_id)
            print(f"Got job status: {job_status}")
        print(f"Job {job_id} ended.")
        return

    def download_job_outputs(self, job_id):
        cmd = ["conductor", "downloader", "--job_id", str(job_id)]
        subprocess.run(cmd)

    def submit_jobs(
        self, job_uuid: str, app_render_jobs: list[render_app.AppRenderJob]
    ):
        """
        Submit multiple render jobs to the render server.
        """
        raise NotImplementedError
