import arcade
import arcade.gui
import random

class Intro:
        def __init__(self):
            self.timer = 0
            self.player = 1
            self.manager = arcade.gui.UIManager()
            self.manager.enable()
            self.bat = arcade.Sprite("./assets/bat/idle/idle0.png", 2)
            self.bat.center_x = 100
            self.bat.center_y = 800
            self.bat_movement = [0, 0]
            self.physics_engine = arcade.PhysicsEnginePlatformer(self.bat, walls=[arcade.Sprite("./assets/player/walk/walk0.png", 2)])


        def on_draw(self):
            self.manager.draw()
            self.bat.draw()

        def on_update(self, delta_time):
            self.timer += delta_time
            self.bat.update_animation()
            if self.timer > 0.5:
                self.timer = 0
                self.bat_movement = [random.randint(-5, 5), random.randint(-5, 5)]

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