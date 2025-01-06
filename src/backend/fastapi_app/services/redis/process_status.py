from enum import Enum, auto


class ProcessStatus(Enum):
    EXTRACTING = auto()
    CHUNKING = auto()
    SUMMARIZING = auto()
    COMPLETED = auto()
