import javax.swing.*;
import java.awt.FlowLayout;

public class Main {
    public static void main(String[] args) {
        JFrame frame = new JFrame("VWS");
        GamePanel panel = new GamePanel();

        JPanel container = new JPanel(new FlowLayout(FlowLayout.CENTER, 0, 0));
        container.add(panel);

        frame.setContentPane(container); // set the container, not the panel
        frame.pack(); // let layout define frame size
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);
    }
}