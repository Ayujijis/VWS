from organisms.Animal import Animal

class Sheep(Animal):
    def __init__(self, world, position):
        super().__init__(world, position, strength=4, initiative=4, color="white")
