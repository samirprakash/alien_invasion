import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # load the image and set its rect
        self.image = pygame.image.load("images/alien.bmp")
        self.image.convert()
        self.rect = self.image.get_rect()

        # position the alient to the top-left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def update(self):
        """ Move alien to right """
        self.x += self.settings.alien_speed
        self.rect.x = self.x
