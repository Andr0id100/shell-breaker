import random
from bricks import Breakable, Unbreakable, Explodable, Rainbow, UFO
from bricks.breakable import PATTERN
from components import Bullet
from utils import debug_print

BRICK_LENGTH = 7


class Level3:
    def __init__(self, game):
        self.game = game
        self.grid = []
        self.bricks = []
        self.ufo = []
        
        self.boss_health = 30
        self.boss_max_health = self.boss_health

        self.shield1 = True
        self.shield2 = True


    def build_level(self):
        self.paddle_old = self.game.paddle.col_number
        for _ in range(2):
            self.grid.append([None for _ in range(self.game.COLUMN_COUNT)])

        BRICK_ROW_COUNT = 9
        for r in range(2, self.game.ROW_COUNT):
            row = []
            for c in range(self.game.COLUMN_COUNT):
                row.append(None)
            self.grid.append(row)

        brick = UFO(2, self.game.COLUMN_COUNT//2, self.game)
        self.ufo.append(brick)

        brick = UFO(3, self.game.COLUMN_COUNT//2+len(brick.PATTERN), self.game)
        self.ufo.append(brick)

        brick = UFO(3, self.game.COLUMN_COUNT//2-len(brick.PATTERN), self.game)
        self.ufo.append(brick)

        for i in range(-2, 3):
            brick = UFO(4, self.game.COLUMN_COUNT//2 +
                        i*len(brick.PATTERN), self.game)
            self.ufo.append(brick)

        for brick in self.ufo:
            self.setup_brick(brick)

        brick = Unbreakable(8, 2, self.game)
        self.setup_brick(brick)

        brick = Unbreakable(8, self.game.COLUMN_COUNT-len(brick.PATTERN), self.game)
        self.setup_brick(brick)


    def setup_brick(self, brick):
        self.bricks.append(brick)
        self.reset_physics(brick)

    def reset_physics(self, brick):
        for i in range(len(brick.PATTERN)):
            self.grid[brick.ROW_NUMBER][brick.COL_NUMBER+i] = brick

    def tick(self):
        paddle_pos = self.game.paddle.col_number
        if paddle_pos - 2*7 <= 1 or paddle_pos + 3*7 >= self.game.COLUMN_COUNT+1:
            return

        for r in range(2, 5):
            for c in range(self.game.COLUMN_COUNT):
                self.grid[r][c] = None
                
        for brick in self.ufo:
            brick.COL_NUMBER += paddle_pos-self.paddle_old
            self.reset_physics(brick)
        self.paddle_old = paddle_pos

        if self.game.tick_count % 20 == 0:
            self.game.bombs.append(
                Bullet(4, self.ufo[0].COL_NUMBER+len(self.ufo[0].PATTERN)//2)
            )

        if self.boss_health <= self.boss_max_health//2 and self.shield1:
            self.shield1 = False
            for i in range(9):
                brick = Breakable(9, 2 + i*len(PATTERN), self.game)
                brick.powerup = None
                self.setup_brick(brick)

        if self.boss_health <= self.boss_max_health//4 and self.shield2:
            self.shield2 = False
            for c in range(self.game.COLUMN_COUNT):
                self.grid[9][c] = None
            for i in range(9):
                brick = Breakable(9, 2 + i*len(PATTERN), self.game)
                brick.powerup = None
                self.setup_brick(brick)


    def is_over(self):
        return self.boss_health < 1