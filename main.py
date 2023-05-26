import api
import time
import serial

client = api.Client()
config = api.load_config('config')

while True:
    try: Serial = serial.Serial(config['port'], 19200, timeout=1)
    except serial.SerialException: Serial = None

    if Serial is not None:
        print('Device Detected')
        while True:
            try: State = Serial.isOpen()
            except AttributeError: State = False

            if State:
                try:
                    message = Serial.readline().decode('utf-8')
                    if len(message) > 0:
                        client.GetVolume(message)
                        client.LogMessage()
                        client.SetVolume()
                except serial.SerialException:
                    print("Cannot connect to the device")
                    break
            else:
                print("Cannot connect to the device")
    else:
        print("Device is not detected")
        time.sleep(2.5)