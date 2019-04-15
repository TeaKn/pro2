import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Class representing a position in the Cartesian coordinate plane.
 *
 * The position is represented by its horizontal and vertical coordinates.
 *
 * @author Lovro Šubelj
 */
class Position {
  
  /**
   * Horizontal coordinate or abscissa of the position.
   */
  private int x;
  
  /**
   * Vertical coordinate or ordinate of the position.
   */
  private int y;

  /**
   * Constructs a position in the Cartesian coordinate plane represented by its horizontal and vertical coordinates.
   *
   * @param x horizontal coordinate or abscissa
   * @param y vertical coordinate or ordinate
   */
  public Position(int x, int y) {
    this.x = x;
    this.y = y;
  }

  /**
   * Returns horizontal coordinate of the position in the Cartesian coordinate plane.
   *
   * @return horizontal coordinate or abscissa
   */
  public int getX() {
    return x;
  }

  /**
   * Returns vertical coordinate of the position in the Cartesian coordinate plane.
   *
   * @return vertical coordinate or ordinate
   */
  public int getY() {
    return y;
  }

  /**
   * Returns a new position in the Cartesian coordinate plane moved by the specified point.
   *
   * @param x horizontal coordinate or abscissa of the point
   * @param y vertical coordinate or ordinate of the point
   *
   * @return position moved by the horizontal and vertical coordinates of the specified point
   */
  public Position move(int x, int y) {
    return new Position(getX() + x, getY() + y);
  }
  
  /**
   * Computes Euclidean distance between the position in the Cartesian coordinate plane and the specified point.
   *
   * @param x horizontal coordinate or abscissa of the point
   * @param y vertical coordinate or ordinate of the point
   *
   * @return Euclidean distance between the position and the specified point
   */
  public double distance(int x, int y) {
    return Math.sqrt(Math.pow(getX() - x, 2.0) + Math.pow(getY() - y, 2.0));
  }
  
  /**
   * Returns random unoccupied position in the Cartesian coordinate plane corresponding to the specified {@link Board}.
   *
   * The function ensures that the returned position is unoccupied or empty tested by whether {@link Board#getCell(Position)} equals {@code null}.
   *
   * @param board {@link Board} representing the Cartesian coordinate plane
   *
   * @return random position in the Cartesian coordinate plane corresponding to the specified {@link Board}
   */
  public static Position random(Board board) {
    Position position = new Position((int)(Math.random() * board.getWidth()), (int)(Math.random() * board.getHeight()));
    while (board.getCell(position) != null)
      position = new Position((int)(Math.random() * board.getWidth()), (int)(Math.random() * board.getHeight()));
    
    return position;
  }
  
}

/**
 * Class representing a cell on a {@link Board} represented by the Cartesian coordinate plane.
 *
 * The cell is represented by its {@link Position} in the plane, its intrinsic value and a predefined label.
 *
 * @author Lovro Šubelj
 */
class Cell {
  
  /**
   * {@link Position} of the cell in the Cartesian coordinate plane.
   */
  private Position position;
  
  /**
   * Intrinsic value of the cell equal to a non-negative integer.
   */
  private int value;
  
  /**
   * Predefined label of the cell equal to a single character.
   */
  private char label;
  
  /**
   * Boolean representing whether the cell is occupiable (e.g. empty).
   */
  private boolean occupiable;

  /**
   * Constructs a cell on a {@link Board} represented by the Cartesian coordinate plane.
   *
   * The cell is specified by its {@link Position} in the plane, its intrinsic non-negative value, a predefined label as a single character and whether the cell is occupiable.
   *
   * @param position {@link Position} of the cell on a {@link Board}
   * @param value intrinsic non-negative value of the cell
   * @param label predefined label or character of the cell
   * @param occupiable whether the cell is occupiable
   */
  public Cell(Position position, int value, char label, boolean occupiable) {
    if (value < 0)
      throw new IllegalArgumentException();
    
    this.position = position;
    this.value = value;
    this.label = label;
    this.occupiable = occupiable;
  }

  /**
   * Returns the {@link Position} of the cell on a {@link Board}.
   *
   * @return position of the cell on a {@link Board}
   */
  public Position getPosition() {
    return position;
  }
  
