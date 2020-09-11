class GameStats:
    def __init__(self, ai_game):
        """ initialize statistics """
        self.settings = ai_game.settings
        self.game_active = False
        self.reset_status()
        self.high_score = 0

    def reset_status(self):
        """ initialize statics that can change during the game """
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
