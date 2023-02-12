import arcade

from source.menus.end_screen import EndWindow
from source.player_character import Player
from source.maps.map_manager import MapManager
from source.menus.pause_screen import PauseManager
from source.game_mode import Gamemode,Playermode

# LAYER order:
# 1: Platforms
# 2: Items (BombItem and FireItem)
# 3: Player
# 4: Coins

MAX_LEVEL = 4


class MyGame(arcade.View):
    """
    Main application class.
    """

    def __init__(self, game_mode, player_mode, sound_manager):
        super().__init__()
        self.game_over = False
        self.player_won = -1
        self.level = 0
        self.next_level = True
        self.physics_engine = None
        self.player = None
        self.second_player = None
        self.player_list = None
        self.scene = None
        self.gravity_constant = 0.5
        self.map_manager = MapManager()
        self.moving_platforms = None
        self.pause_manager = PauseManager()

        self.gui_camera = arcade.Camera(self.window.width, self.window.height)
        self.total_time = 0.0
        self.countdown_time = 0
        self.timer_text = arcade.Text(
            text="00:00:00",
            start_x=self.window.width // 2,
            start_y=self.window.height - 50,
            color=arcade.color.WHITE,
            font_size=40,
            anchor_x="center"
        )

        self.game_mode = game_mode
        self.player_mode = player_mode
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.sound_manager = sound_manager

        self.sound_manager.add_sound(f'hit2', f'./assets/sounds/hit2.wav')
        self.sound_manager.add_sound(f'hit', f'./assets/sounds/hit1.wav')
        self.sound_manager.add_sound(f'dead', f'./assets/sounds/diesound.wav')
        self.sound_manager.add_sound(f'coin-collect', f'./assets/sounds/coincollect.wav')
        self.sound_manager.add_sound(f'item-collect', f'./assets/sounds/itemcollect.wav')
        self.sound_manager.add_sound(f'beep', f'./assets/sounds/beep.wav')
        self.sound_manager.add_sound(f'jump', f'./assets/sounds/jump.wav')
        self.sound_manager.add_sound(f'hurt-1', f'./assets/sounds/hurt1.wav')
        self.sound_manager.add_sound(f'hurt-2', f'./assets/sounds/hurt2.wav')
        self.sound_manager.add_sound(f'hurt-3', f'./assets/sounds/hurt3.wav')
        self.sound_manager.add_sound(f'hurt-4', f'./assets/sounds/hurt4.wav')


    def setup(self, level=1):
        """ Set up the game here. Call this function to restart the game. """
        self.game_over = False
        self.load_level(level)
        self.total_time = 0.0


    def load_level(self, level_id):
        self.level = level_id
        if self.level >= MAX_LEVEL:
            self.next_level = False
        self.scene = arcade.Scene.from_tilemap(self.map_manager.load_level(level_id))
        self.sound_manager.stop_all_music()
        self.sound_manager.stop_all_sounds()
        print(f'Loading level{level_id} ...')
        try:
            self.sound_manager.add_music(f'level{level_id}', f'./assets/sounds/level{level_id}.wav')
            self.sound_manager.play_music(f'level{level_id}')
        except FileNotFoundError:
            print(f'No music for level {level_id} found. Default theme will be used...')
            self.sound_manager.add_music('maintheme', './assets/sounds/theme.wav')
            self.sound_manager.play_music('maintheme')


        self.moving_platforms = False
        self.scene = arcade.Scene.from_tilemap(self.map_manager.load_level(level_id))


        self.scene.add_sprite_list_before("Player", "Coins")

        self.player = Player(arcade.get_display_size()[0], arcade.get_display_size()[1], self.sound_manager)
        self.player_list = arcade.SpriteList()
        self.player.center_x = 100
        self.player.center_y = 500
        self.player_list.append(self.player)
        self.scene.add_sprite("Player", self.player_list[0])
        try:
            self.player.physics_engine = arcade.PhysicsEnginePlatformer(self.player_list[0],
                                                                        platforms=self.scene["Moving Platforms"],
                                                                        walls=self.scene["Platforms"],
                                                                        gravity_constant=self.gravity_constant)
            self.moving_platforms = True
        except KeyError:
            self.player.physics_engine = arcade.PhysicsEnginePlatformer(self.player_list[0],
                                                                        walls=self.scene["Platforms"],
                                                                        gravity_constant=self.gravity_constant)

        if self.player_mode == Playermode.DUO.value:
            self.second_player = Player(arcade.get_display_size()[0], arcade.get_display_size()[1], self.player_mode)
            self.second_player_list = arcade.SpriteList()
            self.second_player.center_x = 100
            self.second_player.center_y = 500
            self.second_player_list.append(self.second_player)
            self.scene.add_sprite("Player2", self.second_player_list[0])
            try:
                self.second_player.physics_engine = arcade.PhysicsEnginePlatformer(self.second_player_list[0],
                                                                            platforms=self.scene["Moving Platforms"],
                                                                            walls=self.scene["Platforms"],
                                                                            gravity_constant=self.gravity_constant)
            except KeyError:
                self.second_player.physics_engine = arcade.PhysicsEnginePlatformer(self.second_player_list[0],
                                                                            walls=self.scene["Platforms"],
                                                                            gravity_constant=self.gravity_constant)
                                                        

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Render the screen. """
        self.clear()
        self.scene.draw()
        self.player.powerups.draw()
        self.player.bar_list.draw()

        self.gui_camera.use()
        half_window_width = self.window.width // 2
        point_list = ((half_window_width - 170, self.window.height),
                      (half_window_width + 170, self.window.height),
                      (half_window_width + 150, self.window.height - 90),
                      (half_window_width - 150, self.window.height - 90))
        arcade.draw_polygon_filled(point_list, (59, 68, 75, 150))
        score_text = f"Score: {self.player.score}"
        arcade.draw_text(score_text, half_window_width - 100, self.window.height - 80, arcade.color.WHITE, 14)
        self.timer_text.draw()

    def on_key_press(self, key, modifiers):
        # TODO: remove again, just to test switching levels
        if key == arcade.key.P:
            self.player.decrease_health(5)
        if key == arcade.key.J:
            self.load_level(1)
        if key == arcade.key.K:
            self.load_level(2)
        if key == arcade.key.L:
            self.load_level(3)
        if key == arcade.key.M:
            self.load_level(4)
        self.player.on_key_press(key, modifiers)


    def on_key_release(self, key, modifiers):
        self.player.on_key_release(key, modifiers)

        self.pause_manager.on_key_press(key, self)

    def end_game(self):
        tmp = 0
        tmp_x = 0
        for x in range(len(self.player_list)):
            if self.player_list[x].score > tmp:
                tmp = self.player_list[x].score
                tmp_x = x
        self.player_won = tmp_x
        for x in range(len(self.player_list)):
            if self.player_list[x].health > 0:
                self.player_won = x
        self.game_over = True
        self.window.show_view(EndWindow(self))

    def on_update(self, delta_time):
        self.player_list.on_update(delta_time)
        self.player_list.update()
        self.player_list.update_animation(delta_time)

        if self.player_mode == Playermode.DUO.value:
            self.second_player_list.on_update(delta_time)
            self.second_player_list.update()
            self.second_player_list.update_animation(delta_time)


        for player in self.player_list:
            if player.health <= 0:
                self.end_game()

        if self.moving_platforms:
            self.scene.update(["Moving Platforms"])

        # detect collision with coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player_list[0], self.scene["Coins"])
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.player.increase_score()
            self.sound_manager.play_sound('coin-collect')

        # update timer
        self.total_time += delta_time
        time_passed = 120 - self.total_time
        minutes = int(time_passed) // 60
        seconds = int(time_passed) % 60
        seconds_100s = int((time_passed - (minutes * 60) - seconds) * 100)
        self.timer_text.text = f"{minutes:02d}:{seconds:02d}:{seconds_100s:02d}"
        if time_passed <= 0:
            self.end_game()
        if time_passed <= 10:
            self.countdown_time += delta_time
            if self.countdown_time >= 1:
                self.sound_manager.play_sound('beep')
                self.countdown_time = 0

        # check item collision
        player_collision_list = arcade.check_for_collision_with_lists(self.player, [
            self.scene["FireItem"],
            self.scene["BombItem"]
        ])

        for collision in player_collision_list:
            if self.scene["FireItem"] in collision.sprite_lists:
                self.player.activate_fire_shoot()
            elif self.scene["BombItem"] in collision.sprite_lists:
                self.player.activate_bomb_shoot()
            collision.remove_from_sprite_lists()
        

        if self.player_mode == Playermode.DUO.value:
            # detect collision with coins 2nd player
            coin_hit_list = arcade.check_for_collision_with_list(self.second_player_list[0], self.scene["Coins"])
            for coin in coin_hit_list:
                coin.remove_from_sprite_lists()
                self.second_player.increase_score()
                print(self.second_player.score)
