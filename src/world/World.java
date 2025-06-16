import java.util.*;
import java.io.Serializable;

public class World implements Serializable {
    private static final long serialVersionUID = 1L;
    transient private GamePanel panel;
    private int width = 20, height = 20;
    private Organism[][] grid = new Organism[width][height];
    private List<Organism> organisms = new ArrayList<>();

    private boolean hexMode;

    public World(GamePanel panel, boolean hexMode) {
        this.panel = panel;
        this.hexMode = hexMode;
        seedWorld();
    }

    public void makeTurn() {
        organisms.sort(Comparator.comparingInt(Organism::getInitiative).reversed()
            .thenComparingInt(Organism::getAge).reversed());
        for (Organism o : new ArrayList<>(organisms)) {
          
            o.increaseAge();
            o.action();
        
        }
        panel.repaint();
        checkGameOver();
    }

public void seedWorld() {
    for (int i = 0; i < 40; i++) {
       
            Position pos = getRandomFreePosition();
            if (pos != null) {
                OrganismType type = OrganismType.getRandom();
                spawnOrganism(type.getOrganismClass(), pos);
            
        }
    }
    spawnOrganism(Human.class, new Position(width / 2, height / 2));
}


    public Position getRandomFreePosition() {
        List<Position> free = new ArrayList<>();
        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                if (grid[x][y] == null) free.add(new Position(x, y));
            }
        }
        if (free.isEmpty()) return null;
        return free.get(new Random().nextInt(free.size()));
    }

    public Position getRandomFreeAdjacent(Position pos) {
        List<Position> free = new ArrayList<>();
        for (Position p : getAdjacentPositions(pos)) {
            if (isInBounds(p) && grid[p.x][p.y] == null) free.add(p);
        }
        if (free.isEmpty()) return null;
        return free.get(new Random().nextInt(free.size()));
    }

     public List<Position> getAdjacentPositions(Position pos) {
        List<Position> adj = new ArrayList<>();
        if (!hexMode) {
            int[][] dirs = {
    {-1, -1}, {0, -1}, {1, -1},
    {-1,  0},          {1,  0},
    {-1,  1}, {0,  1}, {1,  1}};

            for (int[] d : dirs) {
                Position p = new Position(pos.x + d[0], pos.y + d[1]);
                if (isInBounds(p)) adj.add(p);
            }
        } else {
            int[][] evenDirs = {{-1,0},{-1,-1},{0,-1},{1,0},{0,1},{-1,1}};
            int[][] oddDirs =  {{-1,0},{0,-1},{1,-1},{1,0},{1,1},{0,1}};
            int[][] dirs = (pos.x % 2 == 0) ? evenDirs : oddDirs;
            for (int[] d : dirs) {
                Position p = new Position(pos.x + d[0], pos.y + d[1]);
                if (isInBounds(p)) adj.add(p);
            }
        }
        return adj;
    }

    public List<Position> getShuffledAdjacent(Position pos) {
        List<Position> adj = getAdjacentPositions(pos);
        Collections.shuffle(adj);
        return adj;
    }

    public Position getRandomAdjacent(Position pos) {
        return getRandomAdjacent(pos, 1);
    }

    public Position getRandomAdjacent(Position pos, int distance) {
        List<Position> candidates = new ArrayList<>();
        for (int dx = -distance; dx <= distance; dx++) {
            for (int dy = -distance; dy <= distance; dy++) {
                if (dx == 0 && dy == 0) continue;
                Position p = new Position(pos.x + dx, pos.y + dy);
                if (isInBounds(p)) candidates.add(p);
            }
        }
        if (candidates.isEmpty()) return null;
        Collections.shuffle(candidates);
        return candidates.get(0);
    }

    public Position getDirectionPosition(Position pos, Direction dir) {
        int x = pos.x, y = pos.y;
        switch (dir) {
            case UP: y--; break;
            case DOWN: y++; break;
            case LEFT: x--; break;
            case RIGHT: x++; break;
        }
        Position newPos = new Position(x, y);
        return isInBounds(newPos) ? newPos : null;
    }

    public void spawnOrganism(Class<? extends Organism> cls, Position pos) {
        try {
            Organism o = cls.getConstructor(World.class, Position.class).newInstance(this, pos);
            organisms.add(o);
            grid[pos.x][pos.y] = o;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void removeOrganism(Organism o) {
        organisms.remove(o);
        Position p = o.getPosition();
        if (isInBounds(p) && grid[p.x][p.y] == o) grid[p.x][p.y] = null;
    }

    public void placeOrganism(Organism o, Position newPos) {
        Position oldPos = o.getPosition();
        if (isInBounds(oldPos)) grid[oldPos.x][oldPos.y] = null;
        if (isInBounds(newPos)) {
            o.position = newPos;
            grid[newPos.x][newPos.y] = o;
        }
    }

    public void moveOrganism(Organism o, Position newPos) {
        if (!isInBounds(newPos)) return;
        Organism target = grid[newPos.x][newPos.y];
        if (target == null) {
            placeOrganism(o, newPos);
        } else {
            target.collision(o);
        }
    }

    public Organism getOrganismAt(Position pos) {
        if (!isInBounds(pos)) return null;
        return grid[pos.x][pos.y];
    }

    private boolean isInBounds(Position p) {
        return p.x >= 0 && p.x < width && p.y >= 0 && p.y < height;
    }

    public void log(String msg) {
    if (panel != null) panel.log(msg);
}

    public List<Organism> getOrganisms() {
    return organisms;
}

public void setPanel(GamePanel panel) {
    this.panel = panel;
}

public GamePanel getPanel() {
    return panel;
}

public void checkGameOver() {
    boolean humanAlive = organisms.stream().anyMatch(o -> o instanceof Human);
    if (!humanAlive && panel != null) {
        panel.showGameOver();
    }
}

}

