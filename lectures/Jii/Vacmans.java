import java.awt.BasicStroke;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.geom.RoundRectangle2D;

import javax.swing.BorderFactory;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JSlider;
import javax.swing.JToggleButton;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

public class Vacmans extends Pacmans {
  
  private GUI GUI;
  
  private long sleep;
  
  private boolean running;
  
  private JToggleButton run;
  
  private JSlider speed;
  
  public Vacmans(int size, int number) {
    this(size, size, number);
  }
  
  public Vacmans(int width, int height, int number) {
    super(width, height, number);
    
    sleep = Pacmans.MOVE_SLEEP_TIME;
    running = false;
    
    run = new JToggleButton();
    speed = new JSlider((int)Pacmans.MOVE_SLEEP_TIME / 2, 500, 500 - (int)sleep);
    
    GUI = new GUI(this);
    GUI.setVisible(true);
  }
  
  public GUI getGUI() {
    return GUI;
  }

  public JToggleButton getRun() {
    return run;
  }

  public JSlider getSpeed() {
    return speed;
  }

  public long getSleep() {
    return sleep;
  }

  public void setSleep(long sleep) {
    this.sleep = sleep;
  }

  public boolean isRunning() {
    return running;
  }

  public void setRunning(boolean running) {
    this.running = running;
  }

  @Override
  protected void draw() {
    /* super.draw(); */
    
    GUI.repaint();
  }

  @Override
  public void play() throws InterruptedException {
    draw();

    while (true) {
      if (isRunning()) {
        setPlays(getPlays() + 1);

        Thread.sleep(PLAY_SLEEP_TIME);

        while (getBoard().hasValue()) {
          if (isRunning()) {
            setRuns(getRuns() + 1);

            move();
          }

          draw();

          Thread.sleep(sleep);
        }
      
        Thread.sleep(PLAY_SLEEP_TIME);
        
        update();
      }
      
      draw();
    }
  }

  public static void main(String[] args) {
    int width = args.length > 0? Integer.parseInt(args[0]): 42;
    int height = args.length > 1? Integer.parseInt(args[0]): 24;
    int number = args.length > 2? Integer.parseInt(args[1]): 7;
    
    Pacmans pacmans = new Vacmans(width, height, number);
    
    try {
      pacmans.play();
    } catch (InterruptedException e) {
      e.printStackTrace();
    }
  }
  
}

class GUI extends JFrame {
  
  protected static final int CELL_SIZE = 24;
  
  protected static final int BORDER_SIZE = 16;
  
  protected static final int INDENT_SIZE = 4;
  
  protected static final int CONTROL_SIZE = 40;
  
  protected static final int CONSOLE_HEIGHT = 48;
  
  protected static final int SUMMARY_HEIGHT = 112;
  
  private static final long serialVersionUID = 1L;
  
  private Vacmans pacmans;

  public GUI(Vacmans pacmans) {
    super();
    
    this.pacmans = pacmans;
    
    setTitle("Pacmans");
    getRootPane().putClientProperty("apple.awt.brushMetalLook", true);
    setPreferredSize(new Dimension(pacmans.getBoard().getWidth() * CELL_SIZE + 2 * BORDER_SIZE, pacmans.getBoard().getHeight() * CELL_SIZE + 2 * BORDER_SIZE + CONSOLE_HEIGHT + SUMMARY_HEIGHT));
    setMinimumSize(new Dimension(pacmans.getBoard().getWidth() * CELL_SIZE + 2 * BORDER_SIZE, pacmans.getBoard().getHeight() * CELL_SIZE + 2 * BORDER_SIZE + CONSOLE_HEIGHT + SUMMARY_HEIGHT));
    setLayout(new BorderLayout());
    
    setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

    add(new Main(pacmans), BorderLayout.CENTER);
    add(new Console(pacmans), BorderLayout.NORTH);
    add(new Summary(pacmans), BorderLayout.SOUTH);
    
    pack();
  }

  public Vacmans getPacmans() {
    return pacmans;
  }
  
}

class Main extends JPanel {
  
  private static final long serialVersionUID = 1L;
  
  private Vacmans pacmans;

