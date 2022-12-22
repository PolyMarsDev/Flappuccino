import pygame, sys, time, random, colorsys, math
from pygame.locals import *
from player import Player
from background import Background
from button import Button
from bean import Bean
from utils import clamp
from utils import checkCollisions
from constant import *

class Game():
    def __init__(self):
        pygame.init()
        
        self.font = pygame.font.Font('data/fonts/font.otf', 100)
        self.font_small = pygame.font.Font('data/fonts/font.otf', 32)
        self.font_20 = pygame.font.Font('data/fonts/font.otf', 20)
        # get some images
        self.shop = pygame.image.load('data/gfx/shop.png')
        self.shop_bg = pygame.image.load('data/gfx/shop_bg.png')
        self.retry_button = pygame.image.load('data/gfx/retry_button.png')
        self.logo = pygame.image.load('data/gfx/logo.png')
        self.title_bg = pygame.image.load('data/gfx/bg.png')
        self.title_bg.fill((255, 30.599999999999998, 0.0), special_flags=pygame.BLEND_ADD)
        self.shadow = pygame.image.load('data/gfx/shadow.png')
        # get sounds
        self.flapfx = pygame.mixer.Sound("data/sfx/flap.wav")
        self.upgradefx = pygame.mixer.Sound("data/sfx/upgrade.wav")
        self.beanfx = pygame.mixer.Sound("data/sfx/bean.wav")
        self.deadfx = pygame.mixer.Sound("data/sfx/dead.wav")
        
        self.display = self.set_display_settings()
        self.player = Player()

    def set_player(self):
        self.player.velocity.xy = 3, 0
        self.player.position.xy = 295, 100
        self.player.currentSprite = self.player.rightSprite

    def set_display_settings(self):
        pygame.display.set_caption('Flappuccino')
        pygame.display.set_icon(Bean().sprite)
        return pygame.display.set_mode((640,480),0,32)

    def load_game(self):
        self.beans = []
        self.buttons = []
        
        # adding three buttons
        self.buttons.append(Button(5, 1, 'data/gfx/button.png', 'data/gfx/flap_indicator.png'))
        self.buttons.append(Button(5, 1, 'data/gfx/button.png', 'data/gfx/speed_indicator.png'))
        self.buttons.append(Button(30, 1, 'data/gfx/button.png', 'data/gfx/beanup_indicator.png'))

        self.beans.append(Bean([random.randrange(0, self.display.get_width() - Bean().sprite.get_width()), 0*-200 - self.player.position.y]))
        self.beans.append(Bean([random.randrange(0, self.display.get_width() - Bean().sprite.get_width()), 1*-200 - self.player.position.y]))
        self.beans.append(Bean([random.randrange(0, self.display.get_width() - Bean().sprite.get_width()), 2*-200 - self.player.position.y]))
        self.beans.append(Bean([random.randrange(0, self.display.get_width() - Bean().sprite.get_width()), 3*-200 - self.player.position.y]))
        self.beans.append(Bean([random.randrange(0, self.display.get_width() - Bean().sprite.get_width()), 4*-200 - self.player.position.y]))
        
        # creating a list of backgrounds, with each index being an object
        self.bg = [Background(), Background(), Background()]
        # some variables that we need
        self.beanCount = 0
        self.startingHeight = self.player.position.y
        self.height = 0
        self.health = 100
        self.flapForce = 3
        self.beanMultiplier = 5
        self.oldBeanMultipler = 5
        self.dead = False

        self.last_time = time.time()
        self.splashScreenTimer = 0
        #splash screen
        # playing a sound

    def set_framerate(self):
        dt = time.time() - self.last_time
        dt *= 60
        self.last_time = time.time()
        return dt

    def splash_screen(self):
        dt = self.set_framerate()

        self.splashScreenTimer += dt

        for event in pygame.event.get():
            # if the user clicks the button
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
                
        # update display
        pygame.display.update()
        # wait for 10 seconds
        pygame.time.delay(10)
        
        self.display.fill((231, 205, 183))
        # fill the start message on the top of the game
        startMessage = self.font_small.render("POLYMARS", True, (171, 145, 123))
        self.display.blit(startMessage, (self.display.get_width()/2 - startMessage.get_width()/2, self.display.get_height()/2 - startMessage.get_height()/2))
        
    def title_screen(self):
        dt = self.set_framerate()
        # get the position of the mouse
        mouseX,mouseY = pygame.mouse.get_pos()  
        # getting the keys pressed
        clicked = False
        # checking events
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
            # if the player quits
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        # so the user clicked, and by any change the mouse's position was on the buttons
        if (clicked and checkCollisions(mouseX, mouseY, 3, 3, self.display.get_width()/2 - self.retry_button.get_width()/2, 288, self.retry_button.get_width(), self.retry_button.get_height())):
            clicked = False
            pygame.mixer.Sound.play(self.upgradefx)
            self.titleScreen = False

        self.display.fill(WHITE)
        self.display.blit(self.title_bg, (0,0)) 
        self.display.blit(self.shadow, (0,0)) 
        self.display.blit(self.logo, (self.display.get_width()/2 - self.logo.get_width()/2, self.display.get_height()/2 - self.logo.get_height()/2 + math.sin(time.time()*5)*5 - 25)) 
        self.display.blit(self.retry_button, (self.display.get_width()/2 - self.retry_button.get_width()/2, 288))
        startMessage = self.font_small.render("START", True, (0, 0, 0))
        self.display.blit(startMessage, (self.display.get_width()/2 - startMessage.get_width()/2, 292))

        pygame.display.update()
        pygame.time.delay(10)
        
    def main(self):
        self.load_game()
        pygame.mixer.Sound.play(self.flapfx)
        
        while self.splashScreenTimer < 100:
            self.splash_screen()  
        
        self.titleScreen = True
        # title screen
        pygame.mixer.Sound.play(self.flapfx)
        while self.titleScreen:
            self.title_screen()

        # the main game loop
        while True:
            self.main_game()

    def main_game(self):
        rotOffset = -5
        
        dt = self.set_framerate()
        # again, get the position
        mouseX,mouseY = pygame.mouse.get_pos()

        jump = False
        clicked = False
            # get events
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN and event.key==K_SPACE:
                jump = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
            if clicked and mouseY < self.display.get_height() - 90:
                jump = True
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            
        camOffset = -self.player.position.y + self.display.get_height()/2 - self.player.currentSprite.get_size()[1]/2

        self.display.fill(WHITE)
        for o in self.bg:
            o.setSprite(((self.player.position.y/50) % 100) / 100)
            self.display.blit(o.sprite, (0, o.position))

        color = colorsys.hsv_to_rgb(((self.player.position.y/50) % 100) / 100,0.5,0.5)
        currentHeightMarker = self.font.render(str(self.height), True, (color[0]*255, color[1]*255, color[2]*255, 50 ))
        self.display.blit(currentHeightMarker, (self.display.get_width()/2 - currentHeightMarker.get_width()/2, camOffset + round((self.player.position.y - self.startingHeight)/self.display.get_height())*self.display.get_height() + self.player.currentSprite.get_height() - 40))
            
        for bean in self.beans:
            self.display.blit(bean.sprite, (bean.position.x, bean.position.y + camOffset))
            
        self.display.blit(pygame.transform.rotate(self.player.currentSprite, clamp(self.player.velocity.y, -10, 5)*rotOffset), (self.player.position.x, self.player.position.y + camOffset))
        self.display.blit(self.shop_bg, (0, 0))
        pygame.draw.rect(self.display,(81,48,20),(21,437,150*(self.health/100),25))
        self.display.blit(self.shop, (0, 0))
            
        for button in self.buttons:
            self.display.blit(button.sprite, (220 + (self.buttons.index(button)*125), 393))
            priceDisplay = self.font_small.render(str(button.price), True, (0,0,0))
            self.display.blit(priceDisplay, (262 + (self.buttons.index(button)*125), 408))
            levelDisplay = self.font_20.render('Lvl. ' + str(button.level), True, (200,200,200))
            self.display.blit(levelDisplay, (234 + (self.buttons.index(button)*125), 441))
            self.display.blit(button.indicator, (202 + (self.buttons.index(button)*125), 377))
        beanCountDisplay = self.font_small.render(str(self.beanCount).zfill(7), True, (0,0,0))
        self.display.blit(beanCountDisplay, (72, 394))
        if self.dead:
            self.display.blit(self.retry_button, (4, 4))
            deathMessage = self.font_small.render("RETRY", True, (0, 0, 0))
            self.display.blit(deathMessage, (24, 8))
            
        self.height = round(-(self.player.position.y - self.startingHeight)/self.display.get_height())
    
        self.player.position.x += self.player.velocity.x*dt
        if self.player.position.x + self.player.currentSprite.get_size()[0] > 640:
            self.player.velocity.x = -abs(self.player.velocity.x)
            self.player.currentSprite = self.player.leftSprite
            rotOffset = 5
        if self.player.position.x < 0:
            self.player.velocity.x = abs(self.player.velocity.x)
            self.player.currentSprite = self.player.rightSprite
            rotOffset = -5
        if jump and not self.dead:
            self.player.velocity.y = - self.flapForce
            pygame.mixer.Sound.play(self.flapfx)
        self.player.position.y += self.player.velocity.y*dt
        self.player.velocity.y = clamp(self.player.velocity.y + self.player.acceleration*dt, -99999999999, 50)

        self.health -= 0.2*dt
        if self.health <= 0 and not self.dead:
            self.dead = True
            pygame.mixer.Sound.play(self.deadfx)

        for bean in self.beans:
            if bean.position.y + camOffset + 90 > self.display.get_height():
                bean.position.y -= self.display.get_height()*2
                bean.position.x = random.randrange(0, self.display.get_width() - bean.sprite.get_width())
            if (checkCollisions(self.player.position.x, self.player.position.y, self.player.currentSprite.get_width(), self.player.currentSprite.get_height(), bean.position.x, bean.position.y, bean.sprite.get_width(), bean.sprite.get_height())):
                self.dead = False
                pygame.mixer.Sound.play(self.beanfx)
                self.beanCount += 1
                self.health = 100
                bean.position.y -= self.display.get_height() - random.randrange(0, 200)
                bean.position.x = random.randrange(0, self.display.get_width() - bean.sprite.get_width())

        for button in self.buttons:
            buttonX,buttonY = 220 + (self.buttons.index(button)*125), 393
            if clicked and not self.dead and checkCollisions(mouseX, mouseY, 3, 3, buttonX, buttonY, button.sprite.get_width(), button.sprite.get_height()):
                if (self.beanCount >= button.price):
                    pygame.mixer.Sound.play(self.upgradefx)
                    button.level += 1
                    self.beanCount -= button.price
                    button.price = round(button.price*2.5)
                    if (self.buttons.index(button) == 0):
                        self.flapForce *= 1.5
                    if (self.buttons.index(button) == 1):
                        self.player.velocity.x *= 1.5
                    if (self.buttons.index(button) == 2):
                        self.oldBeanMultipler = self.beanMultiplier
                        self.beanMultiplier += 10
                        for i in range(self.beanMultiplier):
                            self.beans.append(Bean())
                            self.beans[-1].position.xy = random.randrange(0, self.display.get_width() - bean.sprite.get_width()), self.player.position.y - self.display.get_height() - random.randrange(0, 200)
            
        if self.dead and clicked and checkCollisions(mouseX, mouseY, 3, 3, 4, 4, self.retry_button.get_width(), self.retry_button.get_height()):
            self.set_player()
            self.load_game()
            pygame.mixer.Sound.play(self.upgradefx)

        self.bg[0].position = camOffset + round(self.player.position.y/self.display.get_height())*self.display.get_height()
        self.bg[1].position = self.bg[0].position + self.display.get_height() 
        self.bg[2].position = self.bg[0].position - self.display.get_height()

        pygame.display.update()
        pygame.time.delay(10)

if __name__ == "__main__":
    game = Game()
    game.main()