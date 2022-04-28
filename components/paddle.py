from colorama.ansi import Back
from utils import *
from colorama import Cursor
from components.ball import Ball
import math


class Paddle:
    def __init__(self, ROW_LIMIT, COL_LIMIT):
        self.length = 7
        self.COL_LIMIT = COL_LIMIT

        self.ROW_NUMBER = ROW_LIMIT-2
        self.col_number = COL_LIMIT//2

        self.attached_balls = []

        self.grabby = False
        # self.shooty = True
        self.shooty = False


    def move(self, key):

        if key == 'a':
            self.move_left()
        elif key == 'd':
            self.move_right()

    def move_left(self):
        if self.col_number >= 3:
            self.col_number -= 1
            for b in self.attached_balls:
                b.move_left()

    def move_right(self):
        if self.col_number < self.COL_LIMIT-self.length:
            self.col_number += 1
            for b in self.attached_balls:
                b.move_right()

    def has_balls(self):
        return len(self.attached_balls) > 0

    def in_limits(self, ball):
        return ball.col_number >= self.col_number and ball.col_number <= self.col_number + self.length
    def attach_ball(self, ball):
        self.attached_balls.append(ball)
        ball.attached = True

    def launch_ball(self):
        self.attached_balls[0].attached = False
        self.attached_balls.pop(0)

    def position_check(self, ball):
        return math.floor(ball.row_number) == self.ROW_NUMBER - 1 and math.floor(ball.col_number) >= self.col_number and math.floor(ball.col_number) <= self.col_number + self.length

    def get_display(self):
        if self.shooty:
            return Back.BLACK + '^' + f"{' '*(self.length-2)}^" + Back.RESET
        else:
            return Back.LIGHTYELLOW_EX + f"{' '*self.length}" + Back.RESET

    def increase_size(self):
        # No more than three exapansions
        if self.length < 13:
            self.length += 2

            if self.col_number == 2:
                self.move_right()

            if self.col_number == (self.COL_LIMIT-self.length+2):
                self.move_left()

            self.col_number -= 1

    def decrease_size(self):
        if self.length >= 5:
            self.length -= 2

            self.col_number += 1

    def add_grabby(self):
        self.grabby = True

    def remove_grabby(self):
        self.grabby = False

    def add_shooty(self):
        self.shooty = True

    def remove_shooty(self):
        self.shooty = False

