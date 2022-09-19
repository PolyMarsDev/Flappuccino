import pygame
import sys
import time
import random
import colorsys
import math
from pygame.math import Vector2
from pygame.locals import *
from player import Player
from background import Background
from button import Button
from bean import Bean
from utils import clamp
from utils import checkCollisions


def main():
    pygame.init()
    # set the display
    DISPLAY = pygame.display.set_mode((640, 480), 0, 32)
    pygame.display.set_caption('Flappuccino')
    pygame.display.set_icon(Bean().sprite)
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
    title_bg.fill((255, 30.599999999999998, 0.0),
                  special_flags=pygame.BLEND_ADD)
    shadow = pygame.image.load('data/gfx/shadow.png')
    # get sounds
    flapfx = pygame.mixer.Sound("data/sfx/flap.wav")
    upgradefx = pygame.mixer.Sound("data/sfx/upgrade.wav")
    beanfx = pygame.mixer.Sound("data/sfx/bean.wav")
    deadfx = pygame.mixer.Sound("data/sfx/dead.wav")
    # colors
    WHITE = (255, 255, 255)  # constant
    # variables
    rotOffset = -5
    # creating a new object player
    player = Player()
    beans = []
    buttons = []
    # adding three buttons
    for i in range(3):
        buttons.append(Button())
    # now simply loading images based off of indexes in the list
    buttons[0].typeIndicatorSprite = pygame.image.load(
        'data/gfx/flap_indicator.png')
    buttons[0].price = 5
    buttons[1].typeIndicatorSprite = pygame.image.load(
        'data/gfx/speed_indicator.png')
    buttons[1].price = 5
    buttons[2].typeIndicatorSprite = pygame.image.load(
        'data/gfx/beanup_indicator.png')
    buttons[2].price = 30
    # getting 5 beans
    for i in range(5):
        beans.append(Bean())
    # now looping through the beans list
    for bean in beans:
        bean.position.xy = random.randrange(0, DISPLAY.get_width(
        ) - bean.sprite.get_width()), beans.index(bean)*-200 - player.position.y
    # creating a list of backgrounds, with each index being an object
    bg = [Background(), Background(), Background()]
    # some variables that we need
    beanCount = 0
    startingHeight = player.position.y
    height = 0
    health = 100
    flapForce = 3
    beanMultiplier = 5
    dead = False
    # we need the framerate and then the time
    framerate = 60
    last_time = time.time()
    splashScreenTimer = 0
    # splash screen
    # playing a sound
    pygame.mixer.Sound.play(flapfx)
    while splashScreenTimer < 100:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()

        splashScreenTimer += dt

        for event in pygame.event.get():
            # if the user clicks the button
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        DISPLAY.fill((231, 205, 183))
        # fill the start message on the top of the game
        startMessage = font_small.render("POLYMARS", True, (171, 145, 123))
        DISPLAY.blit(startMessage, (DISPLAY.get_width()/2 - startMessage.get_width() /
                     2, DISPLAY.get_height()/2 - startMessage.get_height()/2))

        # update display
        pygame.display.update()
        # wait for 10 seconds
        pygame.time.delay(10)

    titleScreen = True
    # title screen
    pygame.mixer.Sound.play(flapfx)
    while titleScreen:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()
        # get the position of the mouse
        mouseX, mouseY = pygame.mouse.get_pos()
        # getting the keys pressed
        clicked = False
        keys = pygame.key.get_pressed()
        # checking events
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
            # if the player quits
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        # so the user clicked, and by any change the mouse's position was on the buttons
        if (clicked and checkCollisions(mouseX, mouseY, 3, 3, DISPLAY.get_width()/2 - retry_button.get_width()/2, 288, retry_button.get_width(), retry_button.get_height())):
            clicked = False
            pygame.mixer.Sound.play(upgradefx)
            titleScreen = False

        DISPLAY.fill(WHITE)
        DISPLAY.blit(title_bg, (0, 0))
        DISPLAY.blit(shadow, (0, 0))
        DISPLAY.blit(logo, (DISPLAY.get_width()/2 - logo.get_width()/2,
                     DISPLAY.get_height()/2 - logo.get_height()/2 + math.sin(time.time()*5)*5 - 25))
        DISPLAY.blit(retry_button, (DISPLAY.get_width() /
                     2 - retry_button.get_width()/2, 288))
        startMessage = font_small.render("START", True, (0, 0, 0))
        DISPLAY.blit(startMessage, (DISPLAY.get_width() /
                     2 - startMessage.get_width()/2, 292))

        pygame.display.update()
        pygame.time.delay(10)

    # the main game loop
    while True:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()
        # again, get the position
        mouseX, mouseY = pygame.mouse.get_pos()

        jump = False
        clicked = False
        keys = pygame.key.get_pressed()
        # get events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == K_SPACE:
                jump = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
            if clicked and mouseY < DISPLAY.get_height() - 90:
                jump = True
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        camOffset = -player.position.y + DISPLAY.get_height()/2 - \
            player.currentSprite.get_size()[1]/2

        DISPLAY.fill(WHITE)
        for o in bg:
            o.setSprite(((player.position.y/50) % 100) / 100)
            DISPLAY.blit(o.sprite, (0, o.position))

        color = colorsys.hsv_to_rgb(
            ((player.position.y/50) % 100) / 100, 0.5, 0.5)
        currentHeightMarker = font.render(
            str(height), True, (color[0]*255, color[1]*255, color[2]*255, 50))
        DISPLAY.blit(currentHeightMarker, (DISPLAY.get_width()/2 - currentHeightMarker.get_width()/2, camOffset + round(
            (player.position.y - startingHeight)/DISPLAY.get_height())*DISPLAY.get_height() + player.currentSprite.get_height() - 40))

        for bean in beans:
            DISPLAY.blit(bean.sprite, (bean.position.x,
                         bean.position.y + camOffset))

        DISPLAY.blit(pygame.transform.rotate(player.currentSprite, clamp(
            player.velocity.y, -10, 5)*rotOffset), (player.position.x, player.position.y + camOffset))
        DISPLAY.blit(shop_bg, (0, 0))
        pygame.draw.rect(DISPLAY, (81, 48, 20),
                         (21, 437, 150*(health/100), 25))
        DISPLAY.blit(shop, (0, 0))

        for button in buttons:
            DISPLAY.blit(
                button.sprite, (220 + (buttons.index(button)*125), 393))
            priceDisplay = font_small.render(
                str(button.price), True, (0, 0, 0))
            DISPLAY.blit(
                priceDisplay, (262 + (buttons.index(button)*125), 408))
            levelDisplay = font_20.render(
                'Lvl. ' + str(button.level), True, (200, 200, 200))
            DISPLAY.blit(
                levelDisplay, (234 + (buttons.index(button)*125), 441))
            DISPLAY.blit(button.typeIndicatorSprite,
                         (202 + (buttons.index(button)*125), 377))
        beanCountDisplay = font_small.render(
            str(beanCount).zfill(7), True, (0, 0, 0))
        DISPLAY.blit(beanCountDisplay, (72, 394))
        if dead:
            DISPLAY.blit(retry_button, (4, 4))
            deathMessage = font_small.render("RETRY", True, (0, 0, 0))
            DISPLAY.blit(deathMessage, (24, 8))

        height = round(-(player.position.y - startingHeight) /
                       DISPLAY.get_height())

        player.position.x += player.velocity.x*dt
        if player.position.x + player.currentSprite.get_size()[0] > 640:
            player.velocity.x = -abs(player.velocity.x)
            player.currentSprite = player.leftSprite
            rotOffset = 5
        if player.position.x < 0:
            player.velocity.x = abs(player.velocity.x)
            player.currentSprite = player.rightSprite
            rotOffset = -5
        if jump and not dead:
            player.velocity.y = -flapForce
            pygame.mixer.Sound.play(flapfx)
        player.position.y += player.velocity.y*dt
        player.velocity.y = clamp(
            player.velocity.y + player.acceleration*dt, -99999999999, 50)

        health -= 0.2*dt
        if health <= 0 and not dead:
            dead = True
            pygame.mixer.Sound.play(deadfx)

        for bean in beans:
            if bean.position.y + camOffset + 90 > DISPLAY.get_height():
                bean.position.y -= DISPLAY.get_height()*2
                bean.position.x = random.randrange(
                    0, DISPLAY.get_width() - bean.sprite.get_width())
            if (checkCollisions(player.position.x, player.position.y, player.currentSprite.get_width(), player.currentSprite.get_height(), bean.position.x, bean.position.y, bean.sprite.get_width(), bean.sprite.get_height())):
                dead = False
                pygame.mixer.Sound.play(beanfx)
                beanCount += 1
                health = 100
                bean.position.y -= DISPLAY.get_height() - random.randrange(0, 200)
                bean.position.x = random.randrange(
                    0, DISPLAY.get_width() - bean.sprite.get_width())

        for button in buttons:
            buttonX, buttonY = 220 + (buttons.index(button)*125), 393
            if clicked and not dead and checkCollisions(mouseX, mouseY, 3, 3, buttonX, buttonY, button.sprite.get_width(), button.sprite.get_height()):
                if (beanCount >= button.price):
                    pygame.mixer.Sound.play(upgradefx)
                    button.level += 1
                    beanCount -= button.price
                    button.price = round(button.price*2.5)
                    if (buttons.index(button) == 0):
                        flapForce *= 1.5
                    if (buttons.index(button) == 1):
                        player.velocity.x *= 1.5
                    if (buttons.index(button) == 2):
                        oldBeanMultipler = beanMultiplier
                        beanMultiplier += 10
                        for i in range(beanMultiplier):
                            beans.append(Bean())
                            beans[-1].position.xy = random.randrange(0, DISPLAY.get_width() - bean.sprite.get_width(
                            )), player.position.y - DISPLAY.get_height() - random.randrange(0, 200)

        if dead and clicked and checkCollisions(mouseX, mouseY, 3, 3, 4, 4, retry_button.get_width(), retry_button.get_height()):
            health = 100
            player.velocity.xy = 3, 0
            player.position.xy = 295, 100
            player.currentSprite = player.rightSprite
            beanCount = 0
            height = 0
            flapForce = 3
            beanMultiplier = 5
            buttons = []
            for i in range(3):
                buttons.append(Button())
            buttons[0].typeIndicatorSprite = pygame.image.load(
                'data/gfx/flap_indicator.png')
            buttons[0].price = 5
            buttons[1].typeIndicatorSprite = pygame.image.load(
                'data/gfx/speed_indicator.png')
            buttons[1].price = 5
            buttons[2].typeIndicatorSprite = pygame.image.load(
                'data/gfx/beanup_indicator.png')
            buttons[2].price = 30
            beans = []
            for i in range(5):
                beans.append(Bean())
            for bean in beans:
                bean.position.xy = random.randrange(0, DISPLAY.get_width(
                ) - bean.sprite.get_width()), beans.index(bean)*-200 - player.position.y
            pygame.mixer.Sound.play(upgradefx)
            dead = False

        bg[0].position = camOffset + \
            round(player.position.y/DISPLAY.get_height())*DISPLAY.get_height()
        bg[1].position = bg[0].position + DISPLAY.get_height()
        bg[2].position = bg[0].position - DISPLAY.get_height()

        pygame.display.update()
        pygame.time.delay(10)


if __name__ == "__main__":
    main()
