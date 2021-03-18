from typing import NamedTuple

class Device:
    def __init__(self, vendor_id, vendor_name, product_id, product_name, display_name = ''):
        self.vendor_id = vendor_id
        self.vendor_name = vendor_name
        self.product_id = product_id
        self.product_name = product_name
        self.display_name = display_name if display_name else product_name
        self.zones = []
        self.modes = []
        self.hid_handle = None

    @classmethod
    def from_hid_data(cls, data):
        return cls(
            data['vendor_id'],
            data['manufacturer_string'],
            data['product_id'],
            data['product_string']
        );

    def set_zones(self, zones):
        self.zones = zones

    def set_modes(self, modes):
        self.modes = modes

    def set_handle(self, handle):
        self.hid_handle = handle

class DeviceInfo(NamedTuple):
    vendor_id: int
    product_id: int
    name: str = ''