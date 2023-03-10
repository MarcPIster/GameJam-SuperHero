import arcade

from source.menus.end_screen import EndWindow
from source.player_character import Player
from source.enemy_character import Enemy
from source.maps.map_manager import MapManager
from source.menus.pause_screen import PauseManager
from source.game_mode import Gamemode, Playermode
from random import randrange

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
        self.enemy = None
        self.enemy_list = None
        self.bat_list = []
        self.scene = None
        self.random_bat_spawn = []
        self.gravity_constant = 0.5
        self.map_manager = MapManager()
        self.moving_platforms = None
        self.pause_manager = PauseManager()

        # bat animation
        self.anim_time = 0
        self.current_bat_animation = 0
        self.bat_anim_list = ["./assets/bat/left/left0.png", "./assets/bat/left/left1.png", "./assets/bat/left/left2.png"]

        self.gui_camera = arcade.Camera(self.window.width, self.window.height)
        self.total_time = 0.0
        self.countdown_time = 0
        if game_mode == Gamemode.TIME:
            self.timer_text = arcade.Text(
                text="00:00:00",
                start_x=self.window.width // 2,
                start_y=self.window.height - 50,
                color=arcade.color.WHITE,
                font_size=40,
                anchor_x="center"
            )
        else:
            self.timer_text = arcade.Text(
                text="Fight!",
                start_x=self.window.width // 2,
                start_y=self.window.height - 50,
                color=arcade.color.WHITE,
                font_size=40,
                anchor_x="center"
            )

        self.game_mode = game_mode
        self.player_mode = player_mode
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        # initialize sound manager and add sounds
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
        self.moving_platforms = False
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

        self.player = Player(1000, 650, self.sound_manager, self.scene)
        self.player_list = arcade.SpriteList()
        self.player.center_x = 100
        self.player.center_y = 500
        self.player_list.append(self.player)
        self.scene.add_sprite("Player", self.player_list[0])

        self.enemy_list = arcade.SpriteList()
        self.bat_list = arcade.SpriteList()
        # generate random wave for bat appearance
        for i in range(5):
            self.random_bat_spawn.append(randrange(1, 119))
        if self.player_mode == 1:
            self.enemy = Enemy(arcade.get_display_size()[0], arcade.get_display_size()[1], self.sound_manager, self.scene)
            self.enemy.center_x = 500
            self.enemy.center_y = 500
            self.enemy_list.append(self.enemy)
            self.scene.add_sprite("Enemy", self.enemy_list[0])
            if self.moving_platforms:
                self.enemy.physics_engine = arcade.PhysicsEnginePlatformer(self.enemy_list[0],
                                                                           platforms=self.scene["Moving Platforms"],
                                                                           walls=self.scene["Platforms"],
                                                                           gravity_constant=self.gravity_constant)
            else:
                self.enemy.physics_engine = arcade.PhysicsEnginePlatformer(self.enemy_list[0],
                                                                           walls=self.scene["Platforms"],
                                                                           gravity_constant=self.gravity_constant)

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
            self.second_player = Player(self.window.width, self.window.height, self.sound_manager, self.scene,
                                        self.player_mode)
            self.second_player.center_x = 100
            self.second_player.center_y = 500
            self.player_list.append(self.second_player)
            self.scene.add_sprite("Player2", self.player_list[1])
            try:
                self.second_player.physics_engine = arcade.PhysicsEnginePlatformer(self.player_list[1],
                                                                            platforms=self.scene["Moving Platforms"],
                                                                            walls=self.scene["Platforms"],
                                                                            gravity_constant=self.gravity_constant)
            except KeyError:
                self.second_player.physics_engine = arcade.PhysicsEnginePlatformer(self.player_list[1],
                                                                            walls=self.scene["Platforms"],
                                                                            gravity_constant=self.gravity_constant)
                                                        

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Render the screen. """
        self.clear()
        self.scene.draw()
        for player in self.player_list:
            player.powerups.draw()
            player.bar_list.draw()
            for shot in player.shoot_list:
                shot.sprite.draw()
        if self.player_mode == 1:
            self.enemy.bar_list.draw()
            for shot in self.enemy.shoot_list:
                shot.sprite.draw()

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

    def end_game(self, enemy_won=None):
        if enemy_won != True:
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
        else:
            self.player_won = None
        self.game_over = True
        self.window.show_view(EndWindow(self))

    def check_bullet_collision(self, player, delta_time):
        for shot in player.shoot_list:
            shot.sprite.update()
            if shot.hit == True:
                shot.time_went_by += delta_time
            if shot.total_time <= shot.time_went_by:
                player.shoot_list.remove(shot)
                break

            hit_list = arcade.check_for_collision_with_list(shot.sprite, self.player_list)
            if len(self.enemy_list) > 0:
                hit_list.extend(arcade.check_for_collision_with_list(shot.sprite, self.enemy_list))

            if len(hit_list) > 0:
                for player_to_check in hit_list:
                    player_to_check.decrease_health(shot.damage)
                    player.shoot_list.remove(shot)
                    break

            bat_shot_list = arcade.check_for_collision_with_list(shot.sprite, self.bat_list)

            for bat in bat_shot_list:
                bat.remove_from_sprite_lists()
                player.shoot_list.remove(shot)

    def stop_bullets_on_collision(self, shot):
        if shot.hit:
            return
        if self.level == 4:
            shoot_collision_list = arcade.check_for_collision_with_lists(shot.sprite, [self.scene["Platforms"],
                                                                                       self.scene["Moving Platforms"]])
        else:
            shoot_collision_list = arcade.check_for_collision_with_lists(shot.sprite,
                                                                         [self.scene["Platforms"]])
        if len(shoot_collision_list) > 0:
            shot.set_speed(0)
            shot.hit = True

    def on_update(self, delta_time):
        self.player_list.on_update(delta_time)
        self.player_list.update()
        self.player_list.update_animation(delta_time)
        self.bat_list.update()
        self.bat_animation(delta_time)

        if self.player_mode == 1:
            self.enemy.on_update(delta_time, self.player_list)
            self.enemy_list.update()
            self.enemy_list.update_animation(delta_time)

        for player in self.player_list:
            self.check_bullet_collision(player, delta_time)
        for enemy in self.enemy_list:
            self.check_bullet_collision(enemy, delta_time)

        for player in self.player_list:
            if player.health <= 0:
                if len(self.enemy_list) > 0:
                    self.end_game(True)
                else:
                    self.end_game()

        if len(self.enemy_list) > 0:
            if self.enemy_list[0].health <= 0:
                self.end_game(False)

        if self.moving_platforms:
            self.scene.update(["Moving Platforms"])

        # detect collision with coins
        for i in range(len(self.player_list)):
            coin_hit_list = arcade.check_for_collision_with_list(self.player_list[i], self.scene["Coins"])
            for coin in coin_hit_list:
                coin.remove_from_sprite_lists()
                if i == 0:
                    self.player.increase_score()
                else:
                    self.second_player.increase_score()
                self.sound_manager.play_sound('coin-collect')

        # update timer
        if self.game_mode == Gamemode.TIME.value:
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

            for bat_spawn_time in self.random_bat_spawn:
                if time_passed < bat_spawn_time:
                    for i in range(3):
                        bat = arcade.Sprite("./assets/bat/left/left0.png", 1.5)
                        bat.center_x = self.window.width - 5
                        bat.center_y = self.window.height - 50 - i * 100
                        bat.change_x = -5
                        self.bat_list.append(bat)
                        self.scene.add_sprite("bat", self.bat_list[-1])
                    self.random_bat_spawn.remove(bat_spawn_time)
                    continue


        for bat in self.bat_list:
            if bat.center_x < 0:
                bat.remove_from_sprite_lists()
                continue


        for enemy in self.enemy_list:
            for shot in enemy.shoot_list:
                self.stop_bullets_on_collision(shot)

        for player in self.player_list:
            player_collision_list = arcade.check_for_collision_with_list(player, self.bat_list)

            for bat in player_collision_list:
                player.decrease_health(50)
                bat.remove_from_sprite_lists()
                continue


            # check item collision
            player_collision_list = arcade.check_for_collision_with_lists(player, [
                self.scene["FireItem"],
                self.scene["BombItem"]
            ])
            for shot in player.shoot_list:
                self.stop_bullets_on_collision(shot)

            for collision in player_collision_list:
                if self.scene["FireItem"] in collision.sprite_lists:
                    player.activate_fire_shoot()
                elif self.scene["BombItem"] in collision.sprite_lists:
                    player.activate_bomb_shoot()
                collision.remove_from_sprite_lists()

    def bat_animation(self, delta_time):
        self.anim_time += delta_time

        if self.anim_time < 0.16:
            return

        self.anim_time = 0
        self.current_bat_animation += 1

        if self.current_bat_animation > 2:
            self.current_bat_animation = 0
        for bat in self.bat_list:
            bat.texture = arcade.load_texture(self.bat_anim_list[self.current_bat_animation])