  /**
   * Sets the {@link Position} of the cell on a {@link Board} to the specified position.
   *
   * @param position new position of the cell on a {@link Board}
   */
  public void setPosition(Position position) {
    this.position = position;
  }

  /**
   * Returns the value of the cell on a {@link Board} equal to a non-negative integer.
   *
   * @return value of the cell on a {@link Board}
   */
  public int getValue() {
    return value;
  }

  /**
   * Returns the label of the cell on a {@link Board} equal to a single character.
   *
   * @return label of the cell on a {@link Board}
   */
  public char getLabel() {
    return label;
  }

  /**
   * Returns whether the cell on a {@link Board} is occupiable (e.g. empty).
   *
   * @return whether the cell on a {@link Board} is occupiable
   */
  public boolean isOccupiable() {
    return occupiable;
  }

  /**
   * Returns {@link String} representation of the cell on a {@link Board} equal to its label.
   *
   * @return {@link String} representation of the cell on a {@link Board}
   */
  @Override
  public String toString() {
    return "" + getLabel();
  }

  /**
   * Returns randomly selected cell at the specified {@link Position} on a {@link Board}.
   *
   * The function returns random {@link Coin} with probability {@link Pacmans#COINS_PROBABILITY}, {@link Block} cell with probability {@link Pacmans#BLOCKS_PROBABILITY} and {@link Empty} cell otherwise.
   *
   * @param position {@link Position} of the cell on a {@link Board}
   *
   * @return random cell at the specified {@link Position} on a {@link Board}
   */
  public static Cell random(Position position) {
    double random = Math.random();
    if (random < Pacmans.COINS_PROBABILITY)
      return Coin.random(position);
    else if (random < Pacmans.COINS_PROBABILITY + Pacmans.BLOCKS_PROBABILITY)
      return new Block(position);
    else
      return new Empty(position);
  }
  
}

/**
 * Class representing an empty {@link Cell} on a {@link Board} represented by the Cartesian coordinate plane.
 *
 * The {@link Cell} is represented by its {@link Position} in the plane which is occupiable, while its intrinsic value equals {@code 0} and its label equals {@code ' '}.
 *
 * @author Lovro Šubelj
 */
class Empty extends Cell {

  /**
   * Constructs an empty {@link Cell} on a {@link Board} represented by the Cartesian coordinate plane.
   *
   * The {@link Cell} is specified by its {@link Position} in the plane which is occupiable, while its intrinsic value equals {@code 0} and its label equals {@code ' '}.
   *
   * @param position {@link Position} of the {@link Cell} on a {@link Board}
   */
  public Empty(Position position) {
    super(position, 0, ' ', true);
  }
  
}

/**
 * Class representing a block {@link Cell} on a {@link Board} represented by the Cartesian coordinate plane.
 *
 * The {@link Cell} is represented by its {@link Position} in the plane which is non occupiable, while its intrinsic value equals {@code 0} and its label equals {@code '#'}.
 *
 * @author Lovro Šubelj
 */
class Block extends Cell {

  /**
   * Constructs a block {@link Cell} on a {@link Board} represented by the Cartesian coordinate plane.
   *
   * The {@link Cell} is specified by its {@link Position} in the plane which is non occupiable, while its intrinsic value equals {@code 0} and its label equals {@code '#'}.
   *
   * @param position {@link Position} of the {@link Cell} on a {@link Board}
   */
  public Block(Position position) {
    super(position, 0, '#', false);
  }
  
}

/**
 * Class representing a coin {@link Cell} on a {@link Board} represented by the Cartesian coordinate plane.
 *
 * The {@link Cell} is represented by its {@link Position} in the plane which is occupiable, its intrinsic value and a predefined label.
 *
 * @author Lovro Šubelj
 */
abstract class Coin extends Cell {

  /**
   * Constructs a coin {@link Cell} on a {@link Board} represented by the Cartesian coordinate plane.
   *
   * The {@link Cell} is specified by its {@link Position} in the plane which is occupiable, its intrinsic value and a predefined label.
   *
   * @param position {@link Position} of the {@link Cell} on a {@link Board}
   * @param value intrinsic non-negative value of the {@link Cell}
   * @param label predefined label or character of the {@link Cell}
   */
  public Coin(Position position, int value, char label) {
    super(position, value, label, true);
  }
  
