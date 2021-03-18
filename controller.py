import hid
import importlib
from typing import get_type_hints

from effects.base import Color

packets = None
zones = None

class Controller:
    def __init__(self, device):
        self.device = device
        self.hid_device = hid.device()

        global packets
        global zones
        packets = importlib.import_module('config.packets.' + device.vendor_name)
        zones = importlib.import_module('config.zones.' + device.vendor_name)

    def configure_device(self):
        self.hid_device.open(self.device.vendor_id, self.device.product_id)

        self.device.set_handle(self.hid_device)
        self.device.set_zones(self.get_zones())
        self.device.set_modes(zones.ZoneMode.__members__.keys())

    def get_zones(self):
        attrs = get_type_hints(packets.DataPacket)

        # exclude first and last class attribute; the report id and save_data flag
        # TODO
        return list(attrs)[1:-1]

    def get_zone_properties(self):
        return get_type_hints(zones.Zone)
        
    def get_default_zone(self):
        return zones.Zone(zones.ZoneMode.STATIC, Color(255, 0, 0), 0x28, Color(0, 255, 0), 0x83, 0x14)

    # destructor
    def __del__(self):
        self.hid_device.close()