import pygame
import colorsys


class Background:
    def __init__(self):
        self.sprite = pygame.image.load('data/gfx/bg.png').convert_alpha()
        self.uncoloredSprite = pygame.image.load('data/gfx/bg.png').convert_alpha()
        self.position = 0

    def setSprite(self, tint):
        copy = self.uncoloredSprite.copy()
        color = colorsys.hsv_to_rgb(tint, 1, 1)
        copy.fill((color[0] * 255, color[1] * 255, color[2] * 255), special_flags=pygame.BLEND_ADD)
        self.sprite = copy
