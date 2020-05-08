import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.util.ArrayList;
import java.util.List;

import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;

public class Circles extends JFrame {
	
	private static final long serialVersionUID = 1L;
	
	private List<Circle> circles;
	
	public Circles() {
		super();
		
		circles = new ArrayList<Circle>();
		
		setTitle("Circles");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		getRootPane().putClientProperty("apple.awt.brushMetalLook", true);
		setPreferredSize(new Dimension(800, 600));
		setMinimumSize(new Dimension(600, 450));
		setLayout(new BorderLayout());
		
		JPanel console = new JPanel();
		add(console, BorderLayout.NORTH);
		
		JButton delete = new JButton("Delete");
		delete.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				circles.clear();
				repaint();
			}
		});
		console.add(delete);
		
		console.add(new JLabel("    Color:"));
		
		JComboBox<String> colors = new JComboBox<String>(new String[] { "Red", "Green", "Blue" });
		console.add(colors);
		
		console.add(new JLabel("    Size:"));
		
		JComboBox<Integer> sizes = new JComboBox<Integer>(new Integer[] { 8, 16, 32, 64 });
		console.add(sizes);
		
		JPanel panel = new JPanel() {
			private static final long serialVersionUID = 1L;
			@Override
			public void paint(Graphics g) {
				super.paint(g);
				for (Circle circle: circles) {
					g.setColor(circle.getColor());
					if (circle instanceof Square)
						g.fillRect((int)Math.round(circle.getX() * getWidth()) - circle.getRadius(), (int)Math.round(circle.getY() * getHeight()) - circle.getRadius(), 2 * circle.getRadius(), 2 * circle.getRadius());
					else
						g.fillOval((int)Math.round(circle.getX() * getWidth()) - circle.getRadius(), (int)Math.round(circle.getY() * getHeight()) - circle.getRadius(), 2 * circle.getRadius(), 2 * circle.getRadius());
					g.setColor(Color.BLACK);
					if (circle instanceof Square)
						g.drawRect((int)Math.round(circle.getX() * getWidth()) - circle.getRadius(), (int)Math.round(circle.getY() * getHeight()) - circle.getRadius(), 2 * circle.getRadius(), 2 * circle.getRadius());
					else
						g.drawOval((int)Math.round(circle.getX() * getWidth()) - circle.getRadius(), (int)Math.round(circle.getY() * getHeight()) - circle.getRadius(), 2 * circle.getRadius(), 2 * circle.getRadius());
				}
			}
		};
		panel.addMouseListener(new MouseListener() {
			@Override
			public void mouseReleased(MouseEvent e) { }
			@Override
			public void mousePressed(MouseEvent e) { }
			@Override
			public void mouseExited(MouseEvent e) { }
			@Override
			public void mouseEntered(MouseEvent e) { }
			@Override
			public void mouseClicked(MouseEvent e) {
				Color color = null;
				if (colors.getSelectedItem().equals("Red"))
					color = Color.RED;
				else if (colors.getSelectedItem().equals("Green"))
					color = Color.GREEN;
				else if (colors.getSelectedItem().equals("Blue"))
					color = Color.BLUE;
				if (Math.random() < 0.5)
					circles.add(new Circle(1.0 * e.getX() / panel.getWidth(), 1.0 * e.getY() / panel.getHeight(), (Integer)sizes.getSelectedItem(), color));
				else
					circles.add(new Square(1.0 * e.getX() / panel.getWidth(), 1.0 * e.getY() / panel.getHeight(), (Integer)sizes.getSelectedItem(), color));
				repaint();
			}
		});
		panel.setBackground(Color.WHITE);
		add(panel, BorderLayout.CENTER);
	}

	public static void main(String[] args) {
		new Circles().setVisible(true);
	}

}

class Circle {
	
	private double x;
	
	private double y;
	
	private int radius;
	
	private Color color;

	public Circle(double x, double y, int radius, Color color) {
		super();
		this.x = x;
		this.y = y;
		this.radius = radius;
		this.color = color;
	}

	public double getX() {
		return x;
	}

	public double getY() {
		return y;
	}

	public int getRadius() {
		return radius;
	}

	public Color getColor() {
		return color;
	}
	
}

class Square extends Circle {

	public Square(double x, double y, int radius, Color color) {
		super(x, y, radius, color);
	}

	public int getSize() {
		return 2 * getRadius();
	}
	
}
