from dataclasses import dataclass
from typing import ClassVar


@dataclass
class AppRenderJobFFmpeg:
    """Contains all information to build an ffmpeg command"""

    app_type: ClassVar[str] = "ffmpeg"

    input_file: str
    output_file: str
    input_args: str = ""
    output_args: str = ""
