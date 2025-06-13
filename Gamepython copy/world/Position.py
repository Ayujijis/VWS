class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def neighbors(self, grid_type='square'):
        if grid_type == 'square':
            return [
                Position(self.x + dx, self.y + dy)
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]
            ]
        # hex/grid variants can be added later
        return []
