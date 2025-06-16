from organisms.Plant import Plant
from organisms.Animal import Animal

class Hogweed(Plant):
    IMAGE_FILE = "images/hogweed.png"
    def __init__(self, world, position):
        super().__init__(world, position, strength=10, initiative=0, color="green")

    def action(self):
        from organisms.animal.CyberSheep import CyberSheep  # Delayed import to avoid circular reference
        super().action()
        for pos in self.position.neighbors():
            organism = self.world.get_organism_at(pos)
            if organism and organism.is_animal() and not isinstance(organism, CyberSheep):
                organism.die()
                self.world.log(f"{organism.__class__.__name__} killed by Hogweed at {pos.x},{pos.y}")
