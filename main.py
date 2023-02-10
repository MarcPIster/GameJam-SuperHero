"""
Platformer Game
"""
import arcade
from source.josis_test_player import Player
from source.maps.level_one import MapManager

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Smash Covid"


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.physics_engine = None
        self.map = None
        self.player = None
        self.scene = None
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Player")

        map = MapManager()
        map.level_one()
        self.scene.add_sprite_list("Walls", use_spatial_hash=True, sprite_list=map.sprite_list)

        self.player = Player()
        self.scene.add_sprite("Player", self.player.player_sprite)

        self.player.physics_engine = arcade.PhysicsEngineSimple(self.player.player_sprite, map.sprite_list)

    def on_draw(self):
        """ Render the screen. """

        self.clear()

        self.scene.draw()
        # Code to draw the screen goes here

    def on_key_press(self, key, modifiers):
        self.player.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.player.on_key_release(key, modifiers)

    def on_update(self, delta_time):
        self.player.on_update(delta_time)


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
