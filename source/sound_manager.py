import arcade


import arcade

import arcade

class SoundManager:
    def __init__(self):
        self.sound_list = {}
        self.music_list = {}
        self.player_sound = {}
        self.player_music = {}
        self.volume_sound = 0.5
        self.volume_music = 0.5

    def add_sound(self, sound_name, sound_file):
        self.sound_list[sound_name] = arcade.load_sound(sound_file)

    def play_sound(self, sound_name):
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

    def get_sound_manager(self):
        return self
