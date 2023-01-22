import pygame

class Player:
    position = pygame.Vector2()
    velocity = pygame.Vector2()
    right_sprite = pygame.image.load('data/gfx/player.png')
    left_sprite = pygame.transform.flip(right_sprite, True, False)
    
    def __init__(self):
        self.dead = False
        self.health = 100
        self.height = 0
        self.position.xy = 295, 100
        self.velocity.xy = 3, 0
        self.acceleration = 0.1
        self.flap_force = 3
        self.bean_count = 0
        self.rot_offset = -5
        self.current_sprite = self.right_sprite
    
    def reset(self) -> None:
        self.__init__()
    
    def kill(self, sound: str) -> None:
        self.dead = True
        pygame.mixer.Sound.play(sound)
        
    def set_height(self, new_height: float) -> None:
        self.height = new_height
        
    def flip(self) -> None:
        self.velocity.x *= -1
        self.rot_offset *= -1
        if self.current_sprite == self.right_sprite:
            self.current_sprite = self.left_sprite
        else:
            self.current_sprite = self.right_sprite