import pygame

class Button:
    def __init__(self, price = 3, level = 1, sprite = None, indicator = None):
        self.price = price
        self.level = level
        self.sprite = pygame.image.load(sprite)
        self.indicator = pygame.image.load(indicator)
        
    def change_indicator(self, path = None):
        self.indicator = pygame.image.load(path)