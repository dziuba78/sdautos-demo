# System receptur lakierów AUTOCOLOR / DUXONE

Narzędzie robocze (LibreOffice Calc + Microsoft Excel) do tworzenia, mieszania i analizy własnych receptur lakierniczych.

## Pliki wynikowe

| Plik | Przeznaczenie |
| --- | --- |
| `RECEPTURY_LAKIERY_import.ods` | Aktualny plik roboczy (gdy nie jest zablokowany w LibreOffice) |
| `RECEPTURY_LAKIERY_import_nowy.ods` | Kopia robocza, gdy `import.ods` ma lock (otwierana automatycznie po przebudowie) |
| `RECEPTURY_LAKIERY_dropdown.ods` | Kopia z listami SYSTEM/NR |
| `RECEPTURY_LAKIERY.xlsx` | Ten sam model danych i formuł dla Microsoft Excel |

Oryginalne źródła **nie są zmieniane**. Kopie: `data/backup/`.

## Źródła danych

1. `Sylwek receptury - Wzór autocolor.ods` — kody i katalog Nexa Autocolor (czynnik E z `/E…`)
2. `RECEPTURY DUXONE - Wzór dux.ods` — kody Duxone (drugi arkusz ODS to kopia katalogu Autocolor — **nie** używany jako baza Duxone)
3. `nexa-autocolor-2k-tint-chart-guide.pdf` — nazwy tonerów + procedury dobarwiania Autocolor
4. `Duxone - Tint Descriptions - PL.pdf` — nazwy i procedury dobarwiania Duxone (PL)

Priorytet nazw: **PDF dobarwiania** > katalog ODS. Kolizje (np. `P426-HE02`) są oznaczone, oba warianty zachowane.

## Uruchomienie

1. Otwórz **aktualny** ODS w LibreOffice Calc (konsola przebudowy wypisuje `Aktualny plik roboczy:` — zwykle `RECEPTURY_LAKIERY_import.ods`, przy locku `RECEPTURY_LAKIERY_import_nowy.ods`).
2. Zezwól na makra (lokalny plik, bez sieci).
3. Na arkuszu **START** wybierz system bazowy i wypełnij identyfikację (komórki złote).
4. Wpisz skład na **RECEPTURA_ORYGINALNA** (SYSTEM z listy, potem NR z listy) **albo zaimportuj PDF** (poniżej).
5. Makro `KopiujDoWlasnej` albo przepisz skład na **RECEPTURA_WLASNA** (import PDF kopiuje skład sam).
6. Modyfikuj ilości, dodawaj pigmenty z **drugiego** systemu — to jest dozwolone.
7. Masa docelowa na START (100 / 500 / 1000 / dowolna) — kolumna **ILOŚĆ DO ZWAŻENIA** przelicza na żywo.
8. **ANALIZA** — wykresy, **RAPORT** — wydruk, **HISTORIA** — makro `ZapiszWersje`.

Makra: *Narzędzia → Makra → Uruchom makro → (otwarty ODS) → Standard → modReceptury*

- `NowaReceptura`
- `KopiujDoWlasnej`
- `ZastosujPrzeliczenie`
- `ZapiszWersje`
- `ScalDuplikaty`
- `ImportujZPdf`
- `WczytajOstatniImport`

Arkusze są **bez ochrony** — edycja i zapis (Ctrl+S) bez hasła. Komórki złote = wpis, szare = formuła.

## Import receptury z PDF

1. Na START kliknij **Importuj recepturę z PDF** (albo *Narzędzia → Makra → Uruchom makro → Standard → modReceptury → ImportujZPdf*).
2. Od razu otwiera się **okno Otwórz** LibreOffice/Windows (jak Eksplorator), filtr `PDF (*.pdf)`. Folder startowy: ostatnio użyty, `E:\` albo Dokumenty.
3. Po wyborze pliku parser Python (`scripts/import_receptura_pdf.py`) zapisuje `data/import/ostatni.json` i `ostatni.txt` i wstawia skład.
4. Anulowanie okna **nie czyści** receptury — tylko komunikat informacyjny.
5. Gdy Python nie wstanie **po** wyborze pliku: `python scripts/import_receptura_pdf.py "plik.pdf"`, potem **Wczytaj ostatni import**.
6. Przykład testowy: `data/import/przyklad_receptura_test.pdf`. Przewodnik tint chart **nie** jest recepturą — komunikat „nie znaleziono receptury”, skład nie jest czyszczony.

SYSTEM pigmentu wynika ze **wzorca kodu** (P192/P420/… = AUTOCOLOR, DX/AXT = DUXONE), nie z gołego numeru. Nieznany kod: wiersz zostaje, uwagi `DO WERYFIKACJI`. Bazy pigmentów nie są nadpisywane.

## Klucz pigmentu

`SYSTEM|NR_PIGMENTU` — np. `AUTOCOLOR|P425-900` i `DUXONE|DX5110`.  
Ten sam numer w dwóch systemach to **dwa różne** pigmenty.

## Przebudowa z źródeł

```
python scripts/extract_sources.py
python scripts/build_workbook.py
python scripts/libreoffice_pack.py
python scripts/run_tests.py
```

Wymaga: Python 3, pandas, openpyxl, odfpy, pymupdf, LibreOffice (`C:\Program Files\LibreOffice\program\soffice.exe`).
