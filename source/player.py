import pygame

class player:
    def __init__(self):
        self.animHit = ["./assets/player/hit/hit0.png", "./assets/player/hit/hit1.png"]
        self.animJump = ["./assets/player/jump/jump0.png", "./assets/player/jump/jump1.png"]
        self.animKnockedDown = ["./assets/player/knockedDown/down0.png", "./assets/player/knockedDown/down1.png", "./assets/player/knockedDown/down2.png",
                                "./assets/player/knockedDown/down3.png", "./assets/player/knockedDown/down4.png", "./assets/player/knockedDown/down5.png",
                                "./assets/player/knockedDown/down6.png"]
        self.animShoot = ["./assets/player/shoot/shoot0.png", "./assets/player/shoot/shoot1.png"]
        self.animShot = "./assets/player/shoot/shot.png"
        self.animWalk = ["./assets/player/walk/walk0.png", "./assets/player/walk/walk1.png", "./assets/player/walk/walk2.png", "./assets/player/walk/walk3.png",
                         "./assets/player/walk/walk4.png", "./assets/player/walk/walk5.png"]
        self.pos = [0, 0]
