from organisms.Plant import Plant

class Grass(Plant):
    def __init__(self, world, position):
        super().__init__(world, position, strength=0, initiative=0, color="lightgreen")