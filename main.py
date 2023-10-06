import arcade
import constants
import pyglet.gl as gl


class DarkFall(arcade.Window):
    def __init__(self):
        super().__init__(
            constants.SCREEN_WIDTH,
            constants.SCREEN_HEIGHT,
            constants.TITLE)
        
        map_name = 'resources/levels/level_1/tiles/darkfall.json'
        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, 2, layer_options)

        

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

    def setup(self):
        pass

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Draw our Scene
        self.scene.draw(filter=gl.GL_NEAREST)





def main():
    window = DarkFall()
    window.set_update_rate(1/60)
    window.setup()
    window.background_color = (55,104,128)
    arcade.run()

if __name__ == '__main__':
    main()