  /**
   * Returns randomly selected coin {@link Cell} at the specified {@link Position} on a {@link Board}.
   *
   * The function returns either {@link BigCoin}, {@link SmallCoin} or {@link TinyCoin} with equal probability.
   *
   * @param position {@link Position} of the coin {@link Cell} on a {@link Board}
   *
   * @return random coin {@link Cell} at the specified {@link Position} on a {@link Board}
   */
  public static Coin random(Position position) {
    double random = Math.random();
    if (random < 0.3333)
      return new BigCoin(position);
    else if (random < 0.6667)
      return new SmallCoin(position);
    else
      return new TinyCoin(position);
  }
  
}

/**
 * Class representing a big {@link Coin} on a {@link Board} represented by the Cartesian coordinate plane.
 *
 * The {@link Coin} is represented by its {@link Position} in the plane which is occupiable, while its intrinsic value equals {@link Pacmans#BIG_COIN_VALUE} and its label equals {@code 'O'}.
 *
 * @author Lovro Šubelj
 */
class BigCoin extends Coin {

  /**
   * Constructs a big {@link Coin} on a {@link Board} represented by the Cartesian coordinate plane.
   *
   * The {@link Coin} is specified by its {@link Position} in the plane which is occupiable, while its intrinsic value equals {@link Pacmans#BIG_COIN_VALUE} and its label equals {@code 'O'}.
   *
   * @param position {@link Position} of the {@link Coin} on a {@link Board}
   */
  public BigCoin(Position position) {
    super(position, Pacmans.BIG_COIN_VALUE, 'O');
  }
  
}

/**
 * Class representing a small {@link Coin} on a {@link Board} represented by the Cartesian coordinate plane.
 *
 * The {@link Coin} is represented by its {@link Position} in the plane which is occupiable, while its intrinsic value equals {@link Pacmans#SMALL_COIN_VALUE} and its label equals {@code 'o'}.
 *
 * @author Lovro Šubelj
 */
class SmallCoin extends Coin {

  /**
   * Constructs a small {@link Coin} on a {@link Board} represented by the Cartesian coordinate plane.
   *
   * The {@link Coin} is specified by its {@link Position} in the plane which is occupiable, while its intrinsic value equals {@link Pacmans#SMALL_COIN_VALUE} and its label equals {@code 'o'}.
   *
   * @param position {@link Position} of the {@link Coin} on a {@link Board}
   */
  public SmallCoin(Position position) {
    super(position, Pacmans.SMALL_COIN_VALUE, 'o');
  }
  
}

/**
 * Class representing a tiny {@link Coin} on a {@link Board} represented by the Cartesian coordinate plane.
 *
 * The {@link Coin} is represented by its {@link Position} in the plane which is occupiable, while its intrinsic value equals {@link Pacmans#TINY_COIN_VALUE} and its label equals {@code '°'}.
 *
 * @author Lovro Šubelj
 */
class TinyCoin extends Coin {

  /**
   * Constructs a tiny {@link Coin} on a {@link Board} represented by the Cartesian coordinate plane.
   *
   * The {@link Coin} is specified by its {@link Position} in the plane which is occupiable, while its intrinsic value equals {@link Pacmans#TINY_COIN_VALUE} and its label equals {@code '°'}.
   *
   * @param position {@link Position} of the {@link Coin} on a {@link Board}
   */
  public TinyCoin(Position position) {
    super(position, Pacmans.TINY_COIN_VALUE, '°');
  }
  
}

/**
 * Class representing a pacman {@link Cell} on a {@link Board} represented by the Cartesian coordinate plane.
 *
 * The {@link Cell} is represented by its {@link Position} in the plane which is non occupiable and a predefined label, while its intrinsic value equals {@code 0}
 *
 * @author Lovro Šubelj
 */
class Pacman extends Cell {
  
  /**
   * Boolean representing whether the pacman {@link Cell} is prime (i.e. smart).
   */
  private boolean prime;

