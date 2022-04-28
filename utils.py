from collections import namedtuple
import sys
import termios
import tty

from colorama import Style, Cursor, Back
import random

Coords = namedtuple(typename='Coords', field_names=['row_number', 'col_number'])

def draw(*args, **kwargs):
    print(*args, Style.RESET_ALL, sep="", end="")


def nl(): print()

def debug_print(*args, **kwargs):
    print(Cursor.POS(1, 24), Back.GREEN, *args, Style.RESET_ALL, sep=" ", end="")

def ticker():
    return random.randint(1, 10)

def handler(signum, stack):
    raise Exception("No input")

class GetchUnix:
    def __call__(self):

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
