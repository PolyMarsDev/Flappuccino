import pygame
import sys
import time
import random
import colorsys
import math
import pygame.display as Display
from pygame.locals import *
from pygame.mixer import Sound
from pygame.font import Font
from pygame.image import load as Image
from player import Player
from background import Background
from button import Button
from bean import Bean
from utils import *

pygame.init()
# set the display
Display.set_caption('Flappuccino')
Display.set_icon(Bean().sprite)
DISPLAY = Display.set_mode((640,480),pygame.RESIZABLE | pygame.SCALED,32)
player = Player()
# get sounds
flapfx = Sound("data/sfx/flap.wav")

def start():
    global bean_multiplier, beans, buttons, last_time, clicked, jump, dt, mouse_x, mouse_y, scroll
    indicators = ['data/gfx/flap_indicator.png', 'data/gfx/speed_indicator.png', 'data/gfx/beanup_indicator.png']
    last_time = time.time()
    clicked = False
    jump = False
    scroll = True
    dt = 0
    bean_multiplier = 5
    beans = []
    buttons = []
    mouse_x, mouse_y = pygame.mouse.get_pos()
    player.reset()
    # adding three buttons
    for i in range(3):
        buttons.append(Button(i, indicators[i]))
    buttons[2].set_price(30) 
    # getting 5 beans
    for i in range(5):
        beans.append(Bean(random.randrange(0, DISPLAY.get_width() - Bean().sprite.get_width()) ,i*-200 - player.position.y))
    Sound.play(flapfx)

def func_one(toggle = True):
    global dt, last_time, mouse_x, mouse_y, clicked, keys, jump
    # calculate the change in time (dt)
    dt = (time.time() - last_time) * 60
    # save the current time
    last_time = time.time()
    if(toggle):
        # resetting clicked and jump flags to false
        clicked = jump = False
        # get the position of the mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()  
        # getting the keys pressed
        keys = pygame.key.get_pressed()
    event_handler()

def event_handler():
    global jump, clicked
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN and event.key==K_SPACE:
            jump = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked = True
        if clicked and mouse_y < DISPLAY.get_height() - 90:
            jump = True
        if event.type==QUIT:
            pygame.quit()
            sys.exit()