  /**
   * Constructs a non prime pacman {@link Cell} on a {@link Board} represented by the Cartesian coordinate plane.
   *
   * The {@link Cell} is specified by its {@link Position} in the plane which is non occupiable and a predefined label, while its intrinsic value equals {@code 0}.
   *
   * @param position {@link Position} of the {@link Cell} on a {@link Board}
   * @param label predefined label or character of the {@link Cell}
   */
  public Pacman(Position position, char label) {
    this(position, label, false);
  }
  
  /**
   * Constructs a pacman {@link Cell} on a {@link Board} represented by the Cartesian coordinate plane.
   *
   * The {@link Cell} is specified by its {@link Position} in the plane which is non occupiable and a predefined label, while its intrinsic value equals {@code 0}.
   *
   * @param position {@link Position} of the {@link Cell} on a {@link Board}
   * @param label predefined label or character of the {@link Cell}
   * @param prime whether the {@link Cell} is prime (i.e. smart)
   */
  public Pacman(Position position, char label, boolean prime) {
    super(position, 0, label, false);
    this.prime = prime;
  }

  /**
   * Returns whether the pacman {@link Cell} on a {@link Board} is prime.
   *
   * @return whether the pacman {@link Cell} on a {@link Board} is prime
   */
  public boolean isPrime() {
    return prime;
  }

  /**
   * Sets whether the pacman {@link Cell} on a {@link Board} is prime.
   *
   * @param prime whether the pacman {@link Cell} on a {@link Board} is prime
   */
  public void setPrime(boolean prime) {
    this.prime = prime;
  }
  
}

/**
 * Class representing a board of {@link Cell}-s in the Cartesian coordinate plane.
 *
 * The initial board contains the specified number of randomly positioned {@link Pacman}-s with one prime {@link Pacman}. Other {@link Cell}-s are random {@link Coin}-s with probability {@link Pacmans#COINS_PROBABILITY}, {@link Block} cells with probability {@link Pacmans#BLOCKS_PROBABILITY} and {@link Empty} cells otherwise.
 *
 * @author Lovro Šubelj
 */
class Board {
  
  /**
   * Board of {@link Cell}-s in the Cartesian coordinate plane.
   */
  private Cell[][] board;
  
  /**
   * Constructs a board of {@link Cell}-s in the Cartesian coordinate plane with the specified size (i.e. width and height).
   *
   * The board contains the specified number of randomly positioned {@link Pacman}-s with two prime {@link Pacman}-s. Other {@link Cell}-s are random {@link Coin}-s with probability {@link Pacmans#COINS_PROBABILITY} returned by {@link Coin#random(Position)}, {@link Block} cells with probability {@link Pacmans#BLOCKS_PROBABILITY} and {@link Empty} cells otherwise.
   *
   * @param size width and height of the board of {@link Cell}-s
   * @param pacmans number of {@link Pacman}-s of the board
   */
  public Board(int size, int pacmans) {
    this(size, size, pacmans);
  }
  
  /**
   * Constructs a board of {@link Cell}-s in the Cartesian coordinate plane with the specified width and height.
   *
   * The board contains the specified number of randomly positioned {@link Pacman}-s with two prime {@link Pacman}-s. Other {@link Cell}-s are random {@link Coin}-s with probability {@link Pacmans#COINS_PROBABILITY} returned by {@link Coin#random(Position)}, {@link Block} cells with probability {@link Pacmans#BLOCKS_PROBABILITY} and {@link Empty} cells otherwise.
   *
   * @param width width of the board of {@link Cell}-s
   * @param height height of the board of {@link Cell}-s
   * @param pacmans number of {@link Pacman}-s of the board
   */
  public Board(int width, int height, int pacmans) {
    if (width <= 0 || height <= 0 || pacmans <= 0)
      throw new IllegalArgumentException();
    
    board = new Cell[width][height];
    
    for (int i = 0; i < pacmans; i++) {
      Position position = Position.random(this);
      setCell(position, new Pacman(position, (char)(i + 65), i <= 1));
    }
    
    for (int i = 0; i < width; i++)
      for (int j = 0; j < height; j++)
        if (board[i][j] == null)
          board[i][j] = Cell.random(new Position(i, j));
  }
  
  /**
   * Returns the width of the board of {@link Cell}-s in the Cartesian coordinate plane.
   *
   * @return width of the board of {@link Cell}-s
   */
  public int getWidth() {
    return board.length;
  }
  
