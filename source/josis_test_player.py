import arcade
from arcade.examples.sprite_health import IndicatorBar

PLAYER_HEALTH = 100
PLAYER_ENERGY = 100
INDICATOR_BAR_OFFSET = 74
SHOOTING_BAR_OFFSET = 64
POWERUP_OFFSET = 89


class Player:
    def __init__(self):
        self.player_sprite = arcade.Sprite("./assets/player/walk/walk0.png", 1.5)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 500
        self.physics_engine = None
        self.speed = 5
        self.score = 0

        self.hasFireShoot = False
        self.hasBombShoot = False
        self.powerups = arcade.SpriteList()
        self.activate_bomb_shoot()
        self.activate_fire_shoot()

        self.health = PLAYER_HEALTH
        self.energy = PLAYER_ENERGY
        self.bar_list = arcade.SpriteList()
        self.indicator_bar: IndicatorBar = IndicatorBar(self, self.bar_list,
                                                        (self.player_sprite.center_x, self.player_sprite.center_y))
        self.shooting_bar: IndicatorBar = IndicatorBar(self, self.bar_list,
                                                       (self.player_sprite.center_x, self.player_sprite.center_y),
                                                       arcade.color.ELECTRIC_CYAN)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.SPACE:
            self.shoot(10)
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = self.speed
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -self.speed
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -self.speed
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = self.speed

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.indicator_bar.position = (
            self.player_sprite.center_x,
            self.player_sprite.center_y + INDICATOR_BAR_OFFSET,
        )
        self.shooting_bar.position = (
            self.player_sprite.center_x,
            self.player_sprite.center_y + SHOOTING_BAR_OFFSET
        )
        x_offset = -42
        for powerup in self.powerups:
            powerup.center_x = self.player_sprite.center_x + x_offset
            powerup.center_y = self.player_sprite.center_y + POWERUP_OFFSET
            x_offset += 20

    def increase_score(self):
        self.score += 1

    def decrease_health(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0

        self.indicator_bar.fullness = (self.health / PLAYER_HEALTH)

    def shoot(self, energy):
        self.energy -= energy
        if self.energy <= 0:
            self.energy = 0

        self.shooting_bar.fullness = (self.energy / PLAYER_ENERGY)

    def activate_fire_shoot(self):
        self.hasFireShoot = True
        sprite = arcade.Sprite("./assets/powerups/Fire.png", 0.14)
        self.powerups.append(sprite)

    def activate_bomb_shoot(self):
        self.hasBombShoot = True
        sprite = arcade.Sprite("./assets/powerups/Bomb.png", 0.14)
        self.powerups.append(sprite)
