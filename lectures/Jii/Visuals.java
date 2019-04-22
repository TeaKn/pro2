import java.awt.BasicStroke;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.GridLayout;
import java.awt.Image;
import java.awt.Point;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.awt.image.ImageObserver;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import javax.imageio.ImageIO;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JSlider;
import javax.swing.JTextField;
import javax.swing.JToggleButton;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

public class Visuals {
  
  public static JFrame frame;
  
  public static JButton button;
  
  public static JToggleButton toggle;
  
  public static JSlider slider;
  
  public static String text = "";
  
  public static Point point = new Point(100, 100);
  
  public static Point[] balls = new Point[] { new Point(400, 100), new Point(400, 100), new Point(400, 100), new Point(400, 100), new Point(400, 100) };
  
  public static Point[] directions = new Point[] { new Point(2, -2), new Point(2, -2), new Point(2, -2), new Point(2, -2), new Point(2, -2) };
  
  public static Color color = new Color((float)Math.random(), (float)Math.random(), (float)Math.random(), (float)Math.random());
  
  public static List<List<Point>> lines = new ArrayList<List<Point>>();
  
  public static void main(String[] args) {
    frame = new JFrame();
    
    frame.setTitle("Visuals");
    frame.getRootPane().putClientProperty("apple.awt.brushMetalLook", true);
    frame.setPreferredSize(new Dimension(1024, 768));
    frame.setMinimumSize(new Dimension(800, 600));
    
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    
    frame.setLayout(new BorderLayout());
    
    JPanel panel = new Panel();
    
    panel.addMouseListener(new MouseListener() {
      
      @Override
      public void mouseReleased(MouseEvent e) {
        System.out.println("Mouse released");
      }
      
      @Override
      public void mousePressed(MouseEvent e) {
        System.out.println("Mouse pressed");
        
        if (Visuals.toggle.isSelected())
          Visuals.lines.add(new ArrayList<Point>());
      }
      
      @Override
      public void mouseExited(MouseEvent e) {
        frame.repaint();
      }
      
      @Override
      public void mouseEntered(MouseEvent e) {
        frame.repaint();
      }
      
      @Override
      public void mouseClicked(MouseEvent e) {
        System.out.println("Mouse clicked");
        
        frame.repaint();
      }
      
    });
    
    panel.addMouseMotionListener(new MouseMotionListener() {
      
      @Override
      public void mouseMoved(MouseEvent e) {
        
      }
      
      @Override
      public void mouseDragged(MouseEvent e) {
        System.out.println(e.getX() + " " + e.getY());
        
        if (Visuals.toggle.isSelected()) {
          Visuals.lines.get(Visuals.lines.size() - 1).add(new Point(e.getX(), e.getY()));
          Visuals.frame.repaint();
        }
      }
      
    });
    
    frame.add(panel, BorderLayout.CENTER);
    
    JPanel controls = new Controls();
    
    frame.add(controls, BorderLayout.NORTH);
    
    JPanel layouts = new JPanel();
    layouts.setPreferredSize(new Dimension(frame.getWidth(), 48));
    layouts.setLayout(new BorderLayout());
    
    frame.add(layouts, BorderLayout.SOUTH);
    
    JPanel grid = new JPanel();
    grid.setBackground(Color.WHITE);
    grid.setPreferredSize(new Dimension(frame.getWidth() / 2, 48));
    grid.setLayout(new GridLayout(2, 4));
    
    layouts.add(grid, BorderLayout.WEST);
    
    for (int i = 0; i < 8; i++)
      grid.add(new Backgrounds());
    
    JPanel gridbox = new JPanel();
    gridbox.setLayout(new GridBagLayout());
    
    layouts.add(gridbox, BorderLayout.CENTER);
    
    GridBagConstraints constraints = new GridBagConstraints();
    
    constraints.fill = GridBagConstraints.BOTH;
    constraints.weightx = 1.0;
    constraints.weighty = 1.0;
    constraints.gridx = 0;
    constraints.gridy = 0;
    
    gridbox.add(new Backgrounds(), constraints);
    
    constraints.fill = GridBagConstraints.BOTH;
    constraints.weightx = 0.5;
    constraints.weighty = 0.5;
    constraints.gridx = 1;
    constraints.gridy = 0;
    
    gridbox.add(new Backgrounds(), constraints);
    
    constraints.fill = GridBagConstraints.NONE;
    constraints.gridx = 0;
    constraints.gridy = 1;
    constraints.gridwidth = 2;
    constraints.gridheight = 1;
    constraints.anchor = GridBagConstraints.LAST_LINE_END;
    
    gridbox.add(new Backgrounds(), constraints);
    
    frame.setVisible(true);
    
    int i = 0;
    while (true) {
      for (int j = 0; j < Visuals.balls.length; j++)
        Visuals.balls[j] = new Point((int)(Visuals.balls[j].getX() + Visuals.directions[j].getX()), (int)(Visuals.balls[j].getY() + Visuals.directions[j].getY()));
      
      for (int j = 0; j < Visuals.balls.length; j++) {
        if (Visuals.balls[j].getX() <= 0 || Visuals.balls[j].getX() >= panel.getWidth() - 12)
          Visuals.directions[j] = new Point(-(int)Visuals.directions[j].getX(), (int)Visuals.directions[j].getY());
        if (Visuals.balls[j].getY() <= 0 || Visuals.balls[j].getY() >= panel.getHeight() - 12)
          Visuals.directions[j] = new Point((int)Visuals.directions[j].getX(), -(int)Visuals.directions[j].getY());
      }
      
      if (i > 0 && i % 1000 == 0)
        for (int j = 0; j < Visuals.balls.length; j++)
          Visuals.directions[j] = new Point((int)(10.0 * Math.random() - 5.0), (int)(10.0 * Math.random() - 5.0));
      
      frame.repaint();
      
      try {
        Thread.sleep(10);
      } catch (InterruptedException e) {
        e.printStackTrace();
      }
      
      i++;
    }
  }
  
}

