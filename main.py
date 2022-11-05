import pygame, sys, time, random, colorsys, math, pygame.display as Display
from pygame.locals import *
from pygame.mixer import Sound
from player import Player
from background import Background
from button import Button
from bean import Bean
from utils import *

pygame.init()
# set the display
Display.set_caption('Flappuccino')
Display.set_icon(Bean().sprite)
DISPLAY=Display.set_mode((640,480),pygame.RESIZABLE | pygame.SCALED,32)
player = Player()
# get fonts
font = pygame.font.Font('data/fonts/font.otf', 100)
font_small = pygame.font.Font('data/fonts/font.otf', 32)
font_20 = pygame.font.Font('data/fonts/font.otf', 20)
# get some images
shop = pygame.image.load('data/gfx/shop.png')
shop_bg = pygame.image.load('data/gfx/shop_bg.png')
retry_button = pygame.image.load('data/gfx/retry_button.png')
logo = pygame.image.load('data/gfx/logo.png')
title_bg = pygame.image.load('data/gfx/bg.png')
title_bg.fill((255, 30.599999999999998, 0.0), special_flags=pygame.BLEND_ADD)
shadow = pygame.image.load('data/gfx/shadow.png')
# get sounds
flapfx = Sound("data/sfx/flap.wav")
upgradefx = Sound("data/sfx/upgrade.wav")
beanfx = Sound("data/sfx/bean.wav")
deadfx = Sound("data/sfx/dead.wav")
indicators = ['data/gfx/flap_indicator.png', 'data/gfx/speed_indicator.png', 'data/gfx/beanup_indicator.png']
# colors
WHITE=(255,255,255) # constant

def start():
    global beanMultiplier, beans, buttons, last_time, clicked, jump, dt, mouseX, mouseY
    last_time = time.time()
    clicked = jump = False
    dt = 0
    beanMultiplier = 5
    beans = []
    buttons = []
    mouseX,mouseY = pygame.mouse.get_pos()
    player.reset()
    # adding three buttons
    for i in range(3):
        buttons.append(Button(i, indicators[i]))
    buttons[2].set_price(30) 
    # getting 5 beans
    for i in range(5):
        beans.append(Bean(random.randrange(0, DISPLAY.get_width() - Bean().sprite.get_width()) ,i*-200 - player.position.y))
    Sound.play(flapfx)

def funcOne(toggle = True):
    global dt, last_time, mouseX, mouseY, clicked, keys, jump
    dt = (time.time() - last_time) * 60
    last_time = time.time()
    # get the position of the mouse
    if(toggle):
        mouseX,mouseY = pygame.mouse.get_pos()  
        # getting the keys pressed
        clicked = jump = False
        keys = pygame.key.get_pressed()
    eventHandler()

def eventHandler():
    global jump, clicked
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN and event.key==K_SPACE:
            jump = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked = True
        if clicked and mouseY < DISPLAY.get_height() - 90:
            jump = True
        if event.type==QUIT:
            pygame.quit()
            sys.exit()

