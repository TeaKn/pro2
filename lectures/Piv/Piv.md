###### Programiranje 2 2019/20 (Piv)

## Enostavna analiza podatkov v jeziku Python in Corona

Splošnonamenski programski jezik **Python** je trenutno gotovo **najpopularnejši jezik** zaradi enostavne sintakse in obilice prosto-dostopnih programskih knjižnic, dočim pa vsekakor ni najhitrejši jezik. Jezik se interpretira kar pomeni, da program `demo.py` v ukazni vrstici izvedete kot `python demo.py`. 

_Programming is not science, it is a skill! If you want to run as fast as Usain Bolt, you have to do a lot of running. There is no other way! And it is the same with programming. Just run a lot ;)_

### Pomembnost vozlišč v omrežju in mere središčnosti

**Pomembnost vozlišč** omrežja oziroma grafa lahko definiramo na različne načine. Meram pomembnosti vozlišč običajno rečemo **mere središčnosti**. Le-te poskušajo poiskati npr. najbolj vplivne osebe na Instagramu, Facebooku ali Twiterju ter pa tudi osebe, ki jih je potrebno izolirati iz družbe (npr. karantena), da preprečimo (pre)hitro širjenje bolezni kot je Corona virus.

###### Središčnost stopenj vozlišč

Najbolj **osnovna mera pomembnosti** vozlišč je njihova **stopnja**. Le-ta meri število drugih vozlišč, ki spremljajo vplivneža na Instagramu oziroma jih lahko nek bolnik s Corona virusom neposredno okuži.

Naj bo $A$ matrika sosednosti neusmerjenega omrežja in $n$ število vseh vozlišč. Tedaj je **središčnost stopnje vozlišča $i$** definirana kot

$$k_i = \frac{1}{n-1}\sum_{j\neq i}A_{ij}.$$

V priloženi skripti `Piv.py` je stopnja vozlišč realizirana s funkcijo `DC` (angl. _degree centrality_), ki vrne seznam pomembnosti vozlišč po indeksih.

###### Središčnost lastnega vektorja vozlišč

Stopnja vozlišč vse sosede v omrežju obravnava enako, dočim pa so **nekatera vozlišča privzeto bolj "pomembna" kot druga**, ker imajo npr. nekatere osebe v svojem družbenem omrežju več kontaktov kot druge in posledično lažje okužijo več drugih (angl. _super spreader_).

Naj bo $A$ matrika sosednosti neusmerjenega omrežja. Tedaj je **središčnost lastnega vektorja vozlišča $i$** definirana kot

$$e_i = \lambda\sum_{j\neq i}A_{ij} e_j.$$

Opazimo, da je $e$ lastni vektor matrike sosednosti $A$, ki ustreza največji lastni vrednosti $\lambda$.

V priloženi skripti `Piv.py` je središčnost lastnega vektorja vozlišč realizirana s funkcijo `EC` (angl. _eigenvector centrality_), ki vrne seznam pomembnosti vozlišč po indeksih. Funkcija središčnost vozlišč izračuna z uporabo iteracije, ki začenši npr. z enotskim vektorjem poišče prvi lastni vektor matrike sosednosti.

###### Bližinska središčnost vozlišč

Nekatera vozlišča v omrežju so **privzeto bolj "pomembna" kot druga, ker so bližje ostalim vozliščem** v omrežju, npr. nekatere osebe v družbenem omrežju imajo privzeto osrednjo vlogo in tako kratko pot do okužbe vseh ostalih oseb.

Naj bo $A$ matrika sosednosti neusmerjenega omrežja in $n$ število vseh vozlišč. Tedaj je **bližinska središčnost vozlišča $i$** definirana kot

$$c_i = \frac{1}{n-1}\sum_{j\neq i}\frac{1}{d_{ij}},$$

kjer je $d_{ij}$ razdalja med vozliščema $i$ in $j$ (tj. število povezav v najkrajši poti). Pri tem razdaljo med nepovezanima vozliščema $i$ in $j$ definiramo kot $d_{ij}=\infty$.

V priloženi skripti `Piv.py` je bližinska središčnost vozlišč realizirana s funkcijo `CC` (angl. _closeness centrality_), ki vrne seznam pomembnosti vozlišč po indeksih. Funkcija središčnost vozlišč izračuna z uporabo preiskovanja v širino začenši v vsakem vozlišču omrežja.

###### Google PageRank ocena vozlišč

Verjetno **najbolj znana mera središčnosti vozlišč je PageRank ocena**, ki se navadno uporablja za določanje pomembnosti na spletu. PageRank ocena je dejansko algoritem, ki je pred dvajsetimi leti "ustvaril" Google. Verjetno pa PageRank ocena ni najboljša mera za npr. odkrivanje oseb, ki najhitreje širijo Corona virus.

Naj bo $A$ matrika sosednosti neusmerjenega omrežja in $n$ število vseh vozlišč v omrežju. Tedaj je **PageRank ocena vozlišča $i$** definirana kot

$$p_i = \frac{1-\alpha}{n}+\alpha\sum_jA_{ij}\frac{p_j}{k_j},$$

kjer je $k_j$ stopnja vozlišča $j$ in $\alpha$ konstanta navadno nastavljena na $\alpha=0.85$.

V priloženi skripti `Piv.py` je PageRank ocena vozlišč realizirana s funkcijo `PR` (angl. _PageRank score_), ki vrne seznam pomembnosti vozlišč po indeksih. Funkcija središčnost vozlišč izračuna z uporabo iteracije, ki začenši z enotskim vektorjem poišče prvi lastni vektor Google matrike.

### Pomembnost vozlišč v realnih omrežjih

Priložena skripta `Piv.py` najprej **izpiše deset najpomembnejših vozlišč** glede na zgornje mere v treh realnih omrežjih. To so omrežje prijateljstev med delfini, Twitter okolica predavatelja predmeta in omrežje sodelovanj med filmskimi igralci. Priložena je tudi grafična predstavitev manjših omrežij.

Skripta nato iz spletnega vira prebere podatkih o **umorih in ubojih v seriji _Game of Thrones_**, ki jih predstavi z omrežjem in poišče najpomembnejša vozlišča.

![GoT kills](got_kills.pdf)