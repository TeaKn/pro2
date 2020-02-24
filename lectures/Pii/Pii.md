###### Programiranje 2 2019/20 (Pii)

## Delo s podatki v programskem jeziku Python

Splošnonamenski programski jezik **Python** je trenutno gotovo **najpopularnejši jezik** zaradi enostavne sintakse in obilice prosto-dostopnih programskih knjižnic, dočim pa vsekakor ni najhitrejši jezik. Jezik se interpretira kar pomeni, da program `demo.py` v ukazni vrstici izvedete kot `python demo.py`. 

_Programming is not science, it is a skill! If you want to run as fast as Usain Bolt, you have to do a lot of running. There is no other way! And it is the same with programming. Just run a lot ;)_

### Programske knjižnice in skripte

V programskem jeziku **Python knjižnice in skripte** uvozimo z ukazom `import`. Knjižnice je potrebno uvoziti pred uporabo, dočim obstajajo različne oblike uporabe ukaza `import`.

```py
import mycode
import requests
import requests as req
from requests import *
```

### Anonimne lambda funkcije

V programskem jeziku **Python lambda funkcije** navadno uporabimo, ko le-to potrebujemo le "enkrat" in jih ne želimo definirati z uporabo ukaza `def`. Lambda funkcije izvirajo iz 30. let prejšnjega stoletja, ko so teoretični računalničarji začeli razmišljati o zgradbi sodobnega računalnika.

```py
inc = lambda x: x + 1
print(inc(0))
print((lambda x: x + 1)(0))

pow = lambda x, y: x**y
print(pow(2, 10))

def func(x):
  return lambda y: x * y
double = func(2)
print(double(10))
```

### Izvajanje programskih zank

V programskem jeziku **Python** lahko **programske zanke** predčasno zaključimo z uporabo ukaza `break`, dočim lahko novo iteracijo zanke predčasno pričnemo z uporabo ukaza `continue`.

### Programske zbirke podatkov

V programskem jeziku **Python nabor** določimo z običajnimi oklepaji `(...)` pri čimer ni potrebno, da so elementi nabora enakega tipa. Nabor je **urejena nesprejemljiva zbirka** podatkov kar pomeni, da _ne moremo_ dodajati ali brisati elementov.

```py
t = (0, 1, 'foo', 'bar')
st = t[:2]
ln = len(t)
```

V programskem jeziku **Python seznam** določimo z oglatimi oklepaji `[...]` pri čimer ni potrebno, da so elementi seznama enakega tipa. Seznam je **urejena sprejemljiva zbirka** podatkov kar pomeni, da _lahko_ dodajamo ali brišemo elemente po vrednosti in indeksu.

```py
l = [0, 1, 'foo', 'bar']
sl = l[:2]
ln = len(l)
l[1] = -1
del l[0]
l.remove(-1)
l.append(9.81)
l.extend([0, 'baz'])
```

V programskem jeziku **Python množico** določimo z zavitimi oklepaji `{...}` ali ukazom `set()` pri čimer ni potrebno, da so elementi množice enakega tipa. Množica je **neurejena sprejemljiva zbirka** podatkov kar pomeni, da _lahko_ dodajamo ali brišemo elemente po vrednosti.

```py
s = {0, 1, 'foo', 'bar'}
ln = len(s)
s.remove(1)
s.add(9.81)
s.update([0, 'baz'])
```

V programskem jeziku **Python slovar** določimo z zavitimi oklepaji `{...}` ali ukazom `dict()` pri čimer ni potrebno, da so ključi ali vrednosti slovarja enakega tipa. Slovar je **neurejena sprejemljiva zbirka** podatkov kar pomeni, da _lahko_ dodajamo ali brišemo vrednosti po ključu.

```py
d = {0: 'foo', 'bar': 1}
ln = len(d)
d[1] = 'baz'
d.pop('bar')
d.update({'bar': 1})
l = dict.values()
l = dict.keys()
```

