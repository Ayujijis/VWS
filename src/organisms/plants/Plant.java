public abstract class Plant extends Organism {
    public Plant(World world, Position pos) {
        super(world, pos);
        this.initiative = 0;
    }

    @Override
    public void action() {
        if (Math.random() < 0.05) {
            Position newPos = world.getRandomFreeAdjacent(position);
            if (newPos != null) world.spawnOrganism(getClass(), newPos);
        }
    }

    @Override
    public void collision(Organism attacker) {
        world.removeOrganism(this);
        world.placeOrganism(attacker, position);
    }
}