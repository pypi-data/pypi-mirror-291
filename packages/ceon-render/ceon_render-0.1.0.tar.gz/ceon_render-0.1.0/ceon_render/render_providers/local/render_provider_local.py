import requests
import json
from typing import ClassVar
from abc import ABC
from dataclasses import dataclass, field

from ceon_render.render_provider import (
    RenderProvider,
    RenderProviderAppHandler,
)

# from ceon_render.render_job import CeonRenderJob
from ceon_render import render_app

import render_apps

from . import houdini
from . import ffmpeg


class RenderProviderLocal(RenderProvider):
    name = "local"
    app_handlers = {
        "hou": houdini.RenderProviderAppHandlerHou(),
        "ffmpeg": ffmpeg.RenderProviderAppHandlerFFmpeg(),
    }

    def __init__(self, api_url):
        self.api_url = api_url

    def submit_job(
        self,
        # job_uuid: str,
        app_render_job: render_app.AppRenderJob,
        render_provider_config: dict | None = None,
    ):
        print("SUBMITING via local render provider...")

        # Convert to app render job instances
        print(f"Local server: {self.api_url}")
        try:
            app_handler = self.app_handlers[app_render_job.app_type]
        except KeyError:
            # Todo add UnsupportedAppError exceiption to ceon_render module
            raise Exception(
                f"Unsupported app type '{app_render_job.app_type}' for provider '{self.__class__.__name__}'"
            )
        # local_render_job = app_handler.ceon_to_local(ceon_render_job)
        print(f"Got app handler: {app_handler}")
        payload = app_handler.create_payload(app_render_job)
        app_endpoint = app_handler.endpoint(self.api_url)
        _post_request(app_endpoint, payload)

    def submit_jobs(
        self, job_uuid: str, app_render_jobs: list[render_app.AppRenderJob]
    ):
        """
        Submit multiple render jobs to the render server.
        """
        print(f"Received render jobs: {app_render_jobs}")
        print(f"Submitting job to local render server: {job_uuid}")
        print(f"Local server: {self.api_url}")
        raise NotImplementedError
        self._submit_pipeline(job_uuid, render_jobs_local, self.api_url)

    def _submit_pipeline(
        self,
        job_uuid: str,
        render_jobs: list[render_app.AppRenderJob],
        api_url: str,
    ):
        """
        Send a 'pipeline' submission to the local render server.
        Pipeline submissions include multiple jobs.
        """
        print("Preparing pipeline submission for local rendering server ...")
        # log_dir = f"{JobPaths(job_uuid).logs}/local_rendering"
        log_dir = "/mnt/FileStorage/Dayne/tmp"

        payload_jobs = []
        for render_job in render_jobs:
            app_handler = self.app_handlers[render_job.app_type]
            # local_render_job = app_handler.ceon_to_local(render_job)
            payload = app_handler.create_payload(local_render_job)
            pipeline_payload_job = {
                "app": render_job.app_type,
                "payload": payload,
            }
            payload_jobs.append(pipeline_payload_job)
        payload = {"render_jobs": payload_jobs, "log_dir": log_dir}

        endpoint = f"{api_url}/render/pipeline"
        _post_request(endpoint, payload)


def _post_request(url, payload):
    print(f"Posting request to: {url}")
    print(f"payload: {json.dumps(payload, indent=2)}")
    res = requests.post(url, json=payload)
    print(f"Got res: {res}")
    if res.ok:
        print(f"Got res.json(): {res.json()}")
    else:
        print(f"Failed to submit render. res: {res}")
        raise Exception(f"Got not-ok response ffrom render server: {res}")
