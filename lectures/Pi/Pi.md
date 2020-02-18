###### Programiranje 2 2019/20 (Pi)

## Uvod v programska jezika Python in Java

Programska jezika **Python in Java** sta **splošnonamenska programska jezika** v katerih je moč sestaviti praktično katerikoli program. 

_Programming is not science, it is a skill! If you want to run as fast as Usain Bolt, you have to do a lot of running. There is no other way! And it is the same with programming. Just run a lot ;)_

Programski jezik **Python** je gotovo **(trenutno) najpopularnejši jezik** zaradi enostavne sintakse in obilice prosto-dostopnih programskih knjižnic, dočim pa vsekakor ni najhitrejši jezik. Jezik se interpretira kar pomeni, da program `demo.py` v ukazni vrstici izvedete kot `python demo.py`. 

Programski jezik **Java** je bil razvit kot **(varen) jezik za poljubno napravo**. Sintaksa zahteva daljše programe, ki pa so vsaj desetkrat hitrejši kot programi v jeziku Python. Jezik se prevaja kar pomeni, da program `Demo.java` v ukazni vrstici najprej prevedete kot `javac Demo.java`, kar ustvari datoteko `Demo.class`, katero nato izvedete kot `java Demo`.

### Najkrajši program in izpis na zaslon

V programskem jeziku **Python bloke kode**, ki naj se izvedejo skupaj oziroma zaporedoma, določimo z zamikanjem (glej spodaj). Vsak programski stavek zapišemo v svoji vrstici.

```py
print('Pozdravljeni pri predmetu PRO2!')
```

V programskem jeziku **Java bloke kode**, ki naj se izvedejo skupaj oziroma zaporedoma, določimo z zavitimi oklepaji `{...}` (glej spodaj). Vsak programski stavek zaključimo s podpičjem `;`, dočim je lahko celoten program v eni vrstici.

```java
public class Di {
  public static void main(String[] args) {
    System.out.println("Pozdravljeni pri predmetu PRO2!");
  }
}
```

### Programske spremenljivke in konstante

V programskem jeziku **Python spremenljivke** definiramo in jim določimo začetno vrednost hkrati. Pri tem **ne določimo tipa** spremenljivke.

```py
x = 1
y = 1.23
ch = 'a'
str = "niz znakov"
```

V programskem jeziku **Python konstante** obravnavamo enako kot spremenljivke. Navadno jih označimo z velikimi črkami.

```py
G = 9.81
```

V programskem jeziku **Java spremenljivke** definiramo in jim _lahko_ določimo začetno vrednost hkrati. Pri definiciji **moramo določiti tip** spremenljivke, ki ga ni moč spremeniti. Osnovni tipi spremenljivk so cela števila (tj. `byte/short/int/long`), realna števila (tj. `float/double`) in nizi znakov (tj. `char/String`).

```java
int x = 1;
float y;
y = 1.23;
char ch = 'a';
String str = "niz znakov";
```

V programskem jeziku **Java konstante** označimo z besedo `final` in jih ne moremo naknadno spreminjati. Navadno jih označimo z velikimi črkami.

```java
final float G = 9.81;
```

### Pogojni stavki in programske vejitve

Programske vejitve omogočajo **selektivno izvajanje** programske kode glede na določen logičen pogoj. Najpogosteje se uporabljajo pogojni stavki (tj. `if else` stavki), dočim v večini programskih jezikih obstajajo tudi npr. `switch` stavki in drugi. Vse pogojne stavke je moč gnezditi ipd.

V programskem jeziku **Python pogojne stavke** zapišemo kot je prikazano spodaj.

```py
if x < 1:
	print("Vrednost spremenljivke x je manjša od 1")
elif x < 2:
	print("Vrednost spremenljivke x je med 1 in 2")
else:
	print("Vrednost spremenljivke x večja ali enaka 2")
```

V programskem jeziku **Java pogojne stavke** zapišemo kot je prikazano spodaj.

```java
if (x < 1) {
	System.out.println("Vrednost spremenljivke x je manjša od 1");
}
else if (x < 2) {
	System.out.println("Vrednost spremenljivke x je med 1 in 2");
}
else
	System.out.println("Vrednost spremenljivke x večja ali enaka 2");
```

### Iterativno izvajanje in programske zanke

Programske zanke omogočajo **ponovljeno izvajanje** programske kode dokler velja določen logičen pogoj. Najpogosteje se uporabljajo standardne zanke (tj. `for` in `while` zanke), dočim v večini programskih jezikih obstajajo tudi npr. `do while` zanke in druge. Vse zanke je moč gnezditi ipd.

V programskem jeziku **Python `for` zanko** zapišemo kot je prikazano spodaj.

```py
for i in range(5):
	print("Vrednost spremenljivke i je enaka " + str(i))
```

Ekvivalentno lahko v programskem jeziku **Python `while` zanko** zapišemo kot je prikazano spodaj.

```py
i = 0
while i < 5:
	print("Vrednost spremenljivke i je enaka " + str(i))
	i += 1
```

V programskem jeziku **Java `for` zanko** zapišemo kot je prikazano spodaj.

```java
for (int i = 0; i < 5; i++)
	System.out.println("Vrednost spremenljivke i je enaka " + i);
```

Ekvivalentno lahko v programskem jeziku **Java `while` zanko** zapišemo kot je prikazano spodaj.

```java
int i = 0;
while (i < 5) {
	System.out.println("Vrednost spremenljivke i je enaka " + i);
	i++;
}
```

### Programske metode, procedure in funkcije

Programske metode, procedure in funkcije omogočajo **ponovljeno izvajanje** enake programske kode upoštevajoč podane parametre. Dočim procedure in metode zgolj izvedejo določeno programsko kodo, funkcije poleg tega vrnejo tudi rezultat z uporabo stavka `return`.

V programskem jeziku **Python metodo** zapišemo kot je prikazano spodaj.

```py
def method(i):
	print("Vrednost parametra i je enaka " + str(i))
```

V programskem jeziku **Python funkcijo** zapišemo kot je prikazano spodaj.

```py
def function(i):
	print("Vrednost vhodnega parametra i je enaka " + str(i))
	i += 13
	print("Vrednost rezultata funkcije i je enaka " + str(i))
	return i
```

V programskem jeziku **Java metodo** zapišemo kot je prikazano spodaj.

```java
public static void method(int i) {
	System.out.println("Vrednost parametra i je enaka " + i)
}
```

V programskem jeziku **Java funkcijo** zapišemo kot je prikazano spodaj.

```java
public static int function(int i) {
	System.out.println("Vrednost vhodnega parametra i je enaka " + i);
	i += 13;
	System.out.println("Vrednost rezultata funkcije i je enaka " + i);
	return i;
}
```

_Splošne zbirke podatkov in programske knjižnice bomo obravnavali v nadaljevanju!_