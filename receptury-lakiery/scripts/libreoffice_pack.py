# -*- coding: utf-8 -*-
"""Konwersja przez LibreOffice + wstrzyknięcie makr StarBasic do ODS."""
from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
SOFFICE = Path(r"C:\Program Files\LibreOffice\program\soffice.exe")
XLSX = ROOT / "RECEPTURY_LAKIERY.xlsx"
ODS = ROOT / "RECEPTURY_LAKIERY.ods"
ODS_UNLOCKED = ROOT / "RECEPTURY_LAKIERY_edycja.ods"
ODS_NOWY = ROOT / "RECEPTURY_LAKIERY_nowy.ods"
BAS = ROOT / "macros" / "modReceptury.bas"
LOCK_MAIN = ROOT / ".~lock.RECEPTURY_LAKIERY.ods#"
LOCK_EDYCJA = ROOT / ".~lock.RECEPTURY_LAKIERY_edycja.ods#"

NS = {"manifest": "urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"}


def convert(src: Path, dest_ext: str, outdir: Path) -> Path:
    outdir.mkdir(parents=True, exist_ok=True)
    profile = ROOT / "data" / "extracted" / "lo_profile_headless"
    profile.mkdir(parents=True, exist_ok=True)
    uri = profile.resolve().as_uri()
    cmd = [
        str(SOFFICE),
        "--headless",
        "--norestore",
        "--nolockcheck",
        f"-env:UserInstallation={uri}",
        "--convert-to",
        dest_ext,
        "--outdir",
        str(outdir),
        str(src),
    ]
    subprocess.run(cmd, check=False, timeout=180)
    produced = outdir / (src.stem + "." + dest_ext.split(":")[0])
    if not produced.exists():
        candidates = list(outdir.glob(src.stem + ".*"))
        if not candidates:
            raise FileNotFoundError(f"Brak pliku po konwersji w {outdir}: {cmd}")
        produced = candidates[0]
    return produced


def _rewrite_zip(src_dir: Path, ods_path: Path) -> None:
    tmp_zip = ods_path.with_suffix(".ods.tmpzip")
    with zipfile.ZipFile(tmp_zip, "w", zipfile.ZIP_DEFLATED) as zout:
        for f in src_dir.rglob("*"):
            if f.is_file():
                zout.write(f, f.relative_to(src_dir).as_posix())
    shutil.move(tmp_zip, ods_path)


def unprotect_content_xml(text: str) -> str:
    """Zdejmij ochronę arkuszy w ODS — edycja i zapis bez hasła."""
    text = text.replace('table:protected="true"', 'table:protected="false"')
    text = re.sub(r'\s+table:protection-key="[^"]*"', "", text)
    text = re.sub(r'\s+table:protection-key-digest-algorithm="[^"]*"', "", text)
    text = re.sub(r'\s+loext:protection-key-digest-algorithm-2="[^"]*"', "", text)
    text = text.replace('table:structure-protected="true"', 'table:structure-protected="false"')
    return text


EVENT_LISTENERS = (
    "<office:scripts>"
    "<office:event-listeners>"
    '<script:event-listener script:language="ooo:Basic" '
    'script:event-name="office:ViewCreated" '
    'script:macro-name="Standard.modReceptury.PrzyOtwarciu" '
    'xlink:href="vnd.sun.star.script:Standard.modReceptury.PrzyOtwarciu?language=Basic&amp;location=document" '
    'xlink:type="simple"/>'
    '<script:event-listener script:language="ooo:Basic" '
    'script:event-name="office:Load" '
    'script:macro-name="Standard.modReceptury.PrzyOtwarciu" '
    'xlink:href="vnd.sun.star.script:Standard.modReceptury.PrzyOtwarciu?language=Basic&amp;location=document" '
    'xlink:type="simple"/>'
    "</office:event-listeners>"
    "</office:scripts>"
)


