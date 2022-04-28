from powerups import PowerUp


class FastBall(PowerUp):
    def __init__(self, powerups, row_number, col_number, game):
        super().__init__(powerups, row_number, col_number, game)
        self.game = game
        self.symbol = "F"

    def start_powerup(self):
        for ball in self.game.balls:
            ball.increase_speed()
        super().start_powerup()

    def end_powerup(self):
        for ball in self.game.balls:
            ball.decrease_speed()
        super().end_powerup()


class ThroughBall(PowerUp):
    def __init__(self, powerups, row_number, col_number, game):
        super().__init__(powerups, row_number, col_number, game)
        self.game = game
        self.symbol = "T"

    def start_powerup(self):
        for ball in self.game.balls:
            ball.add_through()
        super().start_powerup()

    def end_powerup(self):
        for ball in self.game.balls:
            ball.remove_through()
        super().end_powerup()

    def is_alive(self):
        for ball in self.game.balls:
            ball.add_through()
        return super().is_alive()
