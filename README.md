# Senzorna prenova: kako prebuditi zakrčeno telo in um

Učbenik za 30-dnevni program za zgornji del trupa. Namenjen je udeležencem, ki jih bolijo vrat, ramena, hrbet ali prsni koš. Razloži, zakaj se telo zakrči, kako to povezuje otroštvo, čustva in dih, in kako vaje pomagajo spet čutiti in voditi lastno telo.

Avtor: Peter Karlovšek · 2. izdaja, delovni osnutek (oktober 2026) · delno po gradivu A. Ernsta in V. Cijan (2021).

## Vsebina

- `Senzorna prenova – zgornji del trupa.html`: učbenik v eni datoteki (9 delov, 37 kratkih poglavij, slovar, viri, sledilnik 30 dni). Odprite ga v brskalniku. Ima kazalo ob strani in temni način, sledilnik pa si kljukice zapomni v brskalniku.
- `Senzorna prenova – zgornji del trupa.pdf`: različica za tisk, zgrajena iz HTML. Kazalo ima številke strani.
- `Senzorna prenova – čustvena inteligenca.html` in `.pdf`: sestrski priročnik iz iste zbirke (7 delov, 18 kratkih poglavij, tedenski načrt, sledilnik 4 tedni, predloga čustvenega dnevnika). Pet stebrov čustvene inteligence z izhodiščem Senzorne prenove: vsako čustvo se začne v telesu.
- `Senzorna prenova – čustvena inteligenca – mladi.html` in `.pdf`: priročnik za mlade od 12 do 16 let (7 delov, 16 kratkih poglavij s stripi, štiritedenski izziv s štampiljkami, kartica za umirjanje, barvni dnevnik razpoloženja). Analiza, kako pisati za to starost, je v `analiza-prirocnik-za-mlade.md`.
- `index.html`: vstopna stran zbirke s povezavami na vse tri knjige.
- `tools/`: orodja za gradnjo PDF.

## Gradnja PDF

Potrebujete Python 3 in Google Chrome (`C:\Program Files\Google\Chrome\Application\chrome.exe`).

```
pip install --target tools/pylib -r tools/requirements.txt
python tools/build_pdf.py
python tools/build_pdf.py "Senzorna prenova – čustvena inteligenca.html"
python tools/build_pdf.py "Senzorna prenova – čustvena inteligenca – mladi.html"
```

Brez argumenta skripta zgradi učbenik, z argumentom pa PDF iz podanega HTML.

Skripta natisne HTML s Chromom brez okna, poišče, na kateri strani se začne vsako poglavje, te številke vpiše v kazalo in natisne še enkrat. PDF nastane ob HTML-ju. Če je PDF odprt v drugem programu, ga zaprite in skripto poženite znova.

Za hiter pregled izbranih strani:

```
python tools/render.py "Senzorna prenova – zgornji del trupa.pdf" tools/build/pregled.png 1,2,3
```

## Pravice

Učbenik je avtorsko delo Petra Karlovška. Brez izrecnega pisnega dovoljenja avtorja ga ni dovoljeno distribuirati, kopirati (delno ali v celoti) ali objavljati.
