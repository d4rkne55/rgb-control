from typing import NamedTuple

from helper.struct import *

@dataclass
class Color(Struct):
    r: UChar
    g: UChar
    b: UChar

    @staticmethod
    def interpolate(start, end, percentage):
        values = [round((b - a) * percentage + a) for a, b in zip(start, end)]

        return Color(*values)

class Effect:
    def __init__(self, colors, interval_time, interpolate):
        self.colors = colors
        self.interval = interval_time
        self.interpolate = interpolate
        self.index = 0

    def get_current_color(self):
        return self.colors[self.index]

    def get_next_color(self):
        index = index + 1 if index < len(self.colors) else 0

        return self.colors[index]

    def run(self):
        pass

    def interpolate(self):
        pass

    def stop(self):
        pass

class ZoneEffect(Effect):
    pass

class PerLedEffect(Effect):
    pass