import sys
from device_detector import DeviceDetector
from controller import Controller
from config.packets.MSI import * # TODO
from effects.base import Color
import inspect
import helper.debug as debug

detector = DeviceDetector()

detected = detector.get_detected_devices()
supported = detector.get_supported_devices()

print(f'The HID API detected {len(detected)} devices, ', end='')

if len(supported) > 0:
    print('of which the following are supported:')

    for i, device in enumerate(detector.get_supported_devices()):
        print(f'{i}\t{device.vendor_name}\t{device.display_name}')
else:
    print('but none of them are supported.')
    print('Exiting.')
    exit()

print()

selection = int(input('Select device number you want to control: '))

device = supported[selection]

controller = Controller(device)
controller.configure_device()

# debug.dump_object(device)

print()
print('Now you can set colors and other information for all lighting zones of the device.')
print('It will loop through every zone and ask you whether you want to configure it. Press Enter if you want to cancel/exit.')
print()

zones = []

for zone_name in device.zones:
    answer = input(f'Configure "{zone_name}" (y/n): ')

    if answer == '':
        exit(0)

    if answer.lower() == 'n':
        zones.append(controller.get_default_zone())
        continue

    zoneProps = controller.get_zone_properties()
    zoneData = []

    for prop in zoneProps:
        propType = zoneProps[prop]

        print('    ', end='')

        # custom types are considered a function, so check if it's a class first
        if inspect.isclass(propType) and issubclass(propType, Color):
            userInput = map(int, input(f'{prop} (r, g, b): ').split(','))
            userInput = Color(*userInput)
        else:
            userInput = int(input(f'{prop}: '))

        zoneData.append(userInput)

    zones.append(Zone(*zoneData))

packet = DataPacket(REPORT_ID, *zones, 0)
packet_bytes = packet.to_binary()

print()
# print(packet_bytes.hex())

if len(packet_bytes) != REPORT_LENGTH:
    print('Generated data packet doesn\'t match expected report size!')
    exit(1)

# current_state = device.hid_handle.get_feature_report(REPORT_ID, REPORT_LENGTH)
# print(bytearray(current_state).hex())

answer = input('Configuration done. Send data to device? (y/n) ')

if answer.lower() != 'y':
    exit(0)

device.hid_handle.send_feature_report(packet_bytes)