SHEET_EVENTS = (
    "<office:event-listeners>"
    '<script:event-listener script:language="ooo:Basic" '
    'script:event-name="on-select" '
    'script:macro-name="Standard.modReceptury.OnWyborKomorki" '
    'xlink:href="vnd.sun.star.script:Standard.modReceptury.OnWyborKomorki?language=Basic&amp;location=document" '
    'xlink:type="simple"/>'
    '<script:event-listener script:language="ooo:Basic" '
    'script:event-name="on-change" '
    'script:macro-name="Standard.modReceptury.OnZmianaKomorki" '
    'xlink:href="vnd.sun.star.script:Standard.modReceptury.OnZmianaKomorki?language=Basic&amp;location=document" '
    'xlink:type="simple"/>'
    "</office:event-listeners>"
)


def inject_document_events(text: str) -> str:
    """Podłącz PrzyOtwarciu — listener SelectionChanged / klik NR PIGMENTU."""
    if "<office:scripts/>" in text:
        return text.replace("<office:scripts/>", EVENT_LISTENERS, 1)
    if "<office:scripts></office:scripts>" in text:
        return text.replace("<office:scripts></office:scripts>", EVENT_LISTENERS, 1)
    if "modReceptury.PrzyOtwarciu" in text:
        return text
    return text.replace("<office:scripts>", EVENT_LISTENERS.replace("</office:scripts>", ""), 1)


def inject_sheet_events(text: str) -> str:
    """Zdarzenia arkusza on-select / on-change — lista NR po kliknięciu."""
    if "OnWyborKomorki" in text and "table:name=\"RECEPTURA_ORYGINALNA\"" in text:
        if "on-select" in text:
            return text
    for name in ("RECEPTURA_ORYGINALNA", "RECEPTURA_WLASNA", "DOBARWIANIE"):
        text = re.sub(
            rf'(<table:table table:name="{name}"[^>]*>)',
            rf"\1{SHEET_EVENTS}",
            text,
            count=1,
        )
    return text


def inject_macros(ods_path: Path) -> None:
    code = BAS.read_text(encoding="utf-8")
    # StarBasic w XML: escape & < >
    xml_code = escape(code)
    lib_xml = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE library:library PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "library.dtd">
<library:library xmlns:library="http://openoffice.org/2000/library" library:name="Standard" library:readonly="false" library:passwordprotected="false">
 <library:element library:name="modReceptury"/>
