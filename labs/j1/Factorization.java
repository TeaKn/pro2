import java.util.Map;
import java.util.List;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.Collections;

public class Factorization {
  
  public static int divisor(int number) {
    for (int i = 2; i < number / 2; i++)
      if (number % i == 0)
        return i;
    
    return number;
  }
  
  public static Map<Integer, Integer> factorize(int number) {
    Map<Integer, Integer> factorization = new HashMap<Integer, Integer>();
    
    while (number > 1) {
      int divisor = divisor(number);
      
      if (factorization.containsKey(divisor))
        factorization.put(divisor, factorization.get(divisor) + 1);
      else
        factorization.put(divisor, 1);
      
      number /= divisor;
    }
    
    return factorization;
  }
  
  public static void factorization(int number) {
    Map<Integer, Integer> factorization = factorize(number);
    
    List<Integer> primes = new ArrayList<Integer>(factorization.keySet());
    Collections.sort(primes);
    
    System.out.print(number + " = ");
    for (int prime: primes)
      System.out.print((primes.get(0).equals(prime)? "": " * ") + prime + (factorization.get(prime) > 1? "^" + factorization.get(prime): ""));
    System.out.println();
  }
  
  public static void main(String[] args) {
    factorization(5);
    factorization(16);
    factorization(43);
    factorization(99);
    factorization(1025);
    factorization(4382);
    factorization(74438);
    factorization(578298);
    factorization(5761665);
  }

}
