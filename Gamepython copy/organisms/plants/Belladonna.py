from organisms.Plant import Plant

class Belladonna(Plant):
    def __init__(self, world, position):
        super().__init__(world, position, strength=99, initiative=0, color="purple")

    def collision(self, other):
        other.die()
        self.die()
        self.world.log(f"{other.__class__.__name__} and Belladonna both died")
