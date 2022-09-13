import pygame


class Bean:
    def __init__(self, BASE_PATH):
        self.sprite = pygame.image.load(BASE_PATH + "/data/gfx/bean.png")
        self.position = pygame.Vector2()
        self.position.xy
