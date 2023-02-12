import arcade


class Shot:
    def __init__(self, x, y, change_x, damage, sprite, scene):
        self.damage = damage
        self.sprite = arcade.Sprite(sprite, 1.5)
        self.sprite.center_x = x
        self.sprite.center_y = y
        self.sprite.change_x = change_x
        self.physics_engine = None
        self.scene = scene

    def add_sprite_to_physical_engine(self):
        try:
            self.physics_engine = arcade.PhysicsEnginePlatformer(self.sprite,
                                                                 platforms=self.scene["Moving Platforms"],
                                                                 walls=self.scene["Platforms"],
                                                                 gravity_constant=0.5)
        except KeyError:
            self.physics_engine = arcade.PhysicsEnginePlatformer(self.sprite,
                                                                walls=self.scene["Platforms"],
                                                                gravity_constant=0.5)
