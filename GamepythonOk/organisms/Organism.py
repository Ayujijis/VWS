from abc import ABC, abstractmethod

class Organism(ABC):
    def __init__(self, world, position, strength, initiative, color):
        self.world = world
        self.position = position
        self.strength = strength
        self.initiative = initiative
        self.age = 0
        self.color = color
        self.alive = True

    def is_animal(self):
        return False

    def is_plant(self):
        return False

    def increment_age(self):
        self.age += 1

    @abstractmethod
    def action(self):
        pass

    @abstractmethod
    def collision(self, other):
        pass

    def die(self):
        self.alive = False
        self.world.remove_organism(self)
        self.world.log(f"{self.__class__.__name__} died at {self.position.x},{self.position.y}")
