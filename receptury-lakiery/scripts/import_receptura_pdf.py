# -*- coding: utf-8 -*-
"""Import składu receptury Autocolor / Duxone z PDF.

Czyta PDF (pymupdf), rozpoznaje kody pigmentów i ilości, zapisuje
data/import/ostatni.json + ostatni.txt (dla makra LibreOffice).
Nie modyfikuje baz pigmentów ani plików poza data/import/.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMPORT_DIR = ROOT / "data" / "import"
PIGMENTY_JSON = ROOT / "data" / "extracted" / "pigmenty.json"
LAST_DIR_FILE = IMPORT_DIR / "ostatni_folder.txt"
EXIT_CANCEL = 3

AC_PREFIX = r"P(?:192|420|425|426|429|433|434|435|440|450)"
AC_CODE_RE = re.compile(rf"\b({AC_PREFIX}-[A-Z0-9]+(?:RT)?|VM\d{{4}})\b", re.I)
DX_CODE_RE = re.compile(r"\b(DX\d{2,5}|AXT\d{3})\b", re.I)
ANY_CODE_RE = re.compile(
    rf"(?:{AC_CODE_RE.pattern})|(?:{DX_CODE_RE.pattern})",
    re.I,
)
QTY_TOKEN_RE = re.compile(
    r"^(\d{1,5}(?:[.,]\d{1,4})?)\s*(g|gr|gramy|gramow|gramów|gramu|grams?|gr\.)?$",
    re.I,
)
PCT_RE = re.compile(r"^(\d{1,3}(?:[.,]\d{1,2})?)\s*%$")
E_FACTOR_RE = re.compile(r"/E[\d.]+$", re.I)
DATE_RE = re.compile(
    r"\b(\d{1,2}[./-]\d{1,2}[./-]\d{2,4}|\d{4}-\d{2}-\d{2})\b"
)
INSTRUCT_RE = re.compile(
    r"(if more than|użyj|use\s+p\d{3}|zamiast|maks\.|max\.?\s+\d|powyżej\s+\d|"
    r"above\s+\d+\s*%|tinting guide|mixing bases|toner symbol)",
    re.I,
)

# Nagłówki kolumny ilości w recepturach (nie w tint chart).
QTY_HEADER_RE = re.compile(
    r"\b(weight|ilo[sś][cć]|grams?|gramy|gramów|qty|quantity|dozowanie|masa\s*\(|weight\s*\(\s*g)\b",
    re.I,
)
GRAM_IN_TEXT_RE = re.compile(
    r"(?<![A-Z0-9-])(\d{1,5}(?:[.,]\d{1,4})?)\s*(?:g|gr|gramy|grams?|gr\.)\b",
    re.I,
)


def _norm_code(raw: str) -> str:
    s = re.sub(r"\s+", "", str(raw).strip().upper())
    return E_FACTOR_RE.sub("", s)


def classify_system(code: str) -> str | None:
    """SYSTEM wyłącznie ze wzorca kodu — nie z samego numeru 123."""
    u = _norm_code(code)
    if DX_CODE_RE.fullmatch(u):
        return "DUXONE"
    if AC_CODE_RE.fullmatch(u):
        return "AUTOCOLOR"
    return None


def _is_code_tail_qty(code: str, qty: float, token: str = "") -> bool:
    """Odrzuć 942 z kodu P420-942 (tint chart / ten sam token)."""
    m = re.search(r"-([A-Z0-9]+)$", code.upper())
    if not m:
        return False
    tail = m.group(1)
    tok = re.sub(r"[^\dA-Z.,]", "", (token or "").upper())
    if tok and (tok == tail or tok.replace(",", ".") == tail):
        return True
    if re.fullmatch(r"\d+", tail):
        try:
            if abs(float(tail) - qty) < 1e-6:
                return True
        except ValueError:
            return False
    return False


def _to_float(num: str) -> float | None:
    t = num.strip().replace(" ", "").replace(",", ".")
    if t.count(".") > 1:
        return None
    try:
        val = float(t)
    except ValueError:
        return None
    if val <= 0 or val > 99999:
        return None
    if val >= 1900 and val <= 2100 and "." not in t:
        return None
    return val


def load_known_codes() -> dict[str, dict]:
    out: dict[str, dict] = {}
    if not PIGMENTY_JSON.exists():
        return out
    data = json.loads(PIGMENTY_JSON.read_text(encoding="utf-8"))
    for rec in data.get("autocolor", []) + data.get("duxone", []):
        sys = str(rec.get("system") or "").upper()
        nr = _norm_code(rec.get("nr_pigmentu") or "")
        if sys and nr:
            out[f"{sys}|{nr}"] = rec
    return out


def extract_pdf_text_and_words(pdf_path: Path) -> tuple[str, list[dict]]:
    import pymupdf as fitz

    doc = fitz.open(pdf_path)
    pages_text: list[str] = []
    words: list[dict] = []
    try:
        for pi, page in enumerate(doc):
            pages_text.append(f"===== PAGE {pi + 1} =====\n{page.get_text('text')}")
            for w in page.get_text("words"):
                x0, y0, x1, y1, token, *_ = w
                words.append(
                    {
                        "page": pi,
                        "x0": float(x0),
                        "y0": float(y0),
                        "x1": float(x1),
                        "y1": float(y1),
                        "t": str(token).strip(),
                    }
                )
    finally:
        doc.close()
    return "\n".join(pages_text), words


def _line_key(w: dict) -> tuple[int, int]:
    return (w["page"], int(round(w["y0"] / 3.0)))


def _qty_from_token(token: str, next_token: str = "") -> float | None:
    t = token.strip()
    if PCT_RE.match(t) or t.endswith("%"):
        return None
    combined = t
    unit_next = bool(re.match(r"^(g|gr|gr\.|gramy|gramow|gramów|grams?)$", next_token, re.I))
    if unit_next:
        combined = f"{t} g"
    m = QTY_TOKEN_RE.match(combined)
    if not m:
        m = QTY_TOKEN_RE.match(t)
        if not m:
            return None
    val = _to_float(m.group(1))
    if val is None:
        return None
    unit = (m.group(2) or "").lower()
    if unit or unit_next:
        return val
    return val


def pair_codes_with_qty(words: list[dict], allow_unitless: bool) -> list[dict]:
    """Paruj kod z ilością w tym samym wierszu, na prawo od kodu."""
    by_line: dict[tuple[int, int], list[dict]] = {}
    for w in words:
        if not w["t"]:
            continue
        by_line.setdefault(_line_key(w), []).append(w)

    hits: list[dict] = []
    for (_page, _y), line in by_line.items():
        line = sorted(line, key=lambda z: z["x0"])
        tokens = [z["t"] for z in line]
        joined = " ".join(tokens)
        if INSTRUCT_RE.search(joined) and not QTY_HEADER_RE.search(joined):
            if not re.search(r"\d+[.,]?\d*\s*g\b", joined, re.I):
                continue
        i = 0
        while i < len(line):
            tok = line[i]["t"]
            nxt = line[i + 1]["t"] if i + 1 < len(line) else ""
            glued = tok + nxt if nxt.startswith("-") or tok.endswith("-") else tok
            m = ANY_CODE_RE.search(glued) or ANY_CODE_RE.search(tok)
            code = None
            if m:
                code = _norm_code(m.group(0))
            elif tok.endswith("-") and nxt and ANY_CODE_RE.search(tok + nxt):
                code = _norm_code(tok + nxt)
                i += 1
            if not code or not classify_system(code):
                i += 1
                continue
            qty = None
            qty_unit = False
            j = i + 1
            while j < len(line):
                cand = line[j]["t"]
                nxtt = line[j + 1]["t"] if j + 1 < len(line) else ""
                if ANY_CODE_RE.search(cand):
                    break
                if PCT_RE.match(cand) or cand.endswith("%"):
                    j += 1
                    continue
                q = _qty_from_token(cand, nxtt)
                if q is not None:
                    if _is_code_tail_qty(code, q, cand):
                        j += 1
                        continue
                    has_unit = bool(
                        (QTY_TOKEN_RE.match(cand) and QTY_TOKEN_RE.match(cand).group(2))
                        or re.match(r"^(g|gr|gr\.|grams?|gramy)$", nxtt, re.I)
                    )
                    if has_unit:
                        qty = q
                        qty_unit = True
                        break
                    if allow_unitless or ("." in cand or "," in cand):
                        qty = q
                j += 1
            if qty is not None and (qty_unit or allow_unitless) and not _is_code_tail_qty(code, qty):
                hits.append({"nr": code, "ilosc": qty, "linia": joined[:200], "z_jednostka": qty_unit})
            i += 1
    return hits


def pair_from_plain_text(text: str, allow_unitless: bool) -> list[dict]:
    """Fallback: linia zawiera kod i liczbę (g)."""
    hits: list[dict] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if INSTRUCT_RE.search(line) and not re.search(r"\d+[.,]?\d*\s*g\b", line, re.I):
            continue
        codes = [_norm_code(m.group(0)) for m in ANY_CODE_RE.finditer(line)]
        codes = [c for c in codes if classify_system(c)]
        if not codes:
            continue
        qty_hits: list[tuple[float, bool]] = []
        for m in re.finditer(
            r"(?<![A-Z0-9/-])(\d{1,5}(?:[.,]\d{1,4})?)\s*(g|gr|gramy|grams?|gr\.)?\b",
            line,
            re.I,
        ):
            after = line[m.end() : m.end() + 1]
            if after == "%":
                continue
            if m.group(0).endswith("%"):
                continue
            val = _to_float(m.group(1))
            if val is None:
                continue
            if any(_is_code_tail_qty(c, val, m.group(1)) for c in codes):
                continue
            unit = m.group(2)
            if unit:
                qty_hits.append((val, True))
            elif allow_unitless:
                qty_hits.append((val, False))
        if not qty_hits:
            continue
        vals = [q for q, _u in qty_hits]
        if len(codes) == 1:
            hits.append({"nr": codes[0], "ilosc": vals[-1], "linia": line[:200], "z_jednostka": qty_hits[-1][1]})
        elif len(codes) == len(vals):
            for c, (q, u) in zip(codes, qty_hits):
                hits.append({"nr": c, "ilosc": q, "linia": line[:200], "z_jednostka": u})
        else:
            hits.append({"nr": codes[0], "ilosc": vals[-1], "linia": line[:200], "z_jednostka": qty_hits[-1][1]})
    return hits


def extract_meta(text: str) -> dict:
    meta = {
        "kod_koloru": "",
        "nazwa_koloru": "",
        "data": "",
        "system": "",
        "nazwa_receptury": "",
    }

    def grab(patterns: list[str]) -> str:
        for pat in patterns:
            m = re.search(pat, text, re.I | re.M)
            if m:
                val = m.group(1).strip(" \t.:;-")
                val = re.sub(r"\s+", " ", val)
                if 1 <= len(val) <= 80:
                    return val
        return ""

    meta["kod_koloru"] = grab(
        [
            r"(?:colour\s*code|color\s*code|kod\s*koloru|kod\s*receptury|formula(?:\s*code)?)\s*[:#]?\s*([A-Z0-9][\w\-./]*)",
            r"(?:receptura\s*nr|formula\s*no\.?)\s*[:#]?\s*([A-Z0-9][\w\-./]*)",
        ]
    )
    meta["nazwa_koloru"] = grab(
        [
            r"(?:colour\s*name|color\s*name|nazwa\s*koloru)\s*[:#]?\s*([^\n]{2,60})",
        ]
    )
    dm = DATE_RE.search(
        grab([r"(?:date|data)\s*[:#]?\s*([^\n]{6,20})"]) or text[:2000]
    )
    if dm:
        meta["data"] = dm.group(1)
    sys_hit = re.search(
        r"\b(AUTOCOLOR|DUXONE|NEXA\s*AUTOCOLOR|2K\s*HS)\b", text, re.I
    )
    if sys_hit:
        raw = sys_hit.group(1).upper()
        if "DUXONE" in raw:
            meta["system"] = "DUXONE"
        elif "AUTOCOLOR" in raw or "NEXA" in raw:
            meta["system"] = "AUTOCOLOR"
    title = grab([r"(?:receptura|formula|mixing\s*scheme)\s*[:#]?\s*([^\n]{3,60})"])
    if title:
        meta["nazwa_receptury"] = title
    return meta


def _dedupe_hits(hits: list[dict]) -> list[dict]:
    """Zachowaj kolejność; zsumuj powtórzenia tego samego kodu+systemu."""
    acc: dict[str, dict] = {}
    order: list[str] = []
    for h in hits:
        nr = h["nr"]
        sys = classify_system(nr) or ""
        key = f"{sys}|{nr}"
        if key not in acc:
            acc[key] = {"nr": nr, "ilosc": 0.0, "linia": h.get("linia", "")}
            order.append(key)
        acc[key]["ilosc"] += float(h["ilosc"])
    return [acc[k] for k in order]


def build_pozycje(hits: list[dict], known: dict[str, dict]) -> list[dict]:
    pozycje = []
    for h in _dedupe_hits(hits):
        nr = h["nr"]
        sys = classify_system(nr)
        if not sys:
            continue
        rec = known.get(f"{sys}|{nr}")
        znany = rec is not None
        uwagi = "" if znany else "DO WERYFIKACJI"
        pozycje.append(
            {
                "system": sys,
                "nr": nr,
                "ilosc": round(float(h["ilosc"]), 3),
                "jednostka": "g",
                "znany": znany,
                "nazwa": (rec.get("nazwa") or "") if rec else "",
                "uwagi": uwagi,
            }
        )
    return pozycje


def infer_base_system(pozycje: list[dict], meta_system: str) -> str:
    n_ac = sum(1 for p in pozycje if p["system"] == "AUTOCOLOR")
    n_dx = sum(1 for p in pozycje if p["system"] == "DUXONE")
    if n_ac and n_dx:
        return "AUTOCOLOR" if n_ac >= n_dx else "DUXONE"
    if n_dx:
        return "DUXONE"
    if n_ac:
        return "AUTOCOLOR"
    if meta_system in ("AUTOCOLOR", "DUXONE"):
        return meta_system
    return "AUTOCOLOR"


def parse_receptura_pdf(pdf_path: Path, known: dict[str, dict] | None = None) -> dict:
    pdf_path = Path(pdf_path)
    result = {
        "ok": False,
        "error": "",
        "komunikat": "",
        "pdf": str(pdf_path),
        "meta": {},
        "pozycje": [],
        "ostrzezenia": [],
    }
    if not pdf_path.exists():
        result["error"] = "Brak pliku PDF"
        result["komunikat"] = f"Nie znaleziono pliku: {pdf_path}"
        return result
    try:
        text, words = extract_pdf_text_and_words(pdf_path)
    except ImportError:
        result["error"] = "pymupdf"
        result["komunikat"] = "Brak biblioteki pymupdf. Zainstaluj: pip install pymupdf"
        return result
    except Exception as exc:
        result["error"] = "pdf"
        result["komunikat"] = f"Nie udało się odczytać PDF: {exc}"
        return result

    if known is None:
        known = load_known_codes()
    allow_unitless = bool(QTY_HEADER_RE.search(text))
    hits = pair_codes_with_qty(words, allow_unitless)
    if not hits:
        hits = pair_from_plain_text(text, allow_unitless)
    hits = [h for h in hits if not _is_code_tail_qty(h["nr"], h["ilosc"])]
    has_grams = bool(GRAM_IN_TEXT_RE.search(text))
    if hits and not has_grams:
        decimal_or_unit = any(
            h.get("z_jednostka") or abs(float(h["ilosc"]) - int(h["ilosc"])) > 1e-9
            for h in hits
        )
        if not (allow_unitless and decimal_or_unit):
            hits = []
    pozycje = build_pozycje(hits, known)
    meta = extract_meta(text)
    result["meta"] = meta

    codes_found = { _norm_code(m.group(0)) for m in ANY_CODE_RE.finditer(text) }
    codes_found = {c for c in codes_found if classify_system(c)}

    if not pozycje:
        result["komunikat"] = "nie znaleziono receptury"
        result["ostrzezenia"].append(
            "Wykryto kody pigmentów bez ilości"
            if codes_found
            else "Brak kodów Autocolor/Duxone i ilości"
        )
        result["ostrzezenia"].append(f"kody_bez_ilosci={len(codes_found)}")
        return result

    unknown = [p for p in pozycje if not p["znany"]]
    mixed = len({p["system"] for p in pozycje}) > 1
    base = infer_base_system(pozycje, meta.get("system") or "")
    meta["system_bazowy"] = base
    meta["mieszany"] = mixed
    if mixed:
        result["ostrzezenia"].append(
            "Receptura miesza AUTOCOLOR i DUXONE — SYSTEM pigmentu ze wzorca kodu."
        )
    if unknown:
        result["ostrzezenia"].append(
            f"{len(unknown)} kod(ów) poza bazą — wstawiono z SYSTEM, uwagi DO WERYFIKACJI."
        )
    if not meta.get("nazwa_receptury"):
        meta["nazwa_receptury"] = f"Import PDF: {pdf_path.stem}"
    result["meta"] = meta
    result["pozycje"] = pozycje
    result["ok"] = True
    result["komunikat"] = (
        f"Zaimportowano {len(pozycje)} pozycji"
        + (f" ({len(unknown)} do weryfikacji)" if unknown else "")
    )
    return result


def write_outputs(result: dict, out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "ostatni.json"
    txt_path = out_dir / "ostatni.txt"
    json_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    lines = [
        f"OK={'1' if result.get('ok') else '0'}",
        f"KOMUNIKAT={result.get('komunikat') or ''}",
        f"ERROR={result.get('error') or ''}",
        f"PDF={result.get('pdf') or ''}",
    ]
    meta = result.get("meta") or {}
    lines += [
        f"KOD_KOLORU={meta.get('kod_koloru') or ''}",
        f"NAZWA_KOLORU={meta.get('nazwa_koloru') or ''}",
        f"DATA={meta.get('data') or ''}",
        f"SYSTEM={meta.get('system_bazowy') or meta.get('system') or ''}",
        f"NAZWA_RECEPTURY={meta.get('nazwa_receptury') or ''}",
        f"MIESZANY={'1' if meta.get('mieszany') else '0'}",
        f"UWAGI={'; '.join(result.get('ostrzezenia') or [])}",
        f"LICZBA={len(result.get('pozycje') or [])}",
    ]
    for i, p in enumerate(result.get("pozycje") or [], 1):
        uwagi = p.get("uwagi") or ""
        lines.append(
            f"P{i}={p['system']}|{p['nr']}|{p['ilosc']:.3f}|{uwagi}"
        )
    txt_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, txt_path


def default_start_dir(hint: str | None = None) -> str:
    """Folder startowy dialogu: hint / ostatni / E:\\ / Dokumenty — nigdy pusty."""
    candidates: list[Path] = []
    if hint:
        raw = Path(str(hint).strip().strip('"'))
        if raw.is_dir():
            candidates.append(raw)
        elif raw.parent.is_dir():
            candidates.append(raw.parent)
    if LAST_DIR_FILE.exists():
        try:
            saved = Path(LAST_DIR_FILE.read_text(encoding="utf-8").strip().strip('"'))
            if saved:
                candidates.append(saved)
        except OSError:
            pass
    candidates.extend(
        [
            Path("E:/"),
            Path.home() / "Documents",
            Path.home() / "Dokumenty",
            IMPORT_DIR,
            Path.home(),
        ]
    )
    for cand in candidates:
        try:
            if cand.exists() and cand.is_dir():
                return str(cand)
        except OSError:
            continue
    return str(Path.home())


def _save_last_dir(folder: Path) -> None:
    try:
        LAST_DIR_FILE.parent.mkdir(parents=True, exist_ok=True)
        LAST_DIR_FILE.write_text(str(folder), encoding="utf-8")
    except OSError:
        pass


def _guid(ole32, text: str):
    import ctypes
    from ctypes import POINTER, byref

    class GUID(ctypes.Structure):
        _fields_ = [
            ("Data1", ctypes.c_uint32),
            ("Data2", ctypes.c_uint16),
            ("Data3", ctypes.c_uint16),
            ("Data4", ctypes.c_ubyte * 8),
        ]

    g = GUID()
    ole32.CLSIDFromString(text, byref(g))
    return g


def _choose_pdf_ifiledialog(initial_dir: str) -> str | None:
    """Natywne okno Windows (IFileOpenDialog = Eksplorator). None = anulowano."""
    import ctypes
    from ctypes import POINTER, byref, c_void_p, c_wchar_p
    from ctypes.wintypes import DWORD, HWND, LPCWSTR, LPWSTR, UINT

    class COMDLG_FILTERSPEC(ctypes.Structure):
        _fields_ = [("pszName", LPCWSTR), ("pszSpec", LPCWSTR)]

    ole32 = ctypes.WinDLL("ole32")
    shell32 = ctypes.WinDLL("shell32")
    user32 = ctypes.WinDLL("user32")
    ole32.CoInitialize(None)

    clsid = _guid(ole32, "{DC1C5A9C-E88A-4DDE-A5A1-60F82A20AEF7}")
    iid = _guid(ole32, "{D57C7288-D4AD-4768-BE02-9D969532D960}")
    iid_item = _guid(ole32, "{43826D1E-E718-42EE-BC55-A1E261C37BFE}")
    dialog = c_void_p()
    ole32.CoCreateInstance.restype = ctypes.c_long
    hr = ole32.CoCreateInstance(byref(clsid), None, 1, byref(iid), byref(dialog))
    if hr != 0 or not dialog:
        raise OSError(f"CoCreateInstance IFileOpenDialog hr={hr}")

    def vtbl(obj):
        return ctypes.cast(obj, POINTER(POINTER(c_void_p)))[0]

    def call(obj, index, restype, *argtypes):
        proto = ctypes.WINFUNCTYPE(restype, c_void_p, *argtypes)
        return proto(vtbl(obj)[index])

    try:
        get_opts = call(dialog, 10, ctypes.c_long, POINTER(DWORD))
        set_opts = call(dialog, 9, ctypes.c_long, DWORD)
        opts = DWORD()
        get_opts(dialog, byref(opts))
        fos = 0x8 | 0x40 | 0x800 | 0x1000  # NOCHANGEDIR | FORCEFILESYSTEM | PATHMUSTEXIST | FILEMUSTEXIST
        set_opts(dialog, opts.value | fos)

        filters = (COMDLG_FILTERSPEC * 2)()
        filters[0].pszName = "PDF (*.pdf)"
        filters[0].pszSpec = "*.pdf"
        filters[1].pszName = "Wszystkie pliki (*.*)"
        filters[1].pszSpec = "*.*"
        call(dialog, 4, ctypes.c_long, UINT, POINTER(COMDLG_FILTERSPEC))(dialog, 2, filters)
        call(dialog, 5, ctypes.c_long, UINT)(dialog, 1)
        call(dialog, 17, ctypes.c_long, LPCWSTR)(
            dialog, "Wskaż PDF receptury Autocolor / Duxone"
        )
        call(dialog, 22, ctypes.c_long, LPCWSTR)(dialog, "pdf")

        folder_item = c_void_p()
        shell32.SHCreateItemFromParsingName.restype = ctypes.c_long
        shell32.SHCreateItemFromParsingName.argtypes = [
            c_wchar_p,
            c_void_p,
            c_void_p,
            POINTER(c_void_p),
        ]
        if (
            shell32.SHCreateItemFromParsingName(
                initial_dir, None, byref(iid_item), byref(folder_item)
            )
            == 0
            and folder_item
        ):
            call(dialog, 12, ctypes.c_long, c_void_p)(dialog, folder_item)

        hwnd = user32.GetForegroundWindow()
        hr_show = call(dialog, 3, ctypes.c_long, HWND)(dialog, hwnd)
        if (hr_show & 0xFFFFFFFF) == 0x800704C7:
            return None
        if hr_show != 0:
            raise OSError(f"IFileOpenDialog.Show hr={hr_show}")

        result_item = c_void_p()
        hr_res = call(dialog, 20, ctypes.c_long, POINTER(c_void_p))(
            dialog, byref(result_item)
        )
        if hr_res != 0 or not result_item:
            return None
        ppsz = LPWSTR()
        hr_name = call(result_item, 5, ctypes.c_long, ctypes.c_ulong, POINTER(LPWSTR))(
            result_item, 0x80058000, byref(ppsz)
        )
        if hr_name != 0 or not ppsz:
            return None
        path = ppsz.value
        ole32.CoTaskMemFree(ppsz)
        return path
    finally:
        try:
            call(dialog, 2, ctypes.c_ulong)(dialog)
        except Exception:
            pass


def _choose_pdf_getopenfilename(initial_dir: str) -> str | None:
    """GetOpenFileNameW (OFN_EXPLORER). None = anulowano."""
    import ctypes
    from ctypes import wintypes

    class OPENFILENAMEW(ctypes.Structure):
        _fields_ = [
            ("lStructSize", wintypes.DWORD),
            ("hwndOwner", wintypes.HWND),
            ("hInstance", wintypes.HINSTANCE),
            ("lpstrFilter", wintypes.LPCWSTR),
            ("lpstrCustomFilter", wintypes.LPWSTR),
            ("nMaxCustFilter", wintypes.DWORD),
            ("nFilterIndex", wintypes.DWORD),
            ("lpstrFile", wintypes.LPWSTR),
            ("nMaxFile", wintypes.DWORD),
            ("lpstrFileTitle", wintypes.LPWSTR),
            ("nMaxFileTitle", wintypes.DWORD),
            ("lpstrInitialDir", wintypes.LPCWSTR),
            ("lpstrTitle", wintypes.LPCWSTR),
            ("Flags", wintypes.DWORD),
            ("nFileOffset", wintypes.WORD),
            ("nFileExtension", wintypes.WORD),
            ("lpstrDefExt", wintypes.LPCWSTR),
            ("lCustData", wintypes.LPARAM),
            ("lpfnHook", ctypes.c_void_p),
            ("lpTemplateName", wintypes.LPCWSTR),
            ("pvReserved", ctypes.c_void_p),
            ("dwReserved", wintypes.DWORD),
            ("FlagsEx", wintypes.DWORD),
        ]

    buf = ctypes.create_unicode_buffer(32768)
    ofn = OPENFILENAMEW()
    ofn.lStructSize = ctypes.sizeof(OPENFILENAMEW)
    ofn.lpstrFilter = "PDF (*.pdf)\0*.pdf\0Wszystkie pliki (*.*)\0*.*\0\0"
    ofn.nFilterIndex = 1
    ofn.lpstrFile = ctypes.cast(buf, wintypes.LPWSTR)
    ofn.nMaxFile = 32768
    ofn.lpstrInitialDir = initial_dir
    ofn.lpstrTitle = "Wskaż PDF receptury Autocolor / Duxone"
    ofn.Flags = 0x00080000 | 0x00001000 | 0x00000800 | 0x00000004 | 0x00000008
    ofn.lpstrDefExt = "pdf"
    comdlg32 = ctypes.WinDLL("comdlg32")
    if comdlg32.GetOpenFileNameW(ctypes.byref(ofn)):
        return buf.value or None
    return None


def _choose_pdf_tk(initial_dir: str) -> str | None:
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    try:
        root.attributes("-topmost", True)
    except tk.TclError:
        pass
    path = filedialog.askopenfilename(
        parent=root,
        title="Wskaż PDF receptury Autocolor / Duxone",
        filetypes=[("PDF (*.pdf)", "*.pdf"), ("Wszystkie pliki (*.*)", "*.*")],
        initialdir=initial_dir,
        defaultextension=".pdf",
    )
    root.destroy()
    return path or None


def _choose_pdf_powershell(initial_dir: str) -> str | None:
    initial = json.dumps(initial_dir)
    title = json.dumps("Wskaż PDF receptury Autocolor / Duxone")
    ps = (
        "Add-Type -AssemblyName System.Windows.Forms | Out-Null; "
        "[System.Windows.Forms.Application]::EnableVisualStyles(); "
        "$d = New-Object System.Windows.Forms.OpenFileDialog; "
        "$d.Filter = 'PDF (*.pdf)|*.pdf|Wszystkie pliki (*.*)|*.*'; "
        f"$d.Title = {title}; "
        f"$d.InitialDirectory = {initial}; "
        "$d.Multiselect = $false; $d.CheckFileExists = $true; $d.RestoreDirectory = $true; "
        "if ($d.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) { "
        "[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false); "
        "[Console]::Out.Write($d.FileName) }"
    )
    proc = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-STA",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            ps,
        ],
        capture_output=True,
        timeout=600,
    )
    if proc.returncode not in (0, None) and not proc.stdout:
        err = (proc.stderr or b"").decode("utf-8", "replace")[:300]
        raise RuntimeError(err or f"powershell {proc.returncode}")
    out = (proc.stdout or b"").decode("utf-8", "replace").strip()
    return out or None


def choose_pdf_path(initial_dir: str | None = None) -> Path | None:
    """Otwórz natywne okno Windows i zwróć PDF albo None (anulowano)."""
    start = default_start_dir(initial_dir)
    pickers = (
        [_choose_pdf_ifiledialog, _choose_pdf_getopenfilename, _choose_pdf_tk, _choose_pdf_powershell]
        if sys.platform == "win32"
        else [_choose_pdf_tk]
    )
    last_exc: Exception | None = None
    for picker in pickers:
        try:
            selected = picker(start)
        except Exception as exc:
            last_exc = exc
            continue
        if not selected:
            return None
        path = Path(selected)
        if path.is_file():
            _save_last_dir(path.parent)
            return path
        return None
    raise RuntimeError(f"Nie udało się otworzyć okna wyboru pliku Windows: {last_exc}")


def make_test_pdf(dest: Path) -> Path:
    import pymupdf as fitz

    dest.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)
    body = (
        "NEXA AUTOCOLOR / DUXONE\n"
        "Formula / receptura\n"
        "Colour code: TST-MIX-01\n"
        "Colour name: Test Silver Mix\n"
        "Date: 09.09.2026\n"
        "System: AUTOCOLOR + DUXONE\n"
        "\n"
        "Mixing scheme\n"
        "Toner              Weight (g)\n"
        "P425-900           50.000 g\n"
        "P425-984           30.000 g\n"
        "DX5110             12.500 g\n"
        "P425-ZZ99           7.500 g\n"
    )
    page.insert_text((72, 72), body, fontsize=12, fontname="helv")
    doc.save(dest)
    doc.close()
    return dest


def make_noqty_pdf(dest: Path) -> Path:
    """PDF z kodami bez ilości — parser ma zwrócić 'nie znaleziono receptury'."""
    import pymupdf as fitz

    dest.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)
    body = (
        "TINTING GUIDE\n"
        "MIXING BASES\n"
        "P425-900 HS Super White\n"
        "P420-907 Red Oxide\n"
        "If more than 10% use P420-907.\n"
        "DX5110 Deep Black\n"
    )
    page.insert_text((72, 72), body, fontsize=12, fontname="helv")
    doc.save(dest)
    doc.close()
    return dest


def run_self_test() -> int:
    known = load_known_codes()
    IMPORT_DIR.mkdir(parents=True, exist_ok=True)
    good = make_test_pdf(IMPORT_DIR / "przyklad_receptura_test.pdf")
    bad = make_noqty_pdf(IMPORT_DIR / "przyklad_brak_receptury.pdf")
    r1 = parse_receptura_pdf(good, known)
    r2 = parse_receptura_pdf(bad, known)
    write_outputs(r1, IMPORT_DIR)
    ok = True
    msgs = []
    if not r1.get("ok") or len(r1.get("pozycje") or []) != 4:
        ok = False
        msgs.append(f"test PDF oczekiwano 4 pozycji, jest {r1}")
    nrs = [p["nr"] for p in r1.get("pozycje") or []]
    syss = [p["system"] for p in r1.get("pozycje") or []]
    if nrs != ["P425-900", "P425-984", "DX5110", "P425-ZZ99"]:
        ok = False
        msgs.append(f"kody {nrs}")
    if syss != ["AUTOCOLOR", "AUTOCOLOR", "DUXONE", "AUTOCOLOR"]:
        ok = False
        msgs.append(f"systemy {syss}")
    zz = next(p for p in r1["pozycje"] if p["nr"] == "P425-ZZ99")
    if zz["znany"] or zz["uwagi"] != "DO WERYFIKACJI":
        ok = False
        msgs.append(f"nieznany {zz}")
    if r1["pozycje"][2]["system"] != "DUXONE":
        ok = False
        msgs.append("DX5110 musi być DUXONE ze wzorca, nie z numeru")
    if r2.get("ok") or "nie znaleziono receptury" not in (r2.get("komunikat") or ""):
        ok = False
        msgs.append(f"PDF bez ilości: {r2.get('komunikat')}")
    tint = ROOT / "data" / "backup" / "nexa-autocolor-2k-tint-chart-guide.pdf"
    if tint.exists():
        r3 = parse_receptura_pdf(tint, known)
        if r3.get("ok"):
            ok = False
            msgs.append(f"tint chart nie jest recepturą, parser zwrócił {len(r3.get('pozycje') or [])} pozycji")
        elif "nie znaleziono receptury" not in (r3.get("komunikat") or ""):
            ok = False
            msgs.append(f"tint chart komunikat: {r3.get('komunikat')}")
    print("SELFTEST", "OK" if ok else "FAIL", "; ".join(msgs) or r1.get("komunikat"))
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Import receptury lakieru z PDF")
    parser.add_argument("pdf", nargs="?", help="Ścieżka PDF receptury")
    parser.add_argument("--out-dir", default=str(IMPORT_DIR), help="Folder JSON/TXT")
    parser.add_argument("--make-test-pdf", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument(
        "--wybierz",
        action="store_true",
        help="Natywne okno Windows (jak Eksplorator), potem parsuj PDF",
    )
    parser.add_argument("--start-dir", default="", help="Folder startowy dialogu")
    args = parser.parse_args(argv)
    if args.self_test:
        return run_self_test()
    out_dir = Path(args.out_dir)
    if args.wybierz:
        picked = choose_pdf_path(args.start_dir or None)
        if picked is None:
            print("ANULOWANO")
            return EXIT_CANCEL
        args.pdf = str(picked)
        print(args.pdf)
    if args.make_test_pdf:
        p = make_test_pdf(out_dir / "przyklad_receptura_test.pdf")
        print(p)
        if not args.pdf:
            args.pdf = str(p)
    if not args.pdf:
        parser.error("Podaj plik PDF, --wybierz albo --self-test / --make-test-pdf")
    result = parse_receptura_pdf(Path(args.pdf))
    json_path, txt_path = write_outputs(result, out_dir)
    print(result.get("komunikat") or result.get("error") or "")
    print(json_path)
    print(txt_path)
    if result.get("ok"):
        return 0
    if (result.get("komunikat") or "").lower().startswith("nie znaleziono"):
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
