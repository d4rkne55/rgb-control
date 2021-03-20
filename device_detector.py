import hid
from collections import defaultdict

from helper.device import Device
from config.support import SUPPORTED_DEVICES

class DeviceDetector:
    def __init__(self):
        self.devices = []
        # defaultdict instead of normal empty dict to help filling nested data
        self.registered = defaultdict(dict)

        self.register_supported_devices()
        self.set_detected_devices()

    def set_detected_devices(self):
        for device_info in hid.enumerate():
            device = Device.from_hid_data(device_info)

            self.devices.append(device)

    def get_detected_devices(self):
        return self.devices

    def register_supported_devices(self):
        for device_info in SUPPORTED_DEVICES:
            # device = Device(*device_info)

            # save to nested dict for easier lookup
            self.registered[device_info.vendor_id][device_info.product_id] = device_info

    def get_supported_devices(self):
        supported = []
        for device in self.devices:
            if device.vendor_id in self.registered and device.product_id in self.registered[device.vendor_id]:
                device.display_name = self.registered[device.vendor_id][device.product_id].name
                supported.append(device)

        return supported