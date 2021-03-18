from helper.struct import *
from config.zones.MSI import Zone

REPORT_ID = 0x52
REPORT_LENGTH = 162

@dataclass
class DataPacket(Struct):
    report_id: UChar# = REPORT_ID
    jrgb_1: Zone
    jrainbow_1: Zone
    # the following 2 are probably jcorsair stuff
    unknown_1: Zone
    unknown_2: Zone
    # uncontrollable "meta" zone?
    unknown_3: Zone
    # pch_1 - pch_4 is at top right/back
    pch_1: Zone
    pch_2: Zone
    pch_3: Zone
    pch_4: Zone
    # right part of chipset cooler
    pch_5: Zone
    # "left"/lower part of chipset cooler
    pch_6: Zone
    # more jcorsair stuff?
    # seems unused, as unaffected by mystic light changes
    unknown_4: Zone
    unknown_5: Zone
    unknown_6: Zone
    unknown_7: Zone
    jrgb_2: Zone
    save_data: bool