class GameStats:
    def __init__(self, ai_game):
        """ initialize statistics """
        self.settings = ai_game.settings
        self.game_active = True
        self._reset_status()

    def _reset_status(self):
        """ initialize statics that can change during the game """
        self.ships_left = self.settings.ship_limit
