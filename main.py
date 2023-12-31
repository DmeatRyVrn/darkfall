import arcade
import constants
import pyglet.gl as gl

PLAYER_MOVEMENT_SPEED = 2
PLAYER_JUMP_SPEED = 10


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.cur_texture = 0
        self.scale = 2
        self.is_walk = False
        self.is_idle_trans = False
        self.is_jump = False
        self.frame_count = 0
        self.cur_speed = 0


        # Track our state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False
        self.delta_time = 0

        # --- Load Textures ---

        # Images from Kenney.nl's Asset Pack 3
        main_path = "resources/persons/oblivious/"

        # Load textures for idle standing
        self.idle_textures = []
        for i in range(1, 15):
            self.idle_textures.append(
                arcade.load_texture(f'{main_path}oblivious_idle{i}.png')
            )
        self.walk_textures = []
        for i in range(1, 7):
            self.walk_textures.append(
                arcade.load_texture(f'{main_path}oblivious_walk{i}.png')
            )
        self.jump_textures = []
        for i in range(1, 6):
            self.jump_textures.append(
                arcade.load_texture(f'{main_path}oblivious_jump{i}.png')
            )
        self.fall_textures = []
        for i in range(1, 3):
            self.jump_textures.append(
                arcade.load_texture(f'{main_path}oblivious_fall{i}.png')
            )

        self.idle_trans_texture = arcade.load_texture(f'{main_path}oblivious_trans.png')
        self.texture = self.idle_textures[0]
        self.hit_box = self.texture.hit_box_points
        #self.hit_box = [(8,0), (8, 32), (21, 32), (21, 0)]


    def update_animation(self, delta_time: float = 1/60):
        #print(self.cur_texture)

        if self.is_idle_trans:
            self.delta_time += delta_time/6
            if self.delta_time >= delta_time:
                self.is_idle_trans = False
                self.delta_time = 0
            self.texture = self.idle_trans_texture
            return
        
        if self.is_jump:
            
            self.delta_time += delta_time/3
            if self.delta_time >= delta_time:

                self.delta_time = 0
                self.cur_texture += 1
                if self.cur_texture >= len(self.jump_textures):
                    self.is_jump = False
                    self.cur_texture = 0
                    self.change_y = PLAYER_JUMP_SPEED
                    self.change_x = self.cur_speed
                    self.cur_speed = 0
            self.texture = self.jump_textures[self.cur_texture]
            return


        if self.change_x == 0:
            self.delta_time += delta_time/3
            if self.delta_time >= delta_time:
                self.delta_time = 0 
                self.cur_texture += 1
            if self.cur_texture >= len(self.idle_textures):
                self.cur_texture = 0
            self.texture = self.idle_textures[self.cur_texture]
            return


        if self.is_walk:
                        
            self.delta_time += delta_time/6
            if self.delta_time >= delta_time:
                self.delta_time = 0
                self.cur_texture += 1

            if self.cur_texture > 5:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture]
            return


class DarkFall(arcade.Window):
    def __init__(self):
        super().__init__(
            constants.SCREEN_WIDTH,
            constants.SCREEN_HEIGHT,
            constants.TITLE)


        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False

        map_name = 'resources/levels/level_1/tiles/darkfall.json'
        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, 2, layer_options)
        self.player = Player()
        self.player.center_x = 80
        self.player.center_y = 320



        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.scene.add_sprite('PLAYER', self.player)
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,

            gravity_constant=1,
            walls=self.scene['Platforms']
        )

    def setup(self):
        pass

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Draw our Scene
        self.scene.draw(filter=gl.GL_NEAREST)

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.scene.update_animation(1/60, ['PLAYER'])

    def process_keychange(self):
        """
        Called when we change a key up/down or we move on/off a ladder.
        """
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = PLAYER_MOVEMENT_SPEED
            elif (
                self.physics_engine.can_jump(y_distance=10)
                and not self.jump_needs_reset
            ):
                
                self.jump_needs_reset = True
                self.player.is_jump = True

        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = -PLAYER_MOVEMENT_SPEED



        # Process left/right
        if self.right_pressed and not self.left_pressed and not self.player.is_jump:
            self.player.cur_speed = PLAYER_MOVEMENT_SPEED
            self.player.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed and not self.player.is_jump:
            self.player.cur_speed = -PLAYER_MOVEMENT_SPEED
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player.change_x = 0
            

    
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        self.player.cur_texture = 0
        if key == arcade.key.UP or key == arcade.key.W:
            self.player.is_idle_trans = True
            
            #self.player.is_jump = True
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
            self.player.is_walk = True
            self.player.is_idle_trans = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
            self.player.is_walk = True
            self.player.is_idle_trans = True

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
            
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
            self.player.is_walk = False
            self.player.is_idle_trans = True

        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
            self.player.is_walk = False
            self.player.is_idle_trans = True
            self.player.cur_speed = 0

        self.process_keychange()


def main():
    window = DarkFall()
    window.set_update_rate(1/60)
    window.setup()
    window.background_color = (55, 104, 128)
    arcade.run()




if __name__ == '__main__':
    main()