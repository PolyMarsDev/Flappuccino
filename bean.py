import pygame
class Bean: 
    sprite = pygame.image.load('data/gfx/bean.png')
    
    def __init__(self, x_pos = 0, y_pos = 0):
        self.position = pygame.Vector2()
        self.position.xy = x_pos, y_pos