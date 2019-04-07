```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class Demo {

  public static void main(String[] args) {
    System.out.println("Let's do Java!");
    
    // This is a line comment
    
    /* This is a block comment */
    
    byte a = 1;
    short b = 2;
    int c = 3;
    long d = 4;
    
    System.out.println(a + b + c + d);
    
    float x = 0.33f;
    double y = 3.14;
    
    System.out.println(x - y);
    
    char chr = 'x';
    String str = "foobar";
    
    System.out.println(chr + " " + str + " " + (int)y);
    
    double r = Math.random();
    boolean bool = r < 0.5;
    
    if (bool) {
      System.out.println(r + " is smaller than 0.5");
    }
    else
      System.out.println(r + " is larger or equal 0.5");
    
    if (c == 3)
      System.out.println("Variable c does equal 3");
    
    if (d != 3)
      System.out.println("Variable d does not equal 3 but " + d);
    
    double s = Math.random();
    
    if (r < 0.5 && s < 0.5)
      System.out.println(r + " and " + s + " are smaller than 0.5");
    
    if (r < 0.5 || s < 0.5)
      System.out.println(r + " or " + s + " is smaller than 0.5");
    
    System.out.format("Random number r equals %.3f\n", r);
    
    final int CONST = 42;
    
    System.out.format("Constant CONST equals %5d\n", CONST);
    
    int integer = Integer.parseInt("123");
    
    System.out.println("Variable integer equals " + integer);
    
    double real = Double.parseDouble("123.456");
    
    System.out.println("Variable real equals " + real);
    
    for (int i = 0; i < 5; i++)
      System.out.println(i + 1);
    
    for (int i = 0; i < 5; i++)
      System.out.println("  " + i + 1);
    
    for (int i = 0; i < 5; i++) {
      for (int j = 0; j < i + 1; j++)
        System.out.print("*");
      System.out.println();
    }
    
    double val = 43.0;
    
    while (val > 1.0) {
      System.out.println(val);
      val /= 2.0;
    }
    
    while (true) {
      System.out.println(val);
      val *= 2.0;
      
      if (val > 100.0)
        break;
    }
    
    System.out.println("Variable val equals " + val);
    
    System.out.println("Square of val equals " + Math.pow(val, 2.0));
    
    System.out.println("Square root of val equals " + Math.sqrt(val));
    
    int fst = 1 + (int)(100.0 * Math.random());
    int snd = 1 + (int)(100.0 * Math.random());
    
    System.out.println("GCD of " + fst + " and " + snd + " using iteration is " + gcd(fst, snd));
    System.out.println("GCD of " + fst + " and " + snd + " using recursion is " + gcd2(fst, snd));
    
    gcds(fst, snd);
    
    double[] table = new double[5];
    
    for (int i = 0; i < table.length; i++)
      System.out.println(table[i]);
    
    for (int i = 0; i < table.length; i++)
      table[i] = Math.random();
    
    for (int i = 0; i < table.length; i++)
      System.out.println(table[i]);
    
    List<Integer> list = new ArrayList<Integer>();
    
    for (int i = 0; i < 5; i++)
      list.add((int)(10.0 * Math.random()));
    
    for (int i = 0; i < list.size(); i++)
      System.out.println((i + 1) + ". item in list is " + list.get(i));
    
    Set<Integer> set = new HashSet<Integer>();
    
    for (int i = 0; i < list.size(); i++)
      set.add(list.get(i));
    
    for (int num: set)
      System.out.println("Item in set is " + num);
    
    Map<Integer, Double> map = new HashMap<Integer, Double>();
    
    for (int i = 0; i < 5; i++) {
      double num = 10.0 * Math.random();
      
      map.put((int)num, num);
    }
    
    for (int key: map.keySet())
      System.out.println("Key " + key + " in map points to value " + map.get(key));
    
    try {
      BufferedReader reader = new BufferedReader(new FileReader("lorem.txt"));
      
      String line;
      while (true) {
        line = reader.readLine();
        
        System.out.println(line);
        
        if (line == null)
          break;
      }
      
      reader.close();
    } catch (IOException e) {
      e.printStackTrace();
    }
    
    XY[] points = new XY[3];
    points[0] = new XY(0, 1);
    points[1] = new XYZ(0, 1);
    points[2] = new XYZ(0, 1, 2);
    
    for (XY point: points)
      System.out.println(point);
    
    Domestic dog = new Dog();
    System.out.println(dog.say());
    System.out.println(dog.friendly());
    
    Domestic cat = new Cat();
    System.out.println(cat.say());
    System.out.println(cat.friendly());
  }

  public static int gcd(int a, int b) {
    while (b != 0) {
      int t = b;
      b = a % b;
      a = t;
    }
    
    return a;
  }
  
  public static int gcd2(int a, int b) {
    if (b == 0)
      return a;
    
    return gcd2(b, a % b);
  }
  
  public static void gcds(int a, int b) {
    System.out.println("GCD of " + a + " and " + b + " using iteration is " + gcd(a, b));
    System.out.println("GCD of " + a + " and " + b + " using recursion is " + gcd2(a, b));
  }
  
}

class XY {
  
  private int x;
  
  private int y;

  public XY(int x, int y) {
    this.x = x;
    this.y = y;
  }

  public int getX() {
    return x;
  }

  public int getY() {
    return y;
  }

  @Override
  public String toString() {
    return "x = " + getX() + ", y = " + getY();
  }
  
}

class XYZ extends XY {

  private int z;
  
  public XYZ(int x, int y) {
    this(x, y, 0);
  }
  
  public XYZ(int x, int y, int z) {
    super(x, y);
    this.z = z;
  }

  public int getZ() {
    return z;
  }
  
  @Override
  public String toString() {
    return super.toString() + ", z = " + getZ();
  }
  
}

interface Animal {
  
  public String say();
  
}

interface Domestic extends Animal {
  
  public boolean friendly();
  
}

class Dog implements Domestic {

  public Dog() {
    super();
  }

  @Override
  public String say() {
    return "Bark! Bark!";
  }

  @Override
  public boolean friendly() {
    return true;
  }
  
}

class Cat implements Domestic {

  public Cat() {
    super();
  }

  @Override
  public String say() {
    return "Meow! Meow!";
  }
  
  @Override
  public boolean friendly() {
    return false;
  }
  
}
```