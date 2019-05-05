## Izziv podatkovnih zbirk

V programskem jeziku Java je podana metoda `void collection(String label, Collection<Double> collection, int size)`, ki **podatkovno zbirko** `collection` najprej **napolni** s `size` naključno izbranimi realnimi števili. Metoda nato `size`-krat **preveri ali je** naključno izbrano realno **število vsebovano v zbirki** ter **izpiše pričakovan čas izvajanja** za podatkovno zbirko velikosti $10^8$.

```java
public static void collection(String label, Collection<Double> collection, int size) {
	long tic = System.currentTimeMillis();
	
	// fills collection with randomly selected numbers
		
	for (int i = 0; i < size; i++)
		collection.add(Math.random());
	
	// tests whether randomly selected numbers are included in collection
		
	for (int i = 0; i < size; i++)
		collection.contains(Math.random());
		
	// prints out collection label and expected running time
		
	System.out.format("\n%12s | '%s'", "Collection", label);
	System.out.format("\n%12s | %,.0f", "Size", 1e8);
	System.out.format("\n%12s | %.1f min\n", "Time", (System.currentTimeMillis() - tic) / 60000.0 / collection.size() * 1e8);
	
	// clears collection and runs garbage collector
	
	collection.clear();
	collection = null;
		
	System.gc();
}
```

Pričakovan izpis klica metode za **seznam** realnih števil **podprt s tabelo** `ArrayList<Double>` je podan spodaj.

```java
collection("ArrayList", new ArrayList<Double>(), (int)5e5);
```

```
  Collection | 'ArrayList'
        Size | 100,000,000
        Time | 1412.8 min
```

Preverite delovanje metode še za **množico** realnih števil implementirano **s pomočjo iskalnega drevesa** `TreeSet<Double>` ter **množico** realnih števil implementirano **s pomočjo zgoščevalne funkcije** `HashSet <Double>`.

```java
collection("TreeSet", new TreeSet<Double>(), (int)1e7);
collection("HashSet", new HashSet<Double>(), (int)1e7);
```

Pričakovan izpis klicov metode je podan spodaj.

```
  Collection | 'TreeSet'
        Size | 100,000,000
        Time | 4.7 min

  Collection | 'HashSet'
        Size | 100,000,000
        Time | 0.9 min
```

Opazimo veliko pohitritev časa izvajanja metode. Pojasnite **s čim "plačamo" pohitritev** časa izvajanja metode (angl. _no free lunch theorem_)! Posodobite metodo tako, da **z dodatnimi meritvami** izvajanja **podprete vaš odgovor**.
