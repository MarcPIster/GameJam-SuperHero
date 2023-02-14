import arcade
import random
import math

def get_vector_to_player(player1_pos, player2_pos):
    x_diff = player2_pos[0] - player1_pos[0]
    y_diff = player2_pos[1] - player1_pos[1]
    dist = math.sqrt(x_diff ** 2 + y_diff ** 2)
    if dist == 0:
        return [0, 0]
    else:
        return [x_diff / dist, y_diff / dist]



class Intro:
        def __init__(self, sound_manager):
            self.timer = 0
            self.sound_manager = sound_manager
            self.sound_manager.add_sound("eat", "./assets/sounds/eat.wav")



            self.anim_time_player = 0
            self.player = arcade.Sprite("./assets/intro/right/run1.png", 1)
            self.player.center_x = 500
            self.player.center_y = 100
            self.player_anim_list = ["./assets/intro/right/run1.png", "./assets/intro/right/run2.png", "./assets/intro/right/run3.png",
                                     "./assets/intro/right/run4.png", "./assets/intro/right/run5.png"]

            self.physics_engine_player = arcade.PhysicsEnginePlatformer(self.player, walls=[arcade.Sprite("./assets/player/walk/walk0.png", 2)])
            self.player_movement = [0, 0]
            self.sprite_list_player = arcade.SpriteList()
            self.current_sprite_index_player = 0
            self.current_sprite_index_bat = 0

            self.anim_time_bat = 0
            self.current_bat_animation = 0
            self.bat_direction = 0
            self.bat_anim_list = ["./assets/bat/left/left0.png", "./assets/bat/left/left1.png",
                                  "./assets/bat/left/left2.png"]

            self.bat = arcade.Sprite("./assets/bat/left/left0.png", 2.5)

            self.bat.center_x = 400
            self.bat.center_y = 800
            self.bat_movement = [0, 0]
            self.physics_engine_bat = arcade.PhysicsEnginePlatformer(self.bat, walls=[arcade.Sprite("./assets/player/walk/walk0.png", 2)])


            self.hit = False


        def on_draw(self):
            self.bat.draw()
            self.player.draw()

        def on_update(self, delta_time):
            self.timer += delta_time
            #self.bat.update_animation()
            if self.timer > 0.5:
                self.timer = 0
                self.bat_movement = [random.randint(-5, 5), random.randint(-5, 4)]

            self.player_movement = get_vector_to_player([self.player.center_x, self.player.center_y], [self.bat.center_x, self.bat.center_y])
            self.player_movement[0] *= 2
            self.player_movement[1] = 0

            self.sprite_list_player.update()

            #bat movment and collision with screen
            if self.bat.left < 0:
                self.bat.left = 0
            elif self.bat.right > 1000 - 1:
                self.bat.right = 1000 - 1
            if self.bat.bottom < 0:
                self.bat.bottom = 0
            elif self.bat.top > 650 - 1:
                self.bat.top = 650 - 1




            self.bat.change_x = self.bat_movement[0]
            self.bat.change_y = self.bat_movement[1]
            self.bat.update()
            self.bat_animation(delta_time)

            self.player.change_x = self.player_movement[0]
            self.player.change_y = self.player_movement[1]
            self.player.update()
            self.player_animation(delta_time)

            self.check_player_collision()

        def check_player_collision(self):
            if self.hit:
                return
            hit_list = arcade.check_for_collision(self.player, self.bat)
            if hit_list:
                self.sound_manager.play_sound("eat")
                self.hit = True
                self.bat.kill()
                #ToDo: turn player into zombie

        def bat_animation(self, delta_time):

            self.anim_time_bat += delta_time
            if self.anim_time_bat < 0.16:
                return

            self.anim_time_bat = 0
            self.current_bat_animation += 1

            if self.current_bat_animation > 2:
                self.current_bat_animation = 0

            if self.bat_movement[0] < 0:
                self.bat_anim_list = ["./assets/bat/left/left0.png", "./assets/bat/left/left1.png",
                                      "./assets/bat/left/left2.png"]
            else:
                self.bat_anim_list = ["./assets/bat/right/right0.png", "./assets/bat/right/right1.png",
                                      "./assets/bat/right/right2.png"]

            self.bat.texture = arcade.load_texture(self.bat_anim_list[self.current_bat_animation])


        def player_animation(self, delta_time):
            self.anim_time_player += delta_time
            if self.anim_time_player < 0.16:
                return

            self.anim_time_player = 0
            self.current_sprite_index_player += 1

            if self.current_sprite_index_player > 4:
                self.current_sprite_index_player = 0

            if self.hit:
                flipped = False
                self.player_anim_list = ["./assets/enemy/walk/walk1.png", "./assets/enemy/walk/walk2.png",
                                         "./assets/enemy/walk/walk3.png",
                                         "./assets/enemy/walk/walk4.png", "./assets/enemy/walk/walk5.png"]
                if self.player_movement[0] < 0:
                    flipped = True
                self.player.texture = arcade.load_texture(self.player_anim_list[self.current_sprite_index_player], flipped_horizontally=flipped)

            else:
                if self.player_movement[0] < 0:
                    self.player_anim_list = ["./assets/intro/left/run1.png", "./assets/intro/left/run2.png", "./assets/intro/left/run3.png",
                                             "./assets/intro/left/run4.png", "./assets/intro/left/run5.png"]
                else:
                    self.player_anim_list = ["./assets/intro/right/run1.png", "./assets/intro/right/run2.png", "./assets/intro/right/run3.png",
                                             "./assets/intro/right/run4.png", "./assets/intro/right/run5.png"]

                self.player.texture = arcade.load_texture(self.player_anim_list[self.current_sprite_index_player])



        def end_intro(self):
            self.player.kill()

