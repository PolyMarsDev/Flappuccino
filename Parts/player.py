import pygame


class Player:
    position = pygame.Vector2()
    position.xy = 295, 100
    velocity = pygame.Vector2()
    acceleration = 0.1
    velocity.xy = 3, 0
    rightSprite = pygame.image.load('data/gfx/player.png').convert_alpha()
    leftSprite = pygame.transform.flip(rightSprite, True, False)
    currentSprite = rightSprite
