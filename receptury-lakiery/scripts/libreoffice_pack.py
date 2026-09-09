# -*- coding: utf-8 -*-
"""Konwersja przez LibreOffice + wstrzyknięcie makr StarBasic do ODS."""
from __future__ import annotations

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
BAS = ROOT / "macros" / "modReceptury.bas"

NS = {"manifest": "urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"}


def convert(src: Path, dest_ext: str, outdir: Path) -> Path:
    outdir.mkdir(parents=True, exist_ok=True)
    profile = ROOT / "data" / "extracted" / "lo_profile"
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
        tmp_zip = ods_path.with_suffix(".ods.tmpzip")
        with zipfile.ZipFile(tmp_zip, "w", zipfile.ZIP_DEFLATED) as zout:
            for f in tmp.rglob("*"):
                if f.is_file():
                    zout.write(f, f.relative_to(tmp).as_posix())
        shutil.move(tmp_zip, ods_path)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


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
    shutil.copy2(ods, ODS)
    inject_macros(ODS)
    print("ODS z makrami:", ODS, "size", ODS.stat().st_size)


if __name__ == "__main__":
    main()
