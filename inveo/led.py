from enum import Enum

ADDRESS_1 = 0x2
ADDRESS_2 = 0x3
ADDRESS_3 = 0x4

class Mode(int, Enum):
    OFF = 0,
    ON = 1,
    ON_READ = 2,
    ON_PROXIMITY = 3,
