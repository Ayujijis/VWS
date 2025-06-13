from organisms.Plant import Plant

class SowThistle(Plant):
    def __init__(self, world, position):
        super().__init__(world, position, strength=0, initiative=0, color="yellow")

    def action(self):
        for _ in range(3):  # Triple spread attempt
            super().action()
