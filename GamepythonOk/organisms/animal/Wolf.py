from organisms.Animal import Animal


class Wolf(Animal):
    IMAGE_FILE = "images/wolf.png"
    def __init__(self, world, position):
        super().__init__(world, position, strength=9, initiative=5, color="gray")