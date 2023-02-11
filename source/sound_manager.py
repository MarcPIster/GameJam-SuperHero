import arcade


class SoundManager:
    def __init__(self, save_manager):
        self.sound_list = {}
        self.music_list = {}
        self.player_sound = {}
        self.player_music = {}
        self.volume_sound = save_manager.get_sound_volume()
        self.volume_music = save_manager.get_music_volume()
        self.save_manager = save_manager

    def add_sound(self, sound_name, sound_file):
        self.sound_list[sound_name] = arcade.load_sound(sound_file)

    def play_sound(self, sound_name):
        if sound_name == "item-collect":
            player = arcade.play_sound(self.sound_list[sound_name], self.volume_sound, speed=2)
        else:
            player = arcade.play_sound(self.sound_list[sound_name], self.volume_sound)
        self.player_sound[sound_name] = player
        return player

    def stop_sound(self, sound_name):
        if sound_name in self.player_sound:
            arcade.stop_sound(self.player_sound[sound_name])
            del self.player_sound[sound_name]

    def add_music(self, music_name, music_file):
        self.music_list[music_name] = arcade.load_sound(music_file)

    def play_music(self, music_name):
        player = arcade.play_sound(self.music_list[music_name], self.volume_music, True)
        self.player_music[music_name] = player
        return player

    def stop_music(self, music_name):
        if music_name in self.player_music:
            arcade.stop_sound(self.player_music[music_name])
            del self.player_music[music_name]

    def get_sound_volume(self):
        return self.volume_sound

    def set_sound_volume(self, volume):
        self.volume_sound = volume
        for player in self.player_sound.values():
            player.volume = volume

    def get_music_volume(self):
        return self.volume_music

    def set_music_volume(self, volume):
        self.volume_music = volume
        for player in self.player_music.values():
            player.volume = volume
    def get_sound_manager(self):
        return self

    def stop_all_sounds(self):
        for player in self.player_sound.values():
            arcade.stop_sound(player)
        self.player_sound = {}

    def stop_all_music(self):
        for player in self.player_music.values():
            arcade.stop_sound(player)
        self.player_music = {}
