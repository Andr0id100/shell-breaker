import random
from bricks import Breakable, Unbreakable, Explodable, Rainbow
from utils import debug_print

BRICK_LENGTH = 7


class Level2:
    def __init__(self, game):
        self.game = game
        self.grid = []
        self.bricks = []

    def build_level(self):
        game = self.game
        for _ in range(2):
            self.grid.append([None for _ in range(game.COLUMN_COUNT)])

        BRICK_ROW_COUNT = 9
        for r in range(game.ROW_COUNT):
            row = []
            for c in range(game.COLUMN_COUNT):
                row.append(None)
            self.grid.append(row)

        for r in range(2, BRICK_ROW_COUNT+2):
            row_brick_count = BRICK_ROW_COUNT+2-r
            for c in range(2, game.COLUMN_COUNT):
                if (c-2) % BRICK_LENGTH == 0 and (c+BRICK_LENGTH) <= game.COLUMN_COUNT:
                    if row_brick_count == 0:
                        break
                    row_brick_count -= 1
                    if random.random() < 0.1:
                        brick = Unbreakable(r, c, game)
                    elif random.random() < 0.2:
                        brick = Rainbow(r, c, game)
                    else:
                        brick = Breakable(r, c, game)
                    self.bricks.append(brick)
                self.grid[r][c] = brick


    def is_over(self):
        for brick in self.bricks:
            if brick.get_display() == "":
                self.bricks.pop(self.bricks.index(brick))
        for brick in self.bricks:
            if type(brick) is not Unbreakable:
                return False
        return True
