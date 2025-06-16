
import javax.swing.*;
import java.util.*;
import java.awt.Component;

public class OrganismSpawner {
    private static final Map<String, Class<? extends Organism>> registry = new LinkedHashMap<>();

    static {
        registry.put("Wolf", Wolf.class);
        registry.put("Sheep", Sheep.class);
        registry.put("Fox", Fox.class);
        registry.put("Turtle", Turtle.class);
        registry.put("Antelope", Antelope.class);
        registry.put("Grass", Grass.class);
        registry.put("Sow Thistle", SowThistle.class);
        registry.put("Guarana", Guarana.class);
        registry.put("Belladonna", Belladonna.class);
        registry.put("Hogweed", Hogweed.class);
    }

    public static void showMenu(World world, Position pos, Component parent) {
    if (world.getOrganismAt(pos) != null) return;

    JPopupMenu menu = new JPopupMenu();
    for (var entry : registry.entrySet()) {
        JMenuItem item = new JMenuItem(entry.getKey());
        item.addActionListener(e -> {
            world.spawnOrganism(entry.getValue(), pos);
            if (world.getPanel() != null) world.getPanel().repaint();
        });
        menu.add(item);
    }
    menu.show(parent, pos.x * 30, pos.y * 30);
}

}