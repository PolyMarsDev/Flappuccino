def main():
    import pygame

    pygame.init()
    pygame.font.init()
    """
    we make the screen here because the .convert() and .convert_alpha() functions need a initialized pygame screen
    so we first import pygame to initialize the screen then we import the Game class because in that class
    we import the reset of the classes and those classes need the .convert() and .convert_alpha() functions to load
    the images correctly
    """
    WIDTH, HEIGHT = 640, 480
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))

    # set what events are allowed so the for event in pygame.event.get() doesnt have to loop throw all of the pygame events
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN])

    from Parts import Game

    game = Game(WIN=WIN)
    game.splash_screen(duration=100)  # the starter splash screen that is show when the game is launched
    game.title_screen()  # the title screen
    game.run()  # the main loop that the game is in


if __name__ == "__main__":
    main()
