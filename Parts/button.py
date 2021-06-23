import pygame


class Button:
    def __init__(self):
        self.level = 1
        self.price = 3
    sprite = pygame.image.load('data/gfx/button.png').convert_alpha()
    type_indicator_sprite = pygame.image.load('data/gfx/null_indicator.png').convert_alpha()
