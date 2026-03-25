import pygame
from code.Menu import Menu
from code.Level import Level


class Game:

    def __init__(self):

        pygame.init()

        self.window = pygame.display.set_mode((800,600))
        pygame.display.set_caption("Feed The Dog")

        self.menu = Menu(self.window)
        self.level = Level(self.window)

    def run(self):

        while True:

            state = self.menu.run()

            if state == "start":
                self.level.run()