import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class Speeding {

  public static int speeding(String in, String out, int distance, double limit) throws IOException {
    return speeding(new File(in), new File(out), distance, limit);
  }

  public static int speeding(File in, File out, int distance, double limit) throws IOException {
    BufferedReader reader = new BufferedReader(new FileReader(in));
    BufferedWriter writer = new BufferedWriter(new FileWriter(out));

    String line; int speeding = 0;
    while ((line = reader.readLine()) != null) {
      String[] array = line.split(" ");

      Drive drive = new Drive(Integer.parseInt(array[0]), Integer.parseInt(array[1]), distance, array[2]);
      if (drive.getSpeed() > limit) {
        writer.write(String.format("%s %.2f\n", drive.getRegistration(), drive.getSpeed()));

        speeding++;
      }
    }

    reader.close(); writer.flush(); writer.close();

    return speeding;
  }

  public static void main(String[] args) {
    try {
      System.out.println(speeding("golovec.txt", "speeding.txt", 622, 80.0));
    } catch (IOException e) {
      e.printStackTrace();
    }
  }

}

class Drive {

  private int start;

  private int finish;

  private int distance;

  private String registration;

  public Drive(int start, int finish, int distance, String registration) {
    this.start = start;
    this.finish = finish;
    this.distance = distance;
    this.registration = registration;
  }

  public int getStart() {
    return start;
  }

  public int getFinish() {
    return finish;
  }

  public int getDistance() {
    return distance;
  }

  public String getRegistration() {
    return registration;
  }

  public double getSpeed() {
    return 3.6 * distance / (finish - start);
  }

}
