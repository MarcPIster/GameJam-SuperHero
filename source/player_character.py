import random

import arcade
from arcade.examples.sprite_health import IndicatorBar

PLAYER_HEALTH = 100
PLAYER_ENERGY = 100
INDICATOR_BAR_OFFSET = 74
SHOOTING_BAR_OFFSET = 64
POWERUP_OFFSET = 89


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]


class Player(arcade.Sprite):
    def __init__(self, x, y, sound_manager):
        super().__init__()
        self.sound_manager = sound_manager


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

        self.hasFireShoot = False
        self.hasBombShoot = False
        self.powerups = arcade.SpriteList()

        self.health = PLAYER_HEALTH
        self.energy = PLAYER_ENERGY
        self.energy_timer = 0
        self.bar_list = arcade.SpriteList()
        self.indicator_bar: IndicatorBar = IndicatorBar(self, self.bar_list,
                                                        (self.player_sprite.center_x, self.player_sprite.center_y))
        self.shooting_bar: IndicatorBar = IndicatorBar(self, self.bar_list,
                                                       (self.player_sprite.center_x, self.player_sprite.center_y),
                                                       arcade.color.ELECTRIC_CYAN)

        self.key_up_pressed = False
        self.key_left_pressed = False
        self.key_right_pressed = False
        self.key_shot_pressed = False

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
        self.update_energy(delta_time)

        self.indicator_bar.position = (
            self.center_x,
            self.center_y + INDICATOR_BAR_OFFSET,
        )
        self.shooting_bar.position = (
            self.center_x,
            self.center_y + SHOOTING_BAR_OFFSET
        )
        x_offset = -42
        for powerup in self.powerups:
            powerup.center_x = self.center_x + x_offset
            powerup.center_y = self.center_y + POWERUP_OFFSET
            x_offset += 20
    
    def update(self):
        """ Move the player """
        # Move player.
        # Remove these lines if physics engine is moving player.
        
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
                self.sound_manager.play_sound("jump") # ToDo: Fix jump soumd, animation may not be the best place to play this
                self.cur_texture = 0
            self.texture = self.jump_texture[self.cur_texture][self.facing_direction]
            return

        if self.cur_texture > 5:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.facing_direction]

    def on_key_press(self, key, modifiers):
        if self.disable_movement == 1:
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
            self.shoot(10)

    def on_key_release(self, key, modifiers):
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

    def decrease_health(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.sound_manager.play_sound("dead")
        self.sound_manager.play_sound(f'hurt-{random.randint(1, 4)}')
        self.indicator_bar.fullness = (self.health / PLAYER_HEALTH)

    def shoot(self, energy):
        self.energy -= energy
        if self.energy <= 0:
            self.energy = 0
        self.sound_manager.play_sound("hit")
        self.shooting_bar.fullness = (self.energy / PLAYER_ENERGY)

    def activate_fire_shoot(self):
        if self.hasFireShoot:
            return
        self.hasFireShoot = True
        self.sound_manager.play_sound("item-collect")
        sprite = arcade.Sprite("./assets/powerups/Fire.png", 0.14)
        self.powerups.append(sprite)

    def activate_bomb_shoot(self):
        if self.hasBombShoot:
            return
        self.hasBombShoot = True
        self.sound_manager.play_sound("item-collect")
        sprite = arcade.Sprite("./assets/powerups/Bomb.png", 0.14)
        self.powerups.append(sprite)

    def update_energy(self, delta_time):
        if self.energy_timer > 1:
            self.energy_timer = 0
            self.energy += 5
            if self.energy > PLAYER_ENERGY:
                self.energy = PLAYER_ENERGY
            self.shooting_bar.fullness = (self.energy / PLAYER_ENERGY)
        self.energy_timer += delta_time