V programskem jeziku **Python zbirko uredimo** z uporabo funkcije `sorted`, ki vrne urejen seznam elementov, dočim morajo biti elementi enakega tipa. Na drugi strani pa metoda `shuffle` ustvari naključno permutacijo elementov seznama, dočim ni potrebno, da so elementi enakega tipa.

```py
s = {'foo', 'bar', 'baz'}
l = sorted(s)

import random
random.shuffle(l)
```

Kaj pa vrne funkcija `enumerate`, če jo uporabimo nad **Python zbirko**? Le-ta se izkaže kot uporabno, ko iteriramo čez elemente zbirke in hkrati potrebujemo indeks (tj. zaporedno številko) elementa.

### Branje podatkov iz datoteke

V programskem jeziku **Python datoteko odpremo** s funkcijo `open`, **beremo** z uporabo funkcij `read` ali `readline` in **zapremo** z metodo `close`. Pri tem je priporočena uporaba programskega konstrukta `with open(..., 'r') as ...`, ki po koncu branja samodejno zapre datoteko. Vsebino datoteke lahko preberemo v celoti, dočim navadno beremo zaporedoma po vrsticah.

```py
file = open('file.txt', 'r')
print(file.readline())
print(file.read())
file.close()

file = open('file.txt', 'r')
for line in file:
  print(line)
file.close()

with open('file.txt', 'r') as file:
	for line in file:
		print(line)
```

### Pisanje podatkov v datoteko

V programskem jeziku **Python datoteko odpremo** s funkcijo `open`, **pišemo** z uporabo metode `write` in **zapremo** z metodo `close`. Pri tem je priporočena uporaba programskega konstrukta `with open(..., 'w'|'a') as ...`, ki po koncu pisanja samodejno zapre datoteko. Vsebino datoteke lahko zapišemo v celoti, dočim navadno pišemo zaporedoma po vrsticah.

```py
file = open('file.txt', 'w')
print(file.write('line\nline\n'))
print(file.write('line\n'))
file.close()

with open('file.txt', 'w') as file:
	for i in range(10):
		file.write('{0:d}. line\n'.format(i + 1))
```

### Luščenje vsebine spletnih strani

V programskem jeziku **Python spletno stran** lahko preberemo z uporabo programskih knjižnic `http.client`, `requests` in drugih. Pri tem spletno stran vedno preberemo v celoti, dočim lahko naknadno iteriramo po vsebini spletne strani z uporabo programskih zank.

Primer uporabe **Python knjižnice `http.client`** je prikazan spodaj.

```py
import http.client
conn = http.client.HTTPSConnection('urnik.fmf.uni-lj.si')
conn.request('GET', '/letnik/11/')
text = conn.getresponse().read().decode()
for char in text:
  print(char)
```

Primera uporabe **Python knjižnice `requests`** je prikazan spodaj.

```py
import requests
req = requests.get('https://urnik.fmf.uni-lj.si/letnik/11/')
text = req.text
for char in text:
  print(char)
  
req = requests.get('http://ip.jsontest.com/')
json = req.json()
for element in json:
  print(element)
```

### Razčlenjevanje nizov z regularnimi izrazi

V programskem jeziku **Python regularne izraze** uporabljamo za razpoznavanje, razčlenjevanje in iskanje nizov znakov. Regularni izraz predstavlja želeni oziroma iskani vzorec znakov, ki ga definiramo kot `r'...'`. Pri tem lahko uporabljamo rezervirane znake oziroma vzorce naštete spodaj.

