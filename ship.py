import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """ A class to manage the ship """

    def __init__(self, ai_game):
        """ Initialize the ship and set its starting position """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        """ Load the ship image and get its rect """
        self.image = pygame.image.load("images/ship.bmp")
        self.image.convert()
        self.rect = self.image.get_rect()

        # Start each new ship at the center bottom of the screen
        self.center_ship()

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """ Update the position based on the movement flag """
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.float_x += self.settings.ship_speed

        if self.moving_left and self.rect.left > 0:
            self.float_x -= self.settings.ship_speed

        self.rect.x = self.float_x

    def blitme(self):
        """ Draw the image at its current location """
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        # Start each new ship at the center bottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.float_x = float(self.rect.x)
