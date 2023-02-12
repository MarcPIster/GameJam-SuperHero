import arcade


class Shot:
    def __init__(self, x, y, change_x, damage, sprite):
        self.x = x
        self.y = y
        self.change_x = change_x
        self.damage = damage
        self.sprite = arcade.Sprite(sprite, 1.5)
        self.physics_engine = None

    def add_sprite_to_physical_engine(self):
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.sprite,
                                                             gravity_constant=0.5)
