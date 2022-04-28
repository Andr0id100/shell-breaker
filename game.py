import math
import random
import sys
import time
import signal
from powerups.paddle import ShootyPaddle

from utils import draw, handler, GetchUnix, debug_print
from colorama import init, Back, Cursor, Fore, Style

from components import Paddle, Ball, Bullet
from bricks import Rainbow, Unbreakable
from levels import Level1, Level2, Level3


class Game:
    def __init__(self):
        init()  # Colorama
        self.tick_count = 1
        self.fall_trigger = False

        self.ROW_COUNT = 20
        self.COLUMN_COUNT = 65
        self.getch = GetchUnix()
        self.paddle = Paddle(self.ROW_COUNT, self.COLUMN_COUNT)

        self.balls = []
        self.balls.append(Ball(self.paddle.ROW_NUMBER -
                               1, self.paddle.col_number+random.randint(0, self.paddle.length-1), self))

        self.paddle.attach_ball(self.balls[0])

        self.powerups = []
        self.free_powerups = []
        self.bullets = []
        self.bombs = []

        self.level = None
        self.setup_level()

        # Info
        self.start_time = time.time()
        self.score = 0
        self.lives_remaining = 500

    def setup_level(self):
        if self.level is None:
            self.level = Level1(self)
        elif type(self.level) is Level1:
            self.level = Level2(self)
        elif type(self.level) is Level2:
            self.level = Level3(self)
        else:
            self.game_over()


        self.bricks = self.level.bricks
        self.grid = self.level.grid

        self.level.build_level()
        self.reset()

    def handle_input(self, ch):
        if ch is not None:
            if ch == 'x':
                sys.exit(0)
            elif ch == 'a' or ch == 'd':
                self.paddle.move(ch)
            elif ch == ' ':
                if self.paddle.has_balls():
                    self.paddle.launch_ball()
            elif ch == 'n':
                self.setup_level()

    def step(self):
        ch = None
        signal.signal(signal.SIGALRM, handler)
        signal.setitimer(signal.ITIMER_REAL, 0.1)
        try:
            ch = self.getch().lower()
        except:
            pass
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0.0)
            self.handle_input(ch)

            self.tick_count += 1

            if self.tick_count >= 500:
                self.fall_trigger = True

            for ball in self.balls:
                ball.collisions(self.paddle, self.grid)

            # Update Rainbow Bricks
            for brick in self.bricks:
                if type(brick) is Rainbow:
                    brick.tick()

            for bullet in self.bullets:
                bullet.row_number -= 1

                if bullet.collide(self.grid):
                    self.bullets.pop(self.bullets.index(bullet))

            for bomb in self.bombs:
                bomb.row_number += 1

                if bomb.row_number == self.paddle.ROW_NUMBER:
                    if bomb.col_number >= self.paddle.col_number and bomb.col_number < self.paddle.col_number + self.paddle.length:
                        self.bombs.pop(self.bombs.index(bomb))
                        self.lost_life()

                if bomb.row_number >= self.ROW_COUNT:
                    self.bombs.pop(self.bombs.index(bomb))

            if self.fall_trigger and type(self.level) is not Level3:
                for ball in self.balls:
                    if ball.row_number == self.paddle.ROW_NUMBER-1 and len(self.paddle.attached_balls) == 0:
                        for brick in self.bricks:
                            brick.ROW_NUMBER += 1

                        for row in range(self.ROW_COUNT, 1, -1):
                            for col in range(1, self.COLUMN_COUNT):
                                self.grid[row][col] = self.grid[row-1][col]

                                if (self.grid[row][col] is not None and type(self.grid[row][col]) is not Unbreakable) and row >= self.ROW_COUNT-1:
                                    self.game_over()

            if self.paddle.shooty:
                if self.tick_count % 5 == 0:
                    self.bullets.append(
                        Bullet(self.paddle.ROW_NUMBER, self.paddle.col_number))
                    self.bullets.append(
                        Bullet(self.paddle.ROW_NUMBER, self.paddle.col_number+self.paddle.length-1))

            self.check_powerups()
            self.check_free_powerups()

            self.render()

            if type(self.level) is Level3:
                self.level.tick()

            if self.level.is_over():
                self.setup_level()
                self.fall_trigger = False
                self.tick_count = 1

    def render(self):
        draw(Cursor.POS(1, 1), "")

        output = self.render_window() + self.render_bricks() + \
            self.render_paddle() + self.render_balls() + self.render_bullets() + \
            self.render_free_powerups() + self.render_info()

        print(output)

    def render_window(self):
        window = ""
        for i in range(1, self.ROW_COUNT+1):
            window += Back.WHITE + " "

            if i == 1 or i == self.ROW_COUNT:
                window += Back.WHITE + " "*(self.COLUMN_COUNT-2)
            else:
                window += Back.LIGHTBLACK_EX + " "*(self.COLUMN_COUNT-2)

            window += Back.WHITE + " " + Back.RESET

            window += "\n"

        return window

    def render_bricks(self):
        bricks = ""
        for brick in self.bricks:
            bricks += Cursor.POS(brick.COL_NUMBER,
                                 brick.ROW_NUMBER) + brick.get_display()

        return bricks

    def render_paddle(self):
        return Cursor.POS(math.floor(self.paddle.col_number), math.floor(self.paddle.ROW_NUMBER)) + Back.LIGHTBLACK_EX + self.paddle.get_display()

    def render_balls(self):
        balls = ""
        for b in self.balls:
            balls += Cursor.POS(math.floor(b.col_number),
                                math.floor(b.row_number)) + b.get_display()
        return balls

    def render_free_powerups(self):
        free_powerups = ""
        for entity in self.free_powerups:
            free_powerups += Cursor.POS(math.floor(entity.col_number),
                                        math.floor(entity.row_number)) + Back.MAGENTA + Fore.WHITE + entity.symbol + Style.RESET_ALL

        return free_powerups

    def render_bullets(self):
        bullets = ""
        for b in self.bullets:
            bullets += Cursor.POS(math.floor(b.col_number),
                                  math.floor(b.row_number)) + b.get_display()
        for b in self.bombs:
            bullets += Cursor.POS(math.floor(b.col_number),
                                  math.floor(b.row_number)) + b.get_display()
        return bullets

    def render_info(self):
        bullet_time_remaining = 0
        for entity in self.powerups:
            if type(entity) is ShootyPaddle:
                bullet_time_remaining = int(entity.valid_until - time.time())
        return f"{Cursor.POS(1, self.ROW_COUNT+1)}Shooting Paddle Time: {bullet_time_remaining}\t\tTime: {self.get_time_passed()}\nLives Remaining: {self.lives_remaining}\nScore: {self.score}"

    def check_powerups(self):
        for powerup in self.powerups:
            if not powerup.is_alive():
                powerup.end_powerup()

    def check_free_powerups(self):
        for entity in self.free_powerups:
            entity.tick()

            if math.floor(entity.row_number) >= self.paddle.ROW_NUMBER:
                if entity.col_number >= self.paddle.col_number and entity.col_number <= self.paddle.col_number + self.paddle.length:
                    entity.start_powerup()
                    # self.powerups.append(entity)
                    self.free_powerups.pop(self.free_powerups.index(entity))
                    # debug_print("GOT")
                    continue

            if entity.row_number >= self.ROW_COUNT-1:
                self.free_powerups.pop(self.free_powerups.index(entity))

    def lost_life(self):
        self.reset()
        self.lives_remaining -= 1
        if self.lives_remaining < 0:
            self.game_over()

    def reset(self):
        self.paddle = Paddle(self.ROW_COUNT, self.COLUMN_COUNT)
        while (len(self.bombs) > 0):
            self.bombs.pop()

        while (len(self.balls) > 0):
            self.balls.pop()
        self.balls.append(Ball(self.paddle.ROW_NUMBER -
                               1, self.paddle.col_number+random.randint(0, self.paddle.length-1), self))

        self.paddle.attach_ball(self.balls[0])

        while (len(self.powerups) > 0):
            self.powerups.pop()

    def get_time_passed(self):
        return int(time.time() - self.start_time)

    def game_over(self):
        sys.exit(0)
