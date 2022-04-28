from bricks import Breakable
import random

class Rainbow(Breakable):
    def __init__(self, row_number, col_number, game):
        super().__init__(row_number, col_number, game)
        self.hit_once = False

    def tick(self):
        if not self.hit_once:
            self.power = random.randint(1, 3)

    def hit(self, ball):
        self.hit_once = True
        return super().hit(ball)
    
        
    