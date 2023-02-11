import arcade
from source.josis_test_player import Player
from source.maps.map_manager import MapManager
from source.menus.pause_screen import PauseManager

# LAYER order:
# 1: Platforms
# 2: Items (BombItem and FireItem)
# 3: Player
# 4: Coins


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

        self.gui_camera = None
        self.total_time = 0.0
        self.timer_text = arcade.Text(
            text="00:00:00",
            start_x=self.window.width // 2,
            start_y=self.window.height - 50,
            color=arcade.color.WHITE,
            font_size=40,
            anchor_x="center"
        )

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
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)
        self.total_time = 0.0

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

        # detect collision with coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player.player_sprite, self.scene["Coins"])
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.player.increase_score()

        # update timer
        self.total_time += delta_time
        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60
        seconds_100s = int((self.total_time - seconds) * 100)
        self.timer_text.text = f"{minutes:02d}:{seconds:02d}:{seconds_100s:02d}"

        # check item collision
        player_collision_list = arcade.check_for_collision_with_lists(self.player.player_sprite, [
            self.scene["FireItem"],
            self.scene["BombItem"]
        ])

        for collision in player_collision_list:
            if self.scene["FireItem"] in collision.sprite_lists:
                self.player.activate_fire_shoot()
            elif self.scene["BombItem"] in collision.sprite_lists:
                self.player.activate_bomb_shoot()
            collision.remove_from_sprite_lists()
