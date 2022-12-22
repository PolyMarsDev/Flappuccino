import pygame
class Bean: 
    def __init__(self, xy = [0,0]):
        self.sprite = pygame.image.load('data/gfx/bean.png')
        self.position = pygame.Vector2()
        self.position.xy = xy