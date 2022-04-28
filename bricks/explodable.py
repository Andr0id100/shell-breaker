import random
from bricks import Brick
from colorama import Back
from powerups import *
from utils import debug_print

PATTERN = "|     |"


class Explodable(Brick):
    def __init__(self, row_number, col_number, game):
        super().__init__(row_number, col_number, game)
        self.points = 1

    def get_display(self):
        return Back.LIGHTYELLOW_EX + PATTERN + Back.RESET

    def hit(self, ball):

        neighbours = self.get_neighbours()
        self.remove_brick(ball)
        for brick in neighbours:
            if brick is not None:
                brick.hit(ball)
                brick.remove_brick(ball)

    def get_neighbours(self):
        left_brick = None
        right_brick = None

        left_brick = self.grid[self.ROW_NUMBER][self.COL_NUMBER - 1]
        if self.COL_NUMBER + len(PATTERN) < len(self.grid[0]):
            right_brick = self.grid[self.ROW_NUMBER][self.COL_NUMBER +
                                                     len(PATTERN)]
        else:
            right_brick = None
        top_brick = self.grid[self.ROW_NUMBER-1][self.COL_NUMBER]
        bottom_brick = self.grid[self.ROW_NUMBER+1][self.COL_NUMBER]

        left_top_brick = self.grid[self.ROW_NUMBER-1][self.COL_NUMBER-1]
        left_bottom_brick = self.grid[self.ROW_NUMBER+1][self.COL_NUMBER-1]

        if self.COL_NUMBER + len(PATTERN) < len(self.grid[0]):
            right_top_brick = self.grid[self.ROW_NUMBER-1][self.COL_NUMBER +
                                                           len(PATTERN)]
            right_bottom_brick = self.grid[self.ROW_NUMBER+1][self.COL_NUMBER +
                                                              len(PATTERN)]

        else:
            right_bottom_brick = None
            right_top_brick = None

        return (left_brick, right_brick, top_brick, bottom_brick, left_top_brick, left_bottom_brick, right_top_brick, right_bottom_brick)
