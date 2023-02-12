import arcade
from source.player_character import Player
from source.maps.map_manager import MapManager
from source.menus.pause_screen import PauseManager
from source.game_mode import Gamemode,Playermode

# LAYER order:
# 1: Platforms
# 2: Player
# 3: Coins

class MyGame(arcade.View):
    """
    Main application class.
    """

    def __init__(self, game_mode, player_mode):
        super().__init__()
        self.physics_engine = None
        self.map = None
        self.player = None
        self.second_player = None
        self.player_list = None
        self.scene = None
        self.gravity_constant = 0.5
        self.map_manager = MapManager()
        self.tile_map = None
        self.moving_platforms = None
        self.pause_manager = None
        self.game_mode = game_mode
        self.player_mode = player_mode
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def load_level(self, level):
        self.moving_platforms = False
        self.scene = arcade.Scene.from_tilemap(level)

        self.scene.add_sprite_list_before("Player", "Coins")

        self.player = Player(arcade.get_display_size()[0], arcade.get_display_size()[1])
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
        self.player_list.on_update(delta_time)
        self.player_list.update()
        self.player_list.update_animation(delta_time)

        if self.player_mode == Playermode.DUO.value:
            self.second_player_list.on_update(delta_time)
            self.second_player_list.update()
            self.second_player_list.update_animation(delta_time)

        if self.moving_platforms:
            self.scene.update(["Moving Platforms"])

        # detect collision with coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player_list[0], self.scene["Coins"])
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.player.increase_score()
            print(self.player.score)
        
        if self.player_mode == Playermode.DUO.value:
            # detect collision with coins 2nd player
            coin_hit_list = arcade.check_for_collision_with_list(self.second_player_list[0], self.scene["Coins"])
            for coin in coin_hit_list:
                coin.remove_from_sprite_lists()
                self.second_player.increase_score()
                print(self.second_player.score)
