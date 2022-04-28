from powerups import PowerUp
from utils import debug_print


class ExpandPaddle(PowerUp):
    def __init__(self, powerups, row_number, col_number, game):
        super().__init__(powerups, row_number, col_number, game)
        self.game = game
        self.symbol = "E"

    def start_powerup(self):
        self.game.paddle.increase_size()
        super().start_powerup()

    def end_powerup(self):
        self.game.paddle.decrease_size()
        super().end_powerup()


class ShrinkPaddle(PowerUp):
    def __init__(self, powerups, row_number, col_number, game):
        super().__init__(powerups, row_number, col_number, game)
        self.game = game
        self.symbol = "S"

    def start_powerup(self):
        self.game.paddle.decrease_size()
        super().start_powerup()

    def end_powerup(self):
        self.game.paddle.increase_size()
        super().end_powerup()


class GrabbyPaddle(PowerUp):
    def __init__(self, powerups, row_number, col_number, game):
        super().__init__(powerups, row_number, col_number, game)
        self.game = game
        self.symbol = "G"

    def start_powerup(self):
        self.game.paddle.add_grabby()
        super().start_powerup()

    def end_powerup(self):
        self.game.paddle.remove_grabby()
        super().end_powerup()

    def is_alive(self):
        self.game.paddle.add_grabby()
        return super().is_alive()


class ShootyPaddle(PowerUp):
    def __init__(self, powerups, row_number, col_number, game):
        super().__init__(powerups, row_number, col_number, game)
        self.game = game
        self.symbol = "B"

    def start_powerup(self):
        self.game.paddle.add_shooty()
        super().start_powerup()

    def end_powerup(self):
        self.game.paddle.remove_shooty()
        super().end_powerup()

    def is_alive(self):
        self.game.paddle.add_shooty()
        return super().is_alive()
