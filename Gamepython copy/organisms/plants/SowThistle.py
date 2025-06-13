from organisms.Plant import Plant

class SowThistle(Plant):
    IMAGE_FILE = "images/thistle.png"
    def __init__(self, world, position):
        super().__init__(world, position, strength=1, initiative=0, color="yellow")

    def action(self):
        for _ in range(3):  # Triple spread attempt
            super().action()
