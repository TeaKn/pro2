public class Collatz {

  public static int next(int number) {
    if (number % 2 == 0)
      return number / 2;
    else
      return 3 * number + 1;
  }

  public static void sequence(int number) {
    System.out.print(String.format("%,d", number));

    while ((number = next(number)) != 1)
      System.out.print(" " + String.format("%,d", number));

    System.out.println(" 1");
  }

  public static int length(int number) {
    int length = 1;
    while ((number = next(number)) != 1)
      length++;

    return length + 1;
  }

  public static int maximum(int number) {
    int maximum = 4;
    while ((number = next(number)) != 1)
      if (number > maximum)
        maximum = number;

    return maximum;
  }

  public static void main(String[] args) {
    for (int number: new int[] { 6, 12, 19, 27, 871 }) {
      System.out.format("Number: %,d\n", number);
      System.out.format("Length: %,d\n", length(number));
      System.out.format("Maximum: %,d\n", maximum(number));

      System.out.print("Sequence: ");
      sequence(number);
      System.out.println();
    }
  }

}
