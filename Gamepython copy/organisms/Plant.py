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
        """
        Default collision for a plant: it gets eaten by the other organism.
        The plant dies and the other organism moves to its position.
        """
        self.world.log(f"{other.__class__.__name__} ate {self.__class__.__name__}")
        plant_position = self.position
        self.die()  # The plant is eaten and removed from the world.
        other.world.move_organism(other, plant_position) # The animal moves into the empty space.