  public Main(Vacmans pacmans) {
    super();
    
    this.pacmans = pacmans;
    
    setFocusable(true);
    setBackground(new Color(246, 246, 246));
    setBorder(BorderFactory.createLineBorder(Color.BLACK));
    
    addKeyListener(new KeyListener() {

      @Override
      public void keyTyped(KeyEvent e) {
        
      }

      @Override
      public void keyPressed(KeyEvent e) {
        if (e.getKeyCode() == KeyEvent.VK_SPACE) {
          pacmans.setRunning(!pacmans.isRunning());
          pacmans.getRun().setSelected(pacmans.isRunning());
          pacmans.getRun().setIcon(pacmans.isRunning()? new ImageIcon("icons/pacman.png"):  new ImageIcon("icons/sacman.png"));
          pacmans.getRun().setToolTipText(pacmans.isRunning()? "Stop pacmans":  "Start pacmans");
        }
        else if (e.getKeyCode() == KeyEvent.VK_R) {
          pacmans.setRunning(false);
          pacmans.getRun().setSelected(false);
          pacmans.getRun().setIcon(new ImageIcon("icons/sacman.png"));
          pacmans.getRun().setToolTipText("Start pacmans");
          pacmans.reset();
        }
        else if (e.getKeyCode() == KeyEvent.VK_RIGHT)
          pacmans.getSpeed().setValue(pacmans.getSpeed().getValue() + 10);
        else if (e.getKeyCode() == KeyEvent.VK_LEFT)
          pacmans.getSpeed().setValue(pacmans.getSpeed().getValue() - 10);
        else if (e.getKeyCode() == KeyEvent.VK_P)
          for (Pacman pacman: pacmans.getPacmans())
            pacman.setPrime(Math.random() < 0.5);
        
        pacmans.getGUI().repaint();
      }

      @Override
      public void keyReleased(KeyEvent e) {
        
      }
      
    });
    
    addMouseListener(new MouseListener() {
      
      @Override
      public void mouseReleased(MouseEvent e) {
        
      }
      
      @Override
      public void mousePressed(MouseEvent e) {
        
      }
      
      @Override
      public void mouseExited(MouseEvent e) {
        
      }
      
      @Override
      public void mouseEntered(MouseEvent e) {
        
      }
      
      @Override
      public void mouseClicked(MouseEvent e) {
        double width = (getWidth() - 2.0 * GUI.BORDER_SIZE) / pacmans.getBoard().getWidth();
        double height = (getHeight() - 2.0 * GUI.BORDER_SIZE) / pacmans.getBoard().getHeight();
        
        if (!pacmans.getBoard().isEmpty() && e.getX() >= GUI.BORDER_SIZE && e.getY() >= GUI.BORDER_SIZE && e.getX() < getWidth() - GUI.BORDER_SIZE && e.getY() < getHeight() - GUI.BORDER_SIZE) {
          Position position = new Position((int)((e.getX() - GUI.BORDER_SIZE) / width), (int)((e.getY() - GUI.BORDER_SIZE) / height));
          
          if (pacmans.getBoard().getCell(position) instanceof Empty) {
            Cell cell;
            while ((cell = Cell.random(position)) instanceof Empty);
            
            pacmans.getBoard().setCell(position, cell);
          }
          else if (!(pacmans.getBoard().getCell(position) instanceof Pacman))
            pacmans.getBoard().setCell(position, new Empty(position));
          
          repaint();
        }
      }
      
    });
  }

