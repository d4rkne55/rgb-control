import hid
import importlib
from typing import get_type_hints
import inspect

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

        zone_names = []
        for attr, attrType in attrs.items():
            # custom types are considered a function, so check if it's a class first
            if inspect.isclass(attrType) and issubclass(attrType, zones.Zone):
                zone_names.append(attr)

        return zone_names

    def get_zone_properties(self):
        return get_type_hints(zones.Zone)

    def get_default_zone_data(self):
        return [zones.ZoneMode.STATIC, Color(255, 0, 0), 0x28, Color(0, 255, 0), 0x83, 0x14]

    def get_default_zone(self):
        return zones.Zone(*self.get_default_zone_data())

    def get_packet_from_data(self, zones_data):
        zones_obj = []
        for zone_data in zones_data.values():
            zones_obj.append(zones.Zone(*zone_data))

        return packets.DataPacket(packets.REPORT_ID, *zones_obj, 0)

    def check_binary_packet(self, packet):
        return len(packet) == packets.REPORT_LENGTH

    def get_device_state(self):
        return self.hid_device.get_feature_report(packets.REPORT_ID, packets.REPORT_LENGTH)

    def send_to_device(self, packet):
        self.hid_device.send_feature_report(packet)

    # destructor
    def __del__(self):
        self.hid_device.close()