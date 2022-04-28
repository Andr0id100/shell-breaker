import time

from utils import debug_print

class PowerUp:
    def __init__(self, powerups, row_number, col_number, game):
        self.powerups = powerups
        self.valid_until = -1
        self.row_number = row_number
        self.col_number = col_number
        self.ROW_LIMIT = game.ROW_COUNT
        self.COL_LIMIT = game.COLUMN_COUNT

    def start_powerup(self):
        self.powerups.append(self)
        self.valid_until = time.time() + 5

    def is_alive(self):
        return time.time() < self.valid_until

    def end_powerup(self):
        self.powerups.pop(self.powerups.index(self))

    def tick(self):
        self.col_number += self.col_velocity
        self.row_number += self.row_velocity

        self.row_velocity += 0.1
        
        if self.col_number >= self.COL_LIMIT or self.col_number < 2:
            self.col_number = self.COL_LIMIT-1 if self.col_number >= self.COL_LIMIT else 2
            self.col_velocity *= -1

        if self.row_number < 2:
            self.row_number = 2
            self.row_velocity *= -1

