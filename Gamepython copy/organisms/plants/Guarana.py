from organisms.Plant import Plant

class Guarana(Plant):
    IMAGE_FILE = "images/guarana.png"
    def __init__(self, world, position):
        super().__init__(world, position, strength=0, initiative=0, color="red")

    def collision(self, other):
        other.strength += 3
        self.world.log(f"{other.__class__.__name__} gained +3 strength from Guarana")
        super().collision(other)
