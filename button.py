import pygame
class Button:
    sprite = pygame.image.load('data/gfx/button.png')
    typeIndicatorSprite = pygame.image.load('data/gfx/null_indicator.png')
    
    def __init__(self):
        self.price = 3
        self.level = 1
        
    def set_price(self, newPrice):
        self.price = newPrice
    
    def set_indicator(self, indicator):
        self.typeIndicatorSprite = pygame.image.load(indicator)