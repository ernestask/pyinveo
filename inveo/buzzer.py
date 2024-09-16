from enum import Enum

ADDRESS = 0x5

class Mode(int, Enum):
    OFF = 0,
    ON = 1,
    ON_READ = 2,
