import pygame
class Bean: 
    sprite = pygame.image.load('data/gfx/bean.png')
    
    def __init__(self):
        self.position = pygame.Vector2()
        self.position.xy