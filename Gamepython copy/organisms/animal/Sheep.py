from organisms.Animal import Animal

class Sheep(Animal):
    IMAGE_FILE = "images/sheep.png"
    def __init__(self, world, position):
        super().__init__(world, position, strength=4, initiative=4, color="white")
