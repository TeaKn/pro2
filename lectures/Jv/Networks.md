```java
import java.awt.BasicStroke;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.FileDialog;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.awt.geom.RoundRectangle2D;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.FilenameFilter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Set;

import javax.swing.AbstractButton;
import javax.swing.ButtonGroup;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JCheckBoxMenuItem;
import javax.swing.JComboBox;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JPanel;
import javax.swing.JRadioButtonMenuItem;
import javax.swing.JSlider;
import javax.swing.KeyStroke;
import javax.swing.UIManager;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

import de.erichseifert.vectorgraphics2d.PDFGraphics2D;

public class Networks {
  
  protected static final String ICONS_FOLDER = "icons";
  
  protected static final String NETWORKS_FOLDER = "nets";
  
  protected static final String LIBRARIES_FOLDER = "libs";
  
  protected static final List<GUI> GUIs = new ArrayList<GUI>();
  
  public static void main(String[] args) throws IOException {
    System.setProperty("apple.laf.useScreenMenuBar", "true");
    
    /* for (File file: new File(NETWORKS_FOLDER).listFiles())
      if (file.getName().endsWith(".net")) {
        GUI GUI = new GUI(file);
        GUI.setVisible(true);
     
        GUIs.add(GUI);
      } */
    
    GUI GUI = new GUI(NETWORKS_FOLDER + "/PhD.net");
    GUI.setVisible(true);

    GUIs.add(GUI);
  }
  
}

class GUI extends JFrame {
  
  private static final long serialVersionUID = 1L;
  
  private File file;
  
  private Graph graph;
  
  private Layouting layouting;
  
  private Settings settings;
  
  private ButtonGroup group;
  
  private JCheckBoxMenuItem[] checks;
  
  private Console console;
  
  private Panel panel;
  
  private Summary summary;
  
  public GUI(String file) throws IOException {
    this(new File(file));
  }
  
  public GUI(File file) throws IOException {
    this(file, Graph.read(file));
  }
  
  public GUI(File file, Graph graph) {
    this(file, graph, Layouting.LGL(graph));
  }
  
  public GUI(File file, Graph graph, Layouting layouting) {
    super();
    
    this.file = file;
    this.graph = graph;
    this.layouting = layouting;
    
    settings = new Settings();
    final GUI GUI = this;

    setTitle("Networks — " + graph.getName());
    getRootPane().putClientProperty("apple.awt.brushMetalLook", true);
    setPreferredSize(new Dimension(1024, 824));
    setMinimumSize(new Dimension(768, 600));
    setLayout(new BorderLayout());
    
    setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);

    add(console = new Console(this), BorderLayout.NORTH);
    add(panel = new Panel(this), BorderLayout.CENTER);
    add(summary = new Summary(this), BorderLayout.SOUTH);
    
    JMenuBar bar = new JMenuBar();
    setJMenuBar(bar);
    
    JMenu menu = new JMenu("File");
      bar.add(menu);
    
      JMenuItem item = new JMenuItem("New");
      item.setAccelerator(KeyStroke.getKeyStroke('N', Toolkit.getDefaultToolkit().getMenuShortcutKeyMask()));
      item.setIcon(UIManager.getIcon("FileView.fileIcon"));
      item.addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(ActionEvent e) {
        Graph graph = Graph.random(256, 2.0);
        
        GUI GUI = new GUI(new File(Networks.NETWORKS_FOLDER + "/" + graph.getName() + ".net"), graph);
        GUI.setVisible(true);
        
        Networks.GUIs.add(GUI);
      }
    });
      menu.add(item);
    
      item = new JMenuItem("Open...");
      item.setAccelerator(KeyStroke.getKeyStroke('O', Toolkit.getDefaultToolkit().getMenuShortcutKeyMask()));
      item.setIcon(UIManager.getIcon("Tree.openIcon"));
      item.addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(ActionEvent e) {
        FileDialog dialog = new FileDialog(GUI, null, FileDialog.LOAD);
          dialog.setFilenameFilter(new FilenameFilter() {
          @Override
          public boolean accept(File directory, String name) {
            return name.endsWith(".net");
          }
        });
          dialog.setDirectory(Networks.NETWORKS_FOLDER);
          dialog.setLocationRelativeTo(GUI);
          if (GUI.getFile() != null)
            dialog.setFile(GUI.getFile().getName());
          dialog.setVisible(true);
        
          String file = dialog.getFile();
          String folder = dialog.getDirectory();
          if (folder != null && file != null)
            try {
              GUI GUI = new GUI(new File(folder + file));
            GUI.setVisible(true);
            
            Networks.GUIs.add(GUI);
          } catch (IOException ex) {
          
          }
      }
    });
      menu.add(item);
    
      item = new JMenuItem("Reload");
      item.addActionListener(new ActionListener() {
        @Override
        public void actionPerformed(ActionEvent e) {
          try {
            if (GUI.getFile() != null && GUI.getFile().exists())
              GUI.graph = Graph.read(GUI.getFile());
            if (GUI.getGraph() != null)
              if (settings.getLayouting().equals(Layouts.RANDOM))
                GUI.setLayouting(new Layouting(GUI.getGraph()));
              else if (settings.getLayouting().equals(Layouts.CIRCULAR))
                GUI.setLayouting(Layouting.circular(GUI.getGraph()));
              else
                GUI.setLayouting(Layouting.LGL(GUI.getGraph()));
            GUI.repaint();
          } catch (IOException ex) {

          }
        }
    });
      menu.add(item);
    
      menu.addSeparator();
    
      item = new JMenuItem("Close");
      item.setAccelerator(KeyStroke.getKeyStroke('W', Toolkit.getDefaultToolkit().getMenuShortcutKeyMask()));
      item.addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(ActionEvent e) {
        dispose();
      }
    });
      menu.add(item);
    
      item = new JMenuItem("Close All");
      item.setAccelerator(KeyStroke.getKeyStroke('W', ActionEvent.SHIFT_MASK + Toolkit.getDefaultToolkit().getMenuShortcutKeyMask()));
      item.addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(ActionEvent e) {
        for (GUI GUI: Networks.GUIs)
          GUI.dispose();
      }
    });
      menu.add(item);
    
      menu.addSeparator();
    
      item = new JMenuItem("Save");
      item.setAccelerator(KeyStroke.getKeyStroke('S', Toolkit.getDefaultToolkit().getMenuShortcutKeyMask()));
      item.setIcon(UIManager.getIcon("FileView.hardDriveIcon"));
      item.addActionListener(new ActionListener() {
        @Override
        public void actionPerformed(ActionEvent e) {
          if (GUI.getGraph() != null && GUI.getFile() != null)
            try {
              Graph.write(GUI.getGraph(), GUI.getFile());
            } catch (IOException ex) {

            }
        }
    });
      menu.add(item);
    
      item = new JMenuItem("Save As...");
      item.addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(ActionEvent e) {
        if (GUI.getGraph() != null && GUI.getFile() != null) {
          FileDialog dialog = new FileDialog(GUI, null, FileDialog.SAVE);
          dialog.setFilenameFilter(new FilenameFilter() {
            @Override
            public boolean accept(File directory, String name) {
              return name.endsWith(".net");
            }
          });
          dialog.setDirectory(Networks.NETWORKS_FOLDER);
          dialog.setLocationRelativeTo(GUI);
          dialog.setFile(GUI.getGraph().getName() + ".txt");
          dialog.setVisible(true);

          String file = dialog.getFile();
          String folder = dialog.getDirectory();
          if (folder != null && file != null)
            try {
              Graph.write(GUI.getGraph(), folder + file);
            } catch (IOException ex) {

            }
        }
      }
    });
      menu.add(item);
    
      item = new JMenuItem("Save All");
      item.setAccelerator(KeyStroke.getKeyStroke('S', ActionEvent.SHIFT_MASK + Toolkit.getDefaultToolkit().getMenuShortcutKeyMask()));
      item.addActionListener(new ActionListener() {
        @Override
        public void actionPerformed(ActionEvent e) {
          for (GUI GUI: Networks.GUIs)
            if (GUI.getGraph() != null && GUI.getFile() != null)
              try {
                Graph.write(GUI.getGraph(), GUI.getFile());
              } catch (IOException ex) {

              }
        }
    });
      menu.add(item);
    
      menu.addSeparator();
    
      item = new JMenuItem("Export...");
      item.setIcon(new JFileChooser().getIcon(new File(Networks.ICONS_FOLDER + "/blank.pdf")));
      item.addActionListener(new ActionListener() {
        @Override
        public void actionPerformed(ActionEvent e) {
          if (GUI.getGraph() != null && GUI.getFile() != null) {
            FileDialog dialog = new FileDialog(GUI, null, FileDialog.SAVE);
            dialog.setFilenameFilter(new FilenameFilter() {
              @Override
              public boolean accept(File directory, String name) {
                return name.endsWith(".pdf");
              }
            });
            dialog.setDirectory(Networks.NETWORKS_FOLDER);
            dialog.setLocationRelativeTo(GUI);
            dialog.setFile(file.getName().replace(".net", ".pdf"));
            dialog.setVisible(true);

            String file = dialog.getFile();
            String folder = dialog.getDirectory();
            if (folder != null && file != null) {
              PDFGraphics2D graphics = new PDFGraphics2D(0, 0, panel.getWidth(), panel.getHeight());
              panel.paint(graphics);

              try {
                FileOutputStream stream = new FileOutputStream(new File(folder + file));

                stream.write(graphics.getBytes());

                stream.flush();
                stream.close();
              } catch (IOException ex) {

              }
            }
          }
        }
    });
      menu.add(item);
    
    menu = new JMenu("Graph");
      bar.add(menu);

      item = new JMenuItem("Clustering");
      item.setAccelerator(KeyStroke.getKeyStroke('C', Toolkit.getDefaultToolkit().getMenuShortcutKeyMask()));
      item.addActionListener(new ActionListener() {
        @Override
        public void actionPerformed(ActionEvent e) {
          getGraph().clustering();
          GUI.repaint();
        }
    });
      menu.add(item);
    
      menu = new JMenu("View");
      bar.add(menu);
    
      item = new JMenuItem("Relayout");
      item.setAccelerator(KeyStroke.getKeyStroke('L', Toolkit.getDefaultToolkit().getMenuShortcutKeyMask()));
      item.addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(ActionEvent e) {
        if (GUI.getSettings().getLayouting().equals(Layouts.RANDOM))
          GUI.setLayouting(new Layouting(GUI.getGraph()));
        else if (GUI.getSettings().getLayouting().equals(Layouts.CIRCULAR))
          GUI.setLayouting(Layouting.circular(GUI.getGraph()));
        else
          GUI.setLayouting(Layouting.LGL(GUI.getGraph()));
        GUI.repaint();
      }
    });
      menu.add(item);
    
      JMenu submenu = new JMenu("Layout");
    menu.add(submenu);

    group = new ButtonGroup();
    for (Layouts layouts: new Layouts[] { Layouts.SPRING, Layouts.CIRCULAR, Layouts.RANDOM }) {
      JRadioButtonMenuItem radio = new JRadioButtonMenuItem(layouts.toString(), layouts.equals(GUI.getSettings().getLayouting()));
      radio.addActionListener(new ActionListener() {
        @Override
        public void actionPerformed(ActionEvent e) {
          GUI.getSettings().setLayouting(Layouts.valueOf(radio.getText().toUpperCase()));
          console.getCombo().setSelectedItem(GUI.getSettings().getLayouting());
          if (GUI.getSettings().getLayouting().equals(Layouts.RANDOM))
            GUI.setLayouting(new Layouting(GUI.getGraph()));
          else if (GUI.getSettings().getLayouting().equals(Layouts.CIRCULAR))
            GUI.setLayouting(Layouting.circular(GUI.getGraph()));
          else
            GUI.setLayouting(Layouting.LGL(GUI.getGraph()));
          GUI.repaint();
        }
      });
      submenu.add(radio);
      group.add(radio);
    }
    
    menu.addSeparator();
    
    checks = new JCheckBoxMenuItem[3];
    checks[0] = new JCheckBoxMenuItem("Centrality", settings.isCentrality());
    checks[0].addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(ActionEvent e) {
        settings.setCentrality(checks[0].isSelected());
        console.getChecks()[0].setSelected(settings.isCentrality());
        GUI.repaint();
      }
    });
    menu.add(checks[0]);
    
    checks[1] = new JCheckBoxMenuItem("Clusters", settings.isClusters());
    checks[1].addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(ActionEvent e) {
        settings.setClusters(checks[1].isSelected());
        console.getChecks()[1].setSelected(settings.isClusters());
        GUI.repaint();
      }
    });
    menu.add(checks[1]);
    
    checks[2] = new JCheckBoxMenuItem("Labels", settings.isLabels());
    checks[2].addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(ActionEvent e) {
        settings.setLabels(checks[2].isSelected());
        console.getChecks()[2].setSelected(settings.isLabels());
        GUI.repaint();
      }
    });
    menu.add(checks[2]);
    
      bar.add(new JMenu("Help"));
    
    pack();
  }
  
  public File getFile() {
    return file;
  }
  
  public Graph getGraph() {
    return graph;
  }

  public Layouting getLayouting() {
    return layouting;
  }

  public void setLayouting(Layouting layouting) {
    this.layouting = layouting;
  }

  public Settings getSettings() {
    return settings;
  }

  public ButtonGroup getGroup() {
    return group;
  }

  public JCheckBoxMenuItem[] getChecks() {
    return checks;
  }

  public Console getConsole() {
    return console;
  }

  public Panel getPanel() {
    return panel;
  }
  
  public Summary getSummary() {
    return summary;
  }

}

class Console extends JPanel {
  
  private static final long serialVersionUID = 1L;
  
  protected static final int CONSOLE_SIZE = 64;
  
  protected static final int CONTROL_SIZE = 48;
  
  private JComboBox<Layouts> combo;
  
  private JCheckBox[] checks;
  
  private GUI GUI;
  
  public Console(GUI GUI) {
    super();
    this.GUI = GUI;
    
    setFocusable(false);
    setPreferredSize(new Dimension(getWidth(), CONSOLE_SIZE));
    
    combo = new JComboBox<Layouts>(new Layouts[] { Layouts.SPRING, Layouts.CIRCULAR, Layouts.RANDOM });
    combo.setToolTipText("Select network layout");
    combo.setSelectedItem(GUI.getSettings().getLayouting());
    combo.setPreferredSize(new Dimension((int)Math.round(2.25 * CONTROL_SIZE), CONTROL_SIZE));
    combo.addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(ActionEvent e) {
        GUI.getSettings().setLayouting((Layouts)combo.getSelectedItem());
        Enumeration<AbstractButton> buttons = GUI.getGroup().getElements();
        while (buttons.hasMoreElements()) {
          AbstractButton button = buttons.nextElement();
          if (button.getText().equals(GUI.getSettings().getLayouting().toString())) {
            button.setSelected(true);
            break;
          }
        }
        if (GUI.getSettings().getLayouting().equals(Layouts.RANDOM))
          GUI.setLayouting(new Layouting(GUI.getGraph()));
        else if (GUI.getSettings().getLayouting().equals(Layouts.CIRCULAR))
          GUI.setLayouting(Layouting.circular(GUI.getGraph()));
        else
          GUI.setLayouting(Layouting.LGL(GUI.getGraph()));
        GUI.repaint();
      }
    });
    add(combo);
    
    JButton button = new JButton(new ImageIcon(Networks.ICONS_FOLDER + "/layout.png"));
    button.setToolTipText("Compute network layout");
    button.setPreferredSize(new Dimension(CONTROL_SIZE, CONTROL_SIZE));
    button.addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(ActionEvent e) {
        if (GUI.getSettings().getLayouting().equals(Layouts.RANDOM))
          GUI.setLayouting(new Layouting(GUI.getGraph()));
        else if (GUI.getSettings().getLayouting().equals(Layouts.CIRCULAR))
          GUI.setLayouting(Layouting.circular(GUI.getGraph()));
        else
          GUI.setLayouting(Layouting.LGL(GUI.getGraph()));
        GUI.repaint();
      }
    });
    add(button);
    
    button = new JButton(new ImageIcon(Networks.ICONS_FOLDER + "/clusters.png"));
    button.setToolTipText("Compute network clustering");
    button.setPreferredSize(new Dimension(CONTROL_SIZE, CONTROL_SIZE));
    button.addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(ActionEvent e) {
        GUI.getGraph().clustering();
        GUI.repaint();
      }
    });
    add(button);
    
    add(new JLabel("    "));
    
    checks = new JCheckBox[3];
    checks[0] = new JCheckBox("Centrality");
    checks[0].setToolTipText("Show node centrality");
    checks[0].addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(ActionEvent e) {
        GUI.getSettings().setCentrality(((JCheckBox)e.getSource()).isSelected());
        GUI.getChecks()[0].setSelected(GUI.getSettings().isCentrality());
        GUI.repaint();
      }
    });
    checks[0].setSelected(GUI.getSettings().isCentrality());
    add(checks[0]);
    
    JSlider slider = new JSlider(8, 32, GUI.getSettings().getNodes());
    slider.setToolTipText("Set node size");
    slider.setPreferredSize(new Dimension((int)Math.round(2.5 * CONTROL_SIZE), CONTROL_SIZE));
    slider.addChangeListener(new ChangeListener() {
      @Override
      public void stateChanged(ChangeEvent e) {
        GUI.getSettings().setNodes(((JSlider)e.getSource()).getValue());
        GUI.repaint();
      }
    });
    add(slider);
    
    checks[1] = new JCheckBox("Clusters");
    checks[1].setToolTipText("Show node clusters");
    checks[1].addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(ActionEvent e) {
        GUI.getSettings().setClusters(((JCheckBox)e.getSource()).isSelected());
        GUI.getChecks()[1].setSelected(GUI.getSettings().isClusters());
        GUI.repaint();
      }
    });
    checks[1].setSelected(GUI.getSettings().isClusters());
    add(checks[1]);
    
    checks[2] = new JCheckBox("Labels");
    checks[2].setToolTipText("Show node labels");
    checks[2].addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(ActionEvent e) {
        GUI.getSettings().setLabels(((JCheckBox)e.getSource()).isSelected());
        GUI.getChecks()[2].setSelected(GUI.getSettings().isLabels());
        GUI.repaint();
      }
    });
    checks[2].setSelected(GUI.getSettings().isLabels());
    add(checks[2]);
    
    slider = new JSlider(1, 32, GUI.getSettings().getTexts());
    slider.setToolTipText("Set label size");
    slider.setPreferredSize(new Dimension((int)Math.round(2.5 * CONTROL_SIZE), CONTROL_SIZE));
    slider.addChangeListener(new ChangeListener() {
      @Override
      public void stateChanged(ChangeEvent e) {
        GUI.getSettings().setTexts(((JSlider)e.getSource()).getValue());
        GUI.repaint();
      }
    });
    add(slider);
  }
  
  public JComboBox<Layouts> getCombo() {
    return combo;
  }

  public JCheckBox[] getChecks() {
    return checks;
  }

  public GUI getGUI() {
    return GUI;
  }

}

class Panel extends JPanel {
  
  private static final long serialVersionUID = 1L;
  
  protected static final Color[] NODE_COLORS = new Color[] { new Color(211, 211, 211), new Color(76, 187, 23), new Color(93, 33, 120), new Color(76, 128, 155), new Color(128, 128, 128) };
  
  protected static final Color EDGE_COLOR = new Color(96, 96, 96);
  
  protected static final Color LABEL_COLOR = Color.BLACK;
  
  protected static final int BORDER_SIZE = 32;
  
  private GUI GUI;
  
  private int selected;
  
  public Panel(GUI GUI) {
    super();
    this.GUI = GUI;
    
    selected = -1;
    
    setBackground(Color.WHITE);
    
    addMouseListener(new MouseListener() {
      
      @Override
      public void mouseReleased(MouseEvent e) {
        selected = -1;
      }
      
      @Override
      public void mousePressed(MouseEvent e) {
        for (int node: GUI.getGraph().getNodes()) {
          int size = GUI.getSettings().getNodes();
          if (GUI.getSettings().isCentrality())
            size = (int)Math.round(4 + 0.25 * size * Math.pow(Math.min(GUI.getGraph().getDegree(node), 12), 0.75));
          if (Math.sqrt(Math.pow(BORDER_SIZE + GUI.getLayouting().getX(node) * (getWidth() - 2 * BORDER_SIZE) - e.getX(), 2.0) + Math.pow(BORDER_SIZE + GUI.getLayouting().getY(node) * (getHeight() - 2 * BORDER_SIZE) - e.getY(), 2.0)) <= size / 2)
            selected = node;
        }
      }
      
      @Override
      public void mouseExited(MouseEvent e) {
        
      }
      
      @Override
      public void mouseEntered(MouseEvent e) {
        
      }
      
      @Override
      public void mouseClicked(MouseEvent e) {
        
      }
      
    });
    
    addMouseMotionListener(new MouseMotionListener() {
      
      @Override
      public void mouseMoved(MouseEvent e) {
        
      }
      
      @Override
      public void mouseDragged(MouseEvent e) {
        if (selected != -1)
          GUI.getLayouting().setPoint(selected, new Point(Math.min(1.0, Math.max(0.0, 1.0 * (e.getX() - BORDER_SIZE) / (getWidth() - 2 * BORDER_SIZE))), Math.min(1.0, Math.max(0.0, 1.0 * (e.getY() - BORDER_SIZE) / (getHeight() - 2 * BORDER_SIZE)))));
        GUI.repaint();
      }
      
    });
  }

  @Override
  public void paint(Graphics g) {
    super.paint(g);
    
    int width = getWidth() - 2 * BORDER_SIZE;
    int height = getHeight() - 2 * BORDER_SIZE;
    
    Graphics2D graphics = (Graphics2D)g;
    
    graphics.setColor(EDGE_COLOR);
    graphics.setStroke(new BasicStroke(2.0f));
    
    for (Edge edge: GUI.getGraph().getEdges())
      if (GUI.getLayouting().getX(edge.getSource()) >= 0.0 && GUI.getLayouting().getY(edge.getSource()) >= 0.0 && GUI.getLayouting().getX(edge.getTarget()) >= 0.0 && GUI.getLayouting().getY(edge.getTarget()) >= 0.0)
        graphics.drawLine((int)Math.round(BORDER_SIZE + GUI.getLayouting().getX(edge.getSource()) * width), (int)Math.round(BORDER_SIZE + GUI.getLayouting().getY(edge.getSource()) * height), (int)Math.round(BORDER_SIZE + GUI.getLayouting().getX(edge.getTarget()) * width), (int)Math.round(BORDER_SIZE + GUI.getLayouting().getY(edge.getTarget()) * height));

    for (int node: GUI.getGraph().getNodes())
      if (GUI.getLayouting().getX(node) >= 0.0 && GUI.getLayouting().getY(node) >= 0.0) {
        int size = GUI.getSettings().getNodes();
        if (GUI.getSettings().isCentrality())
          size = (int)Math.round(4 + 0.25 * size * Math.pow(Math.min(GUI.getGraph().getDegree(node), 12), 0.75));

        graphics.setColor(NODE_COLORS[GUI.getSettings().isClusters()? GUI.getGraph().getCluster(node) % NODE_COLORS.length: 0]);
        graphics.setStroke(new BasicStroke(1.0f));

        graphics.fillOval((int)Math.round(BORDER_SIZE + GUI.getLayouting().getX(node) * width - size / 2), (int)Math.round(BORDER_SIZE + GUI.getLayouting().getY(node) * height - size / 2), size, size);

        graphics.setColor(EDGE_COLOR);
        graphics.setStroke(new BasicStroke(2.0f));

        graphics.drawOval((int)Math.round(BORDER_SIZE + GUI.getLayouting().getX(node) * width - size / 2), (int)Math.round(BORDER_SIZE + GUI.getLayouting().getY(node) * height - size / 2), size, size);
      }
    
    if (GUI.getSettings().isLabels()) {
      graphics.setColor(LABEL_COLOR);
      graphics.setStroke(new BasicStroke(1.0f));
      graphics.setFont(new Font(Font.SANS_SERIF, Font.BOLD, GUI.getSettings().getTexts()));
      FontMetrics metrics = graphics.getFontMetrics();
      
      for (int node: GUI.getGraph().getNodes())
        if (GUI.getLayouting().getX(node) >= 0.0 && GUI.getLayouting().getY(node) >= 0.0)
          graphics.drawString(GUI.getGraph().getLabel(node), (int)Math.round(BORDER_SIZE + GUI.getLayouting().getX(node) * width - metrics.stringWidth(GUI.getGraph().getLabel(node)) / 2), (int)Math.round(BORDER_SIZE + GUI.getLayouting().getY(node) * height + metrics.getAscent() / 2));
    }
  }
  
  public GUI getGUI() {
    return GUI;
  }
  

  public int getSelected() {
    return selected;
  }
  
}

class Summary extends JPanel {
  
  private static final long serialVersionUID = 1L;
  
  protected static final int SUMMARY_HEIGHT = 92;
  
  protected static final int BORDER_SIZE = 16;
  
  private GUI GUI;

  public Summary(GUI GUI) {
    super();
    
    this.GUI = GUI;
    
    setFocusable(false);
    setPreferredSize(new Dimension(getWidth(), SUMMARY_HEIGHT));
  }

  @Override
  public void paint(Graphics g) {
    super.paint(g);
    
    Graphics2D graphics = (Graphics2D)g;

    RoundRectangle2D rectangle = new RoundRectangle2D.Float(getWidth() / 2 - 152, BORDER_SIZE, 304, getHeight() - 2 * BORDER_SIZE, 10, 10);
    
    graphics.setColor(new Color(246, 246, 246));
    
        graphics.fill(rectangle);
    
        graphics.setColor(Color.BLACK);
    
        graphics.draw(rectangle);
    
    graphics.setColor(Color.BLACK);
    graphics.setStroke(new BasicStroke(1.0f));
    
    graphics.setFont(new Font(Font.SANS_SERIF, Font.BOLD, 12));
    FontMetrics metrics = graphics.getFontMetrics();
    
    int y = (getHeight() - 3 * metrics.getHeight()) / 2 + 3 * metrics.getHeight() / 4;
    
    graphics.drawString("Network: ", getWidth() / 2 - 72 - metrics.stringWidth("Network: "), y);
    graphics.drawString("Nodes: ", getWidth() / 2 - 72 - metrics.stringWidth("Nodes: "), y + metrics.getHeight());
    graphics.drawString("Edges: ", getWidth() / 2 - 72 - metrics.stringWidth("Edges: "), y + 2 * metrics.getHeight());

    graphics.drawString("Degree: ", getWidth() / 2 + 72 - metrics.stringWidth("Degree: "), y);
    graphics.drawString("Clusters: ", getWidth() / 2 + 72 - metrics.stringWidth("Clusters: "), y + metrics.getHeight());
    graphics.drawString("WCCs: ", getWidth() / 2 + 72 - metrics.stringWidth("WCCs: "), y + 2 * metrics.getHeight());

    graphics.setFont(new Font(Font.SANS_SERIF, Font.PLAIN, 12));
    metrics = graphics.getFontMetrics();
    
    graphics.drawString("\"" + GUI.getGraph().getName() + "\"", getWidth() / 2 - 72, y);
    graphics.drawString(String.format("%,d (%,d)", GUI.getGraph().getN(), GUI.getGraph().getI()), getWidth() / 2 - 72, y + metrics.getHeight());
    graphics.drawString(String.format("%,d (%,d)", GUI.getGraph().getM(), GUI.getGraph().getL()), getWidth() / 2 - 72, y + 2 * metrics.getHeight());
    
    graphics.drawString(String.format("%.1f (%,d)", GUI.getGraph().getK(), GUI.getGraph().getD()), getWidth() / 2 + 72, y);
    
    Map<Integer, Integer> clustering = GUI.getGraph().getClustering();
    int cluster = 0;
    for (int size: clustering.values())
      if (size > cluster)
        cluster = size;
    
    graphics.drawString(String.format("%,d (%.0f%%)", clustering.size(), 100.0 * cluster / GUI.getGraph().getN()), getWidth() / 2 + 72, y + metrics.getHeight());
    
    List<Integer> components = Graph.components(GUI.getGraph());
    int component = 0;
    for (int size: components)
      if (size > component)
        component = size;
    
    graphics.drawString(String.format("%,d (%.0f%%)", components.size(), 100.0 * component / GUI.getGraph().getN()), getWidth() / 2 + 72, y + 2 * metrics.getHeight());
  }

  public GUI getGUI() {
    return GUI;
  }

}

class Graph {
  
  private int m;
  
  private String name;
  
  private Map<Integer, String> labels;
  
  private Map<Integer, Integer> clusters;
  
  private Map<Integer, Set<Integer>> successors;
  
  private Map<Integer, Set<Integer>> predecessors;

  public Graph(String name) {
    super();
    this.name = name;
    
    m = 0;
    labels = new HashMap<Integer, String>();
    clusters = new HashMap<Integer, Integer>();
    successors = new HashMap<Integer, Set<Integer>>();
    predecessors = new HashMap<Integer, Set<Integer>>();
  }
  
  public boolean isNode(int node) {
    return labels.containsKey(node);
  }
  
  public boolean addNode(int node) {
    return addNode(node, "" + node);
  }
  
  public boolean addNode(int node, int cluster) {
    return addNode(node, "" + node, cluster);
  }
  
  public boolean addNode(int node, String label) {
    return addNode(node, label, 1);
  }
  
  public boolean addNode(int node, String label, int cluster) {
    if (isNode(node))
      return false;

    labels.put(node, label);
    clusters.put(node, cluster);
    predecessors.put(node, new HashSet<Integer>());
    successors.put(node, new HashSet<Integer>());
    
    return true;
  }
  
  public boolean isEdge(Edge edge) {
    return isEdge(edge.getSource(), edge.getTarget());
  }
  
  public boolean addEdge(Edge edge) {
    return addEdge(edge.getSource(), edge.getTarget());
  }
  
  public boolean isEdge(int source, int target) {
    if (!isNode(source) || !isNode(target))
      return false;
    
    return successors.get(source).contains(target);
  }
  
  public boolean addEdge(int source, int target) {
    if (isEdge(source, target))
      return false;
    
    if (!isNode(source))
      throw new IllegalArgumentException("Node " + source + " does not exist");
    
    if (!isNode(target))
      throw new IllegalArgumentException("Node " + target + " does not exist");
    
    m++;
    successors.get(source).add(target);
    predecessors.get(target).add(source);
    
    return true;
  }
  
  public Set<Integer> getSuccessors(int source) {
    if (!isNode(source))
      throw new IllegalArgumentException("Node " + source + " does not exist");
    
    return successors.get(source);
  }
  
  public Set<Integer> getPredecessors(int target) {
    if (!isNode(target))
      throw new IllegalArgumentException("Node " + target + " does not exist");
    
    return predecessors.get(target);
  }
  
  public Set<Integer> getNeighbors(int node) {
    Set<Integer> neighbors = new HashSet<Integer>(getSuccessors(node));
    neighbors.addAll(getPredecessors(node));
    
    return neighbors;
  }
  
  public Set<Integer> getNodes() {
    return labels.keySet();
  }
  
  public Set<Edge> getEdges() {
    Set<Edge> edges = new HashSet<Edge>();
    for (int node: getNodes())
      for (int neighbor: getNeighbors(node))
        edges.add(new Edge(node, neighbor));
    return edges;
  }
  
  public int getOutDegree(int source) {
    return getSuccessors(source).size();
  }
  
  public int getInDegree(int target) {
    return getPredecessors(target).size();
  }
  
  public int getDegree(int node) {
    return getInDegree(node) + getOutDegree(node);
  }
  
  public int getCluster(int node) {
    if (!isNode(node))
      throw new IllegalArgumentException("Node " + node + " does not exist");
    
    return clusters.get(node);
  }
  
  public void setCluster(int node, int cluster) {
    if (!isNode(node))
      throw new IllegalArgumentException("Node " + node + " does not exist");
    
    clusters.put(node, cluster);
  }
  
  public String getLabel(int node) {
    if (!isNode(node))
      throw new IllegalArgumentException("Node " + node + " does not exist");
    
    return labels.get(node);
  }
  
  public String getName() {
    return name;
  }
  
  public double getK() {
    return 2.0 * getM() / getN();
  }
  
  public int getD() {
    int d = 0;
    for (int node: getNodes())
      if (getDegree(node) > d)
        d = getDegree(node);
    return d;
  }
  
  public int getI() {
    int i = 0;
    for (int node: getNodes())
      if (getDegree(node) == 0)
        i++;
    return i;
  }
  
  public int getL() {
    int l = 0;
    for (int node: getNodes())
      for (int neighbor: getNeighbors(node))
      if (node == neighbor)
        l++;
    return l / 2;
  }
  
  public int getN() {
    return labels.size();
  }
  
  public int getM() {
    return m;
  }
  
  public void clustering() {
    List<Integer> nodes = new ArrayList<Integer>(getNodes());
    Map<Integer, Integer> clustering = new HashMap<Integer, Integer>();
    for (int node: nodes)
      clustering.put(node, node);

    boolean changed = true;
    while (changed) {
      changed = false;
      Collections.shuffle(nodes);
      for (int node: nodes) {
        Map<Integer, Integer> clusters = new HashMap<Integer, Integer>();
        for (int neighbor: getNeighbors(node)) {
          if (!clusters.containsKey(clustering.get(neighbor)))
            clusters.put(clustering.get(neighbor), 0);
          clusters.put(clustering.get(neighbor), clusters.get(clustering.get(neighbor)) + getDegree(neighbor));
        }
        if (clusters.size() > 0) {
          int cluster = clusters.keySet().iterator().next();
          for (int candidate: clusters.keySet())
            if (clusters.get(candidate) > clusters.get(cluster))
              cluster = candidate;
          if (clustering.get(node) != cluster) {
            clustering.put(node, cluster);
            changed = true;
          }
        }
      }
    }
    
    Map<Integer, Integer> sizes = new HashMap<Integer, Integer>();
    for (int node: nodes) {
      if (!sizes.containsKey(clustering.get(node)))
        sizes.put(clustering.get(node), 0);
      sizes.put(clustering.get(node), sizes.get(clustering.get(node)) + 1);
    }
    List<Integer> clusters = new ArrayList<Integer>(sizes.keySet());
    Collections.sort(clusters, new Comparator<Integer>() {
      @Override
      public int compare(Integer first, Integer second) {
        return -sizes.get(first).compareTo(sizes.get(second));
      }
    });
    
    Map<Integer, Integer> mapping = new HashMap<Integer, Integer>();
    for (int i = 0; i < clusters.size(); i++)
      mapping.put(clusters.get(i), i + 1);
    for (int node: nodes)
      setCluster(node, mapping.get(clustering.get(node)));
  }
  
  public Map<Integer, Integer> getClustering() {
    Map<Integer, Integer> clustering = new HashMap<Integer, Integer>();
    for (int node: clusters.keySet()) {
      if (!clustering.containsKey(clusters.get(node)))
        clustering.put(clusters.get(node), 0);
      clustering.put(clusters.get(node), clustering.get(clusters.get(node)) + 1);
    }
    return clustering;
  }
  
  @Override
  public String toString() {
    return String.format("%12s | %s\n%12s | %,d (%,d)\n%12s | %,d (%,d)\n%12s | %.4f\n",
      "Graph", "'" + getName() + "'", "Nodes", getN(), getI(), "Edges", getM(), getL(), "Degree", getK());
  }

  public static Graph read(String file) throws IOException {
    return read(new File(file));
  }
  
  public static Graph read(File file) throws IOException {
    Graph graph = new Graph(file.getName().split("\\.")[0]);
    
    BufferedReader reader = new BufferedReader(new FileReader(file));
    
    String line = reader.readLine();
    while ((line = reader.readLine()) != null) {
      if (line.startsWith("*edges") || line.startsWith("*arcs"))
        break;
      
      String[] array = line.split("\"");
      if (array.length > 2)
        graph.addNode(Integer.parseInt(line.split(" ")[0]), array[1], Integer.parseInt(array[2].trim()));
      else
        graph.addNode(Integer.parseInt(line.split(" ")[0]), array[1]);
    }
    
    while ((line = reader.readLine()) != null) {
      String[] nodes = line.split(" ");
      graph.addEdge(Integer.parseInt(nodes[0]), Integer.parseInt(nodes[1]));
    }
    
    reader.close();
    
    return graph;
  }
  
  public static void write(Graph graph, String file) throws IOException {
    write(graph, new File(file));
  }
  
  public static void write(Graph graph, File file) throws IOException {
    List<Integer> nodes = new ArrayList<Integer>(graph.getNodes());
    Collections.sort(nodes);
    
    BufferedWriter writer = new BufferedWriter(new FileWriter(file));
    
    writer.write("*vertices " + graph.getN() + "\n");
    for (int node: nodes)
      writer.write(node + " \"" + graph.getLabel(node) + "\" " + graph.getCluster(node) + "\n");
    
    writer.write("*arcs " + graph.getM() + "\n");
    for (int source: nodes)
      for (int target: graph.getSuccessors(source))
        writer.write(source + " " + target + "\n");
    
    writer.flush();
    writer.close();
  }

  public static Graph random(int nodes, double degree) {
    Graph graph = new Graph("Random");
    for (int i = 0; i < nodes; i++)
      graph.addNode(i + 1, (int)(3.0 * Math.random()));
    
    for (int i = 0; i < nodes; i++)
      for (int j = i + 1; j < nodes; j++)
        if (Math.random() < degree / (nodes - 1))
          graph.addEdge(i + 1, j + 1);
    
    return graph;
  }
  
  public static int component(Graph graph, Set<Integer> nodes, int node) {
    List<Integer> stack = new LinkedList<Integer>();
    stack.add(node); nodes.remove(node);
    int component = 0;
    while (!stack.isEmpty()) {
      node = stack.remove(0);
      for (int neighbor: graph.getNeighbors(node))
        if (nodes.remove(neighbor))
          stack.add(0, neighbor);
      component++;
    }
    return component;
  }
  
  public static List<Integer> components(Graph graph) {
    List<Integer> components = new ArrayList<Integer>();
    Set<Integer> nodes = new HashSet<Integer>(graph.getNodes());
    while (!nodes.isEmpty())
      components.add(component(graph, nodes, nodes.iterator().next()));
    return components;
  }
  
}

class Edge {
  
  private int source;
  
  private int target;

  public Edge(int source, int target) {
    super();
    this.source = source;
    this.target = target;
  }

  public int getSource() {
    return source;
  }

  public int getTarget() {
    return target;
  }
  
}

class Layouting {
  
  private Map<Integer, Point> layouting;
  
  public Layouting(Graph graph) {
    super();
    
    layouting = new HashMap<Integer, Point>();
    for (int node: graph.getNodes())
      layouting.put(node, new Point());
  }
  
  public void setPoint(int node, Point point) {
    if (!layouting.containsKey(node))
      throw new IllegalArgumentException("Node " + node + " does not exist");
    
    layouting.put(node, point);
  }
  
  public Point getPoint(int node) {
    if (!layouting.containsKey(node))
      throw new IllegalArgumentException("Node " + node + " does not exist");
    
    return layouting.get(node);
  }
  
  public double getX(int node) {
    return getPoint(node).getX();
  }
  
  public double getY(int node) {
    return getPoint(node).getY();
  }

  public Map<Integer, Point> getLayouting() {
    return layouting;
  }
  
  public static Layouting circular(Graph graph) {
    List<Integer> nodes = new ArrayList<Integer>(graph.getNodes());
    Collections.shuffle(nodes);
    
    Layouting layouting = new Layouting(graph);
    for (int i = 0; i < nodes.size(); i++)
      layouting.setPoint(nodes.get(i), new Point(0.5 + 0.5 * Math.cos(2.0 * i * Math.PI / graph.getN()), 0.5 + 0.5 * Math.sin(2.0 * i * Math.PI / graph.getN())));
    
    return layouting;
  }
  
  public static Layouting LGL(Graph graph) {
    try {
      long timestamp = System.currentTimeMillis();
      
      Files.copy(new File(Networks.LIBRARIES_FOLDER + "/LGL/lgl.pl").toPath(), new File("lgl.pl").toPath(), StandardCopyOption.COPY_ATTRIBUTES, StandardCopyOption.REPLACE_EXISTING);
      Files.copy(new File(Networks.LIBRARIES_FOLDER + "/LGL/LGLFormatHandler.pm").toPath(), new File("LGLFormatHandler.pm").toPath(), StandardCopyOption.COPY_ATTRIBUTES, StandardCopyOption.REPLACE_EXISTING);
      Files.copy(new File(Networks.LIBRARIES_FOLDER + "/LGL/ParseConfigFile.pm").toPath(), new File("ParseConfigFile.pm").toPath(), StandardCopyOption.COPY_ATTRIBUTES, StandardCopyOption.REPLACE_EXISTING);
      Files.copy(new File(Networks.LIBRARIES_FOLDER + "/LGL/lglbreakup").toPath(), new File("lglbreakup").toPath(), StandardCopyOption.COPY_ATTRIBUTES, StandardCopyOption.REPLACE_EXISTING);
      Files.copy(new File(Networks.LIBRARIES_FOLDER + "/LGL/lglayout2D").toPath(), new File("lglayout2D").toPath(), StandardCopyOption.COPY_ATTRIBUTES, StandardCopyOption.REPLACE_EXISTING);
      Files.copy(new File(Networks.LIBRARIES_FOLDER + "/LGL/lglrebuild").toPath(), new File("lglrebuild").toPath(), StandardCopyOption.COPY_ATTRIBUTES, StandardCopyOption.REPLACE_EXISTING);
      
      BufferedWriter writer = new BufferedWriter(new FileWriter("configuration"));
      
      writer.write("tmpdir = '" + new File(".").getAbsolutePath() + "'\n");
      writer.write("inputfile = '" + new File(timestamp + ".ncol").getAbsolutePath() + "'\n");
      writer.write("finaloutcoords = '" + timestamp + ".coords'\n"); writer.write("treelayout = '0'\n"); writer.write("useoriginalweights = '0'\n");
      writer.write("edgelevelmap = '0'\n"); writer.write("outputmst = '0'\n"); writer.write("threadcount = '1'\n"); writer.write("dimension = '2'\n");
      writer.write("cutoff = ''\n"); writer.write("usemst = '0'\n"); writer.write("issilent = '1'\n"); writer.write("pickupdir = ''\n");
      writer.write("integratetype = ''\n"); writer.write("placmentdistance = ''\n"); writer.write("placementradius = ''\n"); writer.write("placeleafsclose = '0'\n");
      
      writer.flush(); writer.close();
      
      writer = new BufferedWriter(new FileWriter(timestamp + ".ncol"));
      
      for (Edge edge: graph.getEdges())
        if (edge.getSource() < edge.getTarget())
          writer.write(edge.getSource() + " " + edge.getTarget() + "\n");
      
      writer.flush(); writer.close();
  
      long tic = new File(timestamp + ".ncol").lastModified();
      
      Runtime.getRuntime().exec("./lgl.pl -c configuration");
  
      File output = new File(timestamp + ".coords");
      while (!output.canRead() || output.lastModified() < tic)
        Thread.sleep(100L);
      
      Layouting layouting = new Layouting(graph);
      Pair minimums = new Pair(Double.MAX_VALUE, Double.MAX_VALUE);
      Pair maximums = new Pair(-Double.MAX_VALUE, -Double.MAX_VALUE);
  
      BufferedReader reader = new BufferedReader(new FileReader(output));
      
      String line;
      while ((line = reader.readLine()) != null) {
        String[] array = line.split(" ");
        
        Point point = new Point(Double.parseDouble(array[1]), Double.parseDouble(array[2]));
        layouting.setPoint(Integer.parseInt(array[0]), point);
        
        if (point.getX() < minimums.getFirst())
          minimums.setFirst(point.getX());
        if (point.getY() < minimums.getSecond())
          minimums.setSecond(point.getY());
        
        if (point.getX() > maximums.getFirst())
          maximums.setFirst(point.getX());
        if (point.getY() > maximums.getSecond())
          maximums.setSecond(point.getY());
      }
  
      for (int node: graph.getNodes())
        layouting.setPoint(node, new Point((layouting.getX(node) - minimums.getFirst()) / (maximums.getFirst() - minimums.getFirst()), (layouting.getY(node) - minimums.getSecond()) / (maximums.getSecond() - minimums.getSecond())));
      
      reader.close();
  
      new File("lgl.pl").delete(); new File("LGLFormatHandler.pm").delete(); new File("ParseConfigFile.pm").delete();
      new File("lglbreakup").delete(); new File("lglayout2D").delete(); new File("lglrebuild").delete(); new File("configuration").delete();
      
      new File("coordFileList").delete(); new File(timestamp + ".lgl").delete();
      new File(timestamp + ".ncol").delete(); new File(timestamp + ".coords").delete();
  
      for (File file: new File(".").listFiles())
        if (file.isFile() && file.getName().endsWith("_new_lgl.lgl"))
          timestamp = Long.parseLong(file.getName().substring(0, file.getName().indexOf("_new_lgl.lgl")));
  
      new File(timestamp + "_new_lgl.lgl").delete(); new File(timestamp + "_vertex_file_match").delete();
  
      File folder = new File("" + timestamp);
      if (folder.isDirectory())
        for (File file : folder.listFiles())
          file.delete();
      folder.delete();
      
      for (int node: graph.getNodes())
        if (layouting.getPoint(node).getX() < 0 || layouting.getPoint(node).getX() > 1 || layouting.getPoint(node).getY() < 0 || layouting.getPoint(node).getY() > 1)
          layouting.setPoint(node, new Point());
  
      return layouting;
    } catch (Exception e) {
      return new Layouting(graph);
    }
  }
  
}

class Point {
  
  protected double x;
  
  protected double y;
  
  public Point() {
    this(Math.random(), Math.random());
  }

  public Point(double x, double y) {
    super();
    this.x = x;
    this.y = y;
  }

  public double getX() {
    return x;
  }

  public double getY() {
    return y;
  }
  
}

class Pair extends Point {

  public Pair(double first, double second) {
    super(first, second);
  }
  
  public double getFirst() {
    return getX();
  }
  
  public double getSecond() {
    return getY();
  }
  
  public void setFirst(double first) {
    x = first;
  }
  
  public void setSecond(double second) {
    y = second;
  }
  
}

class Settings {
  
  private Layouts layouting;
  
  private boolean centrality;
  
  private boolean clusters;
  
  private boolean labels;
  
  private int nodes;
  
  private int texts;
  
  public Settings() {
    this(Layouts.SPRING, true, true, false, 15, 6);
  }

  public Settings(Layouts layouting, boolean centrality, boolean clusters, boolean labels, int nodes, int texts) {
    super();
    this.layouting = layouting;
    this.centrality = centrality;
    this.clusters = clusters;
    this.labels = labels;
    this.nodes = nodes;
    this.texts = texts;
  }

  public Layouts getLayouting() {
    return layouting;
  }

  public void setLayouting(Layouts layouting) {
    this.layouting = layouting;
  }

  public boolean isCentrality() {
    return centrality;
  }

  public void setCentrality(boolean centrality) {
    this.centrality = centrality;
  }

  public boolean isClusters() {
    return clusters;
  }

  public void setClusters(boolean clusters) {
    this.clusters = clusters;
  }

  public boolean isLabels() {
    return labels;
  }

  public void setLabels(boolean labels) {
    this.labels = labels;
  }

  public int getNodes() {
    return nodes;
  }

  public void setNodes(int nodes) {
    this.nodes = nodes;
  }

  public int getTexts() {
    return texts;
  }

  public void setTexts(int texts) {
    this.texts = texts;
  }
  
}

enum Layouts {
  SPRING,
  CIRCULAR,
  RANDOM;

  @Override
  public String toString() {
    return super.toString().substring(0, 1) + super.toString().substring(1).toLowerCase();
  }

}
```