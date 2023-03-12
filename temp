import serial
from pycaw.pycaw import AudioUtilities
import time

def scan_audio_lines():
    sessions = AudioUtilities.GetAllSessions()

    for session in sessions:
        if session.Process is not None:
            name = session.Process.name()
            print(name)
            for x in range(len(lists)):
                if name in lists[x][2]:
                    lists[x][3].append([name, session])

lists = [["Spotify", None, ["Spotify.exe"], []],
         ["Discord", None, ["LEGOSTARWARSSKYWALKERSAGA_DX11.exe"], []],
         ["Browsers", None, ["firefox.exe", "msedge.exe"], []]]

scan_audio_lines()

while True:
    try:
        Serial = serial.Serial("COM4", 19200, timeout=1)
    except serial.SerialException:
        Serial = None

    if Serial is not None:
        print("Device Connected")
        while True:

            try:
                State = Serial.isOpen()
            except AttributeError:
                break

            if State:

                print(lists)

                try:
                    message = Serial.readline().decode('utf-8')
                except serial.SerialException:
                    message = None

                if message is not None:
                    message = message.replace(' - ', '')
                    message = message.replace('\r\n', '')
                    if len(message) > 0:
                        message = message.split(': ')
                        for list_ in lists:
                            if message[0] in list_[0]:
                                list_[1] = message[1]

            for item in lists:
                if item[1] is not None:
                    volume = int(item[1]) / 100
                    lines_ = item[3]

                    for device in lines_:

                        interface = device[1].SimpleAudioVolume
                        interface.SetMasterVolume(volume, None)

                time.sleep(.001)
    else:
        print("Device NOT Detected")
        time.sleep(2.5)