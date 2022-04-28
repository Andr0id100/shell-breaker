import random

from bricks import Breakable, Unbreakable, Explodable, Rainbow, unbreakable
from utils import debug_print

BRICK_LENGTH = 7


class Level1:
    def __init__(self, game):
        self.game = game
        self.grid = []
        self.bricks = []

    def build_level(self):
        game = self.game
        for _ in range(2):
            self.grid.append([None for _ in range(game.COLUMN_COUNT)])

        for r in range(2, 6+2):
            row = [None, None]

            # Exploding bricks
            if r == 4:
                for c in range(2, game.COLUMN_COUNT):
                    if (c-2) % BRICK_LENGTH == 0 and (c+BRICK_LENGTH) <= game.COLUMN_COUNT:
                        brick = Explodable(r, c, game)
                        self.bricks.append(brick)
                    row.append(brick)
                self.grid.append(row)
                continue

            for c in range(2, game.COLUMN_COUNT):
                if (c-2) % BRICK_LENGTH == 0 and (c+BRICK_LENGTH) <= game.COLUMN_COUNT:
                    if random.random() < 0.1:
                        brick = Unbreakable(r, c, game)
                    elif random.random() < 0.2:
                        brick = Rainbow(r, c, game)
                    else:
                        brick = Breakable(r, c, game)
                    self.bricks.append(brick)
                row.append(brick)
            self.grid.append(row)

        for r in range(4+2, game.ROW_COUNT):
            row = [None, None]
            for c in range(2, game.COLUMN_COUNT):
                row.append(None)
            self.grid.append(row)



    def is_over(self):
        for brick in self.bricks:
            if brick.get_display() == "":
                self.bricks.pop(self.bricks.index(brick))
        for brick in self.bricks:
            if type(brick) is not Unbreakable:
                    return False
        return True