# Analiza źródeł i modelu danych

## 1. Struktura plików źródłowych

Oryginały **nie były modyfikowane**. Kopie: `data/backup/`.

### AUTOCOLOR — `Sylwek receptury - Wzór autocolor.ods`

| Arkusz | Zawartość |
| --- | --- |
| Arkusz1 | Szablon roboczy receptury. Kolumna 26 (AA): 96 unikalnych kodów `P…`. Nagłówki: Pigment, Oryginalna receptura, Receptura po zmianach, Dozowanie, ILOŚĆ/LITR, KOD, DATA. |
| NEXA AUTOCOLOR® CAR | Katalog: kod z czynnikiem E (`P192-475/E1`), numer (`P192-475` / `P420-902RT`), nazwa (`2K REGULATOR BAZY`). 96 rekordów. 2 komórki z błędem `Błąd:504` (puste wiersze — pominięte). |

Czynnik E wyciągnięty z sufiksu `/E`. Jednostka robocza: **g**.

### DUXONE — `RECEPTURY DUXONE - Wzór dux.ods`

| Arkusz | Zawartość |
| --- | --- |
| Arkusz1 | Szablon. Kolumna 26: **79** kodów `DX…`, `DX11`, `AXT100–AXT110`. |
| NEXA AUTOCOLOR® CAR | **Identyczna kopia katalogu AUTOCOLOR.** Nie stanowi bazy Duxone. |

W ODS Duxone **brak nazw** pigmentów.

### PDF (priorytet nazw i procedur)

- `nexa-autocolor-2k-tint-chart-guide.pdf` (2 strony) — Tinting Guide Nexa Autocolor 2K: nazwy, face/flop, reguły RT 10%.
- `Duxone - Tint Descriptions - PL.pdf` (56 stron) — reguły korygowania + opisy DX (kąty 15°/45°/110°).

Kody z PDF spoza ODS (np. `P420-982`, `VM4370`, `P434-CS31`) dodane ze statusem `DODANY Z PDF`. Rekordów ODS nie usunięto.

## 2. Struktura skoroszytu

`RECEPTURY_LAKIERY.ods` / `.xlsx`

1. START — identyfikacja, system bazowy, masa docelowa, KPI, nawigacja  
2. RECEPTURA_ORYGINALNA  
3. RECEPTURA_WLASNA  
4. ANALIZA — 4 wykresy  
5. RAPORT — A4 poziomo  
6. HISTORIA + HISTORIA_POZYCJE  
7. DOBARWIANIE — PDF lookup + reguły  
8. BAZA_AUTOCOLOR / BAZA_DUXONE  
9. PIGMENTY — unia obu baz + filtr  
10. USTAWIENIA  
11. DANE_WYKRESOW, LISTY (ukryte)

## 3. Działanie

- System bazowy receptury i system pigmentu są niezależne — mieszanie AUTOCOLOR/DUXONE jest zamierzone.
- Klucz: `SYSTEM|NR_PIGMENTU`.
- Nazwa / jednostka: `WYSZUKAJ.PIONOWO` / `VLOOKUP` po kluczu (bez FILTER/XLOOKUP).
- STATUS: BEZ ZMIAN / ZWIĘKSZONO / ZMNIEJSZONO / DODANO / USUNIĘTO.
- ILOŚĆ DO ZWAŻENIA = ilość własna × masa docelowa / masa własna (zabezpieczenie /0).
- Duplikat klucza → `DUPLIKAT` (makro `ScalDuplikaty` sumuje).
- Suma %: tolerancja z USTAWIENIA; komunikat `RECEPTURA POPRAWNA` albo `UWAGA — SUMA UDZIAŁÓW = …`.

## 4. Formuły (Excel EN, LibreOffice czyta z XLSX)

`IF`, `IFERROR`, `VLOOKUP`, `SUMIF`, `COUNTIF`, `INDIRECT`, `SUM`, `N`, `TODAY`, `TEXT`, `ABS`, `MAX`, `ISERROR`, `OR`, `AND`, `NA`.

Listy zależne NR: `INDIRECT("Lista_"&B12)` + zakresy `Lista_AUTOCOLOR` / `Lista_DUXONE`.

## 5. Makra

LibreOffice StarBasic: `macros/modReceptury.bas` w ODS (`Standard.modReceptury`).

`NowaReceptura`, `KopiujDoWlasnej`, `ZastosujPrzeliczenie`, `ZapiszWersje`, `ScalDuplikaty`.  
Bez sieci, bez kodu zewnętrznego. XLSX działa na samych formułach.

## 6. Testy

`python scripts/run_tests.py` — **58/58 OK** (struktura, matematyka, przeliczenie LibreOffice: Testy 1–14).

## 7. Wykryte problemy i rozwiązania

| Problem | Rozwiązanie |
| --- | --- |
| Drugi arkusz ODS Duxone = kopia Autocolor | Baza Duxone z kodów Arkusz1 + nazwy z PDF PL |
| Brak Excel COM | LibreOffice headless (`soffice.exe`) |
| FILTER/XLOOKUP nie w Calc | VLOOKUP + INDIRECT + COUNTIF/SUMIF |
| Nazwy Duxone nadpisywane diagramami PDF | Nie nadpisuj pełnej nazwy pustą |
| `P426-HE02` ODS ≠ PDF | Status `KOLIZJA NAZW`, obie nazwy w kolumnach |
| AXT100–110, DX11, DX5155, DX5216 bez PDF | `DO WERYFIKACJI` — bez zgadywania z internetu |
| Tabele Excel słabo w Calc | Nazwane zakresy, 40 wierszy roboczych |

## 8. Ochrona

Arkusze bez ochrony (priorytet: edycja i zapis bez hasła). Komórki złote = wpis. Szare = formuła.
