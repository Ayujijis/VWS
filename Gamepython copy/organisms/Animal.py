import random
from organisms.Organism import Organism
from world.Position import Position

class Animal(Organism):
    def is_animal(self):
        return True

    def action(self):
        neighbors = self.position.neighbors()
        random.shuffle(neighbors)
        for pos in neighbors:
            if not self.world.in_bounds(pos):
                continue
            target = self.world.get_organism_at(pos)
            if target is None:
                self.world.move_organism(self, pos)
                return
            elif target != self:
                target.collision(self)
                return

    def collision(self, attacker):
        if self.strength > attacker.strength:
            attacker.die()
            self.world.log(f"{self.__class__.__name__} repelled {attacker.__class__.__name__}")
        else:
            self.die()
            self.world.move_organism(attacker, self.position)
            self.world.log(f"{attacker.__class__.__name__} killed {self.__class__.__name__}")