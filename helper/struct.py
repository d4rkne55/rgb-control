from typing import NewType, get_type_hints
from dataclasses import dataclass, astuple
from struct import pack

# 1 Byte
Char = NewType('Char', int)
# 1 Byte, unsigned
UChar = NewType('UChar', int)
# 2 Bytes
Short = NewType('Short', int)
# 2 Bytes, unsigned
UShort = NewType('UShort', int)
# 4 Bytes
Int = NewType('Int', int)
# 4 Bytes, unsigned
UInt = NewType('UInt', int)

@dataclass
class Struct:
    __formatMapping = {
        Char: 'c',
        UChar: 'B',
        Short: 'h',
        UShort: 'H',
        Int: 'i',
        UInt: 'I',
        # python std types
        bool: '?',
        int: 'q',
        float: 'd'
    }

    def to_binary(self, subcall = False):
        attrs = get_type_hints(self)
        # formatStr = '' if subcall else '='
        binary = bytearray()

        for attr in attrs:
            value = getattr(self, attr)
            attrType = attrs[attr]

            if issubclass(value.__class__, Struct):
                binary.extend(value.to_binary(True))
                continue

            format = self.__formatMapping.get(attrType)
            # extend() as append() doesn't take bytes
            binary.extend(pack(format, value))

        # if subcall:
        #     return formatStr

        # return pack(formatStr, *astuple(self))
        return binary