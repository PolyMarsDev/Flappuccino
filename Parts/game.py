import colorsys
import math
import pygame
import random
import sys
import time

from . import Background
from . import Bean
from . import Button
from . import Player
from . import check_collisions
from . import clamp


class Game:
    def __init__(self, WIN: pygame.surface.Surface):

        # set the display
        self.WIN = WIN
        pygame.display.set_caption("Flappuccino")
        pygame.display.set_icon(Bean().sprite)

        # get fonts
        self.font = pygame.font.Font('data/fonts/font.otf', 100)
        self.font_small = pygame.font.Font('data/fonts/font.otf', 32)
        self.font_20 = pygame.font.Font('data/fonts/font.otf', 20)

        # load the images
        """
        .convert() and .convert_alpha() are a FPS improvement as when you use the blit function the surface has to be  
        converted to pixels then drawn with the .convert() and .convert_alpha() it converts the image to pixels at the point that 
        it is written in the difference between .convert() and .convert_alpha() is that .convert_alpha() keeps the alpha
        layer intact. the game may start a bit slower but later when there are a lot of bean sprites drawn to the screen
        it is going to help with the performance 
        """
        self.shop = pygame.image.load('data/gfx/shop.png').convert_alpha()
        self.shop_bg = pygame.image.load('data/gfx/shop_bg.png').convert_alpha()
        self.retry_button = pygame.image.load('data/gfx/retry_button.png').convert_alpha()
        self.logo = pygame.image.load('data/gfx/logo.png').convert_alpha()
        self.title_bg = pygame.image.load('data/gfx/bg.png').convert_alpha()
        self.title_bg.fill([255, 30.599999999999998, 0.0], special_flags=pygame.BLEND_ADD)
        self.shadow = pygame.image.load('data/gfx/shadow.png').convert_alpha()

        # get sounds
        self.flap_fx = pygame.mixer.Sound("data/sfx/flap.wav")
        self.upgrade_fx = pygame.mixer.Sound("data/sfx/upgrade.wav")
        self.bean_fx = pygame.mixer.Sound("data/sfx/bean.wav")
        self.dead_fx = pygame.mixer.Sound("data/sfx/dead.wav")

        # create clock obj and set the FPS
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # constants
        self.WHITE = (255, 255, 255)

        # creating a new object player
        self.player = Player()

        # variables
        self.rot_offset = -5
        self.cam_offset = -self.player.position.y + self.WIN.get_height() / 2 - self.player.currentSprite.get_size()[
            1] / 2

        # creating the buttons
        self.buttons = [Button() for _ in range(3)]
        # now simply loading images based off of indexes in the list
        self.buttons[0].type_indicator_sprite = pygame.image.load('data/gfx/flap_indicator.png').convert_alpha()
        self.buttons[0].price = 5
        self.buttons[1].type_indicator_sprite = pygame.image.load('data/gfx/speed_indicator.png').convert_alpha()
        self.buttons[1].price = 5
        self.buttons[2].type_indicator_sprite = pygame.image.load('data/gfx/beanup_indicator.png').convert_alpha()
        self.buttons[2].price = 30

        # creating 5 beans
        self.beans = [Bean() for _ in range(5)]
        # now looping through the beans list
        for bean in self.beans:
            bean.position.xy = random.randrange(0, self.WIN.get_width() - bean.sprite.get_width()), self.beans.index(
                bean) * -200 - self.player.position.y
        # creating a list of backgrounds, with each index being an object
        self.bgs = [Background(), Background(), Background()]
        # some variables that we need
        self.bean_count = 0
        self.starting_height = self.player.position.y
        self.height = 0
        self.health = 100
        self.flap_force = 3
        self.bean_multiplier = 5
        self.dead = False

    def splash_screen(self, duration: int=100):
        last_time = time.time()
        splash_screen_timer = 0

        # draw now because the screen is not updating and there is no reason to refresh the screen for no reason
        # fill the start message on the top of the game
        self.WIN.fill((231, 205, 183))
        start_message = self.font_small.render("POLYMARS", True, (171, 145, 123))
        self.WIN.blit(start_message, (self.WIN.get_width() / 2 - start_message.get_width() / 2,
                                      self.WIN.get_height() / 2 - start_message.get_height() / 2))

        # update display
        pygame.display.update()

        pygame.mixer.Sound.play(self.flap_fx)
        while splash_screen_timer < duration:
            dt = time.time() - last_time
            dt *= 60
            last_time = time.time()

            splash_screen_timer += dt

            # loop throw the events
            for event in pygame.event.get():
                # if the user clicks the button
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(-1)

            # wait for 10 seconds
            pygame.time.delay(10)

    def title_screen(self):
        last_time = time.time()

        pygame.mixer.Sound.play(self.flap_fx)
        while True:
            dt = time.time() - last_time
            dt *= 60
            last_time = time.time()

            # checking events
            for event in pygame.event.get():
                # if the player quits
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # check if the user has pressed the left mouse button
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # so the user clicked, and by any change the mouse's position was on the buttons
                    if pygame.Rect(self.WIN.get_width() / 2 - self.retry_button.get_width() / 2, 288,
                                   self.retry_button.get_width(), self.retry_button.get_height()).collidepoint(event.pos):
                        pygame.mixer.Sound.play(self.upgrade_fx)
                        # the return statement returns None by default. when a function returns a value it exits the function
                        return

            self.WIN.fill(self.WHITE)
            self.WIN.blit(self.title_bg, (0, 0))
            self.WIN.blit(self.shadow, (0, 0))
            self.WIN.blit(self.logo, (self.WIN.get_width() / 2 - self.logo.get_width() / 2,
                                      self.WIN.get_height() / 2 - self.logo.get_height() / 2 + math.sin(
                                          time.time() * 5) * 5 - 25))
            self.WIN.blit(self.retry_button, (self.WIN.get_width() / 2 - self.retry_button.get_width() / 2, 288))
            start_message = self.font_small.render("START", True, (0, 0, 0))
            self.WIN.blit(start_message, (self.WIN.get_width() / 2 - start_message.get_width() / 2, 292))

            pygame.display.update()
            pygame.time.delay(10)

    def event_handler(self):
        """
        the event handler for the main function
        :return: None
        """
        # get events
        for event in pygame.event.get():
            # if the user wants to quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                # the -1 in sys.exit() is optional but is used to say when the user exited with the button pressed
                # 0: compiled with no error
                # 1: run into an error
                # -1: the user exited with the cancel button/terminate
                sys.exit(-1)
            # jump
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN and \
                    event.button == 1 and pygame.mouse.get_pos()[1] <= self.WIN.get_height() - 90:
                if not self.dead:
                    self.player.velocity.y = -self.flap_force
                    pygame.mixer.Sound.play(self.flap_fx)
            # check for click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # check for button pressed (event.pos returns a tuple (x: int, y: int) of the place that the mouse was pressed)
                if event.pos[1] >= self.WIN.get_height() - 90:
                    # loop throw the buttons
                    for button in self.buttons:
                        # get the button x and y
                        button_x, button_y = 220 + (self.buttons.index(button) * 125), 393
                        # check if a button was made (we do the collision with a pygame.Rect() obj with the .collidepoint method)
                        if not self.dead and pygame.Rect(button_x, button_y, button.sprite.get_width(),
                                                         button.sprite.get_height()).collidepoint(event.pos):
                            # check if we have enough beans to buy the upgrade
                            if self.bean_count >= button.price:
                                pygame.mixer.Sound.play(self.upgrade_fx)
                                button.level += 1
                                self.bean_count -= button.price
                                button.price = round(button.price * 2.5)
                                # check what button was pressed so we give the correct buff
                                if self.buttons.index(button) == 0:
                                    self.flap_force *= 1.5
                                if self.buttons.index(button) == 1:
                                    self.player.velocity.x *= 1.5
                                if self.buttons.index(button) == 2:
                                    self.bean_multiplier += 10
                                    # add extra beans and set the location for them
                                    for _ in range(self.bean_multiplier):
                                        self.beans.append(Bean())
                                        self.beans[-1].position.xy = random.randrange(
                                            0,
                                            self.WIN.get_width() - Bean().sprite.get_width()), self.player.position.y - self.WIN.get_height() - random.randrange(
                                            0, 200)
                # check if the user clicked the retry button
                # creating a pygame.Rect obj and check if the button is inside it with the method collidepoint((x, y))
                if self.dead and pygame.Rect(4, 4, self.retry_button.get_width(),
                                             self.retry_button.get_height()).collidepoint(event.pos):

                    # reset variables
                    self.health = 100
                    self.player.velocity.xy = 3, 0
                    self.player.position.xy = 295, 100
                    self.player.currentSprite = self.player.rightSprite
                    self.bean_count = 0
                    self.height = 0
                    self.flap_force = 3
                    self.bean_multiplier = 5
                    # reset buttons
                    self.buttons = [Button() for _ in range(3)]
                    self.buttons[0].type_indicator_sprite = pygame.image.load(
                        'data/gfx/flap_indicator.png').convert_alpha()
                    self.buttons[0].price = 5
                    self.buttons[1].type_indicator_sprite = pygame.image.load(
                        'data/gfx/speed_indicator.png').convert_alpha()
                    self.buttons[1].price = 5
                    self.buttons[2].type_indicator_sprite = pygame.image.load(
                        'data/gfx/beanup_indicator.png').convert_alpha()
                    self.buttons[2].price = 30
                    # reset beans
                    self.beans = [Bean() for _ in range(5)]
                    for bean in self.beans:
                        bean.position.xy = random.randrange(0,
                                                            self.WIN.get_width() - bean.sprite.get_width()), self.beans.index(
                            bean) * -200 - self.player.position.y
                    pygame.mixer.Sound.play(self.upgrade_fx)
                    self.dead = False

    def collision(self):
        """
        the collisions between:
        beans-player and beans is out of the screen
        :return:
        """
        # check if the bird has collided with one of the beans
        for bean in self.beans:
            # check if the beans is out of the screen
            if bean.position.y + self.cam_offset + 90 > self.WIN.get_height():
                bean.position.y -= self.WIN.get_height() * 2
                bean.position.x = random.randrange(0, self.WIN.get_width() - bean.sprite.get_width())
            # check if the bean has collided with the bird
            if check_collisions(self.player.position.x, self.player.position.y, self.player.currentSprite.get_width(),
                                self.player.currentSprite.get_height(), bean.position.x, bean.position.y,
                                bean.sprite.get_width(), bean.sprite.get_height()):
                self.dead = False
                pygame.mixer.Sound.play(self.bean_fx)
                self.bean_count += 1
                self.health = 100
                bean.position.y -= self.WIN.get_height() - random.randrange(0, 200)
                bean.position.x = random.randrange(0, self.WIN.get_width() - bean.sprite.get_width())

    def draw(self):
        """
        it handles all of the drawing for the run method
        :return:
        """
        # fill the background firstly
        self.WIN.fill(self.WHITE)
        # draw the background in the correct location
        for bg in self.bgs:
            bg.setSprite(((self.player.position.y / 50) % 100) / 100)
            self.WIN.blit(bg.sprite, (0, bg.position))

        color = colorsys.hsv_to_rgb(((self.player.position.y / 50) % 100) / 100, 0.5, 0.5)
        currentHeightMarker = self.font.render(str(self.height), True,
                                               (color[0] * 255, color[1] * 255, color[2] * 255, 50))
        self.WIN.blit(currentHeightMarker, (self.WIN.get_width() / 2 - currentHeightMarker.get_width() / 2,
                                            self.cam_offset + round((
                                                                            self.player.position.y - self.starting_height) / self.WIN.get_height()) * self.WIN.get_height() + self.player.currentSprite.get_height() - 40))

        for bean in self.beans:
            self.WIN.blit(bean.sprite, (bean.position.x, bean.position.y + self.cam_offset))

        self.WIN.blit(
            pygame.transform.rotate(self.player.currentSprite, clamp(self.player.velocity.y, -10, 5) * self.rot_offset),
            (self.player.position.x, self.player.position.y + self.cam_offset))
        self.WIN.blit(self.shop_bg, (0, 0))
        pygame.draw.rect(self.WIN, (81, 48, 20), (21, 437, round(150 * (self.health / 100)), 25))
        self.WIN.blit(self.shop, (0, 0))

        for button in self.buttons:
            self.WIN.blit(button.sprite, (220 + (self.buttons.index(button) * 125), 393))
            price_label = self.font_small.render(str(button.price), True, (0, 0, 0))
            self.WIN.blit(price_label, (262 + (self.buttons.index(button) * 125), 408))
            level_label = self.font_20.render('Lvl. ' + str(button.level), True, (200, 200, 200))
            self.WIN.blit(level_label, (234 + (self.buttons.index(button) * 125), 441))
            self.WIN.blit(button.type_indicator_sprite, (202 + (self.buttons.index(button) * 125), 377))
        bean_count_label = self.font_small.render(str(self.bean_count).zfill(7), True, (0, 0, 0))
        self.WIN.blit(bean_count_label, (72, 394))
        if self.dead:
            self.WIN.blit(self.retry_button, (4, 4))
            message_message = self.font_small.render("RETRY", True, (0, 0, 0))
            self.WIN.blit(message_message, (24, 8))

    def run(self):
        """
        the main method that is called when you want to run the game
        :return: None
        """
        last_time = time.time()

        while True:
            self.event_handler()
            self.draw()
            self.collision()
            dt = time.time() - last_time
            dt *= 60
            last_time = time.time()

            self.cam_offset = -self.player.position.y + self.WIN.get_height() / 2 - self.player.currentSprite.get_size()[1] / 2
            self.height = round(-(self.player.position.y - self.starting_height) / self.WIN.get_height())

            self.player.position.x += self.player.velocity.x * dt
            if self.player.position.x + self.player.currentSprite.get_size()[0] >= 640:
                self.player.velocity.x = -abs(self.player.velocity.x)
                self.player.currentSprite = self.player.leftSprite
                self.rot_offset = 5
            if self.player.position.x <= 0:
                self.player.velocity.x = abs(self.player.velocity.x)
                self.player.currentSprite = self.player.rightSprite
                self.rot_offset = -5
            # change the players y position
            self.player.position.y += self.player.velocity.y * dt
            self.player.velocity.y = clamp(self.player.velocity.y + self.player.acceleration * dt, -99999999999, 50)

            # change the health of the bird
            self.health -= 0.2 * dt
            # check if the health of the bird is less that 0
            if self.health <= 0 and not self.dead:
                self.dead = True
                pygame.mixer.Sound.play(self.dead_fx)

            # change the background positions
            self.bgs[0].position = self.cam_offset + round(
                self.player.position.y / self.WIN.get_height()) * self.WIN.get_height()
            self.bgs[1].position = self.bgs[0].position + self.WIN.get_height()
            self.bgs[2].position = self.bgs[0].position - self.WIN.get_height()

            pygame.display.update()
            pygame.time.delay(10)
