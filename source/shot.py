import arcade

class Shot:
    def __init__(self, x, y, change_x,  damage, sprite):
        self.x = x
        self.y = y
        self.change_x = change_x
        self.damage = damage
        self.sprite = arcade.Sprite(sprite, 1.5)
    


    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 2)