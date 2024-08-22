# Provider agnostic classes that store all relevant args required to execute
# a job for a particular app type.

# To make the app args available for providers to consume, these classes should
# be registered via the ceon_render.render_app.register()
# E.g. ceon_render.render_app.register(AppRenderJobHou)
from dataclasses import dataclass, field
from typing import ClassVar, Self, Type
from enum import StrEnum, auto

# from ceon_render.render_pipeline import CeonRenderPipelineJob


class HoudiniRenderType(StrEnum):
    KARMA_CPU = auto()
    KARMA_GPU = auto()
    REDSHIFT = auto()
    SIM = auto()


@dataclass
class AppRenderJobHou:
    """Contains all args required to execute a single houdini render.
    This is the job definition that can be passed to any provider which supports Houdini.
    Individual render providers may require only subsets of this information.
    """

    app_type: ClassVar[str] = "hou"

    hipfile: str  # Path to the hipfile
    target_node: str  # The ROP node inside the hipfile
    node_type: HoudiniRenderType
    output_file: str  # Can include houdini vars e.g. $HIP, $F4
    frame_range: tuple[int, int, int]  # start, end, inc
    frame_dimensions: tuple[int, int]  # width, height
    env: list[str] = field(
        default_factory=list
    )  # [ENV_TO_SET=Value, ANOTHER=Val2]
