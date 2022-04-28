from bricks import Brick
from colorama import Back

class Unbreakable(Brick):
    def __init__(self, row_number, col_number, game):
        super().__init__(row_number, col_number, game)
        self.points = 5
        self.PATTERN = "       "


    def get_display(self):
        return Back.LIGHTWHITE_EX + self.PATTERN + Back.RESET
