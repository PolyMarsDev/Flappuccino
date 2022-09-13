import pygame


class Player:
    def __init__(self, BASE_PATH):
        self.position = pygame.Vector2()
        self.position.xy = 295, 100
        self.velocity = pygame.Vector2()
        self.velocity.xy = 3, 0
        self.acceleration = 0.1
        self.rightSprite = pygame.image.load(BASE_PATH + "/data/gfx/player.png")
        self.leftSprite = pygame.transform.flip(self.rightSprite, True, False)
        self.currentSprite = self.rightSprite
