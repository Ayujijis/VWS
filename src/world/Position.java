import java.io.Serializable;

public class Position implements Serializable {
    private static final long serialVersionUID = 1L;

    public int x, y;

    public Position(int x, int y) {
        this.x = x;
        this.y = y;
    }
    public boolean equals(Object o) {
        if (!(o instanceof Position)) return false;
        Position p = (Position) o;
        return x == p.x && y == p.y;
    }
    public int hashCode() { return x * 31 + y; }
}
