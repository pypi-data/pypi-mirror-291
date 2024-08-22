from typing import Protocol
from typing import Callable
from typing import Type
from typing import ClassVar


# Maps the app_name and a clas containing required args for this app render type.
# The class registered here will be instantiated from the CeonRenderJob.app_render_settings dict.
render_apps: dict[str, Type] = {}


# Base class for creating classes which store all args required to execute
# a rendering job for a particular app.
# This is provider agnostic, will be passed to and handled by the providers.
class AppRenderJob(Protocol):
    app_type: ClassVar[str]  # The name used to identify this app.


# EXAMPLE usage to support rendering jobs in Houdini:
# class AppRenderJobHou(AppRenderJob):
#     app_type: ClassVar[str] = "hou"

#     hipfile: str
#     target_node: str
#     ...

# would contain all args required to execute a houdini render, regardless of provider used.


def register(app_render_settings_class: Type):
    """Register a new render app"""
    app_name = app_render_settings_class.app_type
    if app_name in render_apps.keys():
        raise ValueError(
            f"Cannot register render app because a app with name '{app_name}' already exists"
        )
    render_apps[app_name] = app_render_settings_class


def unregister(render_app_name: str):
    """Unregister a render app"""
    render_apps.pop(render_app_name, None)


def get_app_settings_cls(render_app_name: str):
    """Fetch a render app by their registered name"""
    return render_apps[render_app_name]