</library:library>
"""
    mod_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!DOCTYPE script:module PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "module.dtd">\n'
        '<script:module xmlns:script="http://openoffice.org/2000/script" '
        'script:name="modReceptury" script:language="StarBasic">\n'
        f"{xml_code}\n"
        "</script:module>\n"
    )
    tmp = Path(tempfile.mkdtemp(prefix="ods_macro_"))
    try:
        with zipfile.ZipFile(ods_path, "r") as zin:
            zin.extractall(tmp)
        content = tmp / "content.xml"
        if content.exists():
            xml = unprotect_content_xml(content.read_text(encoding="utf-8"))
            xml = inject_document_events(xml)
            xml = inject_sheet_events(xml)
            content.write_text(xml, encoding="utf-8")
        basic = tmp / "Basic" / "Standard"
        basic.mkdir(parents=True, exist_ok=True)
        (basic / "script-lb.xml").write_text(lib_xml, encoding="utf-8")
        (basic / "modReceptury.xml").write_text(mod_xml, encoding="utf-8")
        manifest = tmp / "META-INF" / "manifest.xml"
        ET.register_namespace("manifest", NS["manifest"])
        tree = ET.parse(manifest)
        root = tree.getroot()
        existing = {el.get(f"{{{NS['manifest']}}}full-path") for el in root}
        entries = [
            ("Basic/", "application/binary"),
            ("Basic/Standard/", "application/binary"),
            ("Basic/Standard/script-lb.xml", "text/xml"),
            ("Basic/Standard/modReceptury.xml", "text/plain"),
        ]
        for path, mt in entries:
            if path in existing:
                continue
            el = ET.SubElement(root, f"{{{NS['manifest']}}}file-entry")
            el.set(f"{{{NS['manifest']}}}full-path", path)
            el.set(f"{{{NS['manifest']}}}media-type", mt)
        tree.write(manifest, encoding="UTF-8", xml_declaration=True)
        _rewrite_zip(tmp, ods_path)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _lock_active(lock_path: Path) -> bool:
    return lock_path.exists()


def _try_copy(src: Path, dest: Path) -> bool:
    try:
        shutil.copy2(src, dest)
        print("Zapisano", dest, "size", dest.stat().st_size)
        return True
    except OSError as exc:
        print("Nie zapisano", dest, "—", exc)
        return False


def publish_ods(built: Path) -> Path:
    """Zapisz ODS; przy locku LibreOffice — nowy odblokowany plik i otwórz go."""
    _try_copy(built, ODS)
    _try_copy(built, ODS_UNLOCKED)
    _try_copy(built, ODS_NOWY)
    locked = _lock_active(LOCK_MAIN) or _lock_active(LOCK_EDYCJA)
    fresh = ROOT / "RECEPTURY_LAKIERY_dropdown.ods"
    if locked or not ODS_UNLOCKED.exists():
        if _try_copy(built, fresh):
            print("Lock LibreOffice aktywny — otwórz świeżą kopię:", fresh)
            return fresh
    if ODS_UNLOCKED.exists() and not _lock_active(LOCK_EDYCJA):
        return ODS_UNLOCKED
    if fresh.exists():
        return fresh
    lista = ROOT / "RECEPTURY_LAKIERY_lista.ods"
    _try_copy(built, lista)
    return lista


def ensure_lo_macros_allowed(profile: Path) -> None:
    """W profilu konwersji/podglądu zezwól na makra (inaczej lista NR się nie otworzy)."""
    user = profile / "user"
    user.mkdir(parents=True, exist_ok=True)
    xcu = user / "registrymodifications.xcu"
    snippet = (
        '<item oor:path="/org.openoffice.Office.Common/Security/Scripting">'
        '<prop oor:name="MacroSecurityLevel" oor:op="fuse"><value>0</value></prop>'
        "</item>"
    )
    if xcu.exists():
        text = xcu.read_text(encoding="utf-8", errors="replace")
        if "MacroSecurityLevel" in text:
            text = re.sub(
                r'<prop oor:name="MacroSecurityLevel"[^>]*>.*?</prop>',
                '<prop oor:name="MacroSecurityLevel" oor:op="fuse"><value>0</value></prop>',
                text,
                count=1,
                flags=re.S,
            )
            xcu.write_text(text, encoding="utf-8")
            return
        if "</oor:items>" in text:
            xcu.write_text(text.replace("</oor:items>", snippet + "</oor:items>", 1), encoding="utf-8")
            return
    xcu.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<oor:items xmlns:oor="http://openoffice.org/2001/registry" '
        'xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
        f"{snippet}\n</oor:items>\n",
        encoding="utf-8",
    )


def open_in_calc(ods_path: Path) -> None:
    if not SOFFICE.exists():
        print("Brak soffice.exe — otwórz ręcznie:", ods_path)
        return
    profile = ROOT / "data" / "extracted" / "lo_profile_gui"
    ensure_lo_macros_allowed(profile)
    uri = profile.resolve().as_uri()
    subprocess.Popen(
        [
            str(SOFFICE),
            "--norestore",
            "--nolockcheck",
            f"-env:UserInstallation={uri}",
            str(ods_path),
        ],
        cwd=str(ROOT),
    )
    print("Otwarto w LibreOffice (makra włączone):", ods_path)


def main() -> None:
    if not SOFFICE.exists():
        raise SystemExit("Nie znaleziono LibreOffice: " + str(SOFFICE))
    if not XLSX.exists():
        raise SystemExit("Brak XLSX — najpierw build_workbook.py")
    work = ROOT / "data" / "extracted" / "lo_convert"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    ods = convert(XLSX, "ods", work)
    inject_macros(ods)
    published = publish_ods(ods)
    open_in_calc(published)


if __name__ == "__main__":
    main()