+ `.` predstavlja poljuben znak razen nove vrstice
+ `^` predstavlja začetek niza znakov ali vrstice
+ `$` predstavlja konec niza znakov ali vrstice
+ `\d` predstavlja poljubno števko ali cifro
+ `\D` predstavlja poljubno neštevko ali necifro
+ `\w` predstavlja poljuben alfanumerični znak
+ `\W` predstavlja poljuben nealfanumerični znak
+ `\s` predstavlja poljuben beli znak (npr. presledek)
+ `\S` predstavlja poljuben nebeli znak (npr. števko)
+ `\` omogoča iskanje ubežnih znakov (npr. `r'\.'`)

(Rezervirane) znake oziroma vzorce lahko združujemo, ponavljamo in gnezdimo kot je našteto spodaj.

+ `(...)` predstavlja zaporednje znakov (npr. `r'(abcd)'`)
+ `[...]` predstavlja množico znakov (npr. `r'[a-zA-Z]'`)
+ `[^...]` predstavlja negacijo znakov (npr. `r'[^a-d]'`)
+ `|` predstavlja disjunkcijo znakov (npr. `r'\d|[a-cd]'`)
+ `*` predstavlja nič ali več ponovitev vzorca (npr. `r'\d*'`)
+ `+` predstavlja eno ali več ponovitev vzorca (npr. `r'[abc]+'`)
+ `?` predstavlja največ eno ponovitev vzorca (npr. `r'[a-c]?'`)
+ `{n}` predstavlja natanko $n$ ponovitev vzorca (npr. `r'[a-c]{3}'`)
+ `{n,m}` predstavlja med $n$ in $m$ ponovitev vzorca (npr. `r'[a-c]{1,3}'`)

Pri delu z regularnimi izrazi navadno uporabljamo **Python knjižnico `re`**. 

**Funkcija `match`** preveri ali _začetek_ niza znakov ustreza podanemu regularnemu izrazu. Funkcija vrne `None`, če se niz ne začne z regularnim izrazom, sicer pa objekt razreda `Match`, ki vrne ujemanje z uporabo funkcije `group`.

```py
import re
string = '-123.45'
regex = r'[+-]?[1-9][0-9]*'
res = re.match(regex, string)
if res == None:
	print('Not an integer!')
else:
	print(res.group())
```

**Funkcija `search`** preveri ali niz znakov _vsebuje_ podani regularni izraz. Funkcija vrne `None`, če niz ne vsebuje regularnega izraza, sicer pa objekt razreda `Match`, ki vrne ujemanje z uporabo funkcije `group`.

```py
import re
string = 'Is this an integer -123?'
regex = r'[+-]?[1-9][0-9]*'
res = re.search(regex, string)
if res == None:
	print('No integer found!')
else:
	print(res.group())
```

**Funkcija `findall`** poišče vse _pojavitve_ podanega regularnega izraza v nizu znakov. Funkcija vrne seznam ujemanj regularnega izraza, ki je lahko prazen.

```py
import re
string = 'Find all integers -123.45!'
regex = r'[+-]?[1-9][0-9]*'
res = re.findall(regex, string)
for int in res:
	print(int)
```

**Funkcija `split`** _razbije_ niz znakov glede na podan regularni izraz. Funkcija vrne seznam razbitja niza znakov, ki je lahko prazen.

```py
import re
string = 'Split by integers -123 and 45!'
regex = r'[+-]?[1-9][0-9]*'
res = re.split(regex, string)
for str in res:
	print(str)
```

**Funkcija `sub`** _zamenja_ vse pojavitve podanega regularnega izraza v nizu znakov. Pri tem lahko zamenjavo določimo kot niz znakov...

```py
import re
string = 'Replace integers -123 and 45!'
regex = r'[+-]?[1-9][0-9]*'
res = re.sub(regex, '<int>', string)
print(res)
```

...ali pa zamenjavo določimo z uporabo podane funkcije.


```py
import re
string = 'Replace integers -123 and 45!'
regex = r'[+-]?[1-9][0-9]*'
def replace(res):
	return 'x' * len(res.group())
res = re.sub(regex, replace, string)
print(res)
```

Pri delu z regularnimi izrazi si pomagajte z **dokumentacijo knjižnice `re`** dostopno na naslovu [https://docs.python.org/3.7/library/re.html](https://docs.python.org/3.7/library/re.html).