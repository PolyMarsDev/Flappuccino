import pygame


class Button:
    def __init__(self):
        self.price = 3
        self.level = 1   
    sprite = pygame.image.load('data/gfx/button.png').convert_alpha()
    type_indicator_sprite = pygame.image.load('data/gfx/null_indicator.png').convert_alpha()