  /**
   * Returns the height of the board of {@link Cell}-s in the Cartesian coordinate plane.
   *
   * @return height of the board of {@link Cell}-s
   */
  public int getHeight() {
    return board[0].length;
  }

  /**
   * Returns the {@link Cell} on the board in the Cartesian coordinate plane at the specified {@link Position}.
   *
   * @param position {@link Position} on the board in the Cartesian coordinate plane
   *
   * @return {@link Cell} on the board at the specified {@link Position}
   */
  public Cell getCell(Position position) {
    return board[position.getX()][position.getY()];
  }
  
  /**
   * Sets the specified {@link Cell} to the specified {@link Position} on the board in the Cartesian coordinate plane.
   *
   * @param position {@link Position} on the board in the Cartesian coordinate plane
   * @param cell new {@link Cell} on the board at the specified {@link Position}
   */
  public void setCell(Position position, Cell cell) {
    board[position.getX()][position.getY()] = cell;
  }
  
  /**
   * Returns the number of {@link Cell}-s on the board in the Cartesian coordinate plane that are instances of the specified {@link Class}.
   *
   * @param cell {@link Class} of the {@link Cell}-s on the board
   *
   * @return number of {@link Cell}-s on the board of the specified {@link Class}
   */
  public int getNumber(Class<?> cell) {
    int number = 0;
    for (int i = 0; i < getWidth(); i++)
      for (int j = 0; j < getHeight(); j++)
        if (getCell(new Position(i, j)).getClass().equals(cell))
          number++;
    
    return number;
  }

  /**
   * Returns the value of the specified {@link Position} on the board in the Cartesian coordinate plane. The function returns {@code -Double.MAX_VALUE} if the specified {@link Position} is not on the board. Next, the function returns the value of the {@link Cell} at the specified {@link Position} returned by {@link Cell#getValue()} if the value is positive or the evaluation is greedy and a randomly selected value with probability {@link Pacmans#GREEDY_PROBABILITY}. Otherwise, the function returns the sum of values of {@link Cell}-s on the board discounted by their distance from the specified {@link Position}.
   *
   * @param position {@link Position} on the board in the Cartesian coordinate plane
   * @param greedy whether the evaluation of the specified {@link Position} on the board is greedy
   *
   * @return value of the specified {@link Position} on the board due to the specified strategy
   */
  public double getValue(Position position, boolean greedy) {
    if (position.getX() < 0 || position.getX() >= getWidth() || position.getY() < 0 || position.getY() >= getHeight() || !getCell(position).isOccupiable())
      return -Double.MAX_VALUE;
    
    double value = getCell(position).getValue();
    if(greedy || value > 0)
      return value;
    
    if (Math.random() < Pacmans.GREEDY_PROBABILITY)
      return Math.random();
    
    value = 0.0;
    for (int i = 0; i < getWidth(); i++)
      for (int j = 0; j < getHeight(); j++)
        if (position.getX() != i || position.getY() != j)
          value += getCell(new Position(i, j)).getValue() / position.distance(i, j);
    
    return value / getWidth() / getHeight();
  }
  
  /**
   * Returns the value of the specified {@link Position} on the board in the Cartesian coordinate plane. The function returns {@code -Double.MAX_VALUE} if the specified {@link Position} is not on the board. Otherwise, the function returns the value of the {@link Cell} at the specified {@link Position} returned by {@link Cell#getValue()}.
   *
   * @param position {@link Position} on the board in the Cartesian coordinate plane
   *
   * @return value of the specified {@link Position} on the board
   */
  public double getValue(Position position) {
    return getValue(position, true);
  }

  /**
   * Returns the sum of values of {@link Cell}-s on the board in the Cartesian coordinate plane returned by {@link Cell#getValue()}.
   *
   * @return sum of values of {@link Cell}-s on the board
   */
  public int getValue() {
    int value = 0;
    for (int i = 0; i < getWidth(); i++)
      for (int j = 0; j < getHeight(); j++)
        value += getCell(new Position(i, j)).getValue();
    
    return value;
  }

