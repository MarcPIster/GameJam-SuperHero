import arcade
from source.josis_test_player import Player
from source.maps.map_manager import MapManager
from source.menus.pause_screen import PauseManager

# LAYER order:
# 1: Platforms
# 2: Player
# 3: Coins

class MyGame(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__()
        self.physics_engine = None
        self.map = None
        self.player = None
        self.scene = None
        self.map_manager = MapManager()
        self.tile_map = None
        self.moving_platforms = None
        self.pause_manager = None
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def load_level(self, level):
        self.moving_platforms = False
        self.scene = arcade.Scene.from_tilemap(level)

        self.scene.add_sprite_list_before("Player", "Coins")

        self.player = Player()
        self.scene.add_sprite("Player", self.player.player_sprite)

        try:
            self.player.physics_engine = arcade.PhysicsEnginePlatformer(self.player.player_sprite,
                                                                        platforms=self.scene["Moving Platforms"],
                                                                        walls=self.scene["Platforms"])
            self.moving_platforms = True
        except KeyError:
            self.player.physics_engine = arcade.PhysicsEngineSimple(self.player.player_sprite,
                                                                    walls=self.scene["Platforms"])

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        self.load_level(self.map_manager.load_level(1))
        self.pause_manager = PauseManager()

    def on_draw(self):
        """ Render the screen. """
        self.clear()
        self.scene.draw()
        # Code to draw the screen goes here

    def on_key_press(self, key, modifiers):
        # TODO: remove again, just to test switching levels
        if key == arcade.key.J:
            self.load_level(self.map_manager.load_level(1))
        if key == arcade.key.K:
            self.load_level(self.map_manager.load_level(2))
        if key == arcade.key.L:
            self.load_level(self.map_manager.load_level(3))
        if key == arcade.key.M:
            self.load_level(self.map_manager.load_level(4))

        self.player.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.player.on_key_release(key, modifiers)
        self.pause_manager.on_key_press(key, self)

    def on_update(self, delta_time):
        self.player.on_update(delta_time)
        if self.moving_platforms:
            self.scene.update(["Moving Platforms"])
