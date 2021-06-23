import pygame


class Bean: 
    def __init__(self):
        self.sprite = pygame.image.load('data/gfx/bean.png').convert_alpha()
        self.position = pygame.Vector2()
        self.position.xy
