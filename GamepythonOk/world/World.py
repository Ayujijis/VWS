from world.Position import Position

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(height)] for _ in range(width)]
        self.organisms = []
        self.log_messages = []

    def add_organism(self, organism):
        self.organisms.append(organism)
        pos = organism.position
        self.grid[pos.x][pos.y] = organism

    def remove_organism(self, organism):
        if organism in self.organisms:
            self.organisms.remove(organism)
            pos = organism.position
            self.grid[pos.x][pos.y] = None

    def move_organism(self, organism, new_pos):
        self.grid[organism.position.x][organism.position.y] = None
        organism.position = new_pos
        self.grid[new_pos.x][new_pos.y] = organism

    def get_organism_at(self, pos):
        if 0 <= pos.x < self.width and 0 <= pos.y < self.height:
            return self.grid[pos.x][pos.y]
        return None

    def in_bounds(self, pos):
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height

    def log(self, message):
        self.log_messages.append(message)
        print(message)  # Optional: also print to console