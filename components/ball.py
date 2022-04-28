import math
from utils import *
from colorama import Cursor, Back, Fore


class Ball:
    def __init__(self, row_number, col_number, game):

        self.row_number = row_number
        self.col_number = col_number

        self.ROW_LIMIT = game.ROW_COUNT
        self.COL_LIMIT = game.COLUMN_COUNT

        self.game = game

        self.attached = False

        self.row_velocity = -(random.random()*0.5 + 0.5)
        self.col_velocity = random.random()*2 - 1

        self.through = False

    def move_left(self):
        self.col_number -= 1

    def move_right(self):
        self.col_number += 1

    def collisions(self, paddle, grid):
        if self not in paddle.attached_balls:
            self.collision_bricks_and_paddle(paddle, grid)
            self.collision_walls()

    # Return True if hit by paddle
    def collision_bricks_and_paddle(self, paddle, grid):
        current_row_number = self.row_number
        current_col_number = self.col_number

        row_number = math.floor(current_row_number)
        col_number = math.floor(current_col_number)

        final_row_number = self.row_number + self.row_velocity
        final_col_number = self.col_number + self.col_velocity

        while True:
            if self.row_velocity > 0:
                if current_row_number > final_row_number:
                    break
            else:
                if current_row_number < final_row_number:
                    break

            if self.col_velocity > 0:
                if current_col_number > final_col_number:
                    break
            else:
                if current_col_number < final_col_number:
                    break

            current_row_number += self.row_velocity * 0.1
            current_col_number += self.col_velocity * 0.1

            current_row_number_floor = math.floor(current_row_number)
            current_col_number_floor = math.floor(current_col_number)

            if current_row_number_floor != row_number or current_col_number_floor != col_number:
                # Monkey patch to prevent out of index problems on collison with right and bottom walls
                if current_row_number_floor >= len(grid) or current_col_number_floor >= len(grid[0]):
                    break

                # Check Paddle
                if current_row_number_floor == paddle.ROW_NUMBER - 1:
                    if current_col_number_floor >= paddle.col_number and current_col_number_floor <= paddle.col_number + paddle.length:
                        if paddle.grabby:
                            paddle.attach_ball(self)
                        self.row_velocity *= -1
                        self.col_velocity = (
                            current_col_number - paddle.col_number + 1)/(paddle.length)*2 - 1
                        break
                # Check Blocks
                if grid[current_row_number_floor][current_col_number_floor] is not None:
                    self.row_number = current_row_number
                    self.col_number = current_col_number
                    if self.through:
                        grid[current_row_number_floor][current_col_number_floor].hit(self)
                        if grid[current_row_number_floor][current_col_number_floor] is not None:
                            grid[current_row_number_floor][current_col_number_floor].remove_brick(self)
                    else:
                        grid[current_row_number_floor][current_col_number_floor].collide(self)
                    break
                else:
                    row_number = current_row_number_floor
                    col_number = current_col_number_floor

        self.row_number = current_row_number
        self.col_number = current_col_number

    def collision_walls(self):
        if self.row_number >= self.ROW_LIMIT:
            self.game.lost_life()

        if self.col_number >= self.COL_LIMIT or self.col_number < 2:
            self.col_number = self.COL_LIMIT-1 if self.col_number >= self.COL_LIMIT else 2
            self.col_velocity *= -1

        if self.row_number < 2:
            self.row_number = 2
            self.row_velocity *= -1


        # For all wall collision
        # if self.row_number >= self.ROW_LIMIT or self.row_number < 2:
        #     self.row_number = self.ROW_LIMIT-1 if self.row_number >= self.ROW_LIMIT else 2
        #     self.row_velocity *= -1

    def get_display(self):
        return Back.LIGHTBLACK_EX+"O"+Back.RESET

    def increase_speed(self):
        if abs(self.row_velocity) < 1.2:
            if self.row_velocity > 0:
                self.row_velocity += 0.3
            else:
                self.row_velocity -= 0.3

    def decrease_speed(self):
        if abs(self.row_velocity) >= 0.8:
            if self.row_velocity > 0:
                self.row_velocity -= 0.3
            else:
                self.row_velocity -= 0.3

    def add_through(self):
        self.through = True

    def remove_through(self):
        self.through = False
