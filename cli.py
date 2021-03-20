import sys
import inspect
from device_detector import DeviceDetector
from controller import Controller
from effects.base import Color
import helper.debug as debug

detector = DeviceDetector()

detected = detector.get_detected_devices()
supported = detector.get_supported_devices()

print(f'The HID API detected {len(detected)} devices, ', end='')

if len(supported) > 0:
    print('of which the following are supported:')

    for i, device in enumerate(supported):
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

zones_data = {}

for zone_name in device.zones:
    answer = input(f'Configure "{zone_name}" (y/n): ')

    if answer == '':
        exit(0)

    if answer.lower() == 'n':
        # TODO
        zones_data[zone_name] = controller.get_default_zone_data()
        continue

    zone_props = controller.get_zone_properties()
    zones_data[zone_name] = []

    for prop in zone_props:
        propType = zone_props[prop]

        print('    ', end='')

        # custom types are considered a function, so check if it's a class first
        if inspect.isclass(propType) and issubclass(propType, Color):
            user_input = map(int, input(f'{prop} (r, g, b): ').split(','))
            user_input = Color(*user_input)
        else:
            user_input = int(input(f'{prop}: '))

        zones_data[zone_name].append(user_input)

packet = controller.get_packet_from_data(zones_data)
packet_bytes = packet.to_binary()

print()
# print(packet_bytes.hex())

if controller.check_binary_packet(packet_bytes) == False:
    print('Generated data packet doesn\'t match expected report size!')
    exit(1)

# current_state = controller.get_device_state()
# print(bytearray(current_state).hex())

answer = input('Configuration done. Send data to device? (y/n) ')

if answer.lower() != 'y':
    exit(0)

controller.send_to_device(packet_bytes)