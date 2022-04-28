import random
from bricks import Brick
from colorama import Back
from powerups import *
from powerups.paddle import ShootyPaddle
from utils import debug_print

colors = ["", Back.RED, Back.BLUE, Back.GREEN]

POWERUPS = (ExpandPaddle, ShrinkPaddle, GrabbyPaddle, ShootyPaddle, FastBall, ThroughBall)
# POWERUPS = (ShootyPaddle, )
# POWERUPS = (ExpandPaddle, )
# POWERUPS = (ThroughBall,)
PATTERN = "|     |"
class Breakable(Brick):
    def __init__(self, row_number, col_number, game):
        super().__init__(row_number, col_number, game)
        self.power = random.randint(1, 3)
        # self.power = 1
        self.points = self.power
        self.game = game
        self.PATTERN = "|     |"


        if random.random() < 0.1:
            choice = random.choice(POWERUPS)
            self.powerup = choice(
                game.powerups, row_number, col_number + len(self.PATTERN)//2, game)
        else:
            self.powerup = None

    def get_display(self):
        return colors[self.power] + self.PATTERN + Back.RESET

    def remove_brick(self, ball):
        if self.powerup is not None:
                self.game.free_powerups.append(self.powerup)
                if ball is None:
                    self.powerup.row_velocity = 1
                    self.powerup.col_velocity = 0
                else:
                    self.powerup.row_velocity = ball.row_velocity
                    self.powerup.col_velocity = ball.col_velocity
                
        super().remove_brick(ball)

    def hit(self, ball):
        self.power -= 1
        if self.power == 0:
            self.remove_brick(ball)
            
