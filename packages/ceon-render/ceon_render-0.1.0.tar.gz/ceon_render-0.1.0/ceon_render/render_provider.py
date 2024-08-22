from typing import Protocol
from typing import Callable
from ceon_render.render_app import AppRenderJob

# from ceon_render.render_job import CeonRenderJob


class RenderProviderAppHandler(Protocol):
    """Handles preparing and submitting a job for a particular app"""

    def submit_job(self):
        """Handles a single job submission for a particular app type"""


class RenderProviderConfig(Protocol):
    """Stores configuration settings for the render provider, such as batch_size or instance type."""

    pass


class RenderProvider(Protocol):
    """Handles submitting, tracking and downloading of render jobs to a particular provider."""

    name: str
    app_handlers: dict[str, RenderProviderAppHandler]

    # def submit_pipeline(ceon_render_job):
    #     """Submit a render pipline to the provider, expecting the provider to handle
    #     job dependencies / chaining"""

    def submit_job(
        self,
        app_render_job: AppRenderJob,
        render_provider_config: RenderProviderConfig | None = None,
    ) -> str:
        """Submit a render job to the provider
        ceon_render_job: A CeonRenderJob instance containing all information about the render job to be executed.
        Usually gets converted to a relevant class instance for the particular provider/app.
        render_provider_config: An optional dict config to modify the provider behaviour (example: Frame batch size)

        Return: An id that is used by the provider to track the job progress and download results.
        """

    def check_for_completion(self, provider_job_id: str):
        """
        Returns:
        - True if the job completed successfully
        - False if the job is in progress.
        - Raise a custom error if the job failed.
        """

    def download_job_outputs(self, provider_job_id: str):
        """Download the output files for the target job_id"""

    def register_app_handler(
        self, app_name: str, app_handler: RenderProviderAppHandler
    ):
        if app_name in self.app_handlers.keys():
            raise KeyError(
                f"Cannot register app_handler in {self.__class__.__name__} because app '{app_name}' already has a registered handler."
            )
        self.app_handlers[app_name] = app_handler

    def supported_apps(self) -> list[str]:
        return list(self.app_handlers.keys())

    # def upload():
    #     """Upload files to the provider's storage"""


render_providers: dict[str, RenderProvider] = {}


def register(render_provider: RenderProvider):
    """Register a new render provider"""
    if render_provider.name in render_providers.keys():
        raise ValueError(
            f"Cannot register render provider because a provider with name '{render_provider.name}' already exists"
        )
    render_providers[render_provider.name] = render_provider


def unregister(render_provider_name: str):
    """Unregister a render provider"""
    render_providers.pop(render_provider_name, None)


def get(render_provider_name: str):
    """Fetch a render provider by their registered name"""
    return render_providers[render_provider_name]


def list_providers() -> list[str]:
    return list(render_providers.keys())
