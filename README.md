# Senzorna prenova: kako prebuditi zakrčeno telo in um

Učbenik za 30-dnevni program za zgornji del trupa. Namenjen je udeležencem, ki jih bolijo vrat, ramena, hrbet ali prsni koš. Razloži, zakaj se telo zakrči, kako to povezuje otroštvo, čustva in dih, in kako vaje pomagajo spet čutiti in voditi lastno telo.

Avtor: Peter Karlovšek · 2. izdaja, delovni osnutek (oktober 2026) · delno po gradivu A. Ernsta in V. Cijan (2021).

## Vsebina

- `Senzorna prenova – zgornji del trupa.html`: učbenik v eni datoteki (9 delov, 37 kratkih poglavij, slovar, viri, sledilnik 30 dni). Odprite ga v brskalniku. Ima kazalo ob strani in temni način, sledilnik pa si kljukice zapomni v brskalniku.
- `Senzorna prenova – zgornji del trupa.pdf`: različica za tisk, zgrajena iz HTML. Kazalo ima številke strani.
- `tools/`: orodja za gradnjo PDF.

## Gradnja PDF

Potrebujete Python 3 in Google Chrome (`C:\Program Files\Google\Chrome\Application\chrome.exe`).

```
pip install --target tools/pylib -r tools/requirements.txt
python tools/build_pdf.py
```

Skripta natisne HTML s Chromom brez okna, poišče, na kateri strani se začne vsako poglavje, te številke vpiše v kazalo in natisne še enkrat. PDF nastane ob HTML-ju. Če je PDF odprt v drugem programu, ga zaprite in skripto poženite znova.

Za hiter pregled izbranih strani:

```
python tools/render.py "Senzorna prenova – zgornji del trupa.pdf" tools/build/pregled.png 1,2,3
```

## Pravice

Učbenik je avtorsko delo Petra Karlovška. Brez izrecnega pisnega dovoljenja avtorja ga ni dovoljeno distribuirati, kopirati (delno ali v celoti) ali objavljati.
