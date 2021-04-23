import pygame
class Button:
    def __init__(self, BASE_PATH):
        self.price = 3
        self.level = 1   
        self.sprite = pygame.image.load(BASE_PATH + '/data/gfx/button.png')
        self.typeIndicatorSprite = pygame.image.load(BASE_PATH + '/data/gfx/null_indicator.png')
