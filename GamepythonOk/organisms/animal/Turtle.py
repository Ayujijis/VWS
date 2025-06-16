from organisms.Animal import Animal
import random

class Turtle(Animal):
    IMAGE_FILE = "images/turtle.png"
    def __init__(self, world, position):
        super().__init__(world, position, strength=2, initiative=1, color="darkgreen")

    def action(self):
        if random.random() < 0.25:  # 25% chance to move
            super().action()

    def collision(self, attacker):
        if attacker.strength >= 5:
            self.world.log(f"{self.__class__.__name__} reflected {attacker.__class__.__name__}")
            return
        super().collision(attacker)
