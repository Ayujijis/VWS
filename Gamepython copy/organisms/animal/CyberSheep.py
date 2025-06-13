from organisms.Animal import Animal
from organisms.plants.Hogweed import Hogweed
from world.Position import Position
import random

class CyberSheep(Animal):
    def __init__(self, world, position):
        super().__init__(world, position, strength=11, initiative=4, color="black")

    def action(self):
        hogweeds = [org for org in self.world.organisms if isinstance(org, Hogweed)]
        if hogweeds:
            # Move toward the nearest Hogweed
            hogweed = min(hogweeds, key=lambda h: abs(h.position.x - self.position.x) + abs(h.position.y - self.position.y))
            dx = int((hogweed.position.x - self.position.x) / max(1, abs(hogweed.position.x - self.position.x))) if hogweed.position.x != self.position.x else 0
            dy = int((hogweed.position.y - self.position.y) / max(1, abs(hogweed.position.y - self.position.y))) if hogweed.position.y != self.position.y else 0
            target_pos = Position(self.position.x + dx, self.position.y + dy)
        else:
            # Act like a normal animal
            neighbors = self.position.neighbors()
            random.shuffle(neighbors)
            for pos in neighbors:
                if self.world.in_bounds(pos):
                    target_pos = pos
                    break
            else:
                return  # No valid move

        if not self.world.in_bounds(target_pos):
            return
        target = self.world.get_organism_at(target_pos)
        if target is None:
            self.world.move_organism(self, target_pos)
        elif target != self:
            target.collision(self)

    def collision(self, attacker):
        # same as Animal but immune to Hogweed's effect
        if self.strength > attacker.strength:
            attacker.die()
            self.world.log(f"{self.__class__.__name__} repelled {attacker.__class__.__name__}")
        else:
            self.die()
            self.world.move_organism(attacker, self.position)
            self.world.log(f"{attacker.__class__.__name__} killed {self.__class__.__name__}")
