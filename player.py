import pygame

class Player:
    position = pygame.Vector2()
    velocity = pygame.Vector2()
    rightSprite = pygame.image.load('data/gfx/player.png')
    leftSprite = pygame.transform.flip(rightSprite, True, False)
    
    def __init__(self):
        self.dead = False
        self.health = 100
        self.height = 0
        self.position.xy = 295, 100
        self.velocity.xy = 3, 0
        self.acceleration = 0.1
        self.flapForce = 3
        self.beanCount = 0
        self.rot_offset = -5
        self.currentSprite = self.rightSprite
    
    def reset(self):
        self.__init__()
    
    def kill(self, sound):
        self.dead = True
        pygame.mixer.Sound.play(sound)
        
    def set_height(self, new_height):
        self.height = new_height
        
    def flip(self):
        self.velocity.x *= -1
        self.rot_offset *= -1
        if self.currentSprite == self.rightSprite:
            self.currentSprite = self.leftSprite
        else:
            self.currentSprite = self.rightSprite