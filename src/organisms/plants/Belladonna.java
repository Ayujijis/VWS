import java.awt.Color;

import javax.swing.ImageIcon;

public class Belladonna extends Plant {
    public Belladonna(World world, Position pos) {
        super(world, pos);
        this.strength = 99;
        this.color = Color.PINK;
        this.icon = new ImageIcon("res/belladonna.png");
    }

    @Override
    public void collision(Organism attacker) {
        world.removeOrganism(attacker);
        world.log(attacker.getName() + " ate Belladonna and died!");
    }

    @Override
    public String getName() { return "Belladonna"; }
}