from bricks import Brick
from colorama import Back, Fore

from utils import debug_print


class UFO(Brick):
    def __init__(self, row_number, col_number, game):
        self.PATTERN = "       "
        super().__init__(row_number, col_number, game)

    def get_display(self):
        health = int((1 - (self.game.level.boss_health/self.game.level.boss_max_health))*len(self.PATTERN))
        return Back.RED + self.PATTERN[:health] + Back.RESET + Back.MAGENTA + self.PATTERN[health:] + Back.RESET

    def hit(self, ball):
        self.game.level.boss_health -= 1
        self.game.score += 10