  /**
   * Returns whether any occupiable {@link Cell} on the board in the Cartesian coordinate plane has positive value returned by {@link Cell#getValue()}.
   *
   * @return whether any occupiable {@link Cell} on the board has positive value
   */
  public boolean hasValue() {
    for (int i = 0; i < getWidth(); i++)
      for (int j = 0; j < getHeight(); j++)
        if (getCell(new Position(i, j)).isOccupiable() && getCell(new Position(i, j)).getValue() > 0)
          return true;
    
    return false;
  }
  
  /**
   * Returns whether any {@link Cell} on the board in the Cartesian coordinate plane is not either {@link Block} or {@link Coin}.
   *
   * @return whether any {@link Cell} on the board is not either {@link Block} or {@link Coin}
   */
  public boolean isEmpty() {
    for (int i = 0; i < getWidth(); i++)
      for (int j = 0; j < getHeight(); j++)
        if (getCell(new Position(i, j)) instanceof Block || getCell(new Position(i, j)) instanceof Coin)
          return false;
    
    return true;
  }
  
  /**
   * Returns {@link String} representation of the board of {@link Cell}-s in the Cartesian coordinate plane.
   *
   * @return {@link String} representation of the board of {@link Cell}-s
   */
  @Override
  public String toString() {
    String string = "   ";
    for (int i = 0; i < 2 * getWidth() + 1; i++)
      string += "-";
    string += "\n";
    
    for (int j = 0; j < getHeight(); j++) {
      string += "   |";
      for (int i = 0; i < getWidth(); i++)
        string += getCell(new Position(i, j)) + "|";
      string += "\n";
    }
    
    string += "   ";
    for (int i = 0; i < 2 * getWidth() + 1; i++)
      string += "-";
    
    return string;
  }

}

public class Pacmans {
  
  protected static final int BIG_COIN_VALUE = 9;
  
  protected static final int SMALL_COIN_VALUE = 3;
  
  protected static final int TINY_COIN_VALUE = 1;
  
  protected static final int NO_MOVE_VALUE = -5;
  
  protected static final long MOVE_SLEEP_TIME = 150;
  
  protected static final long PLAY_SLEEP_TIME = 2500;
  
  protected static final double COINS_PROBABILITY = 0.5;
  
  protected static final double BLOCKS_PROBABILITY = 0.1667;
  
  protected static final double GREEDY_PROBABILITY = 0.2;

  private int runs;
  
  private int plays;
  
  private Board board;
  
  private List<Pacman> pacmans;
  
  private Map<Pacman, Double> scores;
  
  public Pacmans(int size, int number) {
    this(size, size, number);
  }
  
  public Pacmans(int width, int height, int number) {
    runs = 0;
    plays = 0;
    board = new Board(width, height, number);
    
    pacmans = new ArrayList<Pacman>();
    scores = new HashMap<Pacman, Double>();
    
    for (int i = 0; i < width; i++)
      for (int j = 0; j < height; j++)
        if (board.getCell(new Position(i, j)) instanceof Pacman) {
          Pacman pacman = (Pacman)board.getCell(new Position(i, j));
          pacmans.add(pacman);
          scores.put(pacman, 0.0);
        }
    
    Collections.sort(pacmans, new Comparator<Pacman>() {
      @Override
      public int compare(Pacman first, Pacman second) {
        if (scores.get(first).equals(scores.get(second)))
          return new Character(first.getLabel()).compareTo(second.getLabel());
        
        return -scores.get(first).compareTo(scores.get(second));
      }
    });
  }

  public int getRuns() {
    return runs;
  }
  
  public void setRuns(int runs) {
    this.runs = runs;
  }

  public int getPlays() {
    return plays;
  }

  public void setPlays(int plays) {
    this.plays = plays;
  }

  public Board getBoard() {
    return board;
  }

  public List<Pacman> getPacmans() {
    return pacmans;
  }
  
  public Map<Pacman, Double> getScores() {
    return scores;
  }

  protected void move(Pacman pacman) {
    List<Position> positions = new ArrayList<Position>();
    positions.add(pacman.getPosition());
    
    double value = Pacmans.NO_MOVE_VALUE;
    for (Position position: new Position[] { pacman.getPosition().move(0, -1), pacman.getPosition().move(0, 1),
        pacman.getPosition().move(-1, -1), pacman.getPosition().move(-1, 0), pacman.getPosition().move(-1, 1),
        pacman.getPosition().move(1, -1), pacman.getPosition().move(1, 0), pacman.getPosition().move(1, 1) })
      if (board.getValue(position, !pacman.isPrime()) >= value) {
        if (board.getValue(position, !pacman.isPrime()) > value)
          positions.clear();
        positions.add(position);

        value = board.getValue(position, !pacman.isPrime());
      }
    
    Position position = positions.get((int)(Math.random() * positions.size()));
    scores.put(pacman, scores.get(pacman) + board.getValue(position));
    
    board.setCell(pacman.getPosition(), new Empty(pacman.getPosition()));
    board.setCell(position, pacman);
    
    pacman.setPosition(position);
  }
  
  protected void move() {
    Collections.shuffle(pacmans);
    
    for (Pacman pacman: pacmans)
      move(pacman);
    
    Collections.sort(pacmans, new Comparator<Pacman>() {
      @Override
      public int compare(Pacman first, Pacman second) {
        if (scores.get(first).equals(scores.get(second)))
          return new Character(first.getLabel()).compareTo(second.getLabel());
        
        return -scores.get(first).compareTo(scores.get(second));
      }
    });
  }
  
  protected void update() {
    for (int i = 0; i < board.getWidth(); i++)
      for (int j = 0; j < board.getHeight(); j++)
        if (board.getCell(new Position(i, j)) instanceof Block)
          board.setCell(new Position(i, j), Cell.random(new Position(i, j)));
  }

  protected void reset() {
    runs = 0;
    plays = 0;
    board = new Board(board.getWidth(), board.getHeight(), pacmans.size());
    
    pacmans = new ArrayList<Pacman>();
    scores = new HashMap<Pacman, Double>();
    
    for (int i = 0; i < board.getWidth(); i++)
      for (int j = 0; j < board.getHeight(); j++)
        if (board.getCell(new Position(i, j)) instanceof Pacman) {
          Pacman pacman = (Pacman)board.getCell(new Position(i, j));
          pacmans.add(pacman);
          scores.put(pacman, 0.0);
        }
    
    Collections.sort(pacmans, new Comparator<Pacman>() {
      @Override
      public int compare(Pacman first, Pacman second) {
        if (scores.get(first).equals(scores.get(second)))
          return new Character(first.getLabel()).compareTo(second.getLabel());
        
        return -scores.get(first).compareTo(scores.get(second));
      }
    });
  }
  
  protected void draw() {
    System.out.println(this);
  }
  
  public void play() throws InterruptedException {
    draw();

    while (!board.isEmpty()) {
      plays++;
      
      Thread.sleep(PLAY_SLEEP_TIME);
      
      while (board.hasValue()) {
        runs++;
        
        move();
        draw();

        Thread.sleep(MOVE_SLEEP_TIME);
      }

      Thread.sleep(PLAY_SLEEP_TIME);

      update();
      draw();
    }
  }
  
  @Override
  public String toString() {
    String string = "     ";
    for (Pacman pacman: pacmans)
      string += pacman + ":" + scores.get(pacman).intValue() + "  ";
    while (string.length() < 2 * board.getWidth() + 1)
      string = " " + string + " ";
    
    String coins = "     " + plays + "-" + runs + ".  Ʃ:" + board.getValue() + "  ";
    for (Coin coin: new Coin[] { new BigCoin(null), new SmallCoin(null), new TinyCoin(null) })
      if (board.getNumber(coin.getClass()) > 0)
        coins += coin + ":" + board.getNumber(coin.getClass()) + "x" + coin.getValue() + "  ";
    Block block = new Block(null);
    if (board.getNumber(block.getClass()) > 0)
      coins += block + ":" + board.getNumber(block.getClass()) + "x" + block.getValue() + "  ";
    while (coins.length() < 2 * board.getWidth() + 1)
      coins = " " + coins + " ";
    
    return "\n" + board + "\n" + string + "\n" + coins;
  }
  
  public static void main(String[] args) {
    int size = args.length > 0? Integer.parseInt(args[0]): 24;
    int number = args.length > 1? Integer.parseInt(args[1]): 6;
    
    Pacmans pacmans = new Pacmans(size, number);
    
    try {
      pacmans.play();
    } catch (InterruptedException e) {
      e.printStackTrace();
    }
  }
  
}