  @Override
  public void paint(Graphics g) {
    super.paint(g);
    
    Graphics2D graphics = (Graphics2D)g;
    
    double width = (getWidth() - 2.0 * GUI.BORDER_SIZE) / pacmans.getBoard().getWidth();
    double height = (getHeight() - 2.0 * GUI.BORDER_SIZE) / pacmans.getBoard().getHeight();
    
    for (int i = 0; i < pacmans.getBoard().getWidth(); i++)
      for (int j = 0; j < pacmans.getBoard().getHeight(); j++) {
        Cell cell = pacmans.getBoard().getCell(new Position(i, j));
        if (cell instanceof Block) {
          graphics.setColor(new Color(200, 200, 200));
          graphics.setStroke(new BasicStroke(1.0f));
          
          graphics.fillRect(GUI.BORDER_SIZE + (int)Math.round(i * width), GUI.BORDER_SIZE + (int)Math.round(j * height), (int)Math.round(width), (int)Math.round(height));
        }
        else if (cell instanceof Coin) {
          if (cell instanceof BigCoin)
            graphics.setColor(new Color(214, 175, 54));
          else if (cell instanceof SmallCoin)
            graphics.setColor(new Color(167, 167, 173));
          else if (cell instanceof TinyCoin)
            graphics.setColor(new Color(167, 112, 68));
          graphics.setStroke(new BasicStroke(1.0f));
          
          graphics.fillOval(GUI.BORDER_SIZE + (int)Math.round(i * width) + GUI.INDENT_SIZE, GUI.BORDER_SIZE + (int)Math.round(j * height) + GUI.INDENT_SIZE, (int)Math.round(width) - 2 * GUI.INDENT_SIZE, (int)Math.round(height) - 2 * GUI.INDENT_SIZE);
          
          graphics.setColor(Color.BLACK);
          graphics.setStroke(new BasicStroke(1.5f));
          
          graphics.drawOval(GUI.BORDER_SIZE + (int)Math.round(i * width) + GUI.INDENT_SIZE, GUI.BORDER_SIZE + (int)Math.round(j * height) + GUI.INDENT_SIZE, (int)Math.round(width) - 2 * GUI.INDENT_SIZE, (int)Math.round(height) - 2 * GUI.INDENT_SIZE);
          
          graphics.setColor(Color.BLACK);
          graphics.setStroke(new BasicStroke(1.0f));
          graphics.setFont(new Font(Font.SANS_SERIF, Font.BOLD, 9));
          FontMetrics metrics = graphics.getFontMetrics();
          
          String value = "" + cell.getValue();
          graphics.drawString(value, GUI.BORDER_SIZE + (int)Math.round(i * width + 0.5 * width - 0.5 * metrics.stringWidth(value)), GUI.BORDER_SIZE + (int)Math.round(j * height + 0.5 * height + 0.33 * metrics.getHeight()));
        }
        else if (cell instanceof Pacman) {
          graphics.setColor(new Color(33, 46, 64));
          graphics.setStroke(new BasicStroke(1.5f));
          
          graphics.fillArc(GUI.BORDER_SIZE + (int)Math.round(i * width) + GUI.INDENT_SIZE / 2, GUI.BORDER_SIZE + (int)Math.round(j * height) + GUI.INDENT_SIZE / 2, (int)Math.round(width) - GUI.INDENT_SIZE, (int)Math.round(height) - GUI.INDENT_SIZE, 15, 320);
          
          if (((Pacman)cell).isPrime())
            graphics.setColor(new Color(214, 175, 54));
          else
            graphics.setColor(Color.WHITE);
          graphics.setStroke(new BasicStroke(1.0f));
          
          graphics.fillOval(GUI.BORDER_SIZE + (int)Math.round(i * width + 0.4 * width) + GUI.INDENT_SIZE / 2, GUI.BORDER_SIZE + (int)Math.round(j * height + 0.1 * height) + GUI.INDENT_SIZE / 2, GUI.INDENT_SIZE, GUI.INDENT_SIZE);
          
          graphics.setFont(new Font(Font.SANS_SERIF, Font.BOLD, 10));
          FontMetrics metrics = graphics.getFontMetrics();
          
          String label = "" + cell.getLabel();
          graphics.drawString(label, GUI.BORDER_SIZE + (int)Math.round(i * width + 0.33 * width - 0.5 * metrics.stringWidth(label)), GUI.BORDER_SIZE + (int)Math.round(j * height + 0.5 * height + 0.33 * metrics.getHeight()));
        }
      }
    
    graphics.setColor(Color.BLACK);
    graphics.setStroke(new BasicStroke(1.5f));
    for (int i = 0; i <= pacmans.getBoard().getWidth(); i++)
      graphics.drawLine(GUI.BORDER_SIZE + (int)Math.round(i * width), GUI.BORDER_SIZE, GUI.BORDER_SIZE + (int)Math.round(i * width), getHeight() - GUI.BORDER_SIZE);
    for (int j = 0; j <= pacmans.getBoard().getHeight(); j++)
      graphics.drawLine(GUI.BORDER_SIZE, GUI.BORDER_SIZE + (int)Math.round(j * height), getWidth() - GUI.BORDER_SIZE, GUI.BORDER_SIZE + (int)Math.round(j * height));
    
    if (pacmans.getBoard().isEmpty()) {
      graphics.setColor(new Color(200, 200, 200, 200));
      graphics.fillRect(0, 0, getWidth(), getHeight());
      
      graphics.setStroke(new BasicStroke(1.0f));
      graphics.setFont(new Font(Font.SANS_SERIF, Font.BOLD, 32));
      FontMetrics metrics = graphics.getFontMetrics();
      
      RoundRectangle2D rectangle = new RoundRectangle2D.Float((getWidth() - metrics.stringWidth("Empty board! Reset?")) / 2 - GUI.BORDER_SIZE, getHeight() / 2 - GUI.BORDER_SIZE, metrics.stringWidth("Empty board! Reset?") + 2 * GUI.BORDER_SIZE, metrics.getHeight() + GUI.BORDER_SIZE, 10, 10);
      
      graphics.setColor(new Color(246, 246, 246));
      
          graphics.fill(rectangle);
      
          graphics.setColor(Color.BLACK);
      
          graphics.draw(rectangle);
      
      graphics.drawString("Empty board! Reset?", (getWidth() - metrics.stringWidth("Empty board! Reset?")) / 2, getHeight() / 2 + 3 * metrics.getHeight() / 5);
    }
  }

