from organisms.Plant import Plant

class Grass(Plant):
    IMAGE_FILE = "images/grass.png"
    def __init__(self, world, position):
        super().__init__(world, position, strength=0, initiative=0, color="lightgreen")