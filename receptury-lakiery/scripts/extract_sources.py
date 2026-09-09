# -*- coding: utf-8 -*-
"""Ekstrakcja baz pigmentów z ODS + PDF (bez modyfikacji oryginałów)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

from autocolor_tlumaczenia import apply_autocolor_tint

ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / "data" / "backup"
OUT = ROOT / "data" / "extracted"
OUT.mkdir(parents=True, exist_ok=True)

AC_ODS = next(BACKUP.glob("*autocolor*.ods"))
DX_ODS = next(BACKUP.glob("*DUXONE*.ods"))
PDF_AC = BACKUP / "nexa-autocolor-2k-tint-chart-guide.pdf"
PDF_DX = BACKUP / "Duxone - Tint Descriptions - PL.pdf"

AC_CODE_RE = re.compile(
    r"^(P\d{3}-[A-Z0-9]+(?:RT)?|VM\d{4})\s*(RT)?$",
    re.I,
)
DX_CODE_RE = re.compile(r"^(DX\d{2,5}|AXT\d{3}|DX11)$", re.I)


def _norm_code(code: str) -> str:
    code = re.sub(r"\s+", "", str(code).strip().upper())
    return code


def _clean_text(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip(" \n-–")


def parse_autocolor_pdf(text: str) -> dict[str, dict]:
    """Wyciąga kod → {nazwa, opis, procedura} z przewodnika Nexa Autocolor."""
    pages = text.split("===== PAGE")
    body = "\n".join(pages)
    lines = [ln.strip() for ln in body.splitlines()]
    skip_exact = {
        "TINTING GUIDE",
        "MIXING BASES",
        "TONER SYMBOL",
        "TONER",
        "CHARACTERISTICS",
        "PICTOGRAM KEY",
        "BLACKS & WHITES",
        "METALLICS",
        "FLAKE SIZE",
        "FLOP ADJUSTERS",
        "PEARLS",
        "SPECIAL EFFECTS",
        "FACE",
        "COLOUR",
        "FAMILY",
        "TONE",
        "FLOP",
        "COLOUR FAMILY",
        "COLOUR TRAVEL",
        "CHARACTERISTIC KEY",
        "PEARLS",
        "ALUMINIUMS",
        "COLOURED",
        "LENTICULAR",
        "SPECIAL",
        "EFFECTS",
        "LIGHT FACE",
        "LIGHT FLOP",
        "DARK FLOP",
        "MEDIUM FLOP",
        "LIGHT FACE MEDIUM FLOP",
        "LIGHT FACE DARK FLOP",
    }
    skip_startswith = (
        "©2018",
        "The PPG",
        "Part No",
        "COLOUR FAMILY",
        "FACE –",
        "FLOP –",
        "TONE –",
        "FLAKE SIZE",
        "Sensitivity",
    )

    def is_description(line: str) -> bool:
        low = f" {line.lower()} "
        keys = (
            " with ",
            " than ",
            " flop",
            " face",
            " used ",
            " if more",
            " gives ",
            " sparkle",
            " special effect",
            " colour shift",
            " vacuumized",
            " particularly",
            " opaque ",
            " transparent ",
            " high strength",
            " yellow-shade",
            " blue-shade",
            " exhibits ",
            " interference ",
        )
        if any(k in low for k in keys):
            return True
        return len(line) > 48

    items: dict[str, dict] = {}
    i = 0
    while i < len(lines):
        raw = lines[i]
        if not raw:
            i += 1
            continue
        m = AC_CODE_RE.match(raw.replace("  ", " ").strip())
        code = None
        rt = False
        if m:
            code = _norm_code(m.group(1))
            rt = bool(m.group(2)) or code.endswith("RT")
        else:
            # "P420-908 RT Russet" w jednej linii
            m2 = re.match(
                r"^(P\d{3}-[A-Z0-9]+|VM\d{4})\s+(RT\s+)?(.+)$",
                raw,
                re.I,
            )
            if m2 and not raw.upper().startswith("P192"):
                code = _norm_code(m2.group(1))
                rt = bool(m2.group(2)) or code.endswith("RT")
                rest = m2.group(3).strip()
                if rest.upper() in skip_exact:
                    rest = ""
                name_parts = [rest] if rest else []
                desc_parts: list[str] = []
                i += 1
                while i < len(lines):
                    nxt = lines[i]
                    if not nxt:
                        i += 1
                        continue
                    if AC_CODE_RE.match(nxt) or re.match(
                        r"^(P\d{3}-[A-Z0-9]+|VM\d{4})\b", nxt, re.I
                    ):
                        break
                    if nxt in skip_exact or nxt.startswith(skip_startswith):
                        i += 1
                        continue
                    if is_description(nxt) or name_parts:
                        if not name_parts:
                            name_parts.append(nxt)
                        elif is_description(nxt) or len(" ".join(name_parts)) > 40:
                            desc_parts.append(nxt)
                        else:
                            name_parts.append(nxt)
                    else:
                        name_parts.append(nxt)
                    i += 1
                name = _clean_text(" ".join(name_parts))
                desc = _clean_text(" ".join(desc_parts))
                if rt and not code.endswith("RT"):
                    items[code + "RT"] = {
                        "nr_pdf": code,
                        "nazwa_pdf": name,
                        "opis_pdf": desc,
                        "rt": True,
                    }
                items[code] = {
                    "nr_pdf": code,
                    "nazwa_pdf": name,
                    "opis_pdf": desc,
                    "rt": rt,
                }
                continue
        if not code:
            i += 1
            continue
        name_parts = []
        desc_parts = []
        i += 1
        while i < len(lines):
            nxt = lines[i]
            if not nxt:
                i += 1
                continue
            if AC_CODE_RE.match(nxt) or re.match(
                r"^(P\d{3}-[A-Z0-9]+|VM\d{4})\s", nxt, re.I
            ):
                break
            if nxt in skip_exact or nxt.startswith(skip_startswith):
                i += 1
                continue
            if re.match(r"^P\d{3}-", nxt) or re.match(r"^VM\d{4}", nxt):
                break
            if not name_parts:
                name_parts.append(nxt)
            elif is_description(nxt) or len(" ".join(name_parts)) > 40:
                desc_parts.append(nxt)
            else:
                name_parts.append(nxt)
            i += 1
        name = _clean_text(" ".join(name_parts))
        desc = _clean_text(" ".join(desc_parts))
        rec = {
            "nr_pdf": code,
            "nazwa_pdf": name,
            "opis_pdf": desc,
            "rt": rt or code.endswith("RT"),
        }
        items[code] = rec
        if rec["rt"] and not code.endswith("RT"):
            items[code + "RT"] = dict(rec)
    return items


def parse_duxone_pdf(text: str) -> dict[str, dict]:
    """Wyciąga DX/AXT → {nazwa, opis} z 'Duxone - Tint Descriptions - PL'."""
    lines = [ln.strip() for ln in text.splitlines()]
    skip = {
        "Sensitivity: Business Internal",
        "AN AXALTA COATING SYSTEMS BRAND",
        "WWW.DUXONE.COM",
        "DZIĘKUJĘ",
        "OPIS KOMPONENTÓW",
        "LAKIER BAZOWY",
    }
    items: dict[str, dict] = {}
    i = 0
    while i < len(lines):
        raw = lines[i]
        if not raw or raw in skip:
            i += 1
            continue
        m = DX_CODE_RE.match(raw.replace("…", "").strip())
        if not m:
            i += 1
            continue
        code = _norm_code(m.group(1))
        name_parts: list[str] = []
        desc_parts: list[str] = []
        i += 1
        while i < len(lines):
            nxt = lines[i]
            if DX_CODE_RE.match(nxt.replace("…", "").strip()):
                break
            if not nxt or nxt in skip or nxt.startswith("====="):
                i += 1
                continue
            if nxt.startswith("Lakier") or nxt.startswith("Dobarw") or nxt.startswith("Dobrw"):
                i += 1
                continue
            if nxt.startswith("KOMPONENTY") or nxt.startswith("Komponenty Duxone"):
                i += 1
                continue
            if nxt.startswith("–") or nxt.startswith("-") or nxt.startswith("➢"):
                desc_parts.append(nxt.lstrip("-–➢ ").strip())
            elif not name_parts and not nxt[0].isdigit():
                name_parts.append(nxt)
            else:
                desc_parts.append(nxt)
            i += 1
        name = _clean_text(" ".join(name_parts))
        desc = _clean_text("\n".join(desc_parts))
        if code == "DX5":
            continue
        rec = {
            "nr_pdf": code,
            "nazwa_pdf": name,
            "opis_pdf": desc,
        }
        prev = items.get(code)
        if prev and prev.get("nazwa_pdf") and not name:
            continue
        if prev and prev.get("opis_pdf") and not desc:
            rec["opis_pdf"] = prev["opis_pdf"]
            rec["nazwa_pdf"] = name or prev.get("nazwa_pdf", "")
        if prev and prev.get("nazwa_pdf") and name and len(prev["nazwa_pdf"]) >= len(name):
            if not desc:
                continue
            rec["nazwa_pdf"] = prev["nazwa_pdf"]
            if prev.get("opis_pdf") and len(prev["opis_pdf"]) > len(desc):
                rec["opis_pdf"] = prev["opis_pdf"]
        items[code] = rec
    return items


def load_ods_autocolor() -> list[dict]:
    cat = pd.read_excel(AC_ODS, sheet_name="NEXA AUTOCOLOR® CAR", engine="odf", header=None)
    ark = pd.read_excel(AC_ODS, sheet_name="Arkusz1", engine="odf", header=None)
    by_nr: dict[str, dict] = {}
    for _, row in cat.iterrows():
        kod_e = row[0]
        nr = row[1]
        nazwa = row[2]
        if pd.isna(nr) or str(nr).strip() == "":
            continue
        nr_s = str(nr).strip()
        kod_e_s = "" if pd.isna(kod_e) else str(kod_e).strip()
        nazwa_s = "" if pd.isna(nazwa) else str(nazwa).strip()
        m = re.search(r"/E([0-9]+(?:\.[0-9]+)?)$", kod_e_s, re.I)
        e_factor = float(m.group(1)) if m else None
        nr_bazowy = kod_e_s.split("/E")[0] if kod_e_s else nr_s
        by_nr[nr_s] = {
            "nr_pigmentu": nr_s,
            "nr_bazowy": nr_bazowy,
            "kod_e": kod_e_s,
            "czynnik_e": e_factor,
            "nazwa_ods": nazwa_s,
            "w_katalogu": True,
            "w_szablonie": False,
        }
    for val in ark[26].dropna():
        nr_s = str(val).strip()
        if nr_s not in by_nr:
            by_nr[nr_s] = {
                "nr_pigmentu": nr_s,
                "nr_bazowy": nr_s,
                "kod_e": "",
                "czynnik_e": None,
                "nazwa_ods": "",
                "w_katalogu": False,
                "w_szablonie": True,
            }
        else:
            by_nr[nr_s]["w_szablonie"] = True
    return list(by_nr.values())


def load_ods_duxone() -> list[dict]:
    ark = pd.read_excel(DX_ODS, sheet_name="Arkusz1", engine="odf", header=None)
    rows = []
    for val in ark[26].dropna():
        nr_s = str(val).strip()
        if not nr_s:
            continue
        rows.append(
            {
                "nr_pigmentu": nr_s,
                "nr_bazowy": nr_s,
                "kod_e": "",
                "czynnik_e": None,
                "nazwa_ods": "",
                "w_katalogu": False,
                "w_szablonie": True,
            }
        )
    return rows


def merge_autocolor(ods_rows: list[dict], pdf: dict[str, dict]) -> list[dict]:
    used_pdf = set()
    out = []
    for rec in ods_rows:
        nr = rec["nr_pigmentu"]
        nr_n = _norm_code(nr)
        pdf_hit = pdf.get(nr_n) or pdf.get(nr_n.replace("RT", "")) or pdf.get(rec["nr_bazowy"].upper())
        nazwa_pdf = (pdf_hit or {}).get("nazwa_pdf", "")
        opis_pdf = (pdf_hit or {}).get("opis_pdf", "")
        if pdf_hit:
            used_pdf.add(nr_n)
            used_pdf.add(_norm_code(pdf_hit.get("nr_pdf", "")))
        nazwa_ods = rec["nazwa_ods"]
        if nazwa_pdf:
            nazwa = nazwa_pdf
            zrodlo_nazwy = "PDF_AUTOCOLOR"
        else:
            nazwa = nazwa_ods.replace("2K ", "").strip() if nazwa_ods else ""
            zrodlo_nazwy = "ODS_KATALOG" if nazwa_ods else "BRAK"
        status = "OK"
        uwagi = []
        if nazwa_pdf and nazwa_ods:
            a = _fold_name(nazwa_ods)
            b = _fold_name(nazwa_pdf)
            if a and b and a not in b and b not in a:
                status = "KOLIZJA NAZW"
                uwagi.append(f"ODS: {nazwa_ods} | PDF: {nazwa_pdf}")
        if not nazwa:
            status = "DO WERYFIKACJI"
            uwagi.append("Brak nazwy w ODS i PDF")
        procedura = ""
        if opis_pdf:
            if re.search(r"If more than 10%", opis_pdf, re.I):
                procedura = opis_pdf
            else:
                procedura = ""
        out.append(
            {
                "system": "AUTOCOLOR",
                "klucz": f"AUTOCOLOR|{nr}",
                "nr_pigmentu": nr,
                "nr_bazowy": rec["nr_bazowy"],
                "kod_e": rec["kod_e"],
                "czynnik_e": rec["czynnik_e"],
                "nazwa": nazwa,
                "nazwa_ods": nazwa_ods,
                "nazwa_pdf": nazwa_pdf,
                "opis": opis_pdf,
                "procedura_dobarwiania": procedura or opis_pdf,
                "jednostka": "g",
                "kategoria": _autocolor_kategoria(nr, nazwa_ods, nazwa_pdf),
                "status_danych": status,
                "uwagi_danych": "; ".join(uwagi),
                "zrodlo_nazwy": zrodlo_nazwy,
                "w_katalogu_ods": rec["w_katalogu"],
                "w_szablonie_ods": rec["w_szablonie"],
            }
        )
    # pigmenty tylko z PDF (nie usuwamy ODS, dodajemy extra)
    for code, hit in pdf.items():
        if code.endswith("RT"):
            continue
        already = any(
            _norm_code(r["nr_pigmentu"]).replace("RT", "") == code.replace("RT", "")
            or _norm_code(r["nr_bazowy"]) == code
            for r in out
        )
        if already:
            continue
        nr = hit["nr_pdf"]
        out.append(
            {
                "system": "AUTOCOLOR",
                "klucz": f"AUTOCOLOR|{nr}",
                "nr_pigmentu": nr,
                "nr_bazowy": nr,
                "kod_e": "",
                "czynnik_e": None,
                "nazwa": hit.get("nazwa_pdf", ""),
                "nazwa_ods": "",
                "nazwa_pdf": hit.get("nazwa_pdf", ""),
                "opis": hit.get("opis_pdf", ""),
                "procedura_dobarwiania": hit.get("opis_pdf", ""),
                "jednostka": "g",
                "kategoria": _autocolor_kategoria(nr, "", hit.get("nazwa_pdf", "")),
                "status_danych": "DODANY Z PDF",
                "uwagi_danych": "Kod występuje w przewodniku dobarwiania, brak w ODS",
                "zrodlo_nazwy": "PDF_AUTOCOLOR",
                "w_katalogu_ods": False,
                "w_szablonie_ods": False,
            }
        )
        used_pdf.add(code)
    apply_autocolor_tint(out)
    return out


def _fold_name(s: str) -> str:
    s = s.upper()
    s = re.sub(r"\b2K\b", " ", s)
    s = re.sub(r"\bHS\b", " ", s)
    s = re.sub(r"\bRT\b", " ", s)
    s = s.replace("-", " ")
    s = re.sub(r"[^A-Z0-9 ]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _autocolor_kategoria(nr: str, nazwa_ods: str, nazwa_pdf: str) -> str:
    blob = f"{nr} {nazwa_ods} {nazwa_pdf}".upper()
    if nr.startswith("P192"):
        return "Regulator"
    if "XIRALLIC" in blob or nr.startswith("P433"):
        return "Xirallic"
    if "COLORSTREAM" in blob or nr.startswith("P434"):
        return "Colorstream"
    if "CHROMAFLAIR" in blob or nr.startswith("P440-FX") or nr.startswith("VM49"):
        return "ChromaFlair"
    if "PEARL" in blob or "-PP" in nr:
        return "Perła"
    if "ALUMINI" in blob or "FLASH" in blob or "LIQUID METAL" in blob:
        return "Aluminium"
    if "BLACK" in blob or "WHITE" in blob or "GRAPHITE" in blob:
        return "Czerń/Biel"
    if "REGULATOR" in blob or "TONE CONTROLLER" in blob or "FROST" in blob:
        return "Regulator"
    return "Toner"


def merge_duxone(ods_rows: list[dict], pdf: dict[str, dict]) -> list[dict]:
    out = []
    for rec in ods_rows:
        nr = rec["nr_pigmentu"]
        nr_n = _norm_code(nr)
        hit = pdf.get(nr_n)
        nazwa_pdf = (hit or {}).get("nazwa_pdf", "")
        opis_pdf = (hit or {}).get("opis_pdf", "")
        nazwa = nazwa_pdf
        zrodlo = "PDF_DUXONE" if nazwa else "BRAK"
        status = "OK" if nazwa else "DO WERYFIKACJI"
        uwagi = "" if nazwa else "Brak nazwy w PDF dobarwiania i w ODS"
        out.append(
            {
                "system": "DUXONE",
                "klucz": f"DUXONE|{nr}",
                "nr_pigmentu": nr,
                "nr_bazowy": nr,
                "kod_e": "",
                "czynnik_e": None,
                "nazwa": nazwa,
                "nazwa_ods": "",
                "nazwa_pdf": nazwa_pdf,
                "opis": opis_pdf,
                "procedura_dobarwiania": opis_pdf,
                "jednostka": "g",
                "kategoria": _duxone_kategoria(nr, nazwa),
                "status_danych": status,
                "uwagi_danych": uwagi,
                "zrodlo_nazwy": zrodlo,
                "w_katalogu_ods": False,
                "w_szablonie_ods": True,
            }
        )
    known = {_norm_code(r["nr_pigmentu"]) for r in out}
    for code, hit in pdf.items():
        if code in known or not code.startswith("DX"):
            continue
        if len(code) < 4:
            continue
        out.append(
            {
                "system": "DUXONE",
                "klucz": f"DUXONE|{hit['nr_pdf']}",
                "nr_pigmentu": hit["nr_pdf"],
                "nr_bazowy": hit["nr_pdf"],
                "kod_e": "",
                "czynnik_e": None,
                "nazwa": hit.get("nazwa_pdf", ""),
                "nazwa_ods": "",
                "nazwa_pdf": hit.get("nazwa_pdf", ""),
                "opis": hit.get("opis_pdf", ""),
                "procedura_dobarwiania": hit.get("opis_pdf", ""),
                "jednostka": "g",
                "kategoria": _duxone_kategoria(hit["nr_pdf"], hit.get("nazwa_pdf", "")),
                "status_danych": "DODANY Z PDF",
                "uwagi_danych": "Kod w PDF dobarwiania, brak w szablonie ODS",
                "zrodlo_nazwy": "PDF_DUXONE",
                "w_katalogu_ods": False,
                "w_szablonie_ods": False,
            }
        )
    return out


def _duxone_kategoria(nr: str, nazwa: str) -> str:
    n = nr.upper()
    blob = f"{nr} {nazwa}".upper()
    if n.startswith("AXT"):
        return "Dodatek do lakieru bezbarwnego"
    if n in {"DX11"}:
        return "Dodatek"
    if n.startswith("DX01"):
        return "Niska siła krycia"
    if n.startswith("DX53"):
        return "Xirallic/Crystal"
    if "PEARL" in blob or "CRYSTAL" in blob:
        return "Perła"
    if n.startswith("DX52") or "SILVER" in blob or "ALU" in blob:
        return "Aluminium"
    if "ADJUSTER" in blob or "UNISILVER" in blob or "EFFECT WHITE" in blob:
        return "Modyfikator"
    if n.startswith("DX51"):
        return "Solid"
    return "Inne"


def duxone_rules() -> list[dict]:
    return [
        {
            "id": "DX-R01",
            "temat": "Korygowanie — zasada ogólna",
            "tresc": "Wizualne korygowanie koloru (mokre korygowanie) jest zalecane tylko przy nieudanych wynikach w narzędziach kolorystycznych. Zawsze używaj komponentów już obecnych w formule. Ograniczaj liczbę komponentów branych do korekty.",
        },
        {
            "id": "DX-R02",
            "temat": "Kąty obserwacji",
            "tresc": "Kolor obserwuje się pod 3 kątami: 15° (pod kątem), 45° (na wprost), 110° (pod dużym kątem / flop).",
        },
        {
            "id": "DX-R03",
            "temat": "Aluminium — rozjaśnianie",
            "tresc": "Aby uzyskać jaśniejszy kolor aluminium, nie używaj białego komponentu — korzystaj z komponentów aluminium. Biały rozjaśnia flop (110°) i ściemnia 15° oraz 45°. Drobniejsze ziarno = jaśniejsze pod 110°. Grubsze ziarno = ciemniejsze pod 110°.",
        },
        {
            "id": "DX-R04",
            "temat": "Perły",
            "tresc": "Większość pereł jest transparentna. Zwiększają nasycenie kolorów z efektem. Zaleca się perły już obecne w formule. Biała perła rozjaśnia kolory perłowe. Kolor nie powstaje wyłącznie z pereł (wyjątek: tri-stage — warstwa efektowa).",
        },
        {
            "id": "DX-R05",
            "temat": "DX5136 Metallic Adjuster",
            "tresc": "Tylko kolory metaliczne i perłowe. Ściemia NRSP (15°), rozjaśnia flop i ziarno. Maks. 12% masy receptury.",
        },
        {
            "id": "DX-R06",
            "temat": "DX5134 Effect White",
            "tresc": "W kolorach z efektem: bardziej żółty pod 15°, bardziej niebieski i jaśniejszy na flopie. Maks. 40% masy receptury.",
        },
        {
            "id": "DX-R07",
            "temat": "Biel DX5130 ↔ DX0132",
            "tresc": "Zamień DX5130 na DX0132 gdy stężenie DX5130 < 0,45% masy; gdy DX0132 > 8%, zastosuj DX5130. Przelicznik: DX5130 × 10 = DX0132.",
        },
        {
            "id": "DX-R08",
            "temat": "Czerń DX5110 ↔ DX5111 / DX0112",
            "tresc": "DX5111 jest mocniejszy (niebieski odcień); DX5110 × 2 = DX5111. DX5110 (żółte zabarwienie) ↔ DX0112: zamiana gdy DX5110 < 0,45%; gdy DX0112 > 8% wróć do DX5110. Przelicznik DX5110 × 10 = DX0112.",
        },
        {
            "id": "DX-R09",
            "temat": "Czerwień DX5145 zamiast DX5146/DX5189",
            "tresc": "Jeśli zamieniasz DX5146 lub DX5189 na DX5145: zmniejsz stężenie o 5% i zwiększ DX5110 o 10%.",
        },
        {
            "id": "DX-R10",
            "temat": "Próbka koloru",
            "tresc": "Panel min. 10×15 cm, pistolet w pełni otwarty, 50% zakładka, suszenie max 40°C, ocena dopiero po bezbarwnym. Nie zmieniaj kształtu natrysku, nie odmuchuj, nie aplikuj zbyt mokro.",
        },
    ]


def autocolor_rules() -> list[dict]:
    return [
        {
            "id": "AC-R01",
            "temat": "Face / Flop / Tone",
            "tresc": "ŚWIATŁO (FACE) — kąt mocno zależny od metalików/pereł. FLOP (CIEŃ) — kąt zwykle ciemniejszy, zależny od tonerów konwencjonalnych. TONE (ODCIEŃ) — odcień względem sąsiedniej rodziny barw.",
        },
        {
            "id": "AC-R02",
            "temat": "Tonery RT (reduced tone) — próg 10%",
            "tresc": "Jeżeli udział tonera RT przekracza 10%, zastąp odpowiednikiem pełnej mocy: P420-908RT → P420-907; P420-960RT → P429-976; P420-910RT → P425-957; P420-902RT → P425-900; P420-904RT → P425-948.",
        },
        {
            "id": "AC-R03",
            "temat": "P429-980 Speed Red",
            "tresc": "Czysta czerwień do kolorów solid, głównie powyżej 20% udziału.",
        },
        {
            "id": "AC-R04",
            "temat": "P425-941 Strong Red",
            "tresc": "Czysta, wysokowydajna czerwień — głównie kolory solid.",
        },
        {
            "id": "AC-R05",
            "temat": "P425-922 Lagoon Blue",
            "tresc": "Zielonawy niebieski z zielonym flopem — do receptur metalik/perła.",
        },
        {
            "id": "AC-R06",
            "temat": "P426-HE02 / kontrola flopu",
            "tresc": "W PDF: Blue Frost — dodaje żółć na świetle (face) i jasny błękit na flopie w metalikach. W katalogu ODS ten sam kod ma inną nazwę — weryfikuj przed użyciem (status KOLIZJA jeśli wykryta).",
        },
    ]


def main() -> None:
    ac_txt = (OUT / "pdf_autocolor.txt").read_text(encoding="utf-8")
    dx_txt = (OUT / "pdf_duxone.txt").read_text(encoding="utf-8")
    pdf_ac = parse_autocolor_pdf(ac_txt)
    pdf_dx = parse_duxone_pdf(dx_txt)
    ac_ods = load_ods_autocolor()
    dx_ods = load_ods_duxone()
    ac = merge_autocolor(ac_ods, pdf_ac)
    dx = merge_duxone(dx_ods, pdf_dx)

    payload = {
        "zrodla": {
            "ods_autocolor": AC_ODS.name,
            "ods_duxone": DX_ODS.name,
            "pdf_autocolor": PDF_AC.name,
            "pdf_duxone": PDF_DX.name,
        },
        "statystyki": {
            "autocolor_ods": len(ac_ods),
            "autocolor_pdf_kody": len(pdf_ac),
            "autocolor_baza": len(ac),
            "autocolor_kolizje": sum(1 for r in ac if r["status_danych"] == "KOLIZJA NAZW"),
            "autocolor_z_pdf": sum(1 for r in ac if r["status_danych"] == "DODANY Z PDF"),
            "duxone_ods": len(dx_ods),
            "duxone_pdf_kody": len(pdf_dx),
            "duxone_baza": len(dx),
            "duxone_brak_nazwy": sum(1 for r in dx if r["status_danych"] == "DO WERYFIKACJI"),
        },
        "autocolor": ac,
        "duxone": dx,
        "reguly_autocolor": autocolor_rules(),
        "reguly_duxone": duxone_rules(),
        "pdf_autocolor_raw_keys": sorted(pdf_ac.keys()),
        "pdf_duxone_raw_keys": sorted(pdf_dx.keys()),
    }
    (OUT / "pigmenty.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    pd.DataFrame(ac + dx).to_csv(OUT / "pigmenty.csv", index=False, encoding="utf-8-sig")
    print(json.dumps(payload["statystyki"], ensure_ascii=False, indent=2))
    print("AUTOCOLOR PDF kody", sorted(pdf_ac.keys()))
    print("DUXONE PDF kody", sorted(pdf_dx.keys()))
    print("DUXONE bez nazwy", [r["nr_pigmentu"] for r in dx if not r["nazwa"]])
    print("AUTOCOLOR kolizje", [r["nr_pigmentu"] for r in ac if r["status_danych"] == "KOLIZJA NAZW"])


if __name__ == "__main__":
    main()
