import arcade


class MapOne:
    def __init__(self):
        self.sprite_list = arcade.SpriteList(use_spatial_hash=True)

    def setup(self):
        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", 0.5)
            wall.center_x = x
            wall.center_y = 32
            self.sprite_list.append(wall)

        coordinate_list = [[256, 96],
                           [512, 96],
                           [768, 96]]

        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", 0.5)
            wall.position = coordinate
            self.sprite_list.append(wall)
