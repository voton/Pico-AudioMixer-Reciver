import copy
import time
import serial
from pycaw.pycaw import AudioUtilities

groups = [
    ["Music", None, ["Spotify.exe"], []],
    ["Browsers", None, ["firefox.exe", "msedge.exe"], []],
    ["Other", None, [], []]
]
def scan_audio_lines():
    sessions = AudioUtilities.GetAllSessions()
    output = [[], []]

    for session in sessions:
        if session.Process is not None:
            name = session.Process.name()
            output[0].append(name)
            output[1].append(session)

    return output

def log_message():
    message = ""
    for item in groups:
        temp = []

        for lines in item[3]: temp.append(lines[0])

        message += f" - {item[0]} | {item[1]}% | [{temp}]\n"

    print(message)

def append_audio_lines(def_lines):
    lines = [list(row) for row in def_lines]
    temp_lines = [list(row) for row in def_lines]

    for x in range(len(groups)):
        temp_append = []

        for y in range(len(lines[0])):
            if lines[0][y] in groups[x][2]:
                if lines[0][y] in temp_lines[0]:
                    temp_lines[0][y] = None
                    temp_lines[1][y] = None

                    temp_append.append([lines[0][y], lines[1][y]])
        groups[x][3] = temp_append

    temp_append = []
    for y in range(len(temp_lines[0])):
        if temp_lines[0][y] is not None:
            temp_append.append([temp_lines[0][y], temp_lines[1][y]])

    groups[2][3] = temp_append

while True:
    try:
        Serial = serial.Serial("COM3", 19200, timeout=1)
    except serial.SerialException:
        Serial = None

    if Serial is not None:
        print("Device Connected")
        while True:
            try:
                State = Serial.isOpen()
            except AttributeError:
                State = False
                break

            if State:
                audio_lines = scan_audio_lines()
                append_audio_lines(audio_lines)

                log_message()

                try:
                    message = Serial.readline().decode('utf-8')
                except serial.SerialException:
                    message = None

                if message is not None:
                    message = message.replace(' - ', '')
                    message = message.replace('\r\n', '')
                    if len(message) > 0:
                        message = message.split(': ')
                        for list_ in groups:
                            if message[0] in list_[0]:
                                list_[1] = message[1]

            for item in groups:
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