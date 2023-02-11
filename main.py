"""
Platformer Game
"""
import arcade
from source.player import Player
from source.maps.level_one import MapOne

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Smash Covid"
GRAVITY = 0.5


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.physics_engine = None
        self.map = None
        self.player_sprite = None
        self.player_list = None
        self.speed = 3
        self.jumpheight = 10
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        self.map = MapOne()
        self.map.setup()
        self.player_sprite = Player()
        self.player_list = arcade.SpriteList()
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 500
        self.player_list.append(self.player_sprite)
        self.player_sprite.physics_engine = arcade.PhysicsEnginePlatformer(self.player_list[0], walls=self.map.sprite_list, gravity_constant=GRAVITY)

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()

        #self.player.player_sprite.draw()
        self.map.sprite_list.draw()
        self.player_list.draw()
        # Code to draw the screen goes here

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if self.player_sprite.disable_movement == 1:
            return

        if (key == arcade.key.UP or key == arcade.key.W) and self.player_sprite.spacePressed != 1:
            self.player_sprite.spacePressed = 1
            self.player_sprite.key_up_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.key_left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.key_right_pressed = True
        elif (key == arcade.key.SPACE or key == arcade.key.NUM_0) and self.player_sprite.shot != 1:
            self.player_sprite.shot = 1
            self.player_sprite.disable_movement = 1
            self.player_sprite.key_shot_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.spacePressed = 0
            self.player_sprite.key_up_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.key_left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.key_right_pressed = False
        elif key == arcade.key.SPACE or key == arcade.key.NUM_0:
            self.player_sprite.shot = 0
            self.player_sprite.disable_movement = 0
            self.player_sprite.key_shot_pressed = False

    def on_update(self, delta_time):
        self.player_list.on_update()
        self.player_list.update()
        self.player_list.update_animation(delta_time)


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
