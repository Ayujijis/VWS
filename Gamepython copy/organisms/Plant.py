import random
from organisms.Organism import Organism
from world.Position import Position

class Plant(Organism):
    def is_plant(self):
        return True

    def action(self):
        if random.random() < 0.1:  # 10% chance to spread
            neighbors = self.position.neighbors()
            random.shuffle(neighbors)
            for pos in neighbors:
                if self.world.in_bounds(pos) and self.world.get_organism_at(pos) is None:
                    offspring = self.__class__(self.world, pos)
                    self.world.add_organism(offspring)
                    self.world.log(f"{self.__class__.__name__} spread to {pos.x},{pos.y}")
                    break

    def collision(self, other):
        other.die()
        self.world.log(f"{other.__class__.__name__} died touching {self.__class__.__name__}")