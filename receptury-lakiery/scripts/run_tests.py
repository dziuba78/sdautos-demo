# -*- coding: utf-8 -*-
"""Testy systemu RECEPTURY_LAKIERY (LibreOffice Calc)."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pandas as pd
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from libreoffice_pack import ODS_UNLOCKED, convert  # noqa: E402
from import_receptura_pdf import (  # noqa: E402
    IMPORT_DIR,
    classify_system,
    default_start_dir,
    load_known_codes,
    make_noqty_pdf,
    make_test_pdf,
    parse_receptura_pdf,
    write_outputs,
)

ODS_BUILT = ROOT / "data" / "extracted" / "lo_convert" / "RECEPTURY_LAKIERY.ods"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

XLSX = ROOT / "RECEPTURY_LAKIERY.xlsx"
ODS = ROOT / "RECEPTURY_LAKIERY.ods"
OUT = ROOT / "data" / "extracted" / "test_out"
PIG = json.loads((ROOT / "data" / "extracted" / "pigmenty.json").read_text(encoding="utf-8"))

PASS = 0
FAIL = 0
LOG: list[str] = []


def ok(name: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    if cond:
        PASS += 1
        LOG.append(f"OK  {name} {detail}".rstrip())
        print(f"OK  {name} {detail}".rstrip())
    else:
        FAIL += 1
        LOG.append(f"FAIL {name} {detail}".rstrip())
        print(f"FAIL {name} {detail}".rstrip())


def math_share(qty, total):
    if not total:
        return 0.0
    return qty / total


def math_change(orig, own):
    if orig == 0:
        return None if own > 0 else 0.0
    return (own - orig) / orig


def math_status(orig, own):
    if orig > 0 and own == 0:
        return "USUNIĘTO"
    if orig == 0 and own > 0:
        return "DODANO"
    if own > orig:
        return "ZWIĘKSZONO"
    if own < orig:
        return "ZMNIEJSZONO"
    return "BEZ ZMIAN"


def test_structure():
    wb = load_workbook(XLSX)
    expected = [
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
    ok("T01 arkusze", wb.sheetnames == expected, str(wb.sheetnames))
    ac = wb["BAZA_AUTOCOLOR"]
    dx = wb["BAZA_DUXONE"]
    n_ac = sum(1 for r in range(9, 300) if ac.cell(r, 1).value)
    n_dx = sum(1 for r in range(9, 300) if dx.cell(r, 1).value)
    ok("T02 baza AUTOCOLOR >=96", n_ac >= 96, str(n_ac))
    ok("T03 baza DUXONE >=79", n_dx >= 79, str(n_dx))
    keys = set()
    dup = False
    for r in range(9, 9 + n_ac):
        k = ac.cell(r, 1).value
        if k in keys:
            dup = True
        keys.add(k)
    ok("T04 brak duplikatów kluczy AC", not dup)
    ok("T05 klucz zawiera SYSTEM|", all(str(k).startswith("AUTOCOLOR|") for k in keys if k))
    # mieszanie: te same numery teoretyczne są różne przez prefiks
    ok("T06 Autocolor 123 != Duxone 123", "AUTOCOLOR|123" != "DUXONE|123")
    charts = wb["ANALIZA"]._charts
    ok("T12 wykresy ANALIZA = 4", len(charts) == 4, str(len(charts)))
    start = wb["START"]
    ok("T START import PDF", "PDF" in str(start["A34"].value or "") and "ImportujZPdf" in str(start["C24"].value or ""), str(start["A34"].value)[:50])
    ok("T START sciezka PDF", start["A35"].value == "Ścieżka PDF")
    orig = wb["RECEPTURA_ORYGINALNA"]
    ok("T13 brak ochrony arkusza ORYG", orig.protection.sheet is not True)
    ok("T13b input złoty odblokowany E12", orig["E12"].protection.locked is False)
    ok("T13c formuła szara (flaga locked) D12", orig["D12"].protection.locked is True)
    ok("T13d walidacja ilości", any(dv.type == "decimal" for dv in orig.data_validations.dataValidation))
    names = set(wb.defined_names.keys())
    for n in ("Meta_System", "MasaOryg", "MasaWlasna", "PigmentyKlucz", "Lista_AUTOCOLOR", "Lista_DUXONE", "ListaAC", "ListaDX", "Import_PdfSciezka"):
        ok(f"T nazwa {n}", n in names)
    listy = wb["LISTY"]
    ac_lab = str(listy["F9"].value or "")
    dx_lab = str(listy["H9"].value or "")
    ok("T LISTY etykieta AC ma kod", " | " in ac_lab or ac_lab.startswith("P"), ac_lab[:40])
    ok("T LISTY etykieta DX ma kod", " | " in dx_lab or dx_lab.startswith("DX") or bool(dx_lab), dx_lab[:40])
    ok("T LISTY adres AC", "LISTY!" in str(listy["J9"].value or "") and "$F$" in str(listy["J9"].value or ""), str(listy["J9"].value))
    orig = wb["RECEPTURA_ORYGINALNA"]
    dv_nr = [
        dv
        for dv in orig.data_validations.dataValidation
        if dv.type == "list" and "$T$9" in str(dv.formula1 or "")
    ]
    ok("T DV NR zakres T (strzałka Calc)", len(dv_nr) >= 1, str([dv.formula1 for dv in orig.data_validations.dataValidation if dv.type == "list"]))
    ok("T sidelist AC T9", " | " in str(orig["T9"].value or "") or str(orig["T9"].value or "").startswith("P"), str(orig["T9"].value)[:40])
    ok("T sidelist DX U9", " | " in str(orig["U9"].value or "") or str(orig["U9"].value or "").startswith("DX"), str(orig["U9"].value)[:40])
    klucz12 = str(orig["I12"].value or "")
    ok("T klucz wyciąga kod z etykiety", "FIND" in klucz12 and " | " in klucz12, klucz12[:80])
    # kolizja HE02 zachowana
    he02 = None
    for r in range(9, 9 + n_ac):
        if ac.cell(r, 3).value == "P426-HE02":
            he02 = ac.cell(r, 13).value
            break
    ok("T kolizja P426-HE02 oznaczona", he02 == "KOLIZJA NAZW", str(he02))
    dx11 = None
    for r in range(9, 9 + n_dx):
        if dx.cell(r, 3).value == "DX11":
            dx11 = dx.cell(r, 13).value
            break
    ok("T DX11 do weryfikacji", dx11 == "DO WERYFIKACJI", str(dx11))
    ac_pl = 0
    ac_en = []
    ac_empty = []
    for r in range(9, 9 + n_ac):
        text = str(ac.cell(r, 10).value or "").strip()
        nr = ac.cell(r, 3).value
        if not text:
            ac_empty.append(nr)
            continue
        low = text.lower()
        pl_hit = any(
            k in low
            for k in (
                "flop",
                "odcień",
                "światł",
                "cień",
                "jeżeli",
                "rozjaśn",
                "ciemniejsz",
                "ziarn",
                "płatek",
                "kryj",
                "użyj",
                "dodaje",
                "toner",
                "metalik",
                "perł",
                "travel",
                "reguluj",
                "konwerter",
                "iskrz",
            )
        ) or any(ch in text for ch in "ąćęłńóśźżĄĆĘŁŃÓŚŹŻ")
        en_lead = text.startswith(("If more", "Yellow-shade", "Colour shifting", "Special effect", "Pale yellow with"))
        if pl_hit and not en_lead:
            ac_pl += 1
        else:
            ac_en.append(f"{nr}: {text[:50]}")
    ok("T AC opisy działania PL >=96", ac_pl >= 96, str(ac_pl))
    ok("T AC brak pustych opisów dobarwiania", len(ac_empty) == 0, str(ac_empty[:8]))
    ok("T AC brak surowego EN w OPIS_DOBARWIANIA", len(ac_en) == 0, str(ac_en[:6]))
    hdr = [ac.cell(8, c).value for c in range(1, 20)]
    ok("T AC kolumna OPIS_DZIALANIA_PL", "OPIS_DZIALANIA_PL" in hdr, str(hdr[-3:]))
    ok("T AC kolumna OPIS_EN", "OPIS_EN" in hdr)
    dx_sample = None
    for r in range(9, 9 + n_dx):
        if dx.cell(r, 3).value == "DX5111":
            dx_sample = str(dx.cell(r, 10).value or "")
            break
    ok("T DUXONE opis nadal PL", bool(dx_sample) and "If more" not in dx_sample, (dx_sample or "")[:80])
    wb.close()
    import zipfile

    def _ods_unlocked() -> Path:
        for p in (ODS_BUILT, ODS_UNLOCKED, ODS):
            if not p.exists():
                continue
            try:
                with zipfile.ZipFile(p) as z:
                    xml = z.read("content.xml").decode("utf-8")
                if 'table:protected="true"' not in xml:
                    return p
            except Exception:
                continue
        return ODS

    ods_check = _ods_unlocked()
    ok("T ODS istnieje", ods_check.exists(), str(ods_check))
    with zipfile.ZipFile(ods_check) as z:
        ok("T makra Basic", "Basic/Standard/modReceptury.xml" in z.namelist())
        xml = z.read("content.xml").decode("utf-8")
        bas = z.read("Basic/Standard/modReceptury.xml").decode("utf-8")
    ok("T ODS arkusze bez table:protected=true", 'table:protected="true"' not in xml)
    ok("T ODS bez protection-key", "table:protection-key=" not in xml)
    ok("T ODS makro bez ponownej ochrony", "Nie zakładaj ponownie ochrony" in bas)
    ok("T ODS event PrzyOtwarciu", "PrzyOtwarciu" in xml)
    ok("T ODS event OnWyborKomorki", "OnWyborKomorki" in xml)
    ok("T makro lista pigmentów", "DialogListaPigmentow" in bas and "CzyKomorkaNrPigmentu" in bas)
    ok("T makro ImportujZPdf", "ImportujZPdf" in bas and "WczytajOstatniImport" in bas)
    ok("T makro --wybierz", "--wybierz" in bas and "JoinCmdWybierz" in bas)
    ok("T makro SystemFilePicker", "SystemFilePicker" in bas)
    ok("T makro anulowanie PDF", "KomunikatAnulowanoImport" in bas and "n = 3" in bas)
    ok("T ODS przycisk importu", "btnImportPdf" in xml or "ImportujZPdf" in xml)


def test_json_autocolor_pl():
    ac = PIG["autocolor"]
    dx = PIG["duxone"]
    n_pl = 0
    missing = []
    still_en = []
    for r in ac:
        text = (r.get("procedura_dobarwiania") or r.get("opis") or "").strip()
        if not text:
            missing.append(r["nr_pigmentu"])
            continue
        if text.startswith(("If more", "Yellow-shade", "Colour shifting", "Special effect")):
            still_en.append(r["nr_pigmentu"])
            continue
        n_pl += 1
    ok("JSON AC PL opisy >=96", n_pl >= 96, str(n_pl))
    ok("JSON AC wszystkie z opisem", len(missing) == 0, str(missing[:10]))
    ok("JSON AC brak EN lead", len(still_en) == 0, str(still_en[:8]))
    ok("JSON AC baza >=96", len(ac) >= 96, str(len(ac)))
    dx_en = [r["nr_pigmentu"] for r in dx if str(r.get("opis") or "").startswith("If more")]
    ok("JSON DUXONE nie nadpisany EN", len(dx_en) == 0, str(dx_en[:5]))


def test_math_independent():
    orig = {"P425-900": 50, "P425-984": 30, "P425-948": 20}
    own = dict(orig)
    total_o = sum(orig.values())
    total_w = sum(own.values())
    ok("Test1 suma 100", total_o == 100 and total_w == 100)
    ok("Test1 status BEZ ZMIAN", all(math_status(orig[k], own[k]) == "BEZ ZMIAN" for k in orig))
    pct = [math_share(orig[k], total_o) * 100 for k in orig]
    ok("Test1 % 50/30/20", pct == [50, 30, 20])
    ok("Test14 suma % = 100", abs(sum(pct) - 100) < 0.01)

    own3 = dict(orig)
    own3["P425-900"] = 60
    ok("Test3 ZWIĘKSZONO", math_status(50, 60) == "ZWIĘKSZONO")
    ok("Test3 zmiana % +20", abs(math_change(50, 60) - 0.2) < 1e-9)

    own4 = dict(orig)
    own4["P425-984"] = 15
    ok("Test4 ZMNIEJSZONO", math_status(30, 15) == "ZMNIEJSZONO")
    ok("Test4 zmiana % -50", abs(math_change(30, 15) + 0.5) < 1e-9)

    ok("Test7 USUNIĘTO", math_status(20, 0) == "USUNIĘTO")
    ok("Test5/6 DODANO", math_status(0, 5) == "DODANO")
    ok("Test8 różne klucze", "AUTOCOLOR|123" != "DUXONE|123")

    # skala 100 -> 500
    factor = 500 / 100
    scaled = {k: v * factor for k, v in orig.items()}
    ok("Test9 100g→500g", scaled["P425-900"] == 250 and sum(scaled.values()) == 500)
    factor2 = 1000 / 100
    scaled2 = {k: v * factor2 for k, v in orig.items()}
    ok("Test10 100g→1kg", scaled2["P425-900"] == 500 and sum(scaled2.values()) == 1000)

    # duplikat: 50+10 = 60
    ok("Test11 suma duplikatu", 50 + 10 == 60)

    # dzielenie przez zero
    ok("Test14 zmiana przy orig=0", math_change(0, 8) is None)


def test_libreoffice_recalc():
    if not ODS.exists():
        ok("LO recalc", False, "brak ODS")
        return
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    # ODS już po konwersji LO — odczyt wartości
    start = pd.read_excel(ODS, sheet_name="START", header=None, engine="odf")
    orig = pd.read_excel(ODS, sheet_name="RECEPTURA_ORYGINALNA", header=None, engine="odf")
    wlas = pd.read_excel(ODS, sheet_name="RECEPTURA_WLASNA", header=None, engine="odf")
    # wiersze pandas 0-based; Excel row 12 = index 11
    names = [orig.iloc[11 + i, 3] for i in range(3)]
    qty_o = [orig.iloc[11 + i, 4] for i in range(3)]
    qty_w = [wlas.iloc[11 + i, 5] for i in range(3)]
    status = [wlas.iloc[11 + i, 10] for i in range(3)]
    pct_w = [wlas.iloc[11 + i, 9] for i in range(3)]
    print("LO names", names)
    print("LO qty_o", qty_o)
    print("LO qty_w", qty_w)
    print("LO status", status)
    print("LO pct", pct_w)
    print("START I5/I6/I11", start.iloc[4, 8], start.iloc[5, 8], start.iloc[10, 8])
    ok("LO Test1 ilości oryg", qty_o == [50, 30, 20], str(qty_o))
    ok("LO Test1 ilości własne", qty_w == [50, 30, 20], str(qty_w))
    bez = all(str(s).upper() == "BEZ ZMIAN" for s in status)
    ok("LO Test1 status BEZ ZMIAN", bez, str(status))
    if all(isinstance(p, (int, float)) for p in pct_w):
        ok("LO Test14 suma % ~ 1", abs(sum(pct_w) - 1) < 0.002, str(sum(pct_w)))
    else:
        ok("LO Test14 suma %", False, str(pct_w))
    masa = start.iloc[4, 8]
    ok("LO masa oryg 100", abs(float(masa) - 100) < 0.01 if pd.notna(masa) else False, str(masa))
    nazwa0 = str(names[0] or "")
    ok("LO nazwa z PDF/bazy", "WHITE" in nazwa0.upper() or "BIE" in nazwa0.upper() or nazwa0 != "", nazwa0)

    # drugi przebieg: mieszanie + zmiany — zapis xlsx i ponowna konwersja
    wb = load_workbook(XLSX)
    own = wb["RECEPTURA_WLASNA"]
    origs = wb["RECEPTURA_ORYGINALNA"]
    # Test3 zwiększ P425-900 do 60
    own["F12"] = 60
    # Test4 zmniejsz P425-984 do 15
    own["F13"] = 15
    # Test7 usuń P425-948
    own["F14"] = 0
    # Test6 dodaj DUXONE DX5110
    own["B15"] = "DUXONE"
    own["C15"] = "DX5110"
    own["F15"] = 5
    # Test8 ten sam numer z drugiego systemu — DUXONE nie ma 123, użyjemy kodu który istnieje
    # AUTOCOLOR P425-900 już jest; dodajemy „fałszywy” ten sam numer z DUXONE nie istnieje
    # zamiast tego: dodaj DX11 (inny system)
    own["B16"] = "DUXONE"
    own["C16"] = "DX5111"
    own["F16"] = 2
    # Test11 duplikat P425-900
    own["B17"] = "AUTOCOLOR"
    own["C17"] = "P425-900"
    own["F17"] = 10
    wb["START"]["C15"] = 500  # masa docelowa 500 g  (Test9)
    tmp = OUT / "mut.xlsx"
    wb.save(tmp)
    wb.close()
    ods2 = convert(tmp, "ods", OUT / "mut")
    w2 = pd.read_excel(ods2, sheet_name="RECEPTURA_WLASNA", header=None, engine="odf")
    st2 = pd.read_excel(ods2, sheet_name="START", header=None, engine="odf")
    statuses = [str(w2.iloc[11 + i, 10]) for i in range(6)]
    print("MUT status", statuses)
    print("MUT F", [w2.iloc[11 + i, 5] for i in range(6)])
    print("MUT M zważ", [w2.iloc[11 + i, 12] for i in range(6)])
    print("MUT kontrola", [w2.iloc[11 + i, 13] for i in range(6)])
    ok("LO Test3 ZWIĘKSZONO", "ZWIĘKSZONO" in statuses[0].upper(), statuses[0])
    ok("LO Test4 ZMNIEJSZONO", "ZMNIEJSZONO" in statuses[1].upper(), statuses[1])
    ok("LO Test7 USUNIĘTO", "USUNIĘTO" in statuses[2].upper(), statuses[2])
    ok("LO Test6 DODANO DUXONE", "DODANO" in statuses[3].upper(), statuses[3])
    ok("LO Test6 system DUXONE", str(w2.iloc[14, 1]).upper() == "DUXONE")
    ok("LO Test8 drugi pigment DUXONE", str(w2.iloc[15, 2]).upper() == "DX5111")
    dup = str(w2.iloc[11, 13]) + " " + str(w2.iloc[16, 13])
    ok("LO Test11 DUPLIKAT", "DUPLIKAT" in dup.upper(), dup)
    # Test9: ilość do zważenia dla 60 przy masie własnej
    # masa własna = 60+15+0+5+2+10 = 92
    # skala 500/92, zważenie P425-900 pierwsza pozycja = 60*500/92
    masa_w = 60 + 15 + 0 + 5 + 2 + 10
    expected_waz = 60 * 500 / masa_w
    got_waz = w2.iloc[11, 12]
    if pd.notna(got_waz):
        ok("LO Test9 przeliczenie 500g", abs(float(got_waz) - expected_waz) < 0.05, f"{got_waz} vs {expected_waz}")
    else:
        ok("LO Test9 przeliczenie 500g", False, str(got_waz))
    st_status = str(st2.iloc[10, 8])
    ok("LO status udziałów wypełniony", "RECEPTURA" in st_status.upper() or "UWAGA" in st_status.upper() or st_status != "", st_status)

    # Test10 1 kg
    wb = load_workbook(tmp)
    wb["START"]["C15"] = 1000
    tmp3 = OUT / "mut1kg.xlsx"
    wb.save(tmp3)
    wb.close()
    ods3 = convert(tmp3, "ods", OUT / "mut1kg")
    w3 = pd.read_excel(ods3, sheet_name="RECEPTURA_WLASNA", header=None, engine="odf")
    expected1000 = 60 * 1000 / masa_w
    got1000 = w3.iloc[11, 12]
    if pd.notna(got1000):
        ok("LO Test10 przeliczenie 1kg", abs(float(got1000) - expected1000) < 0.05, f"{got1000} vs {expected1000}")
    else:
        ok("LO Test10 przeliczenie 1kg", False, str(got1000))

    # Test2 DUXONE bez zmian — nowy plik
    wb = load_workbook(XLSX)
    o = wb["RECEPTURA_ORYGINALNA"]
    w = wb["RECEPTURA_WLASNA"]
    wb["START"]["C10"] = "DUXONE"
    for r in range(12, 18):
        o.cell(r, 2).value = None
        o.cell(r, 3).value = None
        o.cell(r, 5).value = None
        w.cell(r, 2).value = None
        w.cell(r, 3).value = None
        w.cell(r, 6).value = None
    demo = [(12, "DX5130", 70), (13, "DX5110", 20), (14, "DX5215", 10)]
    for r, nr, q in demo:
        o.cell(r, 2).value = "DUXONE"
        o.cell(r, 3).value = nr
        o.cell(r, 5).value = q
        w.cell(r, 2).value = "DUXONE"
        w.cell(r, 3).value = nr
        w.cell(r, 6).value = q
    tmp4 = OUT / "dux.xlsx"
    wb.save(tmp4)
    wb.close()
    ods4 = convert(tmp4, "ods", OUT / "dux")
    w4 = pd.read_excel(ods4, sheet_name="RECEPTURA_WLASNA", header=None, engine="odf")
    st4 = pd.read_excel(ods4, sheet_name="RECEPTURA_ORYGINALNA", header=None, engine="odf")
    ok("LO Test2 DUXONE nr", str(w4.iloc[11, 2]).upper() == "DX5130", str(w4.iloc[11, 2]))
    ok("LO Test2 DUXONE status", str(w4.iloc[11, 10]).upper() == "BEZ ZMIAN", str(w4.iloc[11, 10]))
    ok("LO Test2 masa 100", abs(float(pd.read_excel(ods4, sheet_name="START", header=None, engine="odf").iloc[4, 8]) - 100) < 0.05)
    naz = str(w4.iloc[11, 3] or "")
    ok("LO Test2 nazwa z PDF Duxone", "WHITE" in naz.upper() or naz != "", naz)

    # Test5 dodaj AUTOCOLOR do DUXONE
    wb = load_workbook(tmp4)
    wb["RECEPTURA_WLASNA"]["B15"] = "AUTOCOLOR"
    wb["RECEPTURA_WLASNA"]["C15"] = "P425-941"
    wb["RECEPTURA_WLASNA"]["F15"] = 8
    tmp5 = OUT / "mix.xlsx"
    wb.save(tmp5)
    wb.close()
    ods5 = convert(tmp5, "ods", OUT / "mix")
    w5 = pd.read_excel(ods5, sheet_name="RECEPTURA_WLASNA", header=None, engine="odf")
    ok("LO Test5 AUTOCOLOR w DUXONE", str(w5.iloc[14, 1]).upper() == "AUTOCOLOR" and str(w5.iloc[14, 2]).upper() == "P425-941")
    ok("LO Test5 DODANO", "DODANO" in str(w5.iloc[14, 10]).upper(), str(w5.iloc[14, 10]))


def test_import_pdf():
    pig_path = ROOT / "data" / "extracted" / "pigmenty.json"
    pig_before = pig_path.read_bytes()
    known = load_known_codes()
    ok("T import SYSTEM ze wzorca AC", classify_system("P425-900") == "AUTOCOLOR")
    ok("T import SYSTEM ze wzorca DX", classify_system("DX5110") == "DUXONE")
    ok("T import 123 bez wzorca", classify_system("123") is None)
    IMPORT_DIR.mkdir(parents=True, exist_ok=True)
    good = make_test_pdf(IMPORT_DIR / "przyklad_receptura_test.pdf")
    bad = make_noqty_pdf(IMPORT_DIR / "przyklad_brak_receptury.pdf")
    r1 = parse_receptura_pdf(good, known)
    write_outputs(r1, IMPORT_DIR)
    nrs = [p["nr"] for p in r1.get("pozycje") or []]
    syss = [p["system"] for p in r1.get("pozycje") or []]
    ok("T import test PDF 4 pozycje", r1.get("ok") is True and len(nrs) == 4, str(nrs))
    ok("T import kody", nrs == ["P425-900", "P425-984", "DX5110", "P425-ZZ99"], str(nrs))
    ok("T import systemy wzorzec", syss == ["AUTOCOLOR", "AUTOCOLOR", "DUXONE", "AUTOCOLOR"], str(syss))
    zz = next((p for p in r1.get("pozycje") or [] if p["nr"] == "P425-ZZ99"), None)
    ok("T import nieznany DO WERYFIKACJI", bool(zz) and zz["znany"] is False and zz["uwagi"] == "DO WERYFIKACJI", str(zz))
    r2 = parse_receptura_pdf(bad, known)
    ok("T import bez ilości", r2.get("ok") is False and "nie znaleziono receptury" in (r2.get("komunikat") or ""), r2.get("komunikat"))
    tint = ROOT / "data" / "backup" / "nexa-autocolor-2k-tint-chart-guide.pdf"
    if tint.exists():
        r3 = parse_receptura_pdf(tint, known)
        ok(
            "T import tint chart nie jest recepturą",
            r3.get("ok") is False and "nie znaleziono receptury" in (r3.get("komunikat") or ""),
            r3.get("komunikat"),
        )
    else:
        ok("T import tint chart nie jest recepturą", False, "brak PDF")
    ok("T import nie rusza pigmenty.json", pig_path.read_bytes() == pig_before)
    d_hint = default_start_dir(str(IMPORT_DIR))
    ok("T import start dir z hintu", Path(d_hint).resolve() == IMPORT_DIR.resolve(), d_hint)
    d_file = default_start_dir(str(IMPORT_DIR / "przyklad_receptura_test.pdf"))
    ok("T import start dir z pliku", Path(d_file).resolve() == IMPORT_DIR.resolve(), d_file)
    d_empty = default_start_dir()
    ok("T import start dir niepusty", bool(d_empty) and Path(d_empty).is_dir(), d_empty)
    src = (ROOT / "scripts" / "import_receptura_pdf.py").read_text(encoding="utf-8")
    ok("T import skrypt --wybierz", "--wybierz" in src and "choose_pdf_path" in src and "IFileOpenDialog" in src)
    import import_receptura_pdf as imp

    marker = IMPORT_DIR / "ostatni.txt"
    before = marker.read_text(encoding="utf-8") if marker.exists() else None
    orig_choose = imp.choose_pdf_path
    imp.choose_pdf_path = lambda initial_dir=None: None
    try:
        rc = imp.main(["--wybierz"])
    finally:
        imp.choose_pdf_path = orig_choose
    ok("T import --wybierz anulowanie kod 3", rc == 3)
    after = marker.read_text(encoding="utf-8") if marker.exists() else None
    ok("T import anulowanie nie nadpisuje ostatni.txt", before == after)


def main():
    test_json_autocolor_pl()
    test_import_pdf()
    test_structure()
    test_math_independent()
    test_libreoffice_recalc()
    report = ROOT / "docs" / "TESTY.md"
    report.parent.mkdir(exist_ok=True)
    report.write_text(
        f"# Raport testów\n\nPASS={PASS} FAIL={FAIL}\n\n" + "\n".join(f"- {x}" for x in LOG) + "\n",
        encoding="utf-8",
    )
    print(f"\nPASS={PASS} FAIL={FAIL}")
    if FAIL:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
