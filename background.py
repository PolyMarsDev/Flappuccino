import pygame
import colorsys

class Background:
    uncolored_sprite = pygame.image.load('data/gfx/bg.png')
    
    def __init__(self):
        self.sprite = pygame.image.load('data/gfx/bg.png')
        self.position = 0
        
    def set_sprite(self, tint: float) -> None:  
        copy = self.uncolored_sprite.copy()
        color = colorsys.hsv_to_rgb(tint,1,1)
        copy.fill((color[0]*255, color[1]*255, color[2]*255), special_flags=pygame.BLEND_ADD)
        self.sprite = copy