  public Vacmans getPacmans() {
    return pacmans;
  }

}

class Console extends JPanel {
  
  private static final long serialVersionUID = 1L;
  
  private Vacmans pacmans;

  public Console(Vacmans pacmans) {
    super();
    
    this.pacmans = pacmans;
    
    setFocusable(false);
    setPreferredSize(new Dimension(getWidth(), GUI.CONSOLE_HEIGHT));
    
    JButton reset = new JButton("Reset");
    JButton prime = new JButton("Prime");
    
    add(new JLabel("    "));
    
    reset.setToolTipText("Reset pacmans");
    reset.addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(ActionEvent e) {
        pacmans.setRunning(false);
        pacmans.getRun().setSelected(false);
        pacmans.getRun().setIcon(new ImageIcon("icons/sacman.png"));
        pacmans.getRun().setToolTipText("Start pacmans");
        pacmans.reset();
        
        pacmans.getGUI().repaint();
      }
    });
    reset.setFont(new Font(Font.SANS_SERIF, Font.PLAIN, 13));
    reset.setFocusable(false);
    add(reset);
    
    prime.setToolTipText("Reprimes pacmans");
    prime.addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(ActionEvent e) {
        for (Pacman pacman: pacmans.getPacmans())
          pacman.setPrime(Math.random() < 0.5);
        
        pacmans.getGUI().repaint();
      }
    });
    prime.setFont(new Font(Font.SANS_SERIF, Font.PLAIN, 13));
    prime.setFocusable(false);
    add(prime);
    
    add(new JLabel("  "));
    
    pacmans.getRun().setToolTipText("Start pacmans");
    pacmans.getRun().setIcon(new ImageIcon("icons/sacman.png"));
    pacmans.getRun().addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(ActionEvent e) {
        pacmans.setRunning(pacmans.getRun().isSelected());
        pacmans.getRun().setIcon(pacmans.getRun().isSelected()? new ImageIcon("icons/pacman.png"):  new ImageIcon("icons/sacman.png"));
        pacmans.getRun().setToolTipText(pacmans.getRun().isSelected()? "Stop pacmans":  "Start pacmans");
        
        pacmans.getGUI().repaint();
      }
    });
    pacmans.getRun().setPreferredSize(new Dimension(GUI.CONTROL_SIZE, GUI.CONTROL_SIZE));
    pacmans.getRun().setFocusable(false);
    add(pacmans.getRun());
    
    add(new JLabel(" "));
    
    pacmans.getSpeed().setToolTipText("Set pacmans speed");
    pacmans.getSpeed().addChangeListener(new ChangeListener() {
      @Override
      public void stateChanged(ChangeEvent e) {
        pacmans.setSleep(500 - pacmans.getSpeed().getValue());
        
        pacmans.getGUI().repaint();
      }
    });
    pacmans.getSpeed().setFocusable(false);
    add(pacmans.getSpeed());
  }

  public Vacmans getPacmans() {
    return pacmans;
  }

}

