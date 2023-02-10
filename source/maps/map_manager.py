import arcade


class MapManager:
    def __init__(self):
        self.tile_map = None

    def load_level(self, level):
        map_name = f"./assets/map/level{level}.json"

        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
            "Moving Platforms": {
                "use_spatial_hash": False,
            },
            "Coins": {
                "use_spatial_hash": True,
            },
        }
        self.tile_map = arcade.load_tilemap(map_name, 0.391, layer_options)
        return self.tile_map
