public class Highlight {

  public static String highlight(String string) {
    String highlighted = "";

    boolean highlight = false;
    for (int i = 0; i < string.length(); i++)
      if (string.charAt(i) == '*')
        highlight = !highlight;
      else
        highlighted += highlight? string.substring(i, i + 1).toUpperCase(): string.charAt(i);

        return highlighted;
  }

  final static String ALPHABET = "abcčdefghijklmnoprsštuvzž., ";

  public static void main(String[] args) {
    System.out.println(highlight("Poudarjena *beseda* in nepoudarjena beseda."));
    System.out.println(highlight("Poudarjeno *besedilo, ki se nadaljuje..."));
    System.out.println(highlight("Poudarjeno *besedilo*, ki se ne nadaljuje."));
    System.out.println(highlight("*g*it repozitorija *g*ithub in *b*it*b*ucket."));

    String random = "";
    for (int i = 0; i < 40; i++)
      if (Math.random() < 0.1)
        random += "*";
      else
        random += ALPHABET.charAt((int)(Math.random() * ALPHABET.length()));
    System.out.println(highlight(random));
  }

}
