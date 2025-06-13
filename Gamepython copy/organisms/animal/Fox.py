from organisms.Animal import Animal
from world.Position import Position
import random

class Fox(Animal):
    def __init__(self, world, position):
        super().__init__(world, position, strength=3, initiative=7, color="orange")

    def action(self):
        neighbors = self.position.neighbors()
        random.shuffle(neighbors)
        for pos in neighbors:
            if not self.world.in_bounds(pos):
                continue
            target = self.world.get_organism_at(pos)
            if target is None or target.strength <= self.strength:
                if target:
                    target.collision(self)
                else:
                    self.world.move_organism(self, pos)
                return