def main():
    global clicked, jump, mouse_y, dt, mouse_x, keys, bean_multiplier, beans, buttons, scroll
    start()
    # get fonts
    font = Font('data/fonts/font.otf', 100)
    font_small = Font('data/fonts/font.otf', 32)
    font_20 = Font('data/fonts/font.otf', 20)
    # get some images
    shop = Image('data/gfx/shop.png')
    shop_bg = Image('data/gfx/shop_bg.png')
    retry_button = Image('data/gfx/retry_button.png')
    logo = Image('data/gfx/logo.png')
    title_bg = Image('data/gfx/bg.png')
    title_bg.fill((255, 30.599999999999998, 0.0), special_flags=pygame.BLEND_ADD)
    shadow = Image('data/gfx/shadow.png')
    upgradefx = Sound("data/sfx/upgrade.wav")
    beanfx = Sound("data/sfx/bean.wav")
    deadfx = Sound("data/sfx/dead.wav")
    # colors
    WHITE=(255,255,255) # constant
    # creating a list of backgrounds, with each index being an object
    bg = [Background(), Background(), Background()]
    # startingHeight = 100 (the initial y position of the player)
    starting_height = player.position.y
    splash_screen_timer = 0
    #splash screen
    while splash_screen_timer < 100:
        func_one(False)
        splash_screen_timer += dt
        DISPLAY.fill((231, 205, 183))
        # fill the start message on the top of the game
        start_message = font_small.render("POLYMARS", True, (171, 145, 123))
        DISPLAY.blit(start_message, (DISPLAY.get_width()/2 - start_message.get_width()/2, DISPLAY.get_height()/2 - start_message.get_height()/2))
        # update display
        Display.update()
        # wait for 10 seconds
        pygame.time.delay(10)
    
    title_screen = True
    # title screen
    Sound.play(flapfx)
    while title_screen:
        func_one()
        # so the user clicked, and by any change the mouse's position was on the buttons
        if (clicked and check_collisions(mouse_x, mouse_y, 3, 3, DISPLAY.get_width()/2 - retry_button.get_width()/2, 288, retry_button.get_width(), retry_button.get_height())):
            clicked = False
            title_screen = False
            Sound.play(upgradefx)

        DISPLAY.fill(WHITE)
        DISPLAY.blit(title_bg, (0,0)) 
        DISPLAY.blit(shadow, (0,0)) 
        DISPLAY.blit(logo, (DISPLAY.get_width()/2 - logo.get_width()/2, DISPLAY.get_height()/2 - logo.get_height()/2 + math.sin(time.time()*5)*5 - 25)) 
        DISPLAY.blit(retry_button, (DISPLAY.get_width()/2 - retry_button.get_width()/2, 288))
        start_message = font_small.render("START", True, (0, 0, 0))
        DISPLAY.blit(start_message, (DISPLAY.get_width()/2 - start_message.get_width()/2, 292))

        Display.update()
        pygame.time.delay(10)

    # the main game loop
    while True:
        func_one()
        
        cam_offset = -player.position.y + (DISPLAY.get_height() - player.current_sprite.get_size()[1])/2
        if(cam_offset <= 0):
            if(not player.dead):
                player.kill(deadfx)
            scroll = False
            cam_offset = 0
        
        DISPLAY.fill(WHITE)
        for o in bg:
            o.setSprite(((player.position.y/50) % 100) / 100)
            DISPLAY.blit(o.sprite, (0, o.position))
        color = colorsys.hsv_to_rgb(((player.position.y/50) % 100) / 100,0.5,0.5)
        current_height_marker = font.render(str(player.height), True, (color[0]*255, color[1]*255, color[2]*255, 50 ))
        DISPLAY.blit(current_height_marker, (DISPLAY.get_width()/2 - current_height_marker.get_width()/2, cam_offset + round((player.position.y - starting_height)/DISPLAY.get_height())*DISPLAY.get_height() + player.current_sprite.get_height() - 40))
        
        
        for bean in beans:
            DISPLAY.blit(bean.sprite, (bean.position.x, bean.position.y + cam_offset))
        
        DISPLAY.blit(pygame.transform.rotate(player.current_sprite, clamp(player.velocity.y, -10, 5)*player.rot_offset), (player.position.x,player.position.y + cam_offset))
        DISPLAY.blit(shop_bg, (0, 0))
        pygame.draw.rect(DISPLAY,(81,48,20),(21,437,150*(player.health/100),25))
        DISPLAY.blit(shop, (0, 0))
        
        for button in buttons:
            DISPLAY.blit(button.sprite, (220 + (button.index*125), 393))
            price_display = font_small.render(str(button.price), True, (0,0,0))
            DISPLAY.blit(price_display, (262 + (button.index*125), 408))
            level_display = font_20.render(f'Lvl. {button.level}', True, (200,200,200))
            DISPLAY.blit(level_display, (234 + (button.index*125), 441))
            DISPLAY.blit(button.type_indicator_sprite, (202 + (button.index*125), 377))
        bean_count_display = font_small.render(str(player.bean_count).zfill(7), True, (0,0,0))
        DISPLAY.blit(bean_count_display, (72, 394))
        if player.dead:
            DISPLAY.blit(retry_button, (4, 4))
            death_message = font_small.render("RETRY", True, (0, 0, 0))
            DISPLAY.blit(death_message, (24, 8))
        
        if(scroll):
            player.set_height(round(-(player.position.y - starting_height)/DISPLAY.get_height()))
            player.position.x += player.velocity.x*dt
            if player.position.x < 0 or player.position.x + player.current_sprite.get_size()[0] > 640:
                player.flip()
            if jump and not player.dead:
                player.velocity.y = -player.flap_force
                Sound.play(flapfx)
            player.position.y += player.velocity.y*dt
            player.velocity.y = clamp(player.velocity.y + player.acceleration*dt, -99999999999, 50)

        if not player.dead:
            player.health -= 0.2*dt
            if player.health <= 0:
                player.kill(deadfx)

        for bean in beans:
            if bean.position.y + cam_offset + 90 > DISPLAY.get_height():
                bean.position.y -= DISPLAY.get_height()*2
                bean.position.x = random.randrange(0, DISPLAY.get_width() - bean.sprite.get_width())
            if (check_collisions(player.position.x, player.position.y, player.current_sprite.get_width(), player.current_sprite.get_height(), bean.position.x, bean.position.y, bean.sprite.get_width(), bean.sprite.get_height())):
                Sound.play(beanfx)
                player.bean_count += 1
                player.health = 100
                bean.position.y -= DISPLAY.get_height() - random.randrange(0, 200)
                bean.position.x = random.randrange(0, DISPLAY.get_width() - bean.sprite.get_width())

        for button in buttons:
            if clicked and not player.dead and check_collisions(mouse_x, mouse_y, 3, 3, button.position.x, button.position.y, button.sprite.get_width(), button.sprite.get_height()):
                if (player.bean_count >= button.price):
                    Sound.play(upgradefx)
                    button.level += 1
                    player.bean_count -= button.price
                    button.price = round(button.price*2.5)
                    if (button.index == 0):
                        player.flap_force *= 1.5
                    if (button.index == 1):
                        player.velocity.x *= 1.5
                    if (button.index == 2):
                        bean_multiplier += 5
                        for _ in range(bean_multiplier):
                            beans.append(Bean(random.randrange(0, DISPLAY.get_width() - Bean().sprite.get_width()), player.position.y - DISPLAY.get_height() - random.randrange(0, 200)))
        
        if player.dead and clicked and check_collisions(mouse_x, mouse_y, 3, 3, 4, 4, retry_button.get_width(), retry_button.get_height()):
            start()

        bg[0].position = cam_offset + round(player.position.y/DISPLAY.get_height())*DISPLAY.get_height()
        bg[1].position = bg[0].position + DISPLAY.get_height() 
        bg[2].position = bg[0].position - DISPLAY.get_height()
        
        Display.update()
        pygame.time.delay(10)

if __name__ == "__main__":
    main()