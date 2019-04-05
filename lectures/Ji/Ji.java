import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Ji {

  public static void main(String[] args) {
    int board = args.length > 0? Integer.parseInt(args[0]): 24;
    int pacmans = args.length > 1? Integer.parseInt(args[1]): 6;
    
    try {
      new Pacmans(board, pacmans).playPacmans();
    } catch (InterruptedException e) {
      e.printStackTrace();
    }
  }

}

class Position {
  
  private int x;
  
  private int y;

  public Position(int x, int y) {
    this.x = x;
    this.y = y;
  }

  public int getX() {
    return x;
  }

  public int getY() {
    return y;
  }

  public Position movePosition(int x, int y) {
    return new Position(getX() + x, getY() + y);
  }
  
  public double computeDistance(int x, int y) {
    return Math.sqrt(Math.pow(getX() - x, 2.0) + Math.pow(getY() - y, 2.0));
  }
  
  public static Position randomPosition(Board board) {
    Position position = new Position((int)(Math.random() * board.getWidth()), (int)(Math.random() * board.getHeight()));
    while (board.getCell(position) != null)
      position = new Position((int)(Math.random() * board.getWidth()), (int)(Math.random() * board.getHeight()));
    
    return position;
  }
  
}

class Cell {
  
  private Position position;
  
  private int value;
  
  private char label;
  
  private boolean occupiable;

  public Cell(Position position, int value, char label, boolean occupiable) {
    this.position = position;
    this.value = value;
    this.label = label;
    this.occupiable = occupiable;
  }

  public Position getPosition() {
    return position;
  }

  public void setPosition(Position position) {
    this.position = position;
  }

  public int getValue() {
    return value;
  }

  public char getLabel() {
    return label;
  }

  public boolean isOccupiable() {
    return occupiable;
  }

  @Override
  public String toString() {
    return "" + getLabel();
  }

  public static Cell randomCell(Position position) {
    double random = Math.random();
    if (random < Pacmans.COINS_PROBABILITY)
      return Coin.randomCoin(position);
    else if (random < Pacmans.COINS_PROBABILITY + Pacmans.BLOCKS_PROBABILITY)
      return new Block(position);
    else
      return new Empty(position);
  }
  
}

class Empty extends Cell {

  public Empty(Position position) {
    super(position, 0, ' ', true);
  }
  
}

class Block extends Cell {

  public Block(Position position) {
    super(position, 0, '#', false);
  }
  
}

class Coin extends Cell {

  public Coin(Position position, int value, char label) {
    super(position, value, label, true);
  }
  
  public static Coin randomCoin(Position position) {
    double random = Math.random();
    if (random < 0.3333)
      return new BigCoin(position);
    else if (random < 0.6667)
      return new SmallCoin(position);
    else
      return new TinyCoin(position);
  }
  
}

class BigCoin extends Coin {

  public BigCoin(Position position) {
    super(position, Pacmans.BIG_COIN_VALUE, 'O');
  }
  
}

class SmallCoin extends Coin {

  public SmallCoin(Position position) {
    super(position, Pacmans.SMALL_COIN_VALUE, 'o');
  }
  
}

class TinyCoin extends Coin {

  public TinyCoin(Position position) {
    super(position, Pacmans.TINY_COIN_VALUE, '°');
  }
  
}

class Pacman extends Cell {
  
  private boolean prime;

  public Pacman(Position position, char label) {
    this(position, label, false);
  }
  
  public Pacman(Position position, char label, boolean prime) {
    super(position, 0, label, false);
    this.prime = prime;
  }

  public boolean isPrime() {
    return prime;
  }
  
}

class Board {
  
  private Cell[][] board;
  
  private List<Pacman> pacmans;

  public Board(int size, int number) {
    this(size, size, number);
  }
  
  public Board(int width, int height, int number) {
    board = new Cell[width][height];
    pacmans = new ArrayList<Pacman>();
    
    for (int i = 0; i < number; i++) {
      Position position = Position.randomPosition(this);
      Pacman pacman = new Pacman(position, (char)(i + 65), i == 0);
      
      setCell(position, pacman);
      pacmans.add(pacman);
    }
    
    for (int i = 0; i < getWidth(); i++)
      for (int j = 0; j < getHeight(); j++)
        if (board[i][j] == null)
          board[i][j] = Cell.randomCell(new Position(i, j));
  }
  
  public int getWidth() {
    return board.length;
  }
  
  public int getHeight() {
    return board[0].length;
  }
  
  public int getValue() {
    int value = 0;
    for (int i = 0; i < getWidth(); i++)
      for (int j = 0; j < getHeight(); j++)
        value += getCell(new Position(i, j)).getValue();
    
    return value;
  }
  
  public boolean hasValue() {
    for (int i = 0; i < getWidth(); i++)
      for (int j = 0; j < getHeight(); j++)
        if (getCell(new Position(i, j)).isOccupiable() && getCell(new Position(i, j)).getValue() > 0)
          return true;
    
    return false;
  }
  
  public Cell getCell(Position position) {
    return board[position.getX()][position.getY()];
  }
  
  public void setCell(Position position, Cell cell) {
    board[position.getX()][position.getY()] = cell;
  }
  
  public int getValue(Position position) {
    if (position.getX() >= 0 && position.getX() < getWidth() && position.getY() >= 0 && position.getY() < getHeight() && getCell(position).isOccupiable())
      return getCell(position).getValue();
    
    return -Integer.MAX_VALUE;
  }
  
  public double getValue(Position position, boolean prime) {
    if (position.getX() < 0 || position.getX() >= getWidth() || position.getY() < 0 || position.getY() >= getHeight() || !getCell(position).isOccupiable())
      return -Double.MAX_VALUE;
    
    double value = getValue(position);
    if(!prime || value > 0)
      return value;
    
    return Math.random() < Pacmans.PRIME_PROBABILITY? getPrime(position): Math.random();
  }
  
  private double getPrime(Position position) {
    double prime = 0.0;
    for (int i = 0; i < getWidth(); i++)
      for (int j = 0; j < getHeight(); j++)
        if (position.getX() != i || position.getY() != j)
          prime += getCell(new Position(i, j)).getValue() / position.computeDistance(i, j);
    
    return prime / getWidth() / getHeight();
  }

  public int getCount(Cell cell) {
    int count = 0;
    for (int i = 0; i < getWidth(); i++)
      for (int j = 0; j < getHeight(); j++)
        if (getCell(new Position(i, j)).getClass().equals(cell.getClass()))
          count++;
    
    return count;
  }
  
  public List<Pacman> getPacmans() {
    return pacmans;
  }
  
  @Override
  public String toString() {
    String board = "   ";
    for (int i = 0; i < 2 * getWidth() + 1; i++)
      board += "-";
    board += "\n";
    
    for (int j = 0; j < getHeight(); j++) {
      board += "   |";
      for (int i = 0; i < getWidth(); i++)
        board += getCell(new Position(i, j)) + "|";
      board += "\n";
    }
    
    board += "   ";
    for (int i = 0; i < 2 * getWidth() + 1; i++)
      board += "-";
    
    return board;
  }

}

class Pacmans {
  
  public static final int BIG_COIN_VALUE = 9;
  
  public static final int SMALL_COIN_VALUE = 3;
  
  public static final int TINY_COIN_VALUE = 1;
  
  public static final int NO_MOVE_VALUE = -5;
  
  public static final long MOVE_SLEEP_TIME = 100;
  
  public static final long PLAY_SLEEP_TIME = 2500;
  
  public static final double COINS_PROBABILITY = 0.5;
  
  public static final double BLOCKS_PROBABILITY = 0.1667;
  
  public static final double PRIME_PROBABILITY = 0.8;

  private int runs;
  
  private int plays;
  
  private Board board;
  
  private Map<Pacman, Integer> scores;
  
  public Pacmans(int size, int number) {
    this(size, size, number);
  }
  
  public Pacmans(int width, int height, int number) {
    runs = 0;
    plays = 0;
    board = new Board(width, height, number);
    
    scores = new HashMap<Pacman, Integer>();
    for (Pacman pacman: board.getPacmans())
      scores.put(pacman, 0);
  }

  public int getRuns() {
    return runs;
  }
  
  public int getPlays() {
    return plays;
  }

  public Board getBoard() {
    return board;
  }

  public Map<Pacman, Integer> getScores() {
    return scores;
  }

  private void movePacman(Pacman pacman) {
    List<Position> positions = new ArrayList<Position>();
    positions.add(pacman.getPosition());
    
    double value = Pacmans.NO_MOVE_VALUE;
    for (Position position: new Position[] { pacman.getPosition().movePosition(0, -1), pacman.getPosition().movePosition(0, 1),
        pacman.getPosition().movePosition(-1, -1), pacman.getPosition().movePosition(-1, 0), pacman.getPosition().movePosition(-1, 1),
        pacman.getPosition().movePosition(1, -1), pacman.getPosition().movePosition(1, 0), pacman.getPosition().movePosition(1, 1) })
      if (board.getValue(position, pacman.isPrime()) >= value) {
        if (board.getValue(position, pacman.isPrime()) > value)
          positions.clear();
        positions.add(position);

        value = board.getValue(position, pacman.isPrime());
      }
    
    Position position = positions.get((int)(Math.random() * positions.size()));
    scores.put(pacman, scores.get(pacman) + board.getValue(position));
    
    board.setCell(pacman.getPosition(), new Empty(pacman.getPosition()));
    board.setCell(position, pacman);
    
    pacman.setPosition(position);
  }
  
  private void movePacmans() {
    for (Pacman pacman: board.getPacmans())
      movePacman(pacman);
  }
  
  private void sortPacmans() {
    Collections.sort(board.getPacmans(), new Comparator<Pacman>() {
      @Override
      public int compare(Pacman first, Pacman second) {
        if (scores.get(first).equals(scores.get(second)))
          return new Character(first.getLabel()).compareTo(second.getLabel());
        
        return -scores.get(first).compareTo(scores.get(second));
      }
    });
  }
  
  public void playPacmans() throws InterruptedException {
    System.out.println(this);

    Thread.sleep(PLAY_SLEEP_TIME);

    while (board.hasValue()) {
      plays++;
      
      while (board.hasValue()) {
        movePacmans();
        sortPacmans();
        runs++;

        System.out.println(this);

        Thread.sleep(MOVE_SLEEP_TIME);
      }

      Thread.sleep(PLAY_SLEEP_TIME);

      for (int i = 0; i < board.getWidth(); i++)
        for (int j = 0; j < board.getHeight(); j++)
          if (board.getCell(new Position(i, j)) instanceof Block)
            board.setCell(new Position(i, j), Cell.randomCell(new Position(i, j)));

      System.out.println(this);

      Thread.sleep(PLAY_SLEEP_TIME);
    }
  }
  
  @Override
  public String toString() {
    String pacmans = "     ";
    for (Pacman pacman: board.getPacmans())
      pacmans += pacman + ":" + scores.get(pacman) + "  ";
    while (pacmans.length() < 2 * board.getWidth() + 1)
      pacmans = " " + pacmans + " ";
    
    String coins = "     " + plays + "-" + runs + ".  Ʃ:" + board.getValue() + "  ";
    for (Coin coin: new Coin[] { new BigCoin(null), new SmallCoin(null), new TinyCoin(null) })
      if (board.getCount(coin) > 0)
        coins += coin + ":" + board.getCount(coin) + "x" + coin.getValue() + "  ";
    Block block = new Block(null);
    if (board.getCount(block) > 0)
      coins += block + ":" + board.getCount(block) + "x" + block.getValue() + "  ";
    while (coins.length() < 2 * board.getWidth() + 1)
      coins = " " + coins + " ";
    
    return "\n" + board + "\n" + pacmans + "\n" + coins;
  }
  
}
