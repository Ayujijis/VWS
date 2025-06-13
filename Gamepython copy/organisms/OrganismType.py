import random
from enum import Enum

# Forward-declare placeholder classes. In the final application,
# these will be the actual, imported organism classes.
class Wolf: pass
class Sheep: pass
class Fox: pass
class Turtle: pass
class Antelope: pass
class CyberSheep: pass
class Grass: pass
class SowThistle: pass
class Guarana: pass
class Belladonna: pass
class Hogweed: pass


class OrganismType(Enum):
    WOLF = Wolf
    SHEEP = Sheep
    FOX = Fox
    TURTLE = Turtle
    ANTELOPE = Antelope
    CYBER_SHEEP = CyberSheep
    GRASS = Grass
    SOW_THISTLE = SowThistle
    GUARANA = Guarana
    BELLADONNA = Belladonna
    HOGWEED = Hogweed

    @classmethod
    def get_random(cls):
        return random.choice(list(cls))

    @property
    def organism_class(self):
        return self.value