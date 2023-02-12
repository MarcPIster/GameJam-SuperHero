import arcade


class Shot:
    def __init__(self, x, y, speed, jumpiness, damage, sprite, scene, scale=1.5):
        self.damage = damage
        self.sprite = arcade.Sprite(sprite, 1.5)
        self.sprite.scale = scale
        self.sprite.center_x = x
        self.sprite.center_y = y
        self.sprite.change_x = speed
        self.sprite.change_y = jumpiness
        self.speed = speed
        self.physics_engine = None
        self.scene = scene
        self.hit = False

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

    def set_speed(self, speed):
        self.speed = speed
        self.sprite.change_x = speed
