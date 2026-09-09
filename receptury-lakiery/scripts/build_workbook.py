# -*- coding: utf-8 -*-
"""Budowa skoroszytu RECEPTURY_LAKIERY — kompatybilny z LibreOffice Calc i Excelem."""
from __future__ import annotations

import json
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.series import DataPoint
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import (
    Alignment,
    Border,
    Font,
    PatternFill,
    Protection,
    Side,
)
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.page import PageMargins
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.chart.legend import Legend

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data" / "extracted" / "pigmenty.json").read_text(encoding="utf-8"))
OUT_XLSX = ROOT / "RECEPTURY_LAKIERY.xlsx"

N = 40  # wiersze robocze receptury
R0 = 12  # pierwszy wiersz danych
R1 = R0 + N - 1  # 51
H0 = 12  # historia
HN = 200

NAVY = "1B2A4A"
NAVY2 = "243656"
GOLD = "C4A35A"
INPUT = "FFF4D0"
FORMULA = "F3F5F8"
WHITE = "FFFFFF"
LINE = "C5CDD6"
OK_GREEN = "C6EFCE"
WARN = "FCE4D6"
RED_SOFT = "F4CCCC"
BLUE_SOFT = "D6EAF8"
AMBER = "FFE699"
GRAY = "E8E8E8"

thin = Border(
    left=Side(style="thin", color=LINE),
    right=Side(style="thin", color=LINE),
    top=Side(style="thin", color=LINE),
    bottom=Side(style="thin", color=LINE),
)
thick_bottom = Border(bottom=Side(style="medium", color=GOLD))


def font_title():
    return Font(name="Calibri", size=18, bold=True, color=WHITE)


def font_h():
    return Font(name="Calibri", size=11, bold=True, color=WHITE)


def font_label():
    return Font(name="Calibri", size=10, bold=True, color=NAVY)


def font_n():
    return Font(name="Calibri", size=10, color="222222")


def fill(hex_color: str) -> PatternFill:
    return PatternFill("solid", fgColor=hex_color)


def align_c():
    return Alignment(horizontal="center", vertical="center", wrap_text=True)


def align_l():
    return Alignment(horizontal="left", vertical="center", wrap_text=True)


