from enum import IntEnum

from helper.struct import *
from effects.base import Color

@dataclass
class Zone(Struct):
    mode: UChar
    color: Color
    # bitfield of flags for speed and brightness
    meta_flags: UChar
    # seems unused, as unaffected static green
    color2: Color
    color_flags: UChar = 0
    padding: UChar = 0

class ZoneMode(IntEnum):
    OFF = 0
    STATIC = 1
    BREATHING = 2
    FLASHING = 3
    DOUBLE_FLASHING = 4
    LIGHTNING = 5
    RAINBOW = 15
    COLOR_CHANGE = 22
    COLOR_WAVE = 23
    RAINBOW_WAVE = 26