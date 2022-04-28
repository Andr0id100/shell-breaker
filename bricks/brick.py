import math

from colorama.ansi import Back

from utils import debug_print

class Brick:
    def __init__(self, row_number, col_number, game):
        self.ROW_NUMBER = row_number
        self.COL_NUMBER= col_number
        self.game = game

        self.grid = game.grid

    def __repr__(self):
        return "    "

    def hit(self, ball):
        pass

    def collide(self, ball):
        self.hit(ball)

        # Check this, maybe instead of just directly left or right, the ball should be instead just one block above or below the left and right positions
        if ball.row_number == self.ROW_NUMBER:
            ball.col_velocity *= -1
        else:
            ball.row_velocity *= -1

    def remove_brick(self, ball):
        self.get_display = lambda : ""
        # self.game.bricks.pop(self.game.bricks.index(self))

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == self:
                        self.grid[i][j] = None
        self.game.score += self.points