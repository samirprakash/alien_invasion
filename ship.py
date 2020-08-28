""" Ship class """
import pygame


class Ship:
    """ A class to manage the ship """

    def __init__(self, ai_game):
        """ Initialize the ship and set its starting position """
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        """ Load the ship image and get its rect """
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.float_x = float(self.rect.x)

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
