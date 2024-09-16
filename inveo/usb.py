from enum import Enum

ADDRESS = 0x1

class Mode(int, Enum):
    KEYBOARD = 1,
    CDC = 2,
