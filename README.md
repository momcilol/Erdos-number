# Erdos-number

## Projekat iz Veštačke inteligencije
Na osnovu data seta [dblp](https://dblp.org/) napraviti program koji pronalazi najkraću putanju od datog profesora do Paula Erdösa.  

### Priprema podataka

#### Sređivanje podataka
Pomoću skripti **`prepare_xml.sh`** i **`quot.sh`** i još malo sređivanja dobili smo pročišćen **`dblp.xml`** fajl.

#### Izbor baze
Kako je dataset prevelik (**`dblp.xml 3.5 GB`**) a zadatak u sebi sadrži rad sa grafovima, prirodno je bilo izabrati neku grafovsku bazu iz koje ćemo čitati podatke. U ovom projektu korišćena je [**`NEO4J`**](https://neo4j.com/) grafovska baza.

#### Parsiranje i ubacivanje podataka
Kako se paralelno parsiranje podataka iz `xml` fajla i ubacivanje u bazu pokazalo kao veoma sporo (1% na ~3.5h), pribegli smo učitavanju preko `csv` fajla. Za parsiranje i prebacivanje podataka iz `xml` u `csv` fajl koristili smo **`another_try.py`** python skriptu, a za ubacivanje podataka u bazu pokrenut je upit dat u fajlu **`import_cooperations.cyp `**.

### Program
Program **`erdos_number.py`** je osmišljen kao konzolna aplikacija koja se koristi prema uputstvima datim prilikom pokretanja programa.

#### Pretrage
Program obuhvata implementacije pretraga:
1. Breadth First Search (BFS)
2. Iterative Deepening Search(IDS)
3. Bidirectional Breadth First Search (BBFS)

#### Rad programa
U fajlu **`output_erdos_number.txt`** dato je jedno izvršavanje programa.
