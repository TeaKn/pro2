```java
import java.awt.BasicStroke;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Polygon;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.geom.RoundRectangle2D;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;

import javax.swing.BorderFactory;
import javax.swing.JFrame;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JPanel;
import javax.swing.KeyStroke;
import javax.swing.UIManager;

public class Quoridor {
  
  protected static final long GAME_SLEEP = 100L;
  
  protected static final long MOVE_SLEEP = 1000L;
  
  protected static final double MOVE_PROBABILITY = 0.66;
  
  private boolean first;
  
  private boolean finished;
  
  private boolean running;
  
  private Player[] players;
  
  private Set<Wall> walls;
  
  private GUI GUI;
  
  public Quoridor() {
    super();

    reset();
    
    GUI = new GUI(this);
    GUI.setVisible(true);
  }
  
  public boolean isFirst() {
    return first;
  }

  public boolean isFinished() {
    return finished;
  }
  
  public void setFinished() {
    finished = true;
  }
  
  public boolean isRunning() {
    return running;
  }
  
  public void setRunning() {
    running = !running;
  }

  public void nextPlayer() {
    first = !first;
  }
  
  public Player[] getPlayers() {
    return players;
  }
  
  public Player getPlayer() {
    return players[first? 0: 1];
  }
  
  public Player getOther() {
    return players[first? 1: 0];
  }

  public Set<Wall> getWalls() {
    return walls;
  }
  
  public Graph getGraph() {
    return new Graph(walls);
  }
  
  public Graph getGraph(Wall wall) {
    Graph graph = new Graph(walls);
    graph.removeEdge(wall);
    return graph;
  }
  
  public GUI getGUI() {
    return GUI;
  }

  protected void draw() {
    if (GUI != null)
      GUI.repaint();
  }

  public void play() {
    while (true) {
      if (getPlayer() instanceof AI && isRunning() && !isFinished()) {
        try {
          Thread.sleep(MOVE_SLEEP);
        } catch (InterruptedException e) {

        }
        
        AI player = (AI)getPlayer();
        if (player.getWalls() == 0 || Math.random() < MOVE_PROBABILITY || !player.wall(this))
          player.move(this);
        if (player.hasWon())
          setFinished();
        nextPlayer();
      }
      
      draw();
      
      try {
        Thread.sleep(GAME_SLEEP);
      } catch (InterruptedException e) {

      }
    }
  }

  public void reset(boolean first) {
    players[first? 0: 1] = players[first? 0: 1] instanceof AI? new AI(first): new Player(first);
    for (Iterator<Wall> iterator = walls.iterator(); iterator.hasNext(); )
      if (iterator.next().isFirst() == first)
        iterator.remove();
  }
  
  public void reset() {
    first = true;
    finished = false;
    running = false;
    players = new Player[] { new AI(true), new AI(false) };
    walls = new TreeSet<Wall>();
  }
  
  public void rewall() {
    for (Player player: players)
      player.resetWalls();
    walls = new TreeSet<Wall>();
  }
  
  public void reinit(boolean first) {
    players[first? 0: 1] = players[first? 0: 1] instanceof AI? new Player(players[first? 0: 1]): new AI(players[first? 0: 1]);
  }
  
  public static void main(String[] args) {
    System.setProperty("apple.laf.useScreenMenuBar", "true");
    
    new Quoridor().play();
  }
  
}

class GUI extends JFrame {
  
  private static final long serialVersionUID = 1L;
  
  protected static final int BORDER_SIZE = 32;
  
  protected static final float GRID_WIDTH = 6.0f;

  protected static final Color WALL_COLOR = new Color(64, 64, 64);
  
  protected static final Color GRID_COLOR = new Color(160, 160, 160);
  
  protected static final Color FIRST_COLOR = new Color(232, 76, 61);
  
  protected static final Color SECOND_COLOR = new Color(52 + 32, 73 + 32, 94 + 32);
  
  protected static final Color BACKGROUND_COLOR = new Color(236, 240, 241);
  
  private Quoridor quoridor;

  public GUI(Quoridor quoridor) {
    super();
    
    this.quoridor = quoridor;
    
    setTitle("Quoridor");
    getRootPane().putClientProperty("apple.awt.brushMetalLook", true);
    setPreferredSize(new Dimension(600, 600));
    setMinimumSize(new Dimension(600, 600));
    setLayout(new BorderLayout());
    
    setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

    add(new Main(quoridor), BorderLayout.CENTER);
    
    JMenuBar bar = new JMenuBar();
    setJMenuBar(bar);
    
    JMenu menu = new JMenu("File");
      bar.add(menu);
    
      JMenuItem item = new JMenuItem("New");
      item.setAccelerator(KeyStroke.getKeyStroke('N', Toolkit.getDefaultToolkit().getMenuShortcutKeyMask()));
      item.setIcon(UIManager.getIcon("FileView.fileIcon"));
      item.setEnabled(false);
      menu.add(item);
    
      item = new JMenuItem("Open...");
      item.setAccelerator(KeyStroke.getKeyStroke('O', Toolkit.getDefaultToolkit().getMenuShortcutKeyMask()));
      item.setIcon(UIManager.getIcon("Tree.openIcon"));
      item.setEnabled(false);
      menu.add(item);
    
      menu.addSeparator();
    
      item = new JMenuItem("Save");
      item.setAccelerator(KeyStroke.getKeyStroke('S', Toolkit.getDefaultToolkit().getMenuShortcutKeyMask()));
      item.setIcon(UIManager.getIcon("FileView.hardDriveIcon"));
      item.setEnabled(false);
      menu.add(item);
    
      item = new JMenuItem("Save As...");
      item.setEnabled(false);
      menu.add(item);
    
      menu.addSeparator();
    
      item = new JMenuItem("Export...");
      item.setEnabled(false);
      menu.add(item);
    
    menu = new JMenu("Game");
      bar.add(menu);
    
      item = new JMenuItem("Simulate");
      item.setAccelerator(KeyStroke.getKeyStroke('S', Toolkit.getDefaultToolkit().getMenuShortcutKeyMask()));
      item.addActionListener(new ActionListener() {
      
      @Override
      public void actionPerformed(ActionEvent e) {
        quoridor.setRunning();
        quoridor.draw();
      }
      
    });
      menu.add(item);
    
      menu.addSeparator();
    
      item = new JMenuItem("New Player");
      item.setEnabled(false);
      menu.add(item);
    
      item = new JMenuItem("Next Player");
      item.setAccelerator(KeyStroke.getKeyStroke('P', Toolkit.getDefaultToolkit().getMenuShortcutKeyMask()));
      item.addActionListener(new ActionListener() {
      
      @Override
      public void actionPerformed(ActionEvent e) {
        quoridor.nextPlayer();
        quoridor.draw();
      }
      
    });
      menu.add(item);
    
      menu.addSeparator();
    
      for (Player player: quoridor.getPlayers()) {
        item = new JMenuItem("Toggle " + player.getName());
        item.addActionListener(new ActionListener() {

          @Override
          public void actionPerformed(ActionEvent e) {
            quoridor.reinit(player.isFirst());
            quoridor.draw();
          }

        });
        menu.add(item);
      }
    
      menu.addSeparator();
    
      for (Player player: quoridor.getPlayers()) {
        item = new JMenuItem("Reset " + player.getName());
        item.setAccelerator(KeyStroke.getKeyStroke(player.getName().charAt(0), ActionEvent.SHIFT_MASK));
        item.addActionListener(new ActionListener() {

          @Override
          public void actionPerformed(ActionEvent e) {
            if (!quoridor.isFinished())
              quoridor.reset(player.isFirst());
            quoridor.draw();
          }

        });
        menu.add(item);
      }
    
      menu.addSeparator();
    
      item = new JMenuItem("Reset Game");
      item.setAccelerator(KeyStroke.getKeyStroke('R', Toolkit.getDefaultToolkit().getMenuShortcutKeyMask()));
      item.addActionListener(new ActionListener() {
      
      @Override
      public void actionPerformed(ActionEvent e) {
        quoridor.reset();
        quoridor.draw();
      }
      
    });
      menu.add(item);
    
      item = new JMenuItem("Reset Walls");
      item.setAccelerator(KeyStroke.getKeyStroke('W', Toolkit.getDefaultToolkit().getMenuShortcutKeyMask()));
      item.addActionListener(new ActionListener() {
      
      @Override
      public void actionPerformed(ActionEvent e) {
        quoridor.rewall();
        quoridor.draw();
      }
      
    });
      menu.add(item);
    
      item = new JMenuItem("Reset AI");
      item.setEnabled(false);
      menu.add(item);
    
      menu = new JMenu("Other");
      menu.setEnabled(false);
      bar.add(menu);
    
      bar.add(new JMenu("Help"));
    
    pack();
  }

  public Quoridor getQuoridor() {
    return quoridor;
  }
  
}

class Main extends JPanel {
  
  private static final long serialVersionUID = 1L;
  
  private Quoridor quoridor;

  public Main(Quoridor quoridor) {
    super();
    
    this.quoridor = quoridor;
    
    setFocusable(true);
    setBackground(GUI.BACKGROUND_COLOR);
    setBorder(BorderFactory.createLineBorder(Color.BLACK));
    
    /* addKeyListener(new KeyListener() {

      @Override
      public void keyTyped(KeyEvent e) {
     
      }

      @Override
      public void keyPressed(KeyEvent e) {
        if (e.getKeyCode() == KeyEvent.VK_R && (e.getModifiers() & KeyEvent.VK_META) != 0)
          quoridor.reset();
     
        quoridor.draw();
      }

      @Override
      public void keyReleased(KeyEvent e) {
     
      }
     
    }); */
    
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
        if (!quoridor.isFinished() && !(quoridor.getPlayer() instanceof AI)) {
          double width = (getWidth() - 2 * GUI.BORDER_SIZE) / 9.0;
          double height = (getHeight() - 2 * GUI.BORDER_SIZE) / 9.0;

          double x = (e.getX() - GUI.BORDER_SIZE) / width;
          double y = (e.getY() - GUI.BORDER_SIZE) / height;

          int X = (int)Math.round(x);
          int Y = (int)Math.round(y);

          if (x > 0.0 && x < 9.0 && y > 0.0 && y < 9.0)
            if (Math.abs(x - X) * width <= GUI.GRID_WIDTH / 2.0 || Math.abs(y - Y) * height <= GUI.GRID_WIDTH / 2.0) {
              if (quoridor.getPlayer().getWalls() > 0) {
                Wall wall = null;
                if (Math.abs(x - X) * width <= GUI.GRID_WIDTH / 2.0 && X > 0 && X < 9)
                  wall = new Wall(X, (int)Math.floor(y), quoridor.isFirst(), false);
                else if (Math.abs(y - Y) * height <= GUI.GRID_WIDTH / 2.0 && Y > 0 && y < 9)
                  wall = new Wall((int)Math.floor(x), Y, quoridor.isFirst(), true);
                
                if (wall != null && !quoridor.getWalls().contains(wall) && quoridor.getGraph(wall).isConnected()) {
                  quoridor.getWalls().add(wall);
                  quoridor.getPlayer().removeWall();
                  quoridor.nextPlayer();
                }
              }
            }
            else {
              X = (int)Math.floor(x);
              Y = (int)Math.floor(y);

              if (Math.abs(quoridor.getPlayer().getX() - X) + Math.abs(quoridor.getPlayer().getY() - Y) == 1 && (quoridor.getOther().getX() != X || quoridor.getOther().getY() != Y)) {
                boolean illegal = false;
                for (Wall wall: quoridor.getWalls())
                  if (wall.isHorizontal() && quoridor.getPlayer().getX() == X && X == wall.getX() && (quoridor.getPlayer().getY() > Y? quoridor.getPlayer().getY() == wall.getY(): Y == wall.getY()) || !wall.isHorizontal() && quoridor.getPlayer().getY() == Y && Y == wall.getY() && (quoridor.getPlayer().getX() > X? quoridor.getPlayer().getX() == wall.getX(): X == wall.getX())) {
                    illegal = true;
                    break;
                  }

                if (!illegal) {
                  quoridor.getPlayer().setX(X);
                  quoridor.getPlayer().setY(Y);
                  quoridor.nextPlayer();
                }
              }
            }

          for (Player player: quoridor.getPlayers())
            if (player.hasWon())
              quoridor.setFinished();
        }
        
        quoridor.draw();
      }
      
    });
    
  }

  @Override
  public void paint(Graphics g) {
    super.paint(g);
    
    Graphics2D graphics = (Graphics2D)g;
    
    double width = (getWidth() - 2 * GUI.BORDER_SIZE) / 9.0;
    double height = (getHeight() - 2 * GUI.BORDER_SIZE) / 9.0;
    
    graphics.setColor(new Color(GUI.SECOND_COLOR.getRed(), GUI.SECOND_COLOR.getGreen(), GUI.SECOND_COLOR.getBlue(), 96));
    graphics.setStroke(new BasicStroke(1.0f));
    
    graphics.fillRect(GUI.BORDER_SIZE, GUI.BORDER_SIZE, getWidth() - 2 * GUI.BORDER_SIZE, (int)Math.round(height));
    
    graphics.setColor(new Color(GUI.FIRST_COLOR.getRed(), GUI.FIRST_COLOR.getGreen(), GUI.FIRST_COLOR.getBlue(), 128));
    graphics.setStroke(new BasicStroke(1.0f));
    
    graphics.fillRect(GUI.BORDER_SIZE, (int)Math.round(GUI.BORDER_SIZE + 8 * height), getWidth() - 2 * GUI.BORDER_SIZE, (int)Math.round(height));
    
    graphics.setColor(GUI.GRID_COLOR);
    graphics.setStroke(new BasicStroke(GUI.GRID_WIDTH));
    
    for (int i = 1; i < 9; i++) {
      graphics.drawLine(GUI.BORDER_SIZE, (int)Math.round(GUI.BORDER_SIZE + i * height), getWidth() - GUI.BORDER_SIZE, (int)Math.round(GUI.BORDER_SIZE + i * height));
      graphics.drawLine((int)Math.round(GUI.BORDER_SIZE + i * width), GUI.BORDER_SIZE, (int)Math.round(GUI.BORDER_SIZE + i * width), getHeight() - GUI.BORDER_SIZE);
    }
    
    for (Wall wall: quoridor.getWalls()) {
      if (wall.isFirst())
        graphics.setColor(GUI.FIRST_COLOR);
      else
        graphics.setColor(GUI.SECOND_COLOR);
      
      if (wall.isHorizontal())
        graphics.drawLine((int)Math.round(GUI.BORDER_SIZE + wall.getX() * width), (int)Math.round(GUI.BORDER_SIZE + wall.getY() * height), (int)Math.round(GUI.BORDER_SIZE + (wall.getX() + 1) * width), (int)Math.round(GUI.BORDER_SIZE + wall.getY() * height));
      else
        graphics.drawLine((int)Math.round(GUI.BORDER_SIZE + wall.getX() * width), (int)Math.round(GUI.BORDER_SIZE + wall.getY() * height), (int)Math.round(GUI.BORDER_SIZE + wall.getX() * width), (int)Math.round(GUI.BORDER_SIZE + (wall.getY() + 1) * height));
    }
    
    graphics.setColor(GUI.WALL_COLOR);
    graphics.setStroke(new BasicStroke(GUI.GRID_WIDTH));

    graphics.drawLine(GUI.BORDER_SIZE, GUI.BORDER_SIZE, getWidth() - GUI.BORDER_SIZE, GUI.BORDER_SIZE);
    graphics.drawLine(GUI.BORDER_SIZE, GUI.BORDER_SIZE, GUI.BORDER_SIZE, getHeight() - GUI.BORDER_SIZE);
    
    graphics.drawLine(GUI.BORDER_SIZE, (int)Math.round(GUI.BORDER_SIZE + 9 * height), getWidth() - GUI.BORDER_SIZE, (int)Math.round(GUI.BORDER_SIZE + 9 * height));
    graphics.drawLine((int)Math.round(GUI.BORDER_SIZE + 9 * width), GUI.BORDER_SIZE, (int)Math.round(GUI.BORDER_SIZE + 9 * width), getHeight() - GUI.BORDER_SIZE);
    
    graphics.setColor(GUI.GRID_COLOR);
    graphics.setStroke(new BasicStroke(1.0f));
    
    for (int i = 1; i < 9; i++)
      for (int j = 1; j < 9; j++)
        graphics.fillRect((int)Math.round(GUI.BORDER_SIZE + i * width - GUI.GRID_WIDTH / 2), (int)Math.round(GUI.BORDER_SIZE + j * height - GUI.GRID_WIDTH / 2), (int)GUI.GRID_WIDTH, (int)GUI.GRID_WIDTH);
    
    for (Player player: quoridor.getPlayers()) {
      if (player.isFirst())
        graphics.setColor(GUI.FIRST_COLOR);
      else
        graphics.setColor(GUI.SECOND_COLOR);
      graphics.setStroke(new BasicStroke(1.0f));

      Polygon triangle = new Polygon();
      triangle.addPoint((int)Math.round(GUI.BORDER_SIZE + player.getX() * width + width / 4), (int)Math.round(GUI.BORDER_SIZE + player.getY() * height + 5 * height / 6));
      triangle.addPoint((int)Math.round(GUI.BORDER_SIZE + player.getX() * width + 3 * width / 4), (int)Math.round(GUI.BORDER_SIZE + player.getY() * height + 5 * height / 6));
      triangle.addPoint((int)Math.round(GUI.BORDER_SIZE + player.getX() * width + width / 2), (int)Math.round(GUI.BORDER_SIZE + player.getY() * height + height / 4));
      graphics.fillPolygon(triangle);
      
      graphics.setColor(GUI.WALL_COLOR);
      graphics.setStroke(new BasicStroke(GUI.GRID_WIDTH / 2));
      
      if (!quoridor.isFinished() && quoridor.isFirst() == player.isFirst())
        graphics.drawPolygon(triangle);
      
      if (player.isFirst())
        graphics.setColor(GUI.FIRST_COLOR);
      else
        graphics.setColor(GUI.SECOND_COLOR);
      graphics.setStroke(new BasicStroke(1.0f));
      
      graphics.fillOval((int)Math.round(GUI.BORDER_SIZE + player.getX() * width + width / 3), (int)Math.round(GUI.BORDER_SIZE + player.getY() * height + height / 6), (int)Math.round(width / 3), (int)Math.round(height / 3));
      
      graphics.setColor(GUI.WALL_COLOR);
      graphics.setStroke(new BasicStroke(GUI.GRID_WIDTH / 2));
      
      if (!quoridor.isFinished() && quoridor.isFirst() == player.isFirst())
        graphics.drawOval((int)Math.round(GUI.BORDER_SIZE + player.getX() * width + width / 3), (int)Math.round(GUI.BORDER_SIZE + player.getY() * height + height / 6), (int)Math.round(width / 3), (int)Math.round(height / 3));
      
      if (player instanceof AI) {
        graphics.setFont(new Font(Font.SANS_SERIF, Font.BOLD, 10));
        FontMetrics metrics = graphics.getFontMetrics();
      
        graphics.drawString("AI", (int)Math.round(GUI.BORDER_SIZE + player.getX() * width + width / 3 + metrics.stringWidth("AI") / 2), (int)Math.round(GUI.BORDER_SIZE + player.getY() * height + height / 4 + 3 * metrics.getHeight() / 4));
      }
      
      if (player.isFirst())
        graphics.setColor(GUI.FIRST_COLOR);
      else
        graphics.setColor(GUI.SECOND_COLOR);
      graphics.setStroke(new BasicStroke(1.0f));
      
      if (!quoridor.isFinished() && quoridor.isFirst() == player.isFirst())
        graphics.fillOval(GUI.BORDER_SIZE, quoridor.isFirst()? GUI.BORDER_SIZE / 4: getHeight() - 3 * GUI.BORDER_SIZE / 4, GUI.BORDER_SIZE / 2, GUI.BORDER_SIZE / 2);
      
      for (int i = 0; i < player.getWalls(); i++)
        graphics.fillRect((int)Math.round(getWidth() - 5 * GUI.BORDER_SIZE / 4 + GUI.GRID_WIDTH / 4 - i * GUI.BORDER_SIZE * 0.4), player.isFirst()? GUI.BORDER_SIZE / 2: getHeight() - 3 * GUI.BORDER_SIZE / 4, GUI.BORDER_SIZE / 4, GUI.BORDER_SIZE / 4);
      
      graphics.setColor(GUI.WALL_COLOR);
      graphics.setStroke(new BasicStroke(GUI.GRID_WIDTH / 4));
      
      for (int i = 0; i < player.getWalls(); i++)
        graphics.drawRect((int)Math.round(getWidth() - 5 * GUI.BORDER_SIZE / 4 + GUI.GRID_WIDTH / 4 - i * GUI.BORDER_SIZE * 0.4), player.isFirst()? GUI.BORDER_SIZE / 2: getHeight() - 3 * GUI.BORDER_SIZE / 4, GUI.BORDER_SIZE / 4, GUI.BORDER_SIZE / 4);
      
      if (!quoridor.isFinished() && quoridor.isFirst() == player.isFirst()) {
        graphics.setStroke(new BasicStroke(GUI.GRID_WIDTH / 3));
        
        graphics.drawOval(GUI.BORDER_SIZE, quoridor.isFirst()? GUI.BORDER_SIZE / 4: getHeight() - 3 * GUI.BORDER_SIZE / 4, GUI.BORDER_SIZE / 2, GUI.BORDER_SIZE / 2);
        
        if (player instanceof AI) {
          graphics.setFont(new Font(Font.SANS_SERIF, Font.BOLD, 10));
          FontMetrics metrics = graphics.getFontMetrics();
          
          graphics.drawString("AI", GUI.BORDER_SIZE + metrics.stringWidth("AI") / 3, quoridor.isFirst()? 3 * GUI.BORDER_SIZE / 4 - metrics.getHeight() / 3: getHeight() - GUI.BORDER_SIZE / 4 - metrics.getHeight() / 3);
        }
        
      }
    }
    
    if (quoridor.isFinished()) {
      graphics.setColor(new Color(GUI.BACKGROUND_COLOR.getRed(), GUI.BACKGROUND_COLOR.getGreen(), GUI.BACKGROUND_COLOR.getBlue(), 128));
      graphics.fillRect(0, 0, getWidth(), getHeight());
      
      graphics.setStroke(new BasicStroke(1.0f));
      graphics.setFont(new Font(Font.SANS_SERIF, Font.BOLD, 24));
      FontMetrics metrics = graphics.getFontMetrics();
      
      String message = quoridor.getPlayers()[quoridor.getPlayers()[0].hasWon()? 0: 1].getName() + " player won!";
      
      RoundRectangle2D rectangle = new RoundRectangle2D.Float((getWidth() - metrics.stringWidth(message)) / 2 - GUI.BORDER_SIZE, getHeight() / 2 - GUI.BORDER_SIZE, metrics.stringWidth(message) + 2 * GUI.BORDER_SIZE, metrics.getHeight() + GUI.BORDER_SIZE / 2, 10, 10);
      
      graphics.setColor(Color.WHITE);
      
          graphics.fill(rectangle);
      
          graphics.setColor(Color.BLACK);
      
          graphics.draw(rectangle);
      
      graphics.drawString(message, (getWidth() - metrics.stringWidth(message)) / 2, getHeight() / 2 - GUI.BORDER_SIZE / 2 + metrics.getHeight() / 2);
    }
  }

  public Quoridor getQuoridor() {
    return quoridor;
  }

}

class Player {
  
  private int x;
  
  private int y;
  
  private int walls;
  
  private boolean first;
  
  private String name;
  
  public Player(boolean first) {
    this(4, first? 0: 8, first);
  }
  
  public Player(int x, int y, boolean first) {
    super();
    
    this.x = x;
    this.y = y;
    this.first = first;

    resetWalls();
    name = first? "Red": "Blue";
  }
  
  public Player(Player player) {
    super();
    
    x = player.getX();
    y = player.getY();
    walls = player.getWalls();
    first = player.isFirst();
    name = player.getName();
  }

  public int getX() {
    return x;
  }

  public int getY() {
    return y;
  }

  public void setX(int x) {
    this.x = x;
  }

  public void setY(int y) {
    this.y = y;
  }
  
  public int getWalls() {
    return walls;
  }
  
  public void resetWalls() {
    walls = 15;
  }

  public void removeWall() {
    if (walls > 0)
      walls--;
  }

  public boolean isFirst() {
    return first;
  }
  
  public String getName() {
    return name;
  }

  public boolean hasWon() {
    return first && y == 8 || !first && y == 0;
  }
  
}

class Wall extends Player implements Comparable<Wall> {
  
  private boolean horizontal;

  public Wall(int x, int y, boolean first, boolean horizontal) {
    super(x, y, first);
    
    this.horizontal = horizontal;
  }

  public boolean isHorizontal() {
    return horizontal;
  }

  @Override
  public int compareTo(Wall obj) {
    return (obj.getX() + " " + obj.getY() + " " + obj.isHorizontal()).compareTo(getX() + " " + getY() + " " + isHorizontal());
  }

  @Override
  public boolean equals(Object obj) {
    if (obj instanceof Wall)
      return ((Wall)obj).getX() == getX() && ((Wall)obj).getY() == getY() && ((Wall)obj).isHorizontal() == isHorizontal();
    
    return false;
  }
  
}

class AI extends Player {

  public AI(boolean first) {
    super(first);
  }

  public AI(int x, int y, boolean first) {
    super(x, y, first);
  }
  
  public AI(Player player) {
    super(player);
  }
  
  public boolean move(Quoridor quoridor) {
    List<Move> moves = new ArrayList<Move>();
    if (getX() > 0 && (quoridor.getOther().getX() != getX() - 1 || quoridor.getOther().getY() != getY()) && !quoridor.getWalls().contains(new Wall(getX(), getY(), true, false)))
      moves.add(new Move(getX() - 1, getY()));
    if (getX() < 8 && (quoridor.getOther().getX() != getX() + 1 || quoridor.getOther().getY() != getY()) && !quoridor.getWalls().contains(new Wall(getX() + 1, getY(), true, false)))
      moves.add(new Move(getX() + 1, getY()));
    if (getY() > 0 && (quoridor.getOther().getX() != getX() || quoridor.getOther().getY() != getY() - 1) && !quoridor.getWalls().contains(new Wall(getX(), getY(), true, true)))
      moves.add(new Move(getX(), getY() - 1));
    if (getY() < 8 && (quoridor.getOther().getX() != getX() || quoridor.getOther().getY() != getY() + 1) && !quoridor.getWalls().contains(new Wall(getX(), getY() + 1, true, true)))
      moves.add(new Move(getX(), getY() + 1));
    
    if (moves.isEmpty())
      return false;
    
    Move move = moves.get((int)(Math.random() * moves.size()));
    
    setX(move.getX());
    setY(move.getY());
    
    return true;
  }
  
  public boolean wall(Quoridor quoridor) {
    List<Wall> walls = new ArrayList<Wall>();
    for (int i = 1; i < 9; i++)
      for (int j = 0; j < 9; j++)
        walls.add(new Wall(i, j, isFirst(), false));
    for (int i = 0; i < 9; i++)
      for (int j = 1; j < 9; j++)
        walls.add(new Wall(i, j, isFirst(), true));
    
    for (Iterator<Wall> iterator = walls.iterator(); iterator.hasNext(); ) {
      Wall wall = iterator.next();
      if (quoridor.getWalls().contains(wall) || !quoridor.getGraph(wall).isConnected())
        iterator.remove();
    }
    
    if (walls.isEmpty())
      return false;
    
    Wall wall = walls.get((int)(Math.random() * walls.size()));
    
    quoridor.getWalls().add(wall);
    removeWall();
    
    return true;
  }
  
}

class Move {
  
  private int x;
  
  private int y;

  public Move(int x, int y) {
    super();
    this.x = x;
    this.y = y;
  }

  public int getX() {
    return x;
  }

  public int getY() {
    return y;
  }
  
}

class Graph {

  private List<Set<Integer>> adjacency;

  public Graph() {
    super();
    
    adjacency = new ArrayList<Set<Integer>>();
    for (int i = 0; i < 81; i++)
      adjacency.add(new HashSet<Integer>());
  }
  
  public Graph(Set<Wall> walls) {
    this();
    
    for (int i = 0; i < 9; i++)
      for (int j = 0; j < 8; j++)
        if (!walls.contains(new Wall(j + 1, i, false, false)))
          addEdge(9 * i + j, 9 * i + j + 1);
  
    for (int j = 0; j < 9; j++)
      for (int i = 0; i < 8; i++)
        if (!walls.contains(new Wall(j, i + 1, false, true)))
          addEdge(9 * i + j, 9 * (i + 1) + j);
  }
  
  public void addEdge(int i, int j) {
    adjacency.get(i).add(j);
    adjacency.get(j).add(i);
  }
  
  public void removeEdge(int i, int j) {
    adjacency.get(i).remove(j);
    adjacency.get(j).remove(i);
  }
  
  public void removeEdge(Wall wall) {
    if (wall.isHorizontal())
      removeEdge(9 * (wall.getY() - 1) + wall.getX(), 9 * wall.getY() + wall.getX());
    else
      removeEdge(9 * wall.getY() + wall.getX() - 1, 9 * wall.getY() + wall.getX());
  }
  
  public Set<Integer> getNeighbors(int i) {
    return adjacency.get(i);
  }

  public List<Set<Integer>> getAdjacency() {
    return adjacency;
  }
  
  public boolean isConnected() {
    Set<Integer> nodes = new HashSet<Integer>();
    for (int i = 1; i < 81; i++)
      nodes.add(i);
    
    List<Integer> stack = new LinkedList<Integer>();
    stack.add(0);
    
    int LCC = 0;
    while (!stack.isEmpty()) {
      int i = stack.remove(0);
      for (int j: getNeighbors(i))
        if (nodes.remove(j))
          stack.add(0, j);
      
      LCC++;
    }
    
    return LCC == 81;
  }

}
```