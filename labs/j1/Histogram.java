import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Histogram {

  private int size;

  private int interval;

  private int maximum;

  private int[] histogram;

  public Histogram(List<Integer> numbers) {
    this(numbers, 12);
  }

  public Histogram(List<Integer> numbers, int interval) {
    this(numbers, interval, MAXIMUM);
  }

  public Histogram(List<Integer> numbers, int interval, int maximum) {
    size = numbers.size();

    this.interval = interval;
    this.maximum = maximum;

    histogram = new int[(int)Math.ceil(1.0 * maximum / interval)];
    for (int number: numbers)
      histogram[number / interval]++;
  }

  public int[] getHistogram() {
    return histogram;
  }

  public int getValue(int i) {
    return histogram[i];
  }

  public int getLength() {
    return histogram.length;
  }

  public int getMaximum() {
    return maximum;
  }

  public int getInterval() {
    return interval;
  }

  public int getSize() {
    return size;
  }

  @Override
  public String toString() {
    String string = "";
    for (int i = 0; i < histogram.length; i++)
      string += (i > 0? "\n": "") + String.format("%10s %3d - %4.1f%%", "[" + i * interval + "," + Math.min(maximum, (i + 1) * interval)+ "):", histogram[i], 100.0 * histogram[i] / size);

    return string;
  }

  static final int MAXIMUM = 123;

  static void write(String file) throws IOException {
    write(new File(file));
  }

  static void write(File file) throws IOException {
    BufferedWriter writer = new BufferedWriter(new FileWriter(file));

    for (int i = 0; i < 1000; i++) {
      int numbers = 1 + (int)(5 * Math.random());
      for (int j = 0; j < numbers; j++)
        writer.write((int)(MAXIMUM * Math.random()) + " ");
      writer.write("\n");
    }

    writer.flush();
    writer.close();
  }

  static List<Integer> read(String file) throws IOException {
    return read(new File(file));
  }

  static List<Integer> read(File file) throws IOException {
    List<Integer> numbers = new ArrayList<Integer>();

    BufferedReader reader = new BufferedReader(new FileReader(file));

    String line;
    while ((line = reader.readLine()) != null) {
      String[] array = line.split(" ");
      for (int i = 0; i < array.length; i++)
        if (array[i].length() > 0)
          numbers.add(Integer.parseInt(array[i]));
    }

    reader.close();

    return numbers;
  }

  public static void main(String[] args) {
    List<Integer> numbers = null;
    try {
      write("numbers.txt");

      numbers = read("numbers.txt");
    } catch (IOException e) {
      e.printStackTrace();

      System.exit(0);
    }

    Histogram histogram = new Histogram(numbers);

    System.out.println(histogram);
  }

}