def main():
    global clicked, jump, mouseY, dt, mouseX, keys, beanMultiplier, beans, buttons
    start()
    # creating a list of backgrounds, with each index being an object
    bg = [Background(), Background(), Background()]
    # some variables that we need
    startingHeight = player.position.y
    splashScreenTimer = 0
    #splash screen
    while splashScreenTimer < 100:
        funcOne(False)
        splashScreenTimer += dt
        DISPLAY.fill((231, 205, 183))
        # fill the start message on the top of the game
        startMessage = font_small.render("POLYMARS", True, (171, 145, 123))
        DISPLAY.blit(startMessage, (DISPLAY.get_width()/2 - startMessage.get_width()/2, DISPLAY.get_height()/2 - startMessage.get_height()/2))
        # update display
        Display.update()
        # wait for 10 seconds
        pygame.time.delay(10)
    
    titleScreen = True
    # title screen
    Sound.play(flapfx)
    while titleScreen:
        funcOne()
        # so the user clicked, and by any change the mouse's position was on the buttons
        if (clicked and checkCollisions(mouseX, mouseY, 3, 3, DISPLAY.get_width()/2 - retry_button.get_width()/2, 288, retry_button.get_width(), retry_button.get_height())):
            clicked = False
            Sound.play(upgradefx)
            titleScreen = False

        DISPLAY.fill(WHITE)
        DISPLAY.blit(title_bg, (0,0)) 
        DISPLAY.blit(shadow, (0,0)) 
        DISPLAY.blit(logo, (DISPLAY.get_width()/2 - logo.get_width()/2, DISPLAY.get_height()/2 - logo.get_height()/2 + math.sin(time.time()*5)*5 - 25)) 
        DISPLAY.blit(retry_button, (DISPLAY.get_width()/2 - retry_button.get_width()/2, 288))
        startMessage = font_small.render("START", True, (0, 0, 0))
        DISPLAY.blit(startMessage, (DISPLAY.get_width()/2 - startMessage.get_width()/2, 292))

        Display.update()
        pygame.time.delay(10)

    # the main game loop
    while True:
        funcOne()
        
        camOffset = -player.position.y + DISPLAY.get_height()/2 - player.currentSprite.get_size()[1]/2
        
        DISPLAY.fill(WHITE)
        for o in bg:
            o.setSprite(((player.position.y/50) % 100) / 100)
            DISPLAY.blit(o.sprite, (0, o.position))

        color = colorsys.hsv_to_rgb(((player.position.y/50) % 100) / 100,0.5,0.5)
        currentHeightMarker = font.render(str(player.height), True, (color[0]*255, color[1]*255, color[2]*255, 50 ))
        DISPLAY.blit(currentHeightMarker, (DISPLAY.get_width()/2 - currentHeightMarker.get_width()/2, camOffset + round((player.position.y - startingHeight)/DISPLAY.get_height())*DISPLAY.get_height() + player.currentSprite.get_height() - 40))
        
        for bean in beans:
            DISPLAY.blit(bean.sprite, (bean.position.x, bean.position.y + camOffset))
        
        DISPLAY.blit(pygame.transform.rotate(player.currentSprite, clamp(player.velocity.y, -10, 5)*player.rot_offset), (player.position.x,player.position.y + camOffset))
        DISPLAY.blit(shop_bg, (0, 0))
        pygame.draw.rect(DISPLAY,(81,48,20),(21,437,150*(player.health/100),25))
        DISPLAY.blit(shop, (0, 0))
        
        for button in buttons:
            DISPLAY.blit(button.sprite, (220 + (button.index*125), 393))
            priceDisplay = font_small.render(str(button.price), True, (0,0,0))
            DISPLAY.blit(priceDisplay, (262 + (button.index*125), 408))
            levelDisplay = font_20.render('Lvl. ' + str(button.level), True, (200,200,200))
            DISPLAY.blit(levelDisplay, (234 + (button.index*125), 441))
            DISPLAY.blit(button.typeIndicatorSprite, (202 + (button.index*125), 377))
        beanCountDisplay = font_small.render(str(player.beanCount).zfill(7), True, (0,0,0))
        DISPLAY.blit(beanCountDisplay, (72, 394))
        if player.dead:
            DISPLAY.blit(retry_button, (4, 4))
            deathMessage = font_small.render("RETRY", True, (0, 0, 0))
            DISPLAY.blit(deathMessage, (24, 8))
        
        player.set_height(round(-(player.position.y - startingHeight)/DISPLAY.get_height()))
 
        player.position.x += player.velocity.x*dt
        if player.position.x < 0 or player.position.x + player.currentSprite.get_size()[0] > 640:
            player.flip()
        if jump and not player.dead:
            player.velocity.y = -player.flapForce
            Sound.play(flapfx)
        player.position.y += player.velocity.y*dt
        player.velocity.y = clamp(player.velocity.y + player.acceleration*dt, -99999999999, 50)

        player.health -= 0.2*dt
        if player.health <= 0 and not player.dead:
            player.kill(deadfx)
            

        for bean in beans:
            if bean.position.y + camOffset + 90 > DISPLAY.get_height():
                bean.position.y -= DISPLAY.get_height()*2
                bean.position.x = random.randrange(0, DISPLAY.get_width() - bean.sprite.get_width())
            if (checkCollisions(player.position.x, player.position.y, player.currentSprite.get_width(), player.currentSprite.get_height(), bean.position.x, bean.position.y, bean.sprite.get_width(), bean.sprite.get_height())):
                Sound.play(beanfx)
                player.beanCount += 1
                player.health = 100
                bean.position.y -= DISPLAY.get_height() - random.randrange(0, 200)
                bean.position.x = random.randrange(0, DISPLAY.get_width() - bean.sprite.get_width())

        for button in buttons:
            if clicked and not player.dead and checkCollisions(mouseX, mouseY, 3, 3, button.position.x, button.position.y, button.sprite.get_width(), button.sprite.get_height()):
                if (player.beanCount >= button.price):
                    Sound.play(upgradefx)
                    button.level += 1
                    player.beanCount -= button.price
                    button.price = round(button.price*2.5)
                    if (button.index == 0):
                        player.flapForce *= 1.5
                    if (button.index == 1):
                        player.velocity.x *= 1.5
                    if (button.index == 2):
                        beanMultiplier += 10
                        for _ in range(beanMultiplier):
                            beans.append(Bean(random.randrange(0, DISPLAY.get_width() - Bean().sprite.get_width()), player.position.y - DISPLAY.get_height() - random.randrange(0, 200)))
        
        if player.dead and clicked and checkCollisions(mouseX, mouseY, 3, 3, 4, 4, retry_button.get_width(), retry_button.get_height()):
            start()

        bg[0].position = camOffset + round(player.position.y/DISPLAY.get_height())*DISPLAY.get_height()
        bg[1].position = bg[0].position + DISPLAY.get_height() 
        bg[2].position = bg[0].position - DISPLAY.get_height()
        
        Display.update()
        pygame.time.delay(10)

if __name__ == "__main__":
    main()