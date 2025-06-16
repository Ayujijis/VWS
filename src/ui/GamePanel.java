import javax.swing.*;
import java.awt.*;
import java.awt.event.*;


public class GamePanel extends JPanel {
    private World world;
    private JTextArea logArea = new JTextArea();
    
    private static final int TILE_SIZE = 30;
    private static final boolean USE_HEX_GRID = false; // Toggle hex mode
    

    public GamePanel() {
        setLayout(new BorderLayout());
        
        logArea.setEditable(false);
        JScrollPane scrollPane = new JScrollPane(logArea);
        scrollPane.setPreferredSize(new Dimension(700, 100));
        add(scrollPane, BorderLayout.SOUTH);
        setPreferredSize(new Dimension(TILE_SIZE * 20, TILE_SIZE * 20 + 100));
        this.world = new World(this, USE_HEX_GRID);
        setFocusable(true);
        addMouseListener(new MouseAdapter() {
    @Override
    public void mousePressed(MouseEvent e) {
        if (SwingUtilities.isLeftMouseButton(e)) {
            int x = e.getX() / TILE_SIZE;
            int y = e.getY() / TILE_SIZE;
            Position pos = new Position(x, y);
            OrganismSpawner.showMenu(world, pos, GamePanel.this);
            
        }
    }
});

        addKeyListener(new KeyAdapter() {

    public void keyPressed(KeyEvent e) {
        Human human = world.getOrganisms().stream()
            .filter(o -> o instanceof Human)
            .map(o -> (Human) o)
            .findFirst().orElse(null);

        switch (e.getKeyCode()) {
            case KeyEvent.VK_R -> SaveLoadManager.load("save.dat", GamePanel.this);
            case KeyEvent.VK_L -> SaveLoadManager.save(world, "save.dat");
            case KeyEvent.VK_UP -> {
                if (human != null) human.queueMove(Direction.UP);
            }
            case KeyEvent.VK_DOWN -> {
                if (human != null) human.queueMove(Direction.DOWN);
            }
            case KeyEvent.VK_LEFT -> {
                if (human != null) human.queueMove(Direction.LEFT);
            }
            case KeyEvent.VK_RIGHT -> {
                if (human != null) human.queueMove(Direction.RIGHT);
            }
            case KeyEvent.VK_SPACE -> {
                if (human != null && human.canActivatePower()) {
                     human.activatePower(); // Sets cooldown and flag

                    for (int dx = -1; dx <= 1; dx++) {
                        for (int dy = -1; dy <= 1; dy++) {
                            if (dx == 0 && dy == 0) continue;
                            Position target = new Position(human.getPosition().x + dx, human.getPosition().y + dy);
                            Organism o = world.getOrganismAt(target);
                            if (o != null && o != human) {
                                world.log("Human's power destroyed " + o.getName() + " at (" + target.x + "," + target.y + ")");
                                world.removeOrganism(o);
                            }
                        }
                    }

                    world.log("Human used power!");
                    world.getPanel().repaint();
                }
}
        }
        if (human != null) world.makeTurn();
    }
});
    }

    public void log(String msg) {
        logArea.append(msg + "\n");
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        for (int x = 0; x < 20; x++) {
            for (int y = 0; y < 20; y++) {
                Position pos = new Position(x, y);
                Organism o = world.getOrganismAt(pos);

                if (USE_HEX_GRID) {
                    int px = (int) (x * TILE_SIZE * 0.75);
                    int py = (int) (y * TILE_SIZE + (x % 2) * (TILE_SIZE / 2.0));
                    drawHex(g, px, py, TILE_SIZE, o);
                } else {
                    int px = x * TILE_SIZE;
                    int py = y * TILE_SIZE;
                    g.setColor(Color.LIGHT_GRAY);
                    g.drawRect(px, py, TILE_SIZE, TILE_SIZE);
                    if (o != null) {
                        Image sprite = o.getSprite();
if (sprite != null) {
    g.drawImage(sprite, px, py, TILE_SIZE, TILE_SIZE, this);
} else {
    g.setColor(o.getColor());
    g.fillRect(px + 2, py + 2, TILE_SIZE - 4, TILE_SIZE - 4);
}

                    }
                }
            }
        }
    }

    private void drawHex(Graphics g, int x, int y, int size, Organism o) {
        Polygon hex = new Polygon();
        for (int i = 0; i < 6; i++) {
            double angle = Math.toRadians(60 * i);
            int dx = (int) (x + size * Math.cos(angle));
            int dy = (int) (y + size * Math.sin(angle));
            hex.addPoint(dx, dy);
        }
        g.setColor(Color.LIGHT_GRAY);
        g.drawPolygon(hex);
        if (o != null) {
            g.setColor(o.getColor());
            g.fillPolygon(hex);
        }
    }

    public void setWorld(World newWorld) {
    this.world = newWorld;
    repaint();
    requestFocusInWindow();
}

public void showGameOver() {
    JOptionPane.showMessageDialog(this, "Game Over! The human has died.", "Game Over", JOptionPane.INFORMATION_MESSAGE);
    removeKeyListener(getKeyListeners()[0]); // Optional: disables input
}


}