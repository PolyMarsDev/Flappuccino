import pygame
from pygame.image import load
class Button:
    sprite = load('data/gfx/button.png')
    typeIndicatorSprite = load('data/gfx/null_indicator.png')
    
    def __init__(self, index, indicator):
        self.price = 5
        self.level = 1
        self.index = index
        self.typeIndicatorSprite = load(indicator)
        self.position = pygame.Vector2()
        self.position.xy = 220 + (self.index*125), 393
        
    def set_price(self, newPrice):
        self.price = newPrice