import pygame

class Player:
    position = pygame.Vector2()
    velocity = pygame.Vector2()
    dead = False
    health = 100
    position.xy = 295, 100
    velocity.xy = 3, 0
    acceleration = 0.1
    flapForce = 3
    beanCount = 0
    rightSprite = pygame.image.load('data/gfx/player.png')
    currentSprite = rightSprite
    leftSprite = pygame.transform.flip(rightSprite, True, False)
    
    def reset(self):
        self.position.xy = 295, 100
        self.velocity.xy = 3, 0
        self.acceleration = 0.1
        self.currentSprite = self.rightSprite
        self.dead = False
        self.health = 100
        self.beanCount = 0
        self.flapForce = 3
    
    def invert_death(self):
        self.dead = not self.dead