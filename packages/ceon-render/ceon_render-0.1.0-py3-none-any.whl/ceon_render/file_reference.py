from dataclasses import dataclass
from enum import StrEnum, auto


class CeonFileSourceType(StrEnum):
    """Describes where the target file should be found.
    PROJECT: File path relative to the CEON project dir.
    JOB_INPUT: File path relative to the job inputs dir.
    JOB_OUTPUT: File path relative to the job outputs dir.
    TASK_INPUT: Target is a task name. Resolve the input file of the targeted task.
    TASK_OUTPUT: Target is a task name. Resolve the output file of the targeted task.
    ABSOLUTE: An absolute file path that points to a file on disk.
    """

    PROJECT = auto()
    JOB_INPUT = auto()
    JOB_OUTPUT = auto()
    TASK_INPUT = auto()
    TASK_OUTPUT = auto()
    ABSOLUTE = auto()


@dataclass
class CeonFileReference:
    """
    Contains the information used to identify a target file.
    target: The value of the file to look for. This could be a file path or a task name depending on the file_source type.
    file_source: A CeonFileSourceType enum describing where to search for the file. This allows lookup of files based on
    job or task inputs/outputs.
    """

    target: str
    file_source: CeonFileSourceType = CeonFileSourceType.ABSOLUTE
