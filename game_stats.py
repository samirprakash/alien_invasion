class GameStats:
    def __init__(self, ai_game):
        """ initialize statistics """
        self.settings = ai_game.settings
        self.game_active = False
        self.reset_status()

    def reset_status(self):
        """ initialize statics that can change during the game """
        self.ships_left = self.settings.ship_limit