class Controls extends JPanel {

  private static final long serialVersionUID = 1L;

  public Controls() {
    super();
    
    /* setBackground(Color.YELLOW); */
    
    Visuals.button = new JButton("Clear");
    
    Visuals.button.addActionListener(new ActionListener() {
      
      @Override
      public void actionPerformed(ActionEvent e) {
        Visuals.lines.clear();
        Visuals.frame.repaint();
      }
      
    });
    
    add(Visuals.button);
    
    Visuals.toggle = new JToggleButton("Press me");
    Visuals.toggle.setPreferredSize(new Dimension(96, 48));
    
    Visuals.toggle.addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(ActionEvent e) {
        Visuals.toggle.setText(Visuals.toggle.isSelected()? "Drawing": "Press me");
      }
    });
    
    add(Visuals.toggle);
    
    add(new JLabel("    Slider:"));
    
    Visuals.slider = new JSlider(0, 100, 50);
    
    Visuals.slider.addChangeListener(new ChangeListener() {
      @Override
      public void stateChanged(ChangeEvent e) {
        Visuals.frame.repaint();
      }
    });
    
    add(Visuals.slider);
    
    JCheckBox check = new JCheckBox("Unchecked");
    
    check.addActionListener(new ActionListener() {
      
      @Override
      public void actionPerformed(ActionEvent e) {
        check.setText(check.isSelected()? "Checked": "Unchecked");
      }
      
    });
    
    check.addKeyListener(new KeyListener() {
      
      @Override
      public void keyTyped(KeyEvent e) {

      }
      
      @Override
      public void keyReleased(KeyEvent e) {
      
      }
      
      @Override
      public void keyPressed(KeyEvent e) {
        if (e.getKeyCode() == KeyEvent.VK_LEFT)
          Visuals.point.setLocation(Visuals.point.getX() - Visuals.slider.getValue(), Visuals.point.getY());
        else if (e.getKeyCode() == KeyEvent.VK_RIGHT)
          Visuals.point.setLocation(Visuals.point.getX() + Visuals.slider.getValue(), Visuals.point.getY());
        else if (e.getKeyCode() == KeyEvent.VK_UP)
          Visuals.point.setLocation(Visuals.point.getX(), Visuals.point.getY() - Visuals.slider.getValue());
        else if (e.getKeyCode() == KeyEvent.VK_DOWN)
          Visuals.point.setLocation(Visuals.point.getX(), Visuals.point.getY() + Visuals.slider.getValue());
        else if (e.getKeyCode() == KeyEvent.VK_D)
          for (int i = 0; i < Visuals.directions.length; i++)
            Visuals.directions[i] = new Point((int)(10.0 * Math.random() - 5.0), (int)(10.0 * Math.random() - 5.0));
        else if (e.getKeyCode() == KeyEvent.VK_C)
          Visuals.color = new Color((float)Math.random(), (float)Math.random(), (float)Math.random(), (float)Math.random());
        
        Visuals.frame.repaint();
      }
      
    });
    
    add(check);
    
    JTextField field = new JTextField();
    field.setPreferredSize(new Dimension(96, 24));
    
    field.addKeyListener(new KeyListener() {
      
      @Override
      public void keyTyped(KeyEvent e) {
        
      }
      
      @Override
      public void keyReleased(KeyEvent e) {
        
      }
      
      @Override
      public void keyPressed(KeyEvent e) {
        if (e.getKeyCode() == KeyEvent.VK_ENTER && field.getText().length() > 0) {
          Visuals.text += " " + field.getText();
          field.setText("");
          Visuals.frame.repaint();
        }
      }
      
    });
    
    add(field);
    
    JComboBox<String> combo = new JComboBox<String>();
    combo.addItem("First");
    combo.addItem("Second");
    combo.addItem("Third");
    combo.addItem("Last");
    
    combo.setToolTipText("This is combo box has no action");
    
    add(combo);
  }
  
}

class Panel extends JPanel {

  private static final long serialVersionUID = 1L;

  public Panel() {
    super();
    
    setBackground(Color.WHITE);
  }

