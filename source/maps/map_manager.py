import arcade


class MapManager:
    def __init__(self):
        self.tile_map = None

    def get_level_one(self):
        return self.load_level("./assets/map/level1.json")

    def get_level_two(self):
        return self.load_level("./assets/map/level2.json")

    def get_level_three(self):
        return self.load_level("./assets/map/level3.json")

    def load_level(self, path):
        map_name = path

        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
        }
        self.tile_map = arcade.load_tilemap(map_name, 0.391, layer_options)
        return self.tile_map
