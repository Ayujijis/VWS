from organisms.Animal import Animal
from world.Position import Position

class Human(Animal):
    def __init__(self, world, position):
        super().__init__(world, position, strength=5, initiative=4, color="blue")
        self.ability_cooldown = 0
        self.ability_active = False

    def action(self):
        if self.ability_active:
            self.use_special_ability()
            self.ability_active = False
            self.ability_cooldown = 5

        # Example: stand still (movement could be controlled via key input)
        pass

        if self.ability_cooldown > 0:
            self.ability_cooldown -= 1

    def activate_ability(self):
        if self.ability_cooldown == 0:
            self.ability_active = True
            self.world.log("Human activated special ability!")
        else:
            self.world.log("Ability on cooldown for {} turns".format(self.ability_cooldown))

    def use_special_ability(self):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                target_pos = Position(self.position.x + dx, self.position.y + dy)
                if self.world.in_bounds(target_pos):
                    target = self.world.get_organism_at(target_pos)
                    if target:
                        target.die()
                        self.world.log(f"Human eliminated {target.__class__.__name__} at {target_pos.x},{target_pos.y}")
