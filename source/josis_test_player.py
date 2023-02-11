import arcade


class Player:
    def __init__(self):
        self.player_sprite = arcade.Sprite("./assets/player/walk/walk0.png", 1.5)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 500
        self.physics_engine = None
        self.speed = 5
        self.score = 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = self.speed
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -self.speed
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -self.speed
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = self.speed

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        self.physics_engine.update()

    def increase_score(self):
        self.score += 1
