from uuid import uuid4
from dataclasses import dataclass, field

from .file_reference import CeonFileReference


@dataclass(kw_only=True)
class CeonRenderPipelineJob:
    """
    Defines a job to be run as part of a pipeline.
    Stores only the logistical information relevant to the pipeline (target app/node/file to render, ffmpeg cmd to execute etc)
    It is agnostic of specific render settings/implementtions such as resolution, frame ranges, batch size etc.
    """

    job_name: str  # Human readable identifier for this job.
    app_type: str
    app_version: str
    app_render_settings: dict  # Args required for this particular app_type

    job_input: CeonFileReference  # Input file
    job_output: str  # Output file

    # Store other render jobs which must be completed before this one can start
    job_dependencies: list[str] = field(default_factory=list)
    job_id: str = field(default_factory=lambda: uuid4().hex)

    def __post_init__(self):
        if not isinstance(self.job_input, CeonFileReference):
            raise ValueError("job_input must be a CeonFileReference type")

    def __str__(self):
        msg = f"<{self.__class__.__name__} '{self.job_name}' ({self.app_type} OUT:'{self.job_output}')>"
        return msg

    def __repr__(self):
        return self.__str__()


@dataclass
class CeonRenderPipeline:
    """
    output_job: The name of the pipeline_job output to be passed back to the user.
    output_extras: An optional list of additional task names whose outputs will also be passed back to the user.
    """

    pipeline_jobs: list[CeonRenderPipelineJob]
    output_job: str
    output_extras: list[str] = field(default_factory=list)
    # output_extras: list[CeonRenderPipelineExtraOutput] = field(default_factory=list)

    def __str__(self):
        job_names = [
            pipeline_job.job_name for pipeline_job in self.pipeline_jobs
        ]
        msg = f"<{self.__class__.__name__} jobS:{job_names} OUT:'{self.output_job}')>"
        return msg

    def __repr__(self):
        return self.__str__()
