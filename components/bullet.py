from colorama import Back

class Bullet:
    def __init__(self, row_number, col_number):
        self.row_number = row_number
        self.col_number = col_number

    def get_display(self):
        return Back.RED+" "+Back.RESET

    def collide(self, grid):
        if grid[self.row_number][self.col_number] is not None:
            grid[self.row_number][self.col_number].hit(None)
            return True
        
        return self.row_number <= 1