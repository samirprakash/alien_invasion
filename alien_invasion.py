import sys

import pygame

from alien import Alien
from bullet import Bullet
from button import Button
from game_stats import GameStats
from settings import Settings
from ship import Ship


class AlienInvasion:
    """ Overall class to manage game assets and behavior """

    def __init__(self):
        """ Initialize the game and create game resources """
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        # custom screen size
        # self.screen = pygame.display.set_mode(
        #     (self.settings.screen_width, self.settings.screen_height))

        self.bg_color = self.settings.bg_color
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.settings.increase_speed()
        self.play_button = Button(self, "Play")

        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        """ Start the main loop for the game """
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_event(self, event):
        """ Evaluate key press events """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p:
            self._start_game()

    def _check_keyup_events(self, event):
        """ Evaluate key unpressed """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()
            self.settings.initalize_dynamic_settings()

    def _start_game(self):
        self.stats.reset_status()
        self.stats.game_active = True

        self.aliens.empty()
        self.bullets.empty()

        self._create_fleet()
        self.ship.center_ship()

        pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """ Fire bullets - max 3 at a time """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """ Move bullets toward the top and delete after exiting screen boundary """
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_collisions()

    def _check_collisions(self):
        # check if any bullet has hit an alien, remove both if so
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # if all the aliens have been destroyed,
        # create a new fleet and remove all active bullets
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _create_fleet(self):
        """ Create fleet of aliens """
        # find the number of aliens in a row
        # spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # space available to display a row of aliens is equal to
        # total screen width - one alien width for the left margin - one alien width for the right margin
        available_space_x = self.settings.screen_width - (2 * alien_width)
        # calculate the numbr of aliens that can be fitted in the calculated space
        number_aliens_x = available_space_x // (2 * alien_width)
        # get the height of the ship
        ship_height = self.ship.rect.height
        # calculate the space available for displaying the full fleet
        # screen height - one alien height from top - ship height from bottom - 2 more alien heights to create space between ship and fleet
        available_space_y = (
            self.settings.screen_height - (10 * alien_height) - ship_height
        )
        # calculate the number of allowed rows in a fleet
        # there is a gap of one alien height between two rows in fleet
        number_rows = available_space_y // (2 * alien_height)

        # create a full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width = alien.rect.width
        # position an alien w.r.t the previous alien
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """ Update the positions of all aliens in the fleet """
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """ respond to the ship being hit by an alien """

        # as long as a ship is left
        if self.stats.ships_left > 0:
            # decrement ship by 1
            self.stats.ships_left -= 1

            # remove any existing aliens or bullets
            self.aliens.empty()
            self.bullets.empty()

            # create a new fleet
            self._create_fleet()
            self.ship.center_ship()
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """ check and respond when the aliens have touched the bottom of the game screen """

        screen_rect = self.screen.get_rect()

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # emulates alien hitting a ship
                self._ship_hit()
                break

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""

        # Redraw the screen during each pass through the loop
        self.screen.fill(self.bg_color)
        self.ship.blitme()

        # draw bullets on screen when space is pressed
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # draw aliens
        self.aliens.draw(self.screen)

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == "__main__":
    # Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
