import arcade
from source.josis_test_player import Player
from source.maps.level_one import MapOne
from source.menus.pause_screen import PauseManager

class MyGame(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__()
        self.physics_engine = None
        self.map = None
        self.player = None
        self.pause_manager = None
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        self.map = MapOne()
        self.map.setup()
        self.player = Player()
        self.player.physics_engine = arcade.PhysicsEngineSimple(self.player.player_sprite, self.map.sprite_list)
        self.pause_manager = PauseManager()

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        self.player.player_sprite.draw()
        self.map.sprite_list.draw()
        # Code to draw the screen goes here

    def on_key_press(self, key, modifiers):
        self.player.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.player.on_key_release(key, modifiers)
        self.pause_manager.on_key_press(key, self)

    def on_update(self, delta_time):
        self.player.on_update(delta_time)