def banner(ws, title: str, last_col: str, subtitle: str = ""):
    ws.merge_cells(f"A1:{last_col}1")
    ws["A1"] = title
    ws["A1"].font = font_title()
    ws["A1"].fill = fill(NAVY)
    ws["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[1].height = 28
    ws.merge_cells(f"A2:{last_col}2")
    ws["A2"] = subtitle
    ws["A2"].font = Font(name="Calibri", size=10, italic=True, color=NAVY)
    ws["A2"].fill = fill("EEF1F6")
    ws.row_dimensions[2].height = 18
    for col in range(1, 20):
        ws.cell(1, col).fill = fill(NAVY)
        ws.cell(2, col).fill = fill("EEF1F6")


def header_row(ws, row: int, headers: list[str], widths: list[float]):
    for i, (h, w) in enumerate(zip(headers, widths), 1):
        cell = ws.cell(row, i, h)
        cell.font = font_h()
        cell.fill = fill(NAVY2)
        cell.alignment = align_c()
        cell.border = thin
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[row].height = 32
    ws.freeze_panes = f"A{row + 1}"
    ws.auto_filter.ref = f"A{row}:{get_column_letter(len(headers))}{row + N}"


def style_input(cell):
    cell.fill = fill(INPUT)
    cell.protection = Protection(locked=False)
    cell.font = font_n()
    cell.border = thin
    cell.alignment = Alignment(horizontal="left", vertical="center")


def style_formula(cell, num_fmt=None):
    cell.fill = fill(FORMULA)
    cell.protection = Protection(locked=True)
    cell.font = font_n()
    cell.border = thin
    if num_fmt:
        cell.number_format = num_fmt


def style_meta_bar(ws, last_col: str):
    """Pasek identyfikacji receptury w wierszach 3–5."""
    labels = [
        (3, "A", "Nazwa", "C", "Meta_Nazwa"),
        (3, "E", "Numer", "F", "Meta_Numer"),
        (3, "H", "System", "I", "Meta_System"),
        (4, "A", "Kolor", "C", "Meta_Kolor"),
        (4, "E", "Kod koloru", "F", "Meta_Kod"),
        (4, "H", "Wersja", "I", "Meta_Wersja"),
        (5, "A", "Producent", "C", "Meta_Producent"),
        (5, "E", "Autor", "F", "Meta_Autor"),
        (5, "H", "Data", "I", "Meta_Data"),
    ]
    for row, lab_col, lab, val_col, _name in labels:
        lc = ws[f"{lab_col}{row}"]
        lc.value = lab
        lc.font = font_label()
        lc.fill = fill("EEF1F6")
        # wartość = odwołanie do START (nadpiszemy po utworzeniu START)
    ws.row_dimensions[3].height = 20
    ws.row_dimensions[4].height = 20
    ws.row_dimensions[5].height = 20
    ws.merge_cells("A6:" + last_col + "6")
    ws["A6"] = ""
    ws["A6"].fill = fill(GOLD)
    ws.row_dimensions[6].height = 6


def protect(ws):
    """Arkusze bez ochrony — pełna edycja i zapis (Ctrl+S) bez hasła.

    Kolory zostają: złote = wpis, szare = formuła. Flagi locked na komórkach
    nie blokują edycji, dopóki arkusz nie jest chroniony.
    """
    ws.protection.sheet = False
    try:
        ws.protection.disable()
    except Exception:
        pass


def add_dv_list(ws, formula: str, sqref: str, allow_blank=True):
    dv = DataValidation(
        type="list",
        formula1=formula,
        allow_blank=allow_blank,
        showDropDown=False,
        showErrorMessage=True,
        errorTitle="Niedozwolona wartość",
        error="Wybierz wartość z listy.",
        promptTitle="Wybór",
        prompt="Wybierz z listy rozwijanej.",
        showInputMessage=True,
    )
    dv.add(sqref)
    ws.add_data_validation(dv)
    return dv


def add_dv_decimal(ws, sqref: str):
    dv = DataValidation(
        type="decimal",
        operator="greaterThanOrEqual",
        formula1="0",
        allow_blank=True,
        showErrorMessage=True,
        errorTitle="Ilość ujemna",
        error="Ilość nie może być ujemna.",
    )
    dv.add(sqref)
    ws.add_data_validation(dv)


def kod_z_pola_nr(cell: str) -> str:
    """Z komórki NR: goły kod albo etykieta 'P425-900 | nazwa' → sam kod (klucz VLOOKUP)."""
    return f'IF(ISNUMBER(FIND(" | ",{cell})),TRIM(LEFT({cell},FIND(" | ",{cell})-1)),{cell})'


def fill_sidelists(ws):
    """Kolumny T/U na arkuszu receptury — źródło strzałki dropdown w Calc.

    Calc pokazuje listę rozwijaną tylko przy zwykłym zakresie komórek
    (nie przy INDIRECT). Makro podmienia T (AUTOCOLOR) ↔ U (DUXONE) wg SYSTEM.
    Kolumn nie ukrywać — ukryte źródło też gubi strzałkę.
    """
    ac = DATA["autocolor"]
    dx = DATA["duxone"]
    ws.cell(8, 20, "LISTA_AC")
    ws.cell(8, 21, "LISTA_DX")
    ws.cell(8, 20).font = font_h()
    ws.cell(8, 21).font = font_h()
    ws.cell(8, 20).fill = fill(NAVY2)
    ws.cell(8, 21).fill = fill(NAVY2)
    for i, rec in enumerate(ac):
        nr = rec["nr_pigmentu"]
        naz = (rec.get("nazwa") or "").strip()
        ws.cell(9 + i, 20, f"{nr} | {naz}" if naz else nr)
    for i, rec in enumerate(dx):
        nr = rec["nr_pigmentu"]
        naz = (rec.get("nazwa") or "").strip()
        ws.cell(9 + i, 21, f"{nr} | {naz}" if naz else nr)
    ws.column_dimensions["T"].width = 36
    ws.column_dimensions["U"].width = 36


def add_dv_nr_pigmentu(ws, sqref: str, system_cell: str = "$B12"):
    """Dropdown NR: zwykły zakres $T$9:$T$n (AUTOCOLOR).

    Calc nie rysuje strzałki przy INDIRECT. Makro SelectionChanged / on-change
    ustawia $U$9:$U$n gdy SYSTEM=DUXONE w tym wierszu.
    """
    last_ac = 8 + len(DATA["autocolor"])
    dv = DataValidation(
        type="list",
        formula1=f"=$T$9:$T${last_ac}",
        allow_blank=True,
        showDropDown=False,
        showErrorMessage=False,
        showInputMessage=True,
        promptTitle="NR PIGMENTU",
        prompt="Kliknij komórkę — lista pigmentów z SYSTEMU tego wiersza (AUTOCOLOR albo DUXONE).",
    )
    dv.add(sqref)
    ws.add_data_validation(dv)
    return dv


def status_cf(ws, col_letter: str):
    rng = f"{col_letter}{R0}:{col_letter}{R1}"
    rules = [
        ("BEZ ZMIAN", GRAY, "333333"),
        ("ZWIĘKSZONO", OK_GREEN, "006100"),
        ("ZMNIEJSZONO", AMBER, "9C5700"),
        ("DODANO", BLUE_SOFT, "1F4E79"),
        ("USUNIĘTO", RED_SOFT, "9C0006"),
    ]
    for text, bg, fg in rules:
        ws.conditional_formatting.add(
            rng,
            CellIsRule(
                operator="equal",
                formula=[f'"{text}"'],
                fill=fill(bg),
                font=Font(name="Calibri", size=10, bold=True, color=fg),
            ),
        )


def write_bases(wb):
    ac = DATA["autocolor"]
    dx = DATA["duxone"]
    headers = [
        "KLUCZ",
        "SYSTEM",
        "NR_PIGMENTU",
        "NR_BAZOWY",
        "KOD_E",
        "CZYNNIK_E",
        "NAZWA",
        "NAZWA_ODS",
        "NAZWA_PDF",
        "OPIS_DOBARWIANIA",
        "JEDNOSTKA",
        "KATEGORIA",
        "STATUS_DANYCH",
        "UWAGI_DANYCH",
        "ZRODLO_NAZWY",
        "W_KATALOGU_ODS",
        "W_SZABLONIE_ODS",
        "OPIS_EN",
        "OPIS_DZIALANIA_PL",
    ]
    widths = [22, 14, 16, 14, 18, 12, 36, 36, 36, 55, 12, 18, 16, 40, 16, 14, 16, 50, 55]

    def dump(ws, rows, title):
        banner(
            ws,
            title,
            "S",
            "Kopia robocza bazy. Oryginalne pliki ODS/PDF nie są zmieniane. Klucz = SYSTEM|NR_PIGMENTU. "
            "AUTOCOLOR: OPIS_DOBARWIANIA i OPIS_DZIALANIA_PL po polsku (tint chart); nazwy katalogowe EN. DUXONE: opisy z PDF PL.",
        )
        for i, h in enumerate(headers, 1):
            cell = ws.cell(8, i, h)
            cell.font = font_h()
            cell.fill = fill(NAVY2)
            cell.alignment = align_c()
            cell.border = thin
            ws.column_dimensions[get_column_letter(i)].width = widths[i - 1]
        ws.freeze_panes = "A9"
        ws.auto_filter.ref = f"A8:S{8 + len(rows)}"
        for r_i, rec in enumerate(rows, 9):
            opis_pl = rec.get("opis_dzialania_pl") or rec.get("procedura_dobarwiania") or rec.get("opis") or ""
            vals = [
                rec["klucz"],
                rec["system"],
                rec["nr_pigmentu"],
                rec["nr_bazowy"],
                rec.get("kod_e") or "",
                rec.get("czynnik_e") if rec.get("czynnik_e") is not None else "",
                rec["nazwa"],
                rec.get("nazwa_ods") or "",
                rec.get("nazwa_pdf") or "",
                rec.get("procedura_dobarwiania") or rec.get("opis") or "",
                rec.get("jednostka") or "g",
                rec.get("kategoria") or "",
                rec.get("status_danych") or "",
                rec.get("uwagi_danych") or "",
                rec.get("zrodlo_nazwy") or "",
                "TAK" if rec.get("w_katalogu_ods") else "NIE",
                "TAK" if rec.get("w_szablonie_ods") else "NIE",
                rec.get("opis_en") or "",
                opis_pl,
            ]
            for c_i, v in enumerate(vals, 1):
                cell = ws.cell(r_i, c_i, v)
                cell.font = font_n()
                cell.border = thin
                cell.alignment = Alignment(vertical="center", wrap_text=True)
                cell.protection = Protection(locked=True)
                if rec.get("status_danych") == "KOLIZJA NAZW":
                    cell.fill = fill(AMBER)
                elif rec.get("status_danych") == "DO WERYFIKACJI":
                    cell.fill = fill(WARN)
                elif rec.get("status_danych") == "DODANY Z PDF":
                    cell.fill = fill(BLUE_SOFT)
                else:
                    cell.fill = fill(WHITE)
            ws.row_dimensions[r_i].height = 48
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        protect(ws)
        return len(rows)

    ws_ac = wb.create_sheet("BAZA_AUTOCOLOR")
    n_ac = dump(ws_ac, ac, "BAZA AUTOCOLOR — Nexa Autocolor 2K")
    ws_dx = wb.create_sheet("BAZA_DUXONE")
    n_dx = dump(ws_dx, dx, "BAZA DUXONE — Axalta Duxone")
    return n_ac, n_dx


def write_pigmenty(wb, n_ac, n_dx):
    ws = wb.create_sheet("PIGMENTY", 0)
    banner(
        ws,
        "PIGMENTY — wspólna baza wyszukiwania",
        "N",
        "Filtruj kolumnę SYSTEM (AUTOCOLOR / DUXONE) oraz NR / NAZWA. AUTOCOLOR 123 i DUXONE 123 to dwa różne pigmenty. Opisy dobarwiania Autocolor — po polsku.",
    )
    ws["A4"] = "INSTRUKCJA"
    ws["A4"].font = font_label()
    ws.merge_cells("B4:N4")
    ws["B4"] = (
        "Włącz filtry w wierszu 8. SYSTEM: AUTOCOLOR lub DUXONE. Wyszukaj numer lub nazwę. "
        "Nie wpisuj numerów ręcznie w recepturze — wybierz SYSTEM, potem NR z listy rozwijanej. "
        "AUTOCOLOR: nazwa katalogowa EN, opis działania PL (kolumna OPIS_DOBARWIANIA)."
    )
    ws["B4"].alignment = align_l()
    headers = [
        "KLUCZ",
        "SYSTEM",
        "NR_PIGMENTU",
        "NAZWA",
        "JEDNOSTKA",
        "CZYNNIK_E",
        "KATEGORIA",
        "STATUS_DANYCH",
        "OPIS_DOBARWIANIA",
        "ZRODLO_NAZWY",
        "NAZWA_ODS",
        "NAZWA_PDF",
        "OPIS_EN",
        "OPIS_DZIALANIA_PL",
    ]
    widths = [22, 14, 16, 36, 12, 12, 22, 16, 55, 16, 32, 32, 50, 55]
    for i, (h, w) in enumerate(zip(headers, widths), 1):
        cell = ws.cell(8, i, h)
        cell.font = font_h()
        cell.fill = fill(NAVY2)
        cell.alignment = align_c()
        cell.border = thin
        ws.column_dimensions[get_column_letter(i)].width = w
    # formuły ściągające z obu baz (INDEX — bez FILTER)
    total = n_ac + n_dx
    for i in range(total):
        r = 9 + i
        if i < n_ac:
            src = f"BAZA_AUTOCOLOR"
            sr = 9 + i
        else:
            src = f"BAZA_DUXONE"
            sr = 9 + (i - n_ac)
        mapping = [1, 2, 3, 7, 11, 6, 12, 13, 10, 15, 8, 9, 18, 19]
        for c, src_c in enumerate(mapping, 1):
            cell = ws.cell(r, c, f"={src}!{get_column_letter(src_c)}{sr}")
            style_formula(cell)
            cell.alignment = Alignment(vertical="center", wrap_text=True)
        ws.row_dimensions[r].height = 40
    ws.freeze_panes = "A9"
    ws.auto_filter.ref = f"A8:N{8 + total}"
    protect(ws)


def _define(wb, name, ref):
    from openpyxl.workbook.defined_name import DefinedName

    # usuń jeśli istnieje
    if name in wb.defined_names:
        del wb.defined_names[name]
    wb.defined_names.add(DefinedName(name, attr_text=ref))


def write_listy(wb, n_ac, n_dx):
    ws = wb.create_sheet("LISTY")
    banner(
        ws,
        "LISTY POMOCNICZE",
        "K",
        "Źródło list rozwijanych NR PIGMENTU. Etykieta = kod | nazwa. Makro i Validity biorą zakres z J9/K9.",
    )
    ws["A8"] = "SYSTEMY"
    ws["A8"].font = font_h()
    ws["A8"].fill = fill(NAVY2)
    ws["A9"] = "AUTOCOLOR"
    ws["A10"] = "DUXONE"
    ws["C8"] = "PRESETY_MASY_G"
    ws["C8"].font = font_h()
    ws["C8"].fill = fill(NAVY2)
    ws["C9"] = 100
    ws["C10"] = 500
    ws["C11"] = 1000
    headers = [
        (5, "AUTOCOLOR_NR"),
        (6, "AUTOCOLOR_LISTA"),
        (7, "DUXONE_NR"),
        (8, "DUXONE_LISTA"),
        (10, "ADRES_LISTA_AC"),
        (11, "ADRES_LISTA_DX"),
    ]
    for col, title in headers:
        cell = ws.cell(8, col, title)
        cell.font = font_h()
        cell.fill = fill(NAVY2)
        cell.alignment = align_c()
    ac = DATA["autocolor"]
    dx = DATA["duxone"]
    for i, rec in enumerate(ac):
        r = 9 + i
        nr = rec["nr_pigmentu"]
        naz = (rec.get("nazwa") or "").strip()
        ws.cell(r, 5, nr)
        ws.cell(r, 6, f"{nr} | {naz}" if naz else nr)
    for i, rec in enumerate(dx):
        r = 9 + i
        nr = rec["nr_pigmentu"]
        naz = (rec.get("nazwa") or "").strip()
        ws.cell(r, 7, nr)
        ws.cell(r, 8, f"{nr} | {naz}" if naz else nr)
    last_ac = 8 + n_ac
    last_dx = 8 + n_dx
    # Tekst adresu — INDIRECT w Validity (Calc nie rozwija nazwy zakresu przez INDIRECT).
    ws["J9"] = f"LISTY!$F$9:$F${last_ac}"
    ws["K9"] = f"LISTY!$H$9:$H${last_dx}"
    ws["J10"] = n_ac
    ws["K10"] = n_dx
    ws["I8"] = "LICZBA"
    ws["I9"] = "wiersze listy →"
    ws["I10"] = "liczba kodów →"
    ws["J11"] = f"$LISTY.$F$9:$F${last_ac}"
    ws["K11"] = f"$LISTY.$H$9:$H${last_dx}"
    for col, width in (("A", 16), ("C", 18), ("E", 16), ("F", 42), ("G", 16), ("H", 42), ("I", 18), ("J", 28), ("K", 28)):
        ws.column_dimensions[col].width = width
    ws.sheet_state = "visible"
    _define(wb, "Lista_Systemow", "LISTY!$A$9:$A$10")
    _define(wb, "Lista_AUTOCOLOR", f"LISTY!$F$9:$F${last_ac}")
    _define(wb, "Lista_DUXONE", f"LISTY!$H$9:$H${last_dx}")
    _define(wb, "ListaAC", f"LISTY!$F$9:$F${last_ac}")
    _define(wb, "ListaDX", f"LISTY!$H$9:$H${last_dx}")
    _define(wb, "ListaAC_NR", f"LISTY!$E$9:$E${last_ac}")
    _define(wb, "ListaDX_NR", f"LISTY!$G$9:$G${last_dx}")
    _define(wb, "PigmentyKlucz", f"PIGMENTY!$A$9:$I${8 + n_ac + n_dx}")
    protect(ws)


def write_ustawienia(wb):
    ws = wb.create_sheet("USTAWIENIA")
    banner(ws, "USTAWIENIA SYSTEMU", "F", "Parametry globalne. Komórki złote — do edycji.")
    items = [
        (8, "A", "Autor domyślny", "B", "Sylwek"),
        (9, "A", "Jednostka masy", "B", "g"),
        (10, "A", "Tolerancja sumy %", "B", 0.15),
        (11, "A", "Ochrona arkuszy", "B", "WYŁĄCZONA"),
        (12, "A", "Następny numer RC", "B", 2),
        (13, "A", "Prefiks numeru", "B", "RC-"),
        (14, "A", "Masa preset 1 (g)", "B", 100),
        (15, "A", "Masa preset 2 (g)", "B", 500),
        (16, "A", "Masa preset 3 (g)", "B", 1000),
        (17, "A", "Wersja systemu", "B", "1.0"),
    ]
    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["B"].width = 22
    ws.column_dimensions["C"].width = 70
    for row, lc, lab, vc, val in items:
        ws[f"{lc}{row}"] = lab
        ws[f"{lc}{row}"].font = font_label()
        cell = ws[f"{vc}{row}"]
        cell.value = val
        style_input(cell)
        if row == 10:
            cell.number_format = "0.00"
    ws["C8"] = "Wpisz nazwisko lakiernika — trafia do nowych receptur."
    ws["C10"] = "Jeżeli |suma % − 100| > tolerancji, START i ANALIZA pokażą ostrzeżenie."
    ws["C11"] = "Arkusze bez hasła — pełna edycja i zapis. Złote = wpis, szare = formuła."
    ws["A19"] = "ZASADA KLUCZA PIGMENTU"
    ws["A19"].font = font_label()
    ws.merge_cells("A20:F22")
    ws["A20"] = (
        "Pigmenty z różnych systemów o tym samym numerze są różne. "
        "Klucz = SYSTEM & \"|\" & NR_PIGMENTU, np. AUTOCOLOR|123 oraz DUXONE|123. "
        "Mieszanie systemów w jednej recepturze jest dozwolone i wymagane."
    )
    ws["A20"].alignment = Alignment(wrap_text=True, vertical="top")
    _define(wb, "Ust_Autor", "USTAWIENIA!$B$8")
    _define(wb, "Ust_Jednostka", "USTAWIENIA!$B$9")
    _define(wb, "Ust_Tolerancja", "USTAWIENIA!$B$10")
    protect(ws)
    ws["B8"].protection = Protection(locked=False)
    ws["B9"].protection = Protection(locked=False)
    ws["B10"].protection = Protection(locked=False)
    ws["B12"].protection = Protection(locked=False)
    ws["B13"].protection = Protection(locked=False)


def write_start(wb):
    ws = wb.create_sheet("START", 0)
    banner(
        ws,
        "SYSTEM RECEPTUR LAKIERÓW",
        "L",
        "AUTOCOLOR  +  DUXONE  |  receptura oryginalna  →  receptura własna  →  analiza  |  LibreOffice Calc / Excel",
    )
    # identyfikacja
    ws.merge_cells("A4:B4")
    ws["A4"] = "IDENTYFIKACJA RECEPTURY"
    ws["A4"].font = Font(name="Calibri", size=12, bold=True, color=WHITE)
    ws["A4"].fill = fill(NAVY2)
    ws.merge_cells("C4:F4")
    ws["C4"].fill = fill(NAVY2)
    labels = [
        (5, "Nazwa receptury", "C", "Meta_Nazwa", "Kolor XYZ"),
        (6, "Numer receptury", "C", "Meta_Numer", "RC-0001"),
        (7, "Nazwa koloru", "C", "Meta_Kolor", ""),
        (8, "Kod koloru", "C", "Meta_Kod", ""),
        (9, "Producent", "C", "Meta_Producent", ""),
        (10, "System bazowy", "C", "Meta_System", "AUTOCOLOR"),
        (11, "Wersja", "C", "Meta_Wersja", 1),
        (12, "Autor", "C", "Meta_Autor", '=Ust_Autor'),
        (13, "Data", "C", "Meta_Data", "=TODAY()"),
        (14, "Uwagi technologiczne", "C", "Meta_Uwagi", ""),
        (15, "Masa docelowa (g)", "C", "MasaDocelowa", 100),
    ]
    ws.column_dimensions["A"].width = 26
    ws.column_dimensions["B"].width = 4
    ws.column_dimensions["C"].width = 28
    ws.column_dimensions["D"].width = 14
    ws.column_dimensions["E"].width = 22
    ws.column_dimensions["F"].width = 16
    ws.column_dimensions["G"].width = 4
    ws.column_dimensions["H"].width = 26
    ws.column_dimensions["I"].width = 16
    ws.column_dimensions["J"].width = 16
    ws.column_dimensions["K"].width = 18
    ws.column_dimensions["L"].width = 18
    for row, lab, col, name, default in labels:
        ws[f"A{row}"] = lab
        ws[f"A{row}"].font = font_label()
        ws[f"A{row}"].fill = fill("EEF1F6")
        cell = ws[f"{col}{row}"]
        cell.value = default
        style_input(cell)
        ws.merge_cells(f"C{row}:F{row}")
        _define(wb, name, f"START!${col}${row}")
    ws["C13"].number_format = "DD.MM.YYYY"
    ws["C11"].number_format = "0"
    ws["C15"].number_format = "0.00"
    add_dv_list(ws, "=Lista_Systemow", "C10")
    add_dv_decimal(ws, "C15")

    # podsumowanie
    ws.merge_cells("H4:L4")
    ws["H4"] = "AKTUALNA RECEPTURA"
    ws["H4"].font = Font(name="Calibri", size=12, bold=True, color=WHITE)
    ws["H4"].fill = fill(NAVY2)
    summaries = [
        (5, "Masa oryginalna (g)", f"=SUM(RECEPTURA_ORYGINALNA!E{R0}:E{R1})"),
        (6, "Masa własna (g)", f"=SUM(RECEPTURA_WLASNA!F{R0}:F{R1})"),
        (7, "Różnica masy (g)", "=I6-I5"),
        (8, "Liczba pozycji (własna)", f'=COUNTIF(RECEPTURA_WLASNA!C{R0}:C{R1},\"<>\")'),
        (9, "Suma % oryginał", f"=IFERROR(SUM(RECEPTURA_ORYGINALNA!G{R0}:G{R1}),0)"),
        (10, "Suma % własna", f"=IFERROR(SUM(RECEPTURA_WLASNA!J{R0}:J{R1}),0)"),
        (11, "Status udziałów", '=IF(I8=0,"BRAK DANYCH",IF(ABS(I10-1)<=Ust_Tolerancja/100,"RECEPTURA POPRAWNA","UWAGA — SUMA UDZIAŁÓW = "&TEXT(I10,"0.00%")))'),
        (12, "Duplikaty (własna)", f'=COUNTIF(RECEPTURA_WLASNA!N{R0}:N{R1},"DUPLIKAT")'),
        (13, "Brak w bazie", f'=COUNTIF(RECEPTURA_WLASNA!O{R0}:O{R1},"BRAK W BAZIE")'),
        (14, "Dodane / usunięte", f'=COUNTIF(RECEPTURA_WLASNA!K{R0}:K{R1},"DODANO")&" / "&COUNTIF(RECEPTURA_WLASNA!K{R0}:K{R1},"USUNIĘTO")'),
        (15, "Zwiększone / zmniejszone", f'=COUNTIF(RECEPTURA_WLASNA!K{R0}:K{R1},"ZWIĘKSZONO")&" / "&COUNTIF(RECEPTURA_WLASNA!K{R0}:K{R1},"ZMNIEJSZONO")'),
    ]
    for row, lab, formula in summaries:
        ws[f"H{row}"] = lab
        ws[f"H{row}"].font = font_label()
        ws[f"H{row}"].fill = fill("EEF1F6")
        cell = ws[f"I{row}"]
        cell.value = formula
        style_formula(cell)
        ws.merge_cells(f"I{row}:L{row}")
    ws["I5"].number_format = "0.00"
    ws["I6"].number_format = "0.00"
    ws["I7"].number_format = "0.00"
    ws["I9"].number_format = "0.00%"
    ws["I10"].number_format = "0.00%"
    _define(wb, "MasaOryg", "START!$I$5")
    _define(wb, "MasaWlasna", "START!$I$6")
    _define(wb, "StatusUdzialow", "START!$I$11")

    ws.conditional_formatting.add(
        "I11",
        FormulaRule(
            formula=['ISNUMBER(SEARCH("UWAGA",I11))'],
            fill=fill(RED_SOFT),
            font=Font(name="Calibri", size=10, bold=True, color="9C0006"),
        ),
    )
    ws.conditional_formatting.add(
        "I11",
        FormulaRule(
            formula=['I11="RECEPTURA POPRAWNA"'],
            fill=fill(OK_GREEN),
            font=Font(name="Calibri", size=10, bold=True, color="006100"),
        ),
    )

    ws.merge_cells("A17:L17")
    ws["A17"] = "PANEL AKCJI  (LibreOffice: Narzędzia → Makra → Zarządzaj makrami → RECEPTURY_LAKIERY.ods)"
    ws["A17"].font = Font(name="Calibri", size=12, bold=True, color=WHITE)
    ws["A17"].fill = fill(NAVY2)

    actions = [
        (18, "A", "1. Nowa receptura", "Wyczyść tabele oryginału i własnej, nadaj nowy numer RC, ustaw wersję = 1. Makro: NowaReceptura"),
        (19, "A", "2. Wpisz oryginał", "Arkusz RECEPTURA_ORYGINALNA: SYSTEM z listy, potem kliknij NR PIGMENTU — lista z wybranej bazy. Ilość w gramach. Nazwa uzupełni się sama."),
        (20, "A", "3. Kopia → własna", "Makro KopiujDoWlasnej kopiuje skład. Albo przepisz SYSTEM/NR i ilości. ILOŚĆ ORYGINALNA dociąga się kluczem."),
        (21, "A", "4. Modyfikuj", "Zmieniaj złote komórki ilości. Dodawaj pigment z drugiego systemu. Ten sam pigment drugi raz → status DUPLIKAT (zsumuj)."),
        (22, "A", "5. Przelicz masę", "Ustaw masę docelową na START. Kolumna ILOŚĆ DO ZWAŻENIA przelicza na żywo. Makro ZastosujPrzeliczenie zapisuje wartości."),
        (23, "A", "6. Analiza / raport", "Otwórz ANALIZA (wykresy) i RAPORT (wydruk). HISTORIA — makro ZapiszWersje nie nadpisuje poprzednich wersji."),
    ]
    for row, col, title, desc in actions:
        ws[f"{col}{row}"] = title
        ws[f"{col}{row}"].font = Font(name="Calibri", size=11, bold=True, color=NAVY)
        ws[f"{col}{row}"].fill = fill(INPUT)
        ws.merge_cells(f"C{row}:L{row}")
        ws[f"C{row}"] = desc
        ws[f"C{row}"].alignment = align_l()
        ws[f"C{row}"].border = thin

    ws.merge_cells("A25:L25")
    ws["A25"] = "NAWIGACJA"
    ws["A25"].font = Font(name="Calibri", size=12, bold=True, color=WHITE)
    ws["A25"].fill = fill(NAVY2)
    links = [
        (26, "A", "RECEPTURA_ORYGINALNA", "Skład oryginalny"),
        (26, "C", "RECEPTURA_WLASNA", "Skład roboczy"),
        (26, "E", "ANALIZA", "Wykresy i KPI"),
        (26, "G", "RAPORT", "Wydruk"),
        (26, "I", "HISTORIA", "Wersje"),
        (27, "A", "PIGMENTY", "Wyszukiwarka"),
        (27, "C", "DOBARWIANIE", "Procedury PDF"),
        (27, "E", "BAZA_AUTOCOLOR", "Baza Autocolor"),
        (27, "G", "BAZA_DUXONE", "Baza Duxone"),
        (27, "I", "USTAWIENIA", "Parametry"),
    ]
    for row, col, sheet, caption in links:
        cell = ws[f"{col}{row}"]
        cell.value = caption
        cell.hyperlink = f"#{sheet}!A1"
        cell.font = Font(name="Calibri", size=10, bold=True, color="1F4E79", underline="single")
        cell.fill = fill(BLUE_SOFT)
        cell.alignment = align_c()
        cell.border = thin
        nxt = get_column_letter(cell.column + 1)
        ws.merge_cells(f"{col}{row}:{nxt}{row}")

    ws.merge_cells("A29:L32")
    ws["A29"] = (
        "Mieszanie systemów: receptura bazowa AUTOCOLOR może zawierać pigmenty DUXONE i odwrotnie. "
        "Nie usuwaj wierszy tabel — zeruj ilość (status USUNIĘTO). "
        "Komórki złote = wpis, szare = formuła (arkusze bez ochrony — edycja i zapis bez hasła). "
        "Źródła nazw: PDF Nexa Autocolor 2K Tint Chart oraz Duxone Tint Descriptions PL; kody z szablonów ODS."
    )
    ws["A29"].alignment = Alignment(wrap_text=True, vertical="top")
    ws["A29"].fill = fill("EEF1F6")
    protect(ws)
    for row in range(5, 16):
        ws[f"C{row}"].protection = Protection(locked=False)


def write_oryg(wb):
    ws = wb.create_sheet("RECEPTURA_ORYGINALNA")
    banner(ws, "RECEPTURA ORYGINALNA", "J", "Skład źródłowy. SYSTEM i NR z listy. Nazwa, jednostka i % liczą się automatycznie.")
    # pasek meta
    meta = [
        (3, "A", "Nazwa", "C", "=Meta_Nazwa"),
        (3, "E", "Numer", "F", "=Meta_Numer"),
        (3, "H", "System bazowy", "I", "=Meta_System"),
        (4, "A", "Kolor", "C", "=Meta_Kolor"),
        (4, "E", "Wersja", "F", "=Meta_Wersja"),
        (4, "H", "Data", "I", "=Meta_Data"),
        (5, "A", "Masa całkowita (g)", "C", "=MasaOryg"),
        (5, "E", "Suma %", "F", f"=IFERROR(SUM(G{R0}:G{R1}),0)"),
        (5, "H", "Status", "I", "=StatusUdzialow"),
    ]
    for row, lc, lab, vc, val in meta:
        ws[f"{lc}{row}"] = lab
        ws[f"{lc}{row}"].font = font_label()
        ws[f"{lc}{row}"].fill = fill("EEF1F6")
        cell = ws[f"{vc}{row}"]
        cell.value = val
        style_formula(cell)
        if vc == "C" and row in (3, 4):
            ws.merge_cells(f"C{row}:D{row}")
    ws["C5"].number_format = "0.00"
    ws["F5"].number_format = "0.00%"
    ws["I4"].number_format = "DD.MM.YYYY"
    ws.merge_cells("A6:J6")
    ws["A6"].fill = fill(GOLD)
    ws.row_dimensions[6].height = 6
    ws.merge_cells("A7:J8")
    ws["A7"] = (
        "Najpierw SYSTEM (AUTOCOLOR / DUXONE) z listy, potem kliknij NR PIGMENTU — otworzy się lista z tej bazy. "
        "Każdy wiersz ma własny SYSTEM (można mieszać). Po wyborze numeru nazwa i jednostka uzupełnią się same. "
        "Ilość ≥ 0. Ten sam klucz dwa razy = DUPLIKAT (zsumuj ilości)."
    )
    ws["A7"].alignment = align_l()

    headers = ["LP", "SYSTEM", "NR PIGMENTU", "NAZWA PIGMENTU", "ILOŚĆ", "JEDNOSTKA", "% UDZIAŁU", "UWAGI", "KLUCZ", "KONTROLA"]
    widths = [6, 14, 36, 36, 12, 12, 12, 28, 22, 18]
    header_row(ws, 11, headers, widths)
    add_dv_list(ws, "=Lista_Systemow", f"B{R0}:B{R1}")
    add_dv_decimal(ws, f"E{R0}:E{R1}")
    fill_sidelists(ws)
    add_dv_nr_pigmentu(ws, f"C{R0}:C{R1}", "$B12")

    for i, r in enumerate(range(R0, R1 + 1), 1):
        ws.cell(r, 1, f'=IF(C{r}="","",{i})')
        style_formula(ws.cell(r, 1))
        style_input(ws.cell(r, 2))
        style_input(ws.cell(r, 3))
        ws.cell(r, 4, f'=IF(C{r}="","",IFERROR(VLOOKUP(I{r},PigmentyKlucz,4,FALSE),"BRAK W BAZIE"))')
        style_formula(ws.cell(r, 4))
        style_input(ws.cell(r, 5))
        ws.cell(r, 5).number_format = "0.000"
        ws.cell(r, 6, f'=IF(C{r}="","",IFERROR(VLOOKUP(I{r},PigmentyKlucz,5,FALSE),Ust_Jednostka))')
        style_formula(ws.cell(r, 6))
        ws.cell(r, 7, f'=IF(OR(C{r}="",MasaOryg=0),"",E{r}/MasaOryg)')
        style_formula(ws.cell(r, 7), "0.00%")
        style_input(ws.cell(r, 8))
        ws.cell(r, 9, f'=IF(C{r}="","",B{r}&"|"&{kod_z_pola_nr(f"C{r}")})')
        style_formula(ws.cell(r, 9))
        ws.cell(
            r,
            10,
            f'=IF(C{r}="","",IF(COUNTIF($I${R0}:$I${R1},I{r})>1,"DUPLIKAT",IF(ISERROR(VLOOKUP(I{r},PigmentyKlucz,1,FALSE)),"BRAK W BAZIE","OK")))',
        )
        style_formula(ws.cell(r, 10))
        ws.cell(r, 2).alignment = align_c()
        ws.cell(r, 3).alignment = align_c()
        ws.cell(r, 5).alignment = align_c()
    ws.conditional_formatting.add(
        f"J{R0}:J{R1}",
        CellIsRule(operator="equal", formula=['"DUPLIKAT"'], fill=fill(AMBER), font=Font(bold=True, color="9C5700")),
    )
    ws.conditional_formatting.add(
        f"J{R0}:J{R1}",
        CellIsRule(operator="equal", formula=['"BRAK W BAZIE"'], fill=fill(RED_SOFT), font=Font(bold=True, color="9C0006")),
    )
    ws.sheet_view.showGridLines = False
    protect(ws)


def write_wlasna(wb):
    ws = wb.create_sheet("RECEPTURA_WLASNA")
    banner(
        ws,
        "RECEPTURA WŁASNA",
        "P",
        "Główny arkusz roboczy. ILOŚĆ ORYGINALNA dociągana kluczem SYSTEM|NR. Można dodać pigment z drugiego systemu.",
    )
    meta = [
        (3, "A", "Nazwa", "C", "=Meta_Nazwa"),
        (3, "E", "Numer", "F", "=Meta_Numer"),
        (3, "H", "System bazowy", "I", "=Meta_System"),
        (3, "K", "Masa docelowa (g)", "M", "=MasaDocelowa"),
        (4, "A", "Kolor", "C", "=Meta_Kolor"),
        (4, "E", "Wersja", "F", "=Meta_Wersja"),
        (4, "H", "Data", "I", "=Meta_Data"),
        (4, "K", "Masa własna (g)", "M", "=MasaWlasna"),
        (5, "A", "Status udziałów", "C", "=StatusUdzialow"),
        (5, "E", "Masa oryg. (g)", "F", "=MasaOryg"),
        (5, "H", "Różnica (g)", "I", "=MasaWlasna-MasaOryg"),
        (5, "K", "Wsp. skali", "M", '=IFERROR(MasaDocelowa/MasaWlasna,0)'),
    ]
    for row, lc, lab, vc, val in meta:
        ws[f"{lc}{row}"] = lab
        ws[f"{lc}{row}"].font = font_label()
        ws[f"{lc}{row}"].fill = fill("EEF1F6")
        cell = ws[f"{vc}{row}"]
        cell.value = val
        style_formula(cell)
    ws["M3"].number_format = "0.00"
    ws["M4"].number_format = "0.00"
    ws["F5"].number_format = "0.00"
    ws["I5"].number_format = "0.00"
    ws["M5"].number_format = "0.0000"
    ws["I4"].number_format = "DD.MM.YYYY"
    ws.merge_cells("C5:D5")
    ws.merge_cells("A6:P6")
    ws["A6"].fill = fill(GOLD)
    ws.row_dimensions[6].height = 6
    ws.merge_cells("A7:P8")
    ws["A7"] = (
        "Kolumny złote: SYSTEM, NR, ILOŚĆ WŁASNA, UWAGI. Kliknij NR PIGMENTU — lista z bazy SYSTEM w tym wierszu (można mieszać AUTOCOLOR i DUXONE). "
        "ILOŚĆ DO ZWAŻENIA = ilość własna × masa docelowa / masa własna (przeliczenie na 100 g / 500 g / 1 kg / dowolna). "
        "STATUS: BEZ ZMIAN / ZWIĘKSZONO / ZMNIEJSZONO / DODANO / USUNIĘTO. "
        "Usunięcie = ilość własna 0 przy ilości oryginalnej > 0."
    )
    ws["A7"].alignment = align_l()

    headers = [
        "LP",
        "SYSTEM",
        "NR PIGMENTU",
        "NAZWA PIGMENTU",
        "ILOŚĆ ORYGINALNA",
        "ILOŚĆ WŁASNA",
        "RÓŻNICA",
        "ZMIANA %",
        "% W RECEPTURZE ORYGINALNEJ",
        "% W RECEPTURZE WŁASNEJ",
        "STATUS",
        "UWAGI",
        "ILOŚĆ DO ZWAŻENIA",
        "KONTROLA",
        "WALIDACJA BAZY",
        "KLUCZ",
    ]
    widths = [6, 14, 36, 32, 16, 14, 12, 12, 16, 16, 14, 22, 16, 14, 16, 22]
    header_row(ws, 11, headers, widths)
    ws.auto_filter.ref = f"A11:P{R1}"
    add_dv_list(ws, "=Lista_Systemow", f"B{R0}:B{R1}")
    add_dv_decimal(ws, f"F{R0}:F{R1}")
    fill_sidelists(ws)
    add_dv_nr_pigmentu(ws, f"C{R0}:C{R1}", "$B12")

    for i, r in enumerate(range(R0, R1 + 1), 1):
        ws.cell(r, 1, f'=IF(C{r}="","",{i})')
        style_formula(ws.cell(r, 1))
        style_input(ws.cell(r, 2))
        style_input(ws.cell(r, 3))
        ws.cell(r, 4, f'=IF(C{r}="","",IFERROR(VLOOKUP(P{r},PigmentyKlucz,4,FALSE),"BRAK W BAZIE"))')
        style_formula(ws.cell(r, 4))
        ws.cell(
            r,
            5,
            f'=IF(C{r}="","",IFERROR(SUMIF(RECEPTURA_ORYGINALNA!$I${R0}:$I${R1},P{r},RECEPTURA_ORYGINALNA!$E${R0}:$E${R1}),0))',
        )
        style_formula(ws.cell(r, 5), "0.000")
        style_input(ws.cell(r, 6))
        ws.cell(r, 6).number_format = "0.000"
        ws.cell(r, 7, f'=IF(C{r}="","",N(F{r})-N(E{r}))')
        style_formula(ws.cell(r, 7), "0.000")
        ws.cell(r, 8, f'=IF(C{r}="","",IF(N(E{r})=0,IF(N(F{r})>0,"",0),IFERROR((N(F{r})-N(E{r}))/N(E{r}),0)))')
        style_formula(ws.cell(r, 8), "0.00%")
        ws.cell(r, 9, f'=IF(C{r}="","",IF(MasaOryg=0,"",N(E{r})/MasaOryg))')
        style_formula(ws.cell(r, 9), "0.00%")
        ws.cell(r, 10, f'=IF(C{r}="","",IF(MasaWlasna=0,"",N(F{r})/MasaWlasna))')
        style_formula(ws.cell(r, 10), "0.00%")
        ws.cell(
            r,
            11,
            f'=IF(C{r}="","",IF(AND(N(E{r})>0,N(F{r})=0),"USUNIĘTO",IF(AND(N(E{r})=0,N(F{r})>0),"DODANO",IF(N(F{r})>N(E{r}),"ZWIĘKSZONO",IF(N(F{r})<N(E{r}),"ZMNIEJSZONO","BEZ ZMIAN")))))',
        )
        style_formula(ws.cell(r, 11))
        style_input(ws.cell(r, 12))
        ws.cell(r, 13, f'=IF(C{r}="","",IFERROR(N(F{r})*MasaDocelowa/MasaWlasna,0))')
        style_formula(ws.cell(r, 13), "0.000")
        ws.cell(r, 14, f'=IF(C{r}="","",IF(COUNTIF($P${R0}:$P${R1},P{r})>1,"DUPLIKAT","OK"))')
        style_formula(ws.cell(r, 14))
        ws.cell(
            r,
            15,
            f'=IF(C{r}="","",IF(B{r}="","BRAK SYSTEMU",IF(ISERROR(VLOOKUP(P{r},PigmentyKlucz,1,FALSE)),"BRAK W BAZIE","OK")))',
        )
        style_formula(ws.cell(r, 15))
        ws.cell(r, 16, f'=IF(C{r}="","",B{r}&"|"&{kod_z_pola_nr(f"C{r}")})')
        style_formula(ws.cell(r, 16))
        for col in (2, 3, 11, 14, 15):
            ws.cell(r, col).alignment = align_c()
    status_cf(ws, "K")
    ws.conditional_formatting.add(
        f"N{R0}:N{R1}",
        CellIsRule(operator="equal", formula=['"DUPLIKAT"'], fill=fill(AMBER), font=Font(bold=True, color="9C5700")),
    )
    ws.conditional_formatting.add(
        f"O{R0}:O{R1}",
        CellIsRule(operator="equal", formula=['"BRAK W BAZIE"'], fill=fill(RED_SOFT), font=Font(bold=True, color="9C0006")),
    )
    ws.sheet_view.showGridLines = False
    protect(ws)


def write_wykresy_data(wb):
    ws = wb.create_sheet("DANE_WYKRESOW")
    banner(ws, "DANE WYKRESÓW", "F", "Źródło dynamiczne — puste wiersze = #N/D, aby wykresy pomijały luki.")
    headers = ["ETYKIETA", "ILOŚĆ ORYGINALNA", "ILOŚĆ WŁASNA", "ZMIANA %", "% SKŁAD WŁASNY", "STATUS", "ABS ZMIANA %"]
    for i, h in enumerate(headers, 1):
        cell = ws.cell(8, i, h)
        cell.font = font_h()
        cell.fill = fill(NAVY2)
        cell.alignment = align_c()
        ws.column_dimensions[get_column_letter(i)].width = 20
    for i, r in enumerate(range(R0, R1 + 1)):
        wr = 9 + i
        src = f"RECEPTURA_WLASNA"
        ws.cell(wr, 1, f'=IF({src}!C{r}="","",{src}!C{r}&" ("&{src}!B{r}&")")')
        ws.cell(wr, 2, f'=IF({src}!C{r}="",NA(),N({src}!E{r}))')
        ws.cell(wr, 3, f'=IF({src}!C{r}="",NA(),N({src}!F{r}))')
        ws.cell(wr, 4, f'=IF(OR({src}!C{r}="",{src}!H{r}=""),NA(),IF(ISNUMBER({src}!H{r}),{src}!H{r},NA()))')
        ws.cell(wr, 5, f'=IF({src}!C{r}="",NA(),IF(N({src}!F{r})=0,NA(),{src}!J{r}))')
        ws.cell(wr, 6, f'=IF({src}!C{r}="","",{src}!K{r})')
        ws.cell(wr, 7, f'=IF({src}!C{r}="",NA(),IF(ISNUMBER({src}!H{r}),ABS(N({src}!H{r})),NA()))')
        for c in range(1, 8):
            style_formula(ws.cell(wr, c))
            if c in (2, 3):
                ws.cell(wr, c).number_format = "0.000"
            if c in (4, 5, 7):
                ws.cell(wr, c).number_format = "0.00%"
    # podsumowanie statusów do wykresu 4
    ws["H8"] = "STATUS"
    ws["I8"] = "LICZBA"
    ws["H8"].font = font_h()
    ws["H8"].fill = fill(NAVY2)
    ws["I8"].font = font_h()
    ws["I8"].fill = fill(NAVY2)
    statuses = ["BEZ ZMIAN", "ZWIĘKSZONO", "ZMNIEJSZONO", "DODANO", "USUNIĘTO"]
    for i, st in enumerate(statuses):
        ws.cell(9 + i, 8, st)
        ws.cell(9 + i, 9, f'=COUNTIF(RECEPTURA_WLASNA!K{R0}:K{R1},H{9 + i})')
        style_formula(ws.cell(9 + i, 8))
        style_formula(ws.cell(9 + i, 9))
    ws.sheet_state = "hidden"
    protect(ws)


def write_analiza(wb):
    ws = wb.create_sheet("ANALIZA")
    banner(ws, "ANALIZA ZMIAN", "L", "KPI i wykresy odświeżają się po przeliczeniu formuł (F9 / LibreOffice: Dane → Przelicz).")
    meta = [
        (3, "A", "Nazwa", "C", "=Meta_Nazwa"),
        (3, "E", "Numer", "F", "=Meta_Numer"),
        (3, "H", "System", "I", "=Meta_System"),
        (4, "A", "Wersja", "C", "=Meta_Wersja"),
        (4, "E", "Data", "F", "=Meta_Data"),
        (4, "H", "Status %", "I", "=StatusUdzialow"),
    ]
    for row, lc, lab, vc, val in meta:
        ws[f"{lc}{row}"] = lab
        ws[f"{lc}{row}"].font = font_label()
        ws[f"{lc}{row}"].fill = fill("EEF1F6")
        cell = ws[f"{vc}{row}"]
        cell.value = val
        style_formula(cell)
    ws["F4"].number_format = "DD.MM.YYYY"
    ws.merge_cells("A6:D6")
    ws["A6"] = "Wskaźniki"
    ws["A6"].font = Font(name="Calibri", size=12, bold=True, color=WHITE)
    ws["A6"].fill = fill(NAVY2)
    kpis = [
        (7, "Masa oryginalna (g)", "=MasaOryg", "0.00"),
        (8, "Masa własna (g)", "=MasaWlasna", "0.00"),
        (9, "Różnica masy (g)", "=MasaWlasna-MasaOryg", "0.00"),
        (10, "Liczba pigmentów (własna)", f'=COUNTIF(RECEPTURA_WLASNA!C{R0}:C{R1},"<>")', "0"),
        (11, "Dodane", f'=COUNTIF(RECEPTURA_WLASNA!K{R0}:K{R1},"DODANO")', "0"),
        (12, "Usunięte", f'=COUNTIF(RECEPTURA_WLASNA!K{R0}:K{R1},"USUNIĘTO")', "0"),
        (13, "Zwiększone", f'=COUNTIF(RECEPTURA_WLASNA!K{R0}:K{R1},"ZWIĘKSZONO")', "0"),
        (14, "Zmniejszone", f'=COUNTIF(RECEPTURA_WLASNA!K{R0}:K{R1},"ZMNIEJSZONO")', "0"),
        (15, "Bez zmian", f'=COUNTIF(RECEPTURA_WLASNA!K{R0}:K{R1},"BEZ ZMIAN")', "0"),
        (16, "Największa zmiana %", f'=IFERROR(MAX(DANE_WYKRESOW!G9:G{8 + N}),0)', "0.00%"),
        (17, "Suma % własna", f"=IFERROR(SUM(RECEPTURA_WLASNA!J{R0}:J{R1}),0)", "0.00%"),
        (18, "Suma % oryginał", f"=IFERROR(SUM(RECEPTURA_ORYGINALNA!G{R0}:G{R1}),0)", "0.00%"),
    ]
    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["B"].width = 16
    ws.column_dimensions["C"].width = 18
    ws.column_dimensions["D"].width = 14
    for row, lab, formula, fmt in kpis:
        ws[f"A{row}"] = lab
        ws[f"A{row}"].font = font_label()
        ws[f"A{row}"].fill = fill("EEF1F6")
        cell = ws[f"B{row}"]
        cell.value = formula
        style_formula(cell, fmt)

    # Wykres 1
    c1 = BarChart()
    c1.type = "col"
    c1.grouping = "clustered"
    c1.title = "Oryginał vs receptura własna (g)"
    c1.y_axis.title = "Ilość (g)"
    c1.x_axis.title = "Pigment (system)"
    data = Reference(wb["DANE_WYKRESOW"], min_col=2, min_row=8, max_col=3, max_row=8 + N)
    cats = Reference(wb["DANE_WYKRESOW"], min_col=1, min_row=9, max_row=8 + N)
    c1.add_data(data, from_rows=False, titles_from_data=True)
    c1.set_categories(cats)
    c1.shape = 4
    c1.legend.position = "b"
    c1.style = 10
    c1.width = 18
    c1.height = 8
    ws.add_chart(c1, "D7")

    c2 = BarChart()
    c2.type = "col"
    c2.title = "Zmiana procentowa ilości"
    c2.y_axis.title = "Zmiana %"
    c2.x_axis.title = "Pigment"
    data2 = Reference(wb["DANE_WYKRESOW"], min_col=4, min_row=8, max_col=4, max_row=8 + N)
    c2.add_data(data2, titles_from_data=True)
    c2.set_categories(cats)
    c2.legend.position = "b"
    c2.style = 12
    c2.width = 18
    c2.height = 8
    ws.add_chart(c2, "D23")

    c3 = PieChart()
    c3.title = "Skład receptury własnej (%)"
    labels = Reference(wb["DANE_WYKRESOW"], min_col=1, min_row=9, max_row=8 + N)
    data3 = Reference(wb["DANE_WYKRESOW"], min_col=5, min_row=8, max_row=8 + N)
    c3.add_data(data3, titles_from_data=True)
    c3.set_categories(labels)
    c3.dataLabels = DataLabelList()
    c3.dataLabels.showPercent = True
    c3.dataLabels.showVal = False
    c3.dataLabels.showCatName = True
    c3.width = 14
    c3.height = 10
    ws.add_chart(c3, "D39")

    c4 = BarChart()
    c4.type = "col"
    c4.title = "Dodane / usunięte / zmienione"
    c4.y_axis.title = "Liczba pigmentów"
    data4 = Reference(wb["DANE_WYKRESOW"], min_col=9, min_row=8, max_row=13)
    cats4 = Reference(wb["DANE_WYKRESOW"], min_col=8, min_row=9, max_row=13)
    c4.add_data(data4, titles_from_data=True)
    c4.set_categories(cats4)
    c4.style = 10
    c4.width = 14
    c4.height = 8
    ws.add_chart(c4, "A23")
    protect(ws)


def write_raport(wb):
    ws = wb.create_sheet("RAPORT")
    banner(ws, "RAPORT RECEPTURY", "H", "Arkusz do wydruku. Ustawienia: A4, poziomo, dopasuj do szerokości.")
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.page_setup.horizontalCentered = True
    ws.oddFooter.left.text = "RECEPTURY LAKIERÓW  |  AUTOCOLOR / DUXONE"
    ws.oddFooter.right.text = "Strona &P / &N"
    ws.page_margins = PageMargins(left=0.5, right=0.5, top=0.6, bottom=0.6)

    ws.merge_cells("A4:H4")
    ws["A4"] = "INFORMACJE"
    ws["A4"].font = Font(name="Calibri", size=12, bold=True, color=WHITE)
    ws["A4"].fill = fill(NAVY2)
    info = [
        (5, "A", "Nazwa", "B", "=Meta_Nazwa"),
        (5, "C", "Kod koloru", "D", "=Meta_Kod"),
        (5, "E", "System bazowy", "F", "=Meta_System"),
        (6, "A", "Numer", "B", "=Meta_Numer"),
        (6, "C", "Wersja", "D", "=Meta_Wersja"),
        (6, "E", "Data", "F", "=Meta_Data"),
        (7, "A", "Producent", "B", "=Meta_Producent"),
        (7, "C", "Autor", "D", "=Meta_Autor"),
        (7, "E", "Masa docelowa (g)", "F", "=MasaDocelowa"),
        (8, "A", "Uwagi", "B", "=Meta_Uwagi"),
    ]
    for row, lc, lab, vc, val in info:
        ws[f"{lc}{row}"] = lab
        ws[f"{lc}{row}"].font = font_label()
        cell = ws[f"{vc}{row}"]
        cell.value = val
        style_formula(cell)
    ws.merge_cells("B8:H8")
    ws["F6"].number_format = "DD.MM.YYYY"
    ws["F7"].number_format = "0.00"

    ws.merge_cells("A10:H10")
    ws["A10"] = "SKŁAD (RECEPTURA WŁASNA — ILOŚĆ DO ZWAŻENIA)"
    ws["A10"].font = Font(name="Calibri", size=12, bold=True, color=WHITE)
    ws["A10"].fill = fill(NAVY2)
    for i, h in enumerate(["LP", "SYSTEM", "PIGMENT", "NAZWA", "ILOŚĆ (g)", "%", "STATUS", "JEDN."], 1):
        cell = ws.cell(11, i, h)
        cell.font = font_h()
        cell.fill = fill(NAVY2)
        cell.alignment = align_c()
        cell.border = thin
    widths = [6, 14, 16, 32, 12, 10, 14, 10]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for i, r in enumerate(range(R0, R1 + 1)):
        wr = 12 + i
        ws.cell(wr, 1, f'=IF(RECEPTURA_WLASNA!C{r}="","",RECEPTURA_WLASNA!A{r})')
        ws.cell(wr, 2, f'=IF(RECEPTURA_WLASNA!C{r}="","",RECEPTURA_WLASNA!B{r})')
        ws.cell(wr, 3, f'=IF(RECEPTURA_WLASNA!C{r}="","",RECEPTURA_WLASNA!C{r})')
        ws.cell(wr, 4, f'=IF(RECEPTURA_WLASNA!C{r}="","",RECEPTURA_WLASNA!D{r})')
        ws.cell(wr, 5, f'=IF(RECEPTURA_WLASNA!C{r}="","",RECEPTURA_WLASNA!M{r})')
        ws.cell(wr, 6, f'=IF(RECEPTURA_WLASNA!C{r}="","",RECEPTURA_WLASNA!J{r})')
        ws.cell(wr, 7, f'=IF(RECEPTURA_WLASNA!C{r}="","",RECEPTURA_WLASNA!K{r})')
        ws.cell(wr, 8, f'=IF(RECEPTURA_WLASNA!C{r}="","",Ust_Jednostka)')
        for c in range(1, 9):
            style_formula(ws.cell(wr, c))
        ws.cell(wr, 5).number_format = "0.000"
        ws.cell(wr, 6).number_format = "0.00%"

    # zmiany — pod składem, start row 12+N+1 = 53
    cr = 12 + N + 1
    ws.merge_cells(f"A{cr}:H{cr}")
    ws[f"A{cr}"] = "ZMIANY WZGLĘDEM ORYGINAŁU"
    ws[f"A{cr}"].font = Font(name="Calibri", size=12, bold=True, color=WHITE)
    ws[f"A{cr}"].fill = fill(NAVY2)
    for i, h in enumerate(["LP", "PIGMENT", "SYSTEM", "ORYGINAŁ", "WŁASNA", "RÓŻNICA", "ZMIANA %", "STATUS"], 1):
        cell = ws.cell(cr + 1, i, h)
        cell.font = font_h()
        cell.fill = fill(NAVY2)
        cell.alignment = align_c()
        cell.border = thin
    for i, r in enumerate(range(R0, R1 + 1)):
        wr = cr + 2 + i
        ws.cell(wr, 1, f'=IF(RECEPTURA_WLASNA!C{r}="","",RECEPTURA_WLASNA!A{r})')
        ws.cell(wr, 2, f'=IF(RECEPTURA_WLASNA!C{r}="","",RECEPTURA_WLASNA!C{r})')
        ws.cell(wr, 3, f'=IF(RECEPTURA_WLASNA!C{r}="","",RECEPTURA_WLASNA!B{r})')
        ws.cell(wr, 4, f'=IF(RECEPTURA_WLASNA!C{r}="","",RECEPTURA_WLASNA!E{r})')
        ws.cell(wr, 5, f'=IF(RECEPTURA_WLASNA!C{r}="","",RECEPTURA_WLASNA!F{r})')
        ws.cell(wr, 6, f'=IF(RECEPTURA_WLASNA!C{r}="","",RECEPTURA_WLASNA!G{r})')
        ws.cell(wr, 7, f'=IF(RECEPTURA_WLASNA!C{r}="","",RECEPTURA_WLASNA!H{r})')
        ws.cell(wr, 8, f'=IF(RECEPTURA_WLASNA!C{r}="","",RECEPTURA_WLASNA!K{r})')
        for c in range(1, 9):
            style_formula(ws.cell(wr, c))
        for c in (4, 5, 6):
            ws.cell(wr, c).number_format = "0.000"
        ws.cell(wr, 7).number_format = "0.00%"

    sr = cr + 2 + N + 1
    ws.merge_cells(f"A{sr}:H{sr}")
    ws[f"A{sr}"] = "PODSUMOWANIE"
    ws[f"A{sr}"].font = Font(name="Calibri", size=12, bold=True, color=WHITE)
    ws[f"A{sr}"].fill = fill(NAVY2)
    sums = [
        (sr + 1, "Masa całkowita oryg. (g)", "=MasaOryg"),
        (sr + 2, "Masa całkowita własna (g)", "=MasaWlasna"),
        (sr + 3, "Liczba pigmentów", f'=COUNTIF(RECEPTURA_WLASNA!C{R0}:C{R1},"<>")'),
        (sr + 4, "Dodane", f'=COUNTIF(RECEPTURA_WLASNA!K{R0}:K{R1},"DODANO")'),
        (sr + 5, "Usunięte", f'=COUNTIF(RECEPTURA_WLASNA!K{R0}:K{R1},"USUNIĘTO")'),
        (sr + 6, "Zwiększone", f'=COUNTIF(RECEPTURA_WLASNA!K{R0}:K{R1},"ZWIĘKSZONO")'),
        (sr + 7, "Zmniejszone", f'=COUNTIF(RECEPTURA_WLASNA!K{R0}:K{R1},"ZMNIEJSZONO")'),
        (sr + 8, "Status udziałów", "=StatusUdzialow"),
    ]
    for row, lab, formula in sums:
        ws[f"A{row}"] = lab
        ws[f"A{row}"].font = font_label()
        cell = ws[f"B{row}"]
        cell.value = formula
        style_formula(cell)
        ws.merge_cells(f"B{row}:C{row}")
    ws[f"B{sr+1}"].number_format = "0.00"
    ws[f"B{sr+2}"].number_format = "0.00"
    ws.print_title_rows = "1:2"
    protect(ws)


def write_historia(wb):
    ws = wb.create_sheet("HISTORIA")
    banner(
        ws,
        "HISTORIA RECEPTUR",
        "L",
        "Każda wersja to nowy wiersz. Nie nadpisuj poprzednich. Makro ZapiszWersje dopisuje rekord i pozycje.",
    )
    headers = [
        "ID",
        "DATA",
        "NAZWA RECEPTURY",
        "SYSTEM BAZOWY",
        "WERSJA",
        "AUTOR",
        "MASA WŁASNA (g)",
        "KOD KOLORU",
        "LICZBA PIGMENTÓW",
        "UWAGI",
        "STATUS %",
        "ZAPISANO",
    ]
    widths = [12, 14, 28, 16, 10, 16, 16, 14, 16, 36, 28, 22]
    for i, (h, w) in enumerate(zip(headers, widths), 1):
        cell = ws.cell(8, i, h)
        cell.font = font_h()
        cell.fill = fill(NAVY2)
        cell.alignment = align_c()
        cell.border = thin
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A9"
    ws.auto_filter.ref = f"A8:L{8 + HN}"
    for r in range(9, 9 + HN):
        for c in range(1, 13):
            cell = ws.cell(r, c, "")
            style_input(cell)
        ws.cell(r, 2).number_format = "DD.MM.YYYY"
        ws.cell(r, 7).number_format = "0.00"
    ws["A9"] = "RC-0001"
    ws["B9"] = "=TODAY()"
    ws["C9"] = '=Meta_Nazwa'
    ws["D9"] = '=Meta_System'
    ws["E9"] = 1
    ws["F9"] = '=Meta_Autor'
    ws["G9"] = '=MasaWlasna'
    ws["H9"] = '=Meta_Kod'
    ws["I9"] = f'=COUNTIF(RECEPTURA_WLASNA!C{R0}:C{R1},"<>")'
    ws["J9"] = "Wersja startowa systemu"
    ws["K9"] = "=StatusUdzialow"
    ws["L9"] = "SZKIC — zapisz makro ZapiszWersje"
    for c in range(1, 13):
        style_formula(ws.cell(9, c))
        ws.cell(9, c).fill = fill(BLUE_SOFT)

    ws2 = wb.create_sheet("HISTORIA_POZYCJE")
    banner(ws2, "HISTORIA — POZYCJE WERSJI", "I", "Szczegóły składu zapisanych wersji. Klucz powiązania = ID + WERSJA.")
    h2 = ["ID", "WERSJA", "LP", "SYSTEM", "NR PIGMENTU", "NAZWA", "ILOŚĆ ORYG.", "ILOŚĆ WŁASNA", "STATUS"]
    w2 = [12, 10, 8, 14, 16, 32, 14, 14, 14]
    for i, (h, w) in enumerate(zip(h2, w2), 1):
        cell = ws2.cell(8, i, h)
        cell.font = font_h()
        cell.fill = fill(NAVY2)
        cell.alignment = align_c()
        cell.border = thin
        ws2.column_dimensions[get_column_letter(i)].width = w
    ws2.freeze_panes = "A9"
    for r in range(9, 509):
        for c in range(1, 10):
            style_input(ws2.cell(r, c))
    protect(ws)
    protect(ws2)


def write_dobarwianie(wb):
    ws = wb.create_sheet("DOBARWIANIE")
    banner(
        ws,
        "PROCEDURY DOBARWIANIA",
        "F",
        "Źródło: nexa-autocolor-2k-tint-chart-guide.pdf (opisy działania Autocolor przetłumaczone na PL) oraz Duxone - Tint Descriptions - PL.pdf (kopie w data/backup).",
    )
    ws["A4"] = "Wybierz system"
    ws["A4"].font = font_label()
    style_input(ws["B4"])
    ws["B4"] = "AUTOCOLOR"
    add_dv_list(ws, "=Lista_Systemow", "B4")
    ws["A5"] = "Wybierz pigment"
    ws["A5"].font = font_label()
    style_input(ws["B5"])
    fill_sidelists(ws)
    add_dv_nr_pigmentu(ws, "B5", "$B4")
    ws["A6"] = "Klucz"
    ws["C6"] = '=IF(B5="","","")'
    ws["B6"] = f'=IF(OR(B4="",B5=""),"",B4&"|"&{kod_z_pola_nr("B5")})'
    style_formula(ws["B6"])
    ws["A7"] = "Nazwa"
    ws["B7"] = '=IF(B6="", "", IFERROR(VLOOKUP(B6,PigmentyKlucz,4,FALSE),"BRAK W BAZIE"))'
    style_formula(ws["B7"])
    ws.merge_cells("B7:F7")
    ws["A8"] = "Opis działania (PL)"
    ws["B8"] = '=IF(B6="", "", IFERROR(VLOOKUP(B6,PigmentyKlucz,9,FALSE),""))'
    style_formula(ws["B8"])
    ws.merge_cells("B8:F14")
    ws["B8"].alignment = Alignment(wrap_text=True, vertical="top")
    ws["A7"].font = font_label()
    ws["A8"].font = font_label()
    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["B"].width = 22
    ws.column_dimensions["C"].width = 18
    ws.column_dimensions["D"].width = 18
    ws.column_dimensions["E"].width = 40
    ws.column_dimensions["F"].width = 40

    ws.merge_cells("A16:F16")
    ws["A16"] = "REGUŁY AUTOCOLOR (PDF TINTING GUIDE)"
    ws["A16"].font = Font(name="Calibri", size=12, bold=True, color=WHITE)
    ws["A16"].fill = fill(NAVY2)
    r = 17
    for rule in DATA["reguly_autocolor"]:
        ws[f"A{r}"] = rule["id"]
        ws[f"B{r}"] = rule["temat"]
        ws.merge_cells(f"C{r}:F{r}")
        ws[f"C{r}"] = rule["tresc"]
        ws[f"A{r}"].font = font_label()
        ws[f"B{r}"].font = Font(name="Calibri", size=10, bold=True)
        ws[f"C{r}"].alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[r].height = 48
        r += 1
    r += 1
    ws.merge_cells(f"A{r}:F{r}")
    ws[f"A{r}"] = "REGUŁY DUXONE (PDF TINT DESCRIPTIONS PL)"
    ws[f"A{r}"].font = Font(name="Calibri", size=12, bold=True, color=WHITE)
    ws[f"A{r}"].fill = fill(NAVY2)
    r += 1
    for rule in DATA["reguly_duxone"]:
        ws[f"A{r}"] = rule["id"]
        ws[f"B{r}"] = rule["temat"]
        ws.merge_cells(f"C{r}:F{r}")
        ws[f"C{r}"] = rule["tresc"]
        ws[f"A{r}"].font = font_label()
        ws[f"B{r}"].font = Font(name="Calibri", size=10, bold=True)
        ws[f"C{r}"].alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[r].height = 56
        r += 1
    protect(ws)
    ws["B4"].protection = Protection(locked=False)
    ws["B5"].protection = Protection(locked=False)


def seed_demo(wb):
    """Receptura startowa do testów — nie zastępuje baz, tylko wiersze robocze."""
    orig = wb["RECEPTURA_ORYGINALNA"]
    own = wb["RECEPTURA_WLASNA"]
    start = wb["START"]
    start["C5"] = "TEST START — srebrny bazowy"
    start["C6"] = "RC-0001"
    start["C7"] = "Silver test"
    start["C8"] = "TST-001"
    start["C9"] = "Warsztat"
    start["C10"] = "AUTOCOLOR"
    start["C11"] = 1
    start["C15"] = 100
    # 3 pigmenty Autocolor
    demo = [
        (12, "AUTOCOLOR", "P425-900", 50),
        (13, "AUTOCOLOR", "P425-984", 30),
        (14, "AUTOCOLOR", "P425-948", 20),
    ]
    for r, sys, nr, qty in demo:
        orig.cell(r, 2).value = sys
        orig.cell(r, 3).value = nr
        orig.cell(r, 5).value = qty
        own.cell(r, 2).value = sys
        own.cell(r, 3).value = nr
        own.cell(r, 6).value = qty


def order_sheets(wb):
    order = [
        "START",
        "RECEPTURA_ORYGINALNA",
        "RECEPTURA_WLASNA",
        "ANALIZA",
        "RAPORT",
        "HISTORIA",
        "DOBARWIANIE",
        "BAZA_AUTOCOLOR",
        "BAZA_DUXONE",
        "PIGMENTY",
        "USTAWIENIA",
        "HISTORIA_POZYCJE",
        "DANE_WYKRESOW",
        "LISTY",
    ]
    for i, name in enumerate(order):
        wb.move_sheet(name, offset=i - wb.sheetnames.index(name))


def patch_write_pigmenty(wb, n_ac, n_dx):
    # write_pigmenty accidentally added dummy defined name — clean
    dummy = [n for n in list(wb.defined_names.keys()) if n.startswith("DN") or n == ""]
    for n in dummy:
        try:
            del wb.defined_names[n]
        except Exception:
            pass


def main():
    wb = Workbook()
    default = wb.active
    default.title = "_tmp"
    n_ac, n_dx = write_bases(wb)
    write_pigmenty(wb, n_ac, n_dx)
    write_ustawienia(wb)
    write_listy(wb, n_ac, n_dx)
    write_start(wb)
    write_oryg(wb)
    write_wlasna(wb)
    write_wykresy_data(wb)
    write_analiza(wb)
    write_raport(wb)
    write_historia(wb)
    write_dobarwianie(wb)
    seed_demo(wb)
    if "_tmp" in wb.sheetnames:
        del wb["_tmp"]
    patch_write_pigmenty(wb, n_ac, n_dx)
    order_sheets(wb)
    wb.properties.title = "System receptur lakierów AUTOCOLOR / DUXONE"
    wb.properties.creator = "SD Autos — system receptur"
    OUT_XLSX.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT_XLSX)
    print("Zapisano", OUT_XLSX)
    print("AUTOCOLOR", n_ac, "DUXONE", n_dx, "PIGMENTY", n_ac + n_dx)


if __name__ == "__main__":
    main()
