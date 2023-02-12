import arcade
import pyglet
from source.game_mode import Gamemode,Playermode

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]

class Player(arcade.Sprite):
    def __init__(self, x, y, mode=1):
        super().__init__()
        self.player_sprite = arcade.Sprite("./assets/player/walk/walk0.png", 1.5)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 500
        self.physics_engine = None
        self.screen_width = x
        self.screen_height = y
        self.deltaAnimTime = 0
        self.speed = 4
        self.score = 0
        self.jump_height = 10
        self.key_up_pressed = False
        self.key_left_pressed = False
        self.key_right_pressed = False
        self.key_shot_pressed = False
        self.player_mode = mode

        # 0 == no
        # 1 == yes
        self.getHit = 0

        # 0 == no
        # 1 == yes
        self.shot = 0

        # 0 == no
        # 1 == yes
        self.spacePressed = 0

        # 0 == right
        # 1 == left
        self.facing_direction = 0

        # 0 == no
        # 1 == yes
        self.disable_movement = 0

        self.cur_texture = 0
        self.animHit = []
        self.animJump = []
        self.animKnockedDown = []
        self.animShoot = []
        self.animShot = []
        self.animWalk = []
        self.animIdle = []
        self.walk_textures = []
        self.idle_textures = []
        self.hit_texture = []
        self.jump_texture = []
        self.shoot_texture = []
        self.shot_texture = []
        self.knocked_texture = []
        self.set_up()

        # get a list of all controllers:
        if self.player_mode == Playermode.DUO.value:
            controllers = pyglet.input.get_controllers()
            if controllers:
                self.controller = controllers[0]
                self.controller.open()

    def set_up(self):
        self.animHit = ["./assets/player/hit/hit0.png", "./assets/player/hit/hit1.png"]
        self.animJump = ["./assets/player/jump/jump0.png", "./assets/player/jump/jump1.png"]
        self.animKnockedDown = ["./assets/player/knockedDown/down0.png", "./assets/player/knockedDown/down1.png", "./assets/player/knockedDown/down2.png",
                                "./assets/player/knockedDown/down3.png", "./assets/player/knockedDown/down4.png", "./assets/player/knockedDown/down5.png",
                                "./assets/player/knockedDown/down6.png"]
        self.animShoot = ["./assets/player/shoot/shoot0.png", "./assets/player/shoot/shoot1.png"]
        self.animShot = ["./assets/player/shoot/shot.png"]
        self.animWalk = ["./assets/player/walk/walk0.png", "./assets/player/walk/walk1.png", "./assets/player/walk/walk2.png", "./assets/player/walk/walk3.png",
                         "./assets/player/walk/walk4.png", "./assets/player/walk/walk5.png"]
        self.animIdle = ["./assets/player/walk/walk0.png", "./assets/player/walk/walk2.png"]

        for i in range(6):
            texture = load_texture_pair(self.animWalk[i])
            self.walk_textures.append(texture)
        
        for i in range(2):
            texture = load_texture_pair(self.animIdle[i])
            self.idle_textures.append(texture)

        for i in range(2):
            texture = load_texture_pair(self.animHit[i])
            self.hit_texture.append(texture)
        
        for i in range(2):
            texture = load_texture_pair(self.animJump[i])
            self.jump_texture.append(texture)
        
        for i in range(2):
            texture = load_texture_pair(self.animShoot[i])
            self.shoot_texture.append(texture)
        
        self.shot_texture.append(load_texture_pair(self.animShot[0]))

        for i in range(7):
            texture = load_texture_pair(self.animKnockedDown[i])
            self.knocked_texture.append(texture)
        

        self.texture = self.walk_textures[0][self.facing_direction]

    def on_update(self, delta_time):
        self.physics_engine.update()
    
    def update(self):
        """ Move the player """
        # Move player.
        # Remove these lines if physics engine is moving player.
        if self.player_mode == Playermode.DUO.value:
            self.on_key_press_second()
            self.on_key_release_second()
        

        if self.disable_movement != 1:
            if self.key_left_pressed:
                self.center_x += -self.speed
                self.facing_direction = 1
            if self.key_right_pressed:
                self.center_x += self.speed
                self.facing_direction = 0
            if self.key_up_pressed:
                self.center_y += self.jump_height

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > self.screen_width - 1:
            self.right = self.screen_width - 1

    def increase_score(self):
        self.score += 1
    
    def update_animation(self, delta_time):
        self.deltaAnimTime += delta_time

        
        if self.deltaAnimTime < 0.15:
            return
        self.deltaAnimTime = 0

        if self.shot == 1:
            self.cur_texture += 1
            if self.cur_texture > 1:
                self.cur_texture = 0
            if self.key_left_pressed:
                self.texture = self.shoot_texture[self.cur_texture][1]
            else:
                self.texture = self.shoot_texture[self.cur_texture][0]
            self.deltaAnimTime = 0
            return 
        
        self.cur_texture += 1

        if self.key_up_pressed == False and self.key_right_pressed == False and self.key_left_pressed == False:
            if self.cur_texture > 1:
                self.cur_texture = 0
            self.texture = self.idle_textures[self.cur_texture][self.facing_direction]
            return

        if self.change_y != 0 or self.key_up_pressed:
            if self.cur_texture > 1:
                self.cur_texture = 0
            self.texture = self.jump_texture[self.cur_texture][self.facing_direction]
            return

        if self.cur_texture > 5:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.facing_direction]

    def on_key_press(self, key, modifiers):
        if self.disable_movement == 1 or self.player_mode == Playermode.DUO.value:
            return

        if (key == arcade.key.UP or key == arcade.key.W) and self.spacePressed != 1:
            self.spacePressed = 1
            self.key_up_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.key_left_pressed = True
            self.facing_direction = 1
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.key_right_pressed = True
            self.facing_direction = 0
        elif (key == arcade.key.SPACE or key == arcade.key.NUM_0) and self.shot != 1:
            self.shot = 1
            self.disable_movement = 1
            self.key_shot_pressed = True

    def on_key_release(self, key, modifiers):
        if self.player_mode == Playermode.DUO.value:
            return

        if key == arcade.key.UP or key == arcade.key.W:
            self.spacePressed = 0
            self.key_up_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.key_left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.key_right_pressed = False
        elif key == arcade.key.SPACE or key == arcade.key.NUM_0:
            self.shot = 0
            self.disable_movement = 0
            self.key_shot_pressed = False

    def on_key_press_second(self):
        if self.disable_movement == 1:
            return

        if self.controller.x == True and self.spacePressed != 1:
            self.spacePressed = 1
            self.key_up_pressed = True
        if round(self.controller.leftx, 0) == -1:
            self.key_left_pressed = True
            self.facing_direction = 1
        if round(self.controller.leftx, 0) == 1:
            self.key_right_pressed = True
            self.facing_direction = 0
        if self.controller.b == True and self.shot != 1:
            self.shot = 1
            self.disable_movement = 1
            self.key_shot_pressed = True

    def on_key_release_second(self):
        if self.controller.x == False:
            self.spacePressed = 0
            self.key_up_pressed = False
        if self.controller.leftx >= 0 and self.controller.leftx <= 0.4:
            self.key_left_pressed = False
            self.key_right_pressed = False
        if self.controller.b == False:
            self.shot = 0
            self.disable_movement = 0
            self.key_shot_pressed = False

    def update_second(self):
        """ Move the player """
        # Move player.
        # Remove these lines if physics engine is moving player.
        self.on_key_press_second()
        self.on_key_release_second()
        
        self.facing_direction = 0

        if self.disable_movement != 1:
            if self.key_left_pressed:
                self.center_x += -self.speed
                self.facing_direction = 1
            if self.key_right_pressed:
                self.center_x += self.speed
            if self.key_up_pressed:
                self.center_y += self.jump_height

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > self.screen_width - 1:
            self.right = self.screen_width - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > self.screen_height - 1:
            self.top = self.screen_height - 1
