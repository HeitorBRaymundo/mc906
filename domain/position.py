class Position:
    def __init__(self, i, j):
        self.i = i
        self.j = j
    
    def move_left(self):
        self.i = self.i - 1