import api
import time
import serial

client = api.Client()
config = api.load_config('config')

while True:
    try: 
        Serial = serial.Serial(config['port'], 19200, timeout=1)
        print('Device Detected')
        while True:
            try: 
                State = Serial.isOpen()
                try:
                    message = Serial.readline().decode('utf-8')
                    if len(message) > 0:
                        client.ScanAudioLines()
                        client.GetVolume(message)
                        client.LogMessage()
                        client.SetVolume()
                except serial.SerialException:
                    print("Device is busy")
                    break
            except AttributeError: 
                print("Cannot connect to the device")
                break
    except serial.SerialException:
        print("Device is not detected")
        time.sleep(2.5)