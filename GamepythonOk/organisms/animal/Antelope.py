from organisms.Animal import Animal
from world.Position import Position
import random

class Antelope(Animal):
    IMAGE_FILE = "images/deer.png"
    def __init__(self, world, position):
        super().__init__(world, position, strength=4, initiative=4, color="brown")

    def action(self):
        moves = [(2,0), (-2,0), (0,2), (0,-2)]
        random.shuffle(moves)
        for dx, dy in moves:
            new_pos = Position(self.position.x + dx, self.position.y + dy)
            if self.world.in_bounds(new_pos):
                target = self.world.get_organism_at(new_pos)
                if target:
                    target.collision(self)
                else:
                    self.world.move_organism(self, new_pos)
                return