class Summary extends JPanel {
  
  private static final long serialVersionUID = 1L;
  
  private Vacmans pacmans;

  public Summary(Vacmans pacmans) {
    super();
    
    this.pacmans = pacmans;
    
    setFocusable(false);
    setPreferredSize(new Dimension(getWidth(), GUI.SUMMARY_HEIGHT));
  }

  @Override
  public void paint(Graphics g) {
    super.paint(g);
    
    Graphics2D graphics = (Graphics2D)g;

    RoundRectangle2D rectangle = new RoundRectangle2D.Float((int)Math.round(0.325 * getWidth()), GUI.BORDER_SIZE, (int)Math.round(0.35 * getWidth()), getHeight() - 2 * GUI.BORDER_SIZE, 10, 10);
    
    graphics.setColor(new Color(246, 246, 246));
    
        graphics.fill(rectangle);
    
        graphics.setColor(Color.BLACK);
    
        graphics.draw(rectangle);
    
    graphics.setColor(Color.BLACK);
    graphics.setStroke(new BasicStroke(1.0f));
    
    graphics.setFont(new Font(Font.SANS_SERIF, Font.BOLD, 12));
    FontMetrics metrics = graphics.getFontMetrics();
    
    int y = (getHeight() - 4 * metrics.getHeight()) / 2 + 3 * metrics.getHeight() / 4;
    
    if (!pacmans.getBoard().isEmpty())
      graphics.drawString("Board value: ", (int)Math.round(0.425 * getWidth()) - metrics.stringWidth("Board value: "), y);
    else
      graphics.drawString("Empty board!        ", (int)Math.round(0.425 * getWidth()) - metrics.stringWidth("Empty board!        ") / 2, y);
    graphics.drawString("Golden coins: ", (int)Math.round(0.425 * getWidth()) - metrics.stringWidth("Golden coins: "), y + metrics.getHeight());
    graphics.drawString("Silver coins: ", (int)Math.round(0.425 * getWidth()) - metrics.stringWidth("Silver coins: "), y + 2 * metrics.getHeight());
    graphics.drawString("Bronze coins: ", (int)Math.round(0.425 * getWidth()) - metrics.stringWidth("Bronze coins: "), y + 3 * metrics.getHeight());
    
    for (int i = 0; i < Math.min(4, pacmans.getPacmans().size()); i++) {
      String number = i == 0? "1st": i == 1? "2nd": i == 2? "3rd" : "4th";
      graphics.drawString(number + " place: ", (int)Math.round(0.575 * getWidth()) - metrics.stringWidth(number + " place: "), y + i * metrics.getHeight());
    }
    
    graphics.setFont(new Font(Font.SANS_SERIF, Font.PLAIN, 12));
    metrics = graphics.getFontMetrics();
    
    if (!pacmans.getBoard().isEmpty())
      graphics.drawString(pacmans.getBoard().getValue() > 0? String.format("%,d €", pacmans.getBoard().getValue()): "empty", (int)Math.round(0.425 * getWidth()), y);
    graphics.drawString(String.format("%,d for %,d €", pacmans.getBoard().getNumber(new BigCoin(null).getClass()), new BigCoin(null).getValue()), (int)Math.round(0.425 * getWidth()), y + metrics.getHeight());
    graphics.drawString(String.format("%,d for %,d €", pacmans.getBoard().getNumber(new SmallCoin(null).getClass()), new SmallCoin(null).getValue()), (int)Math.round(0.425 * getWidth()), y + 2 * metrics.getHeight());
    graphics.drawString(String.format("%,d for %,d €", pacmans.getBoard().getNumber(new TinyCoin(null).getClass()), new TinyCoin(null).getValue()), (int)Math.round(0.425 * getWidth()), y + 3 * metrics.getHeight());

    for (int i = 0; i < Math.min(4, pacmans.getPacmans().size()); i++)
      graphics.drawString(String.format("%s with %,.0f €", pacmans.getPacmans().get(i).getLabel() + (pacmans.getPacmans().get(i).isPrime()? "'": ""), pacmans.getScores().get(pacmans.getPacmans().get(i))), (int)Math.round(0.575 * getWidth()), y + i * metrics.getHeight());
  }

  public Vacmans getPacmans() {
    return pacmans;
  }

}
