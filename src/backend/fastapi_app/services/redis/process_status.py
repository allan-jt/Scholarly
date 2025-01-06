from enum import Enum, auto


class ProcessStatus(Enum):
    PROCCESSING = auto()
    COMPLETED = auto()
    FAILED = auto()
