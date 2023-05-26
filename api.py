import json
from pycaw.pycaw import AudioUtilities

def load_config(file):
    file = open(f'config/{file}.json')
    data = json.load(file)

    return data

class Client:
    def __init__(self):
        self.apps = self.ScanAudioLines()
        self.lines = load_config('audio_config')

        self.SortAudioLines()

    def ScanAudioLines(self):
        sessions = AudioUtilities.GetAllSessions()
        output = []

        for session in sessions:
            if session.Process is not None:
                output.append([session.Process.name(), session])

        return output
    def SortAudioLines(self):
        lines = self.lines
        apps = [list(row) for row in self.apps]
        temp = [list(row) for row in self.apps]

        for app in apps:
            for line in lines:
                if app[0] in line['white_list']:
                    line['active_apps'].append(app[1])
                    temp.pop(temp.index(app))

        if len(temp) > 0:
            for item in temp:
                lines[len(lines) - 1]['active_apps'].append(item[1])
    def GetVolume(self, message):
        if len(message) > 0:
            message = message.replace('-', '')
            message = message.replace(' ', '')
            message = message.replace('\r\n', '')

            message = message.split(':')
            for line in self.lines:
                if message[0] in line['name']:
                    line['volume'] = message[1]
    def SetVolume(self):
        for line in self.lines:
            if line['volume'] != 'None':
                volume = int(line['volume']) / 100
                apps = line['active_apps']

                for app in apps:
                    interface = app.SimpleAudioVolume
                    interface.SetMasterVolume(volume, None)

    def LogMessage(self):
        print("Audio logs:")
        for line in self.lines:
            print(f" - {line['name'].replace('_', ' ')} | {line['volume']}%")
