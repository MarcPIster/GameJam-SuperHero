

class SaveManager:
    def __init__(self):
        self.save_data = []
        self.save_file = ".save"
        self.check_read_or_create_file()

    def check_read_or_create_file(self):
        try:
            with open(self.save_file, 'r') as f:
                self.save_data = []
                content = f.read()
                print("Save file found!")
                print("Content of save file:")
                for line in content.split("\n"):
                    if line == "":
                        continue
                    self.save_data.append(line + "\n")
                print(self.save_data)
        except FileNotFoundError:
            with open(self.save_file, 'w') as f:
                self.save("music_volume: 0.5")
                self.save("sound_volume: 0.5")
                self.write_to_file()
                print("New save file created!")

    def save(self, data):
        for data_line in self.save_data:
            if data_line.split(": ")[0] == data.split(": ")[0]:
                self.save_data[self.save_data.index(data_line)] = data + "\n"
                return
        self.save_data.append(data + "\n")


    def get_music_volume(self):
        if "music_volume" in self.save_data[0]:
            return float(self.save_data[0].split(": ")[1].split("\n")[0])
        else:
            return 0.5

    def get_sound_volume(self):
        if "sound_volume" in self.save_data[1]:
            return float(self.save_data[1].split(": ")[1].split("\n")[0])
        else:
            return 0.5

    def get_save_data(self):
        return self.save_data

    def write_to_file(self):
        with open(self.save_file, 'w') as f:
            for line in self.save_data:
                f.write(line)
            print("Save file updated!")


