import arcade
from math import sqrt
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


class Enemy(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.enemy_sprite = arcade.Sprite("./assets/enemy/idle/idle6.png")
        self.enemy_sprite.center_x = 300
        self.enemy_sprite.center_y = 500
        self.scale = 0.6
        self.physics_engine = None
        self.screen_width = x
        self.screen_height = y
        self.deltaAnimTime = 0
        self.speed = 3
        self.jump_height = 10

        self.health = PLAYER_HEALTH
        self.bar_list = arcade.SpriteList()
        self.indicator_bar: IndicatorBar = IndicatorBar(self, self.bar_list,
                                                        (self.enemy_sprite.center_x, self.enemy_sprite.center_y))

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
        # 0 == right
        # 1 == left
        self.shoot_direction = None

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
        self.animHit = ["./assets/enemy/attack/attack2.png", "./assets/enemy/attack/attack3.png",
                        "./assets/enemy/attack/attack4.png"]
        self.animJump = ["./assets/enemy/walk/walk1.png", "./assets/enemy/walk/walk2.png",
                         "./assets/enemy/walk/walk3.png",
                         "./assets/enemy/walk/walk4.png", "./assets/enemy/walk/walk5.png",
                         "./assets/enemy/walk/walk6.png",
                         "./assets/enemy/walk/walk7.png", "./assets/enemy/walk/walk8.png"]
        self.animKnockedDown = ["./assets/enemy/die/die1.png", "./assets/enemy/die/die2.png",
                                "./assets/enemy/die/die3.png",
                                "./assets/enemy/die/die4.png", "./assets/enemy/die/die5.png"]
        self.animShoot = ["./assets/enemy/attack/attack1.png", "./assets/enemy/attack/attack2.png",
                          "./assets/enemy/attack/attack3.png",
                          "./assets/enemy/attack/attack4.png", "./assets/enemy/attack/attack5.png",
                          "./assets/enemy/attack/attack6.png",
                          "./assets/enemy/attack/attack7.png"]
        self.animShot = ["./assets/enemy/germ.png"]
        self.animWalk = ["./assets/enemy/walk/walk1.png", "./assets/enemy/walk/walk2.png",
                         "./assets/enemy/walk/walk3.png",
                         "./assets/enemy/walk/walk4.png", "./assets/enemy/walk/walk5.png",
                         "./assets/enemy/walk/walk6.png",
                         "./assets/enemy/walk/walk7.png", "./assets/enemy/walk/walk8.png"]
        self.animIdle = ["./assets/enemy/idle/idle5.png", "./assets/enemy/idle/idle6.png"]

        for i in range(len(self.animWalk)):
            texture = load_texture_pair(self.animWalk[i])
            self.walk_textures.append(texture)

        for i in range(len(self.animIdle)):
            texture = load_texture_pair(self.animIdle[i])
            self.idle_textures.append(texture)

        for i in range(len(self.animHit)):
            texture = load_texture_pair(self.animHit[i])
            self.hit_texture.append(texture)

        for i in range(len(self.animJump)):
            texture = load_texture_pair(self.animJump[i])
            self.jump_texture.append(texture)

        for i in range(len(self.animShoot)):
            texture = load_texture_pair(self.animShoot[i])
            self.shoot_texture.append(texture)

        self.shot_texture.append(load_texture_pair(self.animShot[0]))

        for i in range(len(self.animKnockedDown)):
            texture = load_texture_pair(self.animKnockedDown[i])
            self.knocked_texture.append(texture)

        self.texture = self.walk_textures[0][self.facing_direction]

    def on_update(self, delta_time, player_list):
        self.physics_engine.update()
        self.decide_movement(player_list)

        self.indicator_bar.position = (
            self.center_x,
            self.center_y + INDICATOR_BAR_OFFSET,
        )

    def update(self):
        """ Move the enemy """

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

    def update_animation(self, delta_time):
        self.deltaAnimTime += delta_time

        if self.deltaAnimTime < 0.15:
            return
        self.deltaAnimTime = 0

        if self.shot == 1:
            self.cur_texture += 1
            if self.cur_texture > 6:
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
            direction = self.shoot_direction
            if direction is None:
                direction = self.facing_direction
            self.texture = self.idle_textures[self.cur_texture][direction]
            return

        if self.change_y != 0 or self.key_up_pressed:
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.jump_texture[self.cur_texture][self.facing_direction]
            return

        if self.cur_texture > 7:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.facing_direction]

    def decide_movement(self, player_list):
        # find the closest player in player_list
        closest_player_index = 0
        closest_player_distance = None
        for i in range(len(player_list)):
            player = player_list[i]
            distance = sqrt((player.center_x - self.center_x) ** 2 + (player.center_y - self.center_y) ** 2)
            if closest_player_distance is None or distance < closest_player_distance:
                closest_player_distance = distance
                closest_player_index = i

        player = player_list[closest_player_index]
        # follow player and shoot
        if self.shot != 1:
            if player.center_x > self.center_x:
                self.key_right_pressed = True
                self.key_left_pressed = False
            else:
                self.key_left_pressed = True
                self.key_right_pressed = False
            if player.center_y > self.center_y:
                self.key_up_pressed = True
            else:
                self.key_up_pressed = False
            if abs(player.center_x - self.center_x) < 250 and abs(player.center_y - self.center_y) < 50:
                self.key_left_pressed = False
                self.key_right_pressed = False
                self.key_up_pressed = False
                self.spacePressed = 0
                self.shoot_direction = player.center_x < self.center_x
                self.shoot()
            else:
                self.spacePressed = 1
                self.shoot_direction = None

    def decrease_health(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0

        self.indicator_bar.fullness = (self.health / PLAYER_HEALTH)

    def shoot(self):
        print("Imagine enemy shooting here")