  @Override
  public void paint(Graphics g) {
    super.paint(g);
    
    Graphics2D graphics = (Graphics2D)g;
    
    graphics.setColor(new Color(64, 192, 64));
    graphics.fillRect(32, 32, 64, 64);
    
    graphics.setColor(Color.BLACK);
    graphics.setStroke(new BasicStroke(2.0f));
    graphics.drawRect(32, 32, 64, 64);
    
    graphics.setColor(new Color(64, 64, 192));
    graphics.fillRect(getWidth() / 10, getHeight() / 10, 64, 64);
    
    graphics.setColor(Color.WHITE);
    graphics.setStroke(new BasicStroke(2.0f));
    graphics.drawRoundRect(getWidth() / 10 + 16, getHeight() / 10 + 16, 32, 32, 8, 8);
    
    graphics.setColor(new Color((float)Math.random(), (float)Math.random(), (float)Math.random()));
    graphics.setStroke(new BasicStroke(2.0f));
    graphics.drawLine(getWidth() / 6, getHeight() / 3, getWidth() / 3, getHeight() / 6);
    
    graphics.setColor(new Color(192, 64, 64));
    graphics.fillOval(getWidth() / 3 - 32, getHeight() / 3 - 32, 64, 64);
    
    graphics.setColor(new Color(255, 255, 255));
    graphics.fillArc(getWidth() / 3 - 32, getHeight() / 3 - 32, 64, 64, 45, 90);
    
    graphics.setColor(new Color(64, 192, 64));
    graphics.setStroke(new BasicStroke(3.0f));
    graphics.drawOval(getWidth() / 3 - 32, getHeight() / 3 - 32, 64, 64);
    
    graphics.setColor(new Color((float)Math.random(), (float)Math.random(), (float)Math.random()));
    graphics.setFont(new Font(Font.MONOSPACED, Font.BOLD, 16));
    FontMetrics metrics = graphics.getFontMetrics();
    String string = "I am a string of characters!";
    graphics.drawString(string, getWidth() / 2 - metrics.stringWidth(string) / 2, getHeight() / 2 + metrics.getHeight() / 2);
    
    /* Polygon polygon = new Polygon();
    for (int i = 0; i < 4; i++)
      polygon.addPoint((int)(getWidth() * Math.random()), (int)(getHeight() * Math.random()));
  
    graphics.setColor(new Color((float)Math.random(), (float)Math.random(), (float)Math.random(), 0.5f));
    graphics.fillPolygon(polygon);
    
    graphics.setColor(Color.BLACK);
    graphics.setStroke(new BasicStroke(2.0f));
    graphics.drawPolygon(polygon); */
    
    try {
      graphics.drawImage(ImageIO.read(new File("images", "cats.jpg")), getWidth() / 8, 2 * getHeight() / 3, getWidth() / 4, getHeight() / 3, new ImageObserver() {
        @Override
        public boolean imageUpdate(Image img, int infoflags, int x, int y, int width, int height) {
          return false;
        }
      });
    } catch (IOException e) {
      e.printStackTrace();
    }
    
    graphics.setColor(Color.BLACK);
    graphics.setStroke(new BasicStroke(2.0f));
    graphics.drawRect(getWidth() / 8, 2 * getHeight() / 3, getWidth() / 4, getHeight() / 3);
    
    graphics.setColor(Color.BLUE);
    graphics.setStroke(new BasicStroke(2.0f));
    graphics.fillOval((int)Visuals.point.getX(), (int)Visuals.point.getY(), 32, 32);
    
    graphics.setColor(Color.BLACK);
    graphics.setStroke(new BasicStroke(1.0f));
    graphics.setFont(new Font("Times New Roman", Font.BOLD + Font.ITALIC, 20));
    graphics.drawString("Slider is set to " + Visuals.slider.getValue() + "...", getWidth() / 2, 3 * getHeight() / 4);
    
    graphics.setColor(new Color((float)Math.random(), (float)Math.random(), (float)Math.random()));
    graphics.setFont(new Font(Font.SANS_SERIF, Font.PLAIN, 24));
    metrics = graphics.getFontMetrics();
    graphics.drawString(Visuals.text, 2 * getWidth() / 3 - metrics.stringWidth(Visuals.text) / 2, getHeight() / 4 + metrics.getHeight() / 2);
    
    for (List<Point> line: Visuals.lines) {
      graphics.setColor(new Color((float)Math.random(), (float)Math.random(), (float)Math.random()));
      graphics.setStroke(new BasicStroke(4.0f));
      
      for (int i = 0; i < line.size() - 1; i++)
        graphics.drawLine((int)line.get(i).getX(), (int)line.get(i).getY(), (int)line.get(i + 1).getX(), (int)line.get(i + 1).getY());
    }
    
    graphics.setColor(Visuals.color);
    graphics.setStroke(new BasicStroke(1.0f));
    for (Point ball: Visuals.balls)
      graphics.fillOval((int)ball.getX(), (int)ball.getY(), 12, 12);
  }
  
}

class Backgrounds extends JPanel {

  private static final long serialVersionUID = 1L;

  public Backgrounds() {
    super();
    
    setBackground(new Color((float)Math.random(), (float)Math.random(), (float)Math.random()));
  }
  
}
