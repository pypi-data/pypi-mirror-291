from enum import Enum, auto


class SaveType(Enum):
    MOBILE = auto()
    PC = auto()
    AUTODETECT = auto()

class UpgradeAvailability(Enum):
    NOTAVAILABLE = 0
    AVAILABLE = 2
    BOUGHT = 3
    UNKNOWN = 1

class AchivementsUnlock(Enum):
    LOCKED = 0
    UNLOCKED = 1