import inveo.buzzer
import inveo.device
import inveo.led

with inveo.device.Device.open() as dev:
    print('Current configuration:')
    print('\tMode:', dev.mode)
    print('\tUSB mode:', dev.usb_mode)
    print('\tLED 1:', dev.led1_mode)
    print('\tLED 2:', dev.led2_mode)
    print('\tLED 3:', dev.led3_mode)
    print('\tBuzzer:', dev.buzzer_mode)
    print(f'\tRead delay: {dev.read_delay:.1f} s')
    print('\tModel:', dev.model)
    print('\tSoftware version:', dev.software_version)
    print('\tHardware version:', dev.hardware_version)
    print(f'\tLast tag: {dev.last_tag or "None"}')
