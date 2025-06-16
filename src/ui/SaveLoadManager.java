import java.io.*;

import javax.swing.ImageIcon;


public class SaveLoadManager {
    public static void save(World world, String filename) {
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream(filename))) {
            out.writeObject(world);
            world.log("Game saved.");
        } catch (IOException e) {
            e.printStackTrace();
            world.log("Failed to save game.");
        }
    }

    public static World load(String filename, GamePanel panel) {
    try (ObjectInputStream in = new ObjectInputStream(new FileInputStream(filename))) {
        World loadedWorld = (World) in.readObject();
        loadedWorld.setPanel(panel);
        panel.setWorld(loadedWorld);

        // 🔧 Restore sprite icons for organisms
        for (Organism o : loadedWorld.getOrganisms()) {
    if (o instanceof Wolf) {
        o.setIcon(new ImageIcon("res/wolf.png"));
    } else if (o instanceof Antelope) {
        o.setIcon(new ImageIcon("res/deer.png"));
    } else if (o instanceof Human) {
        o.setIcon(new ImageIcon("res/human.png"));
    }
    else if (o instanceof Sheep) {
        o.setIcon(new ImageIcon("res/sheep.png"));
    }
    else if (o instanceof Fox) {
        o.setIcon(new ImageIcon("res/fox.png"));
    }
    else if (o instanceof Turtle) {
        o.setIcon(new ImageIcon("res/turtle.png"));
    }
    else if (o instanceof Belladonna) {
        o.setIcon(new ImageIcon("res/belladonna.png"));
    }
    else if (o instanceof Grass) {
        o.setIcon(new ImageIcon("res/grass.png"));
    }
    else if (o instanceof Guarana) {
        o.setIcon(new ImageIcon("res/guarana.png"));
    }
    else if (o instanceof Hogweed) {
        o.setIcon(new ImageIcon("res/hogweed.png"));
    }
    else if (o instanceof SowThistle) {
        o.setIcon(new ImageIcon("res/thistle.png"));
    }
   

}
        loadedWorld.log("Game loaded.");
        return loadedWorld;

    } catch (IOException | ClassNotFoundException e) {
        e.printStackTrace();
        panel.log("Failed to load game.");
        return null;
    }
}

}