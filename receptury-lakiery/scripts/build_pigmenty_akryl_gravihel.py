# -*- coding: utf-8 -*-
"""Katalogi sklepowe: MOBIHEL 2K akryl MIX oraz pasty GRAVIHEL.

Akryl: 30 składników UNI z karty TDS 2K Acrylic Enamel MIX (zakres 101–131
bez wycofanego 106). Kierunek koloru z nazw katalogowych.
Gravihel: 31 past (20 pasteli, 5 aluminium, 6 pereł) i 8 proszków
fluorescencyjnych z karty TDS past GRAVIHEL.
Ceny nie są uzupełnione.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKLEP = ROOT / "sklep"

# sku, nazwa, kategoria, rodzina, krotki, opis
AKRYL: list[tuple] = [
    ("MIX 101", "Biel", "kolory", "biel",
     "Kryjąca biel. Można jej użyć jako samodzielnego białego lakieru.",
     "Główna biel systemu 2K. Rozjaśnia mieszankę i daje krycie. Z czerwienią MIX 105 schodzi w róż."),
    ("MIX 102", "Pomarańcz", "kolory", "pomarańcz",
     "Pomarańczowo-czerwony. Sam słabo kryje.",
     "Ciepła pomarańcz z czerwoną nutą. Wchodzi razem z pigmentem kryjącym."),
    ("MIX 103", "Błękit brylantowy", "kolory", "niebieski",
     "Mocny błękit o zielonkawym kierunku.",
     "Do czystych niebieskich solidów 2K. Sam nie daje pełnego krycia."),
    ("MIX 104", "Fiolet", "kolory", "fiolet",
     "Fiolet do korekty w stronę czerwonego błękitu.",
     "Przesuwa kolor w fiolet. Używany w mieszance, nie jako samodzielny lakier."),
    ("MIX 105", "Czerwień brylantowa", "kolory", "czerwony",
     "Czerwień z niebieskim odcieniem. Z bielą MIX 101 daje róż.",
     "Czysta, chłodniejsza czerwień. Do różów i czerwonych solidów w mieszance."),
    ("MIX 107", "Zieleń jasna", "kolory", "zielony",
     "Przezroczysta zieleń z żółtym odcieniem.",
     "Rozjaśnia zieleń w stronę żółci. Słabe krycie, tylko jako składnik mieszanki."),
    ("MIX 108", "Ochra", "kolory", "żółty",
     "Brudna, kryjąca ochra. Można jej użyć samodzielnie.",
     "Żółcień tlenkowa. Przytłumia czystość i buduje beże, żółcie ziemiste i brązy."),
    ("MIX 109", "Żółcień", "kolory", "żółty",
     "Brylantowa żółć do większości żółtych kolorów.",
     "Czysta, mocna żółć. Główny żółty składnik solidów 2K."),
    ("MIX 110", "Zieleń", "kolory", "zielony",
     "Zieleń o niebieskawym kierunku.",
     "Chłodniejsza niż MIX 107. Do zielonych solidów w mieszance."),
    ("MIX 111", "Błękit", "kolory", "niebieski",
     "Przezroczysty błękit z zielonym odcieniem.",
     "Koryguje niebieski w stronę zieleni. Sam nie kryje."),
    ("MIX 112", "Czerwień tlenkowa", "kolory", "czerwony",
     "Kryjąca, brudna czerwień tlenkowa. Można jej użyć samodzielnie.",
     "Żółto-tlenkowa czerwień. Do brązów, beżów i przytłumionych czerwieni."),
    ("MIX 113", "Czerń głęboka", "kolory", "czerń",
     "Głęboka czerń o dobrym kryciu. Można jej użyć samodzielnie.",
     "Główna czerń do ciemnych solidów. Pogłębia kolor mocniej niż MIX 116."),
    ("MIX 114", "Czerwień", "kolory", "czerwony",
     "Czerwień z lekkim niebieskim odcieniem.",
     "Czystsza czerwień niż tlenek MIX 112. Do czerwonych solidów w mieszance."),
    ("MIX 115", "Bordo", "kolory", "czerwony",
     "Ciemna czerwień w stronę bordo.",
     "Ściemnia i ochładza czerwień. Składnik mieszanki, nie samodzielny lakier."),
    ("MIX 116", "Czerń", "kolory", "czerń",
     "Czerń o dobrym kryciu. Można jej użyć samodzielnie.",
     "Neutralniejsza czerń niż MIX 113. Do czarnych solidów i ściemniania."),
    ("MIX 117", "Żółcień jasna", "kolory", "żółty",
     "Jasna żółć, słabsza niż MIX 109.",
     "Do bladych żółci i korekt, gdy brylantowa żółć MIX 109 jest za mocna."),
    ("MIX 118", "Biel HP", "kolory", "biel",
     "Biel o wyższej mocy niż MIX 101.",
     "Mocniej rozjaśnia i kryje. Do białych i bardzo jasnych kolorów."),
    ("MIX 119", "Czerwień HP", "kolory", "czerwony",
     "Czerwień o wyższej mocy.",
     "Mocniejszy czerwony składnik, gdy standardowa czerwień jest za słaba."),
    ("MIX 120", "Toner fioletowy", "tonery", "fiolet",
     "Obniżona moc. Do małej korekty w fiolet.",
     "Słabsza wersja fioletu. Precyzyjna korekta pasteli bez przeskoku koloru."),
    ("MIX 121", "Toner zielony", "tonery", "zielony",
     "Obniżona moc. Do małej korekty w zieleń.",
     "Słabsza zieleń. Do jasnych kolorów, w których pełny zielony byłby za mocny."),
    ("MIX 122", "Toner niebieski", "tonery", "niebieski",
     "Obniżona moc. Do małej korekty w błękit.",
     "Słabszy błękit. Do pastelowych korekt."),
    ("MIX 123", "Toner tlenkowy", "tonery", "czerwony",
     "Obniżona moc tlenku czerwonego.",
     "Mała korekta w brudną, żółtawą czerwień bez mocnego krycia MIX 112."),
    ("MIX 124", "Toner ochra", "tonery", "żółty",
     "Obniżona moc ochry.",
     "Delikatnie brudzi żółć i beże. Do małych dodatków."),
    ("MIX 125", "Toner czarny", "tonery", "czerń",
     "Obniżona moc czerni.",
     "Ściemnia pastel bez dziury w kolorze, jaką dałaby pełna czerń."),
    ("MIX 126", "Żółcień HP", "kolory", "żółty",
     "Żółć o wyższej mocy.",
     "Mocniejsza żółć do nasyconych żółtych solidów."),
    ("MIX 127", "Czerwień pomarańczowa", "kolory", "czerwony",
     "Czerwień przesunięta w pomarańcz.",
     "Cieplejsza niż MIX 114. Do czerwonych pomarańczy."),
    ("MIX 128", "Czerwień ciemna", "kolory", "czerwony",
     "Ciemna czerwień.",
     "Ściemnia czerwień głębiej niż MIX 115, bez zejścia w czystą czerń."),
    ("MIX 129", "Błękit królewski", "kolory", "niebieski",
     "Ciemny błękit o fioletowym kierunku.",
     "Głębszy i bardziej czerwony niż MIX 103. Do granatów w mieszance."),
    ("MIX 130", "Żółcień słoneczna", "kolory", "żółty",
     "Ciepła, nasycona żółć.",
     "Bardziej złocista niż MIX 109. Do słonecznych żółci."),
    ("MIX 131", "Czerń głęboka ekstra", "kolory", "czerń",
     "Głębsza czerń niż MIX 113.",
     "Do nasyconych czerni, gdy standardowa głęboka czerń jest za płytka."),
]

GRAVIHEL: list[tuple] = [
    ("GHEL 01", "Biel", "pigmenty", "biel", "",
     "Kryjąca biel. Rozjaśnia pastę w binderze.",
     "Główna biel systemu. Daje krycie jasnych kolorów RAL i NCS."),
    ("GHEL 02", "Ochra", "pigmenty", "żółty", "",
     "Brudna żółć tlenkowa. Przytłumia czystość.",
     "Do beżów, żółci ziemistych i brązów. Kryje mocniej niż czysta żółć."),
    ("GHEL 03", "Żółcień złocista", "pigmenty", "żółty", "",
     "Ciepła, złocista żółć.",
     "Przesuwa żółć w złoto. Do nasyconych żółtych i złotych solidów."),
    ("GHEL 04", "Żółcień jasna", "pigmenty", "żółty", "",
     "Jasna, czystsza żółć.",
     "Do bladych żółci, gdy ochra i złocista żółć są za brudne."),
    ("GHEL 05", "Żółcień zielonkawa", "pigmenty", "zielony", "",
     "Żółć o zielonym odcieniu.",
     "Przesuwa kolor w żółtozielony. Do limonek i chłodnych żółci."),
    ("GHEL 06", "Żółcień czerwonawa", "pigmenty", "żółty", "",
     "Żółć z czerwonym odcieniem.",
     "Ociepla żółć w stronę pomarańczy."),
    ("GHEL 07", "Żółcień pomarańczowa", "pigmenty", "pomarańcz", "",
     "Żółtopomarańcz.",
     "Most między żółcią a pomarańczą GHEL 08."),
    ("GHEL 08", "Pomarańcz", "pigmenty", "pomarańcz", "",
     "Czysty pomarańcz.",
     "Do pomarańczowych solidów i korekty czerwieni w ciepło."),
    ("GHEL 09", "Czerwień tlenkowa", "pigmenty", "czerwony", "",
     "Kryjąca, brudna czerwień tlenkowa.",
     "Do brązów, czerwieni ziemistych i przytłumienia czystej czerwieni."),
    ("GHEL 10", "Czerwień", "pigmenty", "czerwony", "",
     "Czysta czerwień.",
     "Główny czerwony składnik solidów. Czyściejsza niż tlenek GHEL 09."),
    ("GHEL 11", "Czerwień burgund", "pigmenty", "czerwony", "",
     "Ciemna czerwień o burgundowym kierunku.",
     "Ściemnia czerwień bez zejścia w bordo GHEL 12."),
    ("GHEL 12", "Bordo", "pigmenty", "czerwony", "",
     "Głębokie bordo.",
     "Ochładza i ściemnia czerwień w stronę wina."),
    ("GHEL 13", "Fiolet", "pigmenty", "fiolet", "",
     "Fiolet.",
     "Przesuwa błękit w czerwień albo czerwień w błękit."),
    ("GHEL 14", "Magenta", "pigmenty", "fiolet", "",
     "Czysta magenta.",
     "Chłodna, niebieskawa czerwień. Do różów i purpur."),
    ("GHEL 15", "Zieleń", "pigmenty", "zielony", "",
     "Zieleń.",
     "Główny zielony składnik. Czyściejsza niż żółtozielony GHEL 05."),
    ("GHEL 16", "Błękit nieba", "pigmenty", "niebieski", "",
     "Jasny, niebieski o zielonkawym świetle.",
     "Do jasnych błękitów. Chłodniejszy i jaśniejszy niż GHEL 17."),
    ("GHEL 17", "Błękit", "pigmenty", "niebieski", "",
     "Błękit.",
     "Główny niebieski składnik solidów, głębszy niż błękit nieba."),
    ("GHEL 18", "Czerń głęboka", "pigmenty", "czerń", "",
     "Głęboka czerń.",
     "Do nasyconych czerni i mocnego ściemnienia."),
    ("GHEL 19", "Czerń", "pigmenty", "czerń", "",
     "Czerń.",
     "Standardowe ściemnianie. Płytsza niż GHEL 18."),
    ("GHEL 20", "Toner czarny", "pigmenty", "czerń", "",
     "Słabsza czerń do małej korekty.",
     "Ściemnia bez dziury, którą dałaby pełna czerń w jasnym kolorze."),
    ("GHEL 21", "Aluminium drobne", "aluminium", "aluminium", "drobne",
     "Drobne srebro.",
     "Drobny metalik. Do jasnych sreber i drobnego ziarna."),
    ("GHEL 22", "Aluminium grube", "aluminium", "aluminium", "grube",
     "Grube srebro.",
     "Grubsze ziarno, wyraźniejszy błysk. Do efektów, w których drobne srebro jest za gładkie."),
    ("GHEL 23", "Aluminium ekstra grube", "aluminium", "aluminium", "ekstra grube",
     "Bardzo grube srebro.",
     "Najgrubszy płatek tej trójki. Do grubych metalików i struktur, gdzie ziarno ma być widoczne."),
    ("GHEL 24", "Złoto blade", "aluminium", "złoto", "drobne",
     "Blade złote aluminium.",
     "Ciepły metalik. Do złotych i szampańskich kolorów, nie do neutralnego srebra."),
    ("GHEL 25", "Aluminium super drobne", "aluminium", "aluminium", "ekstra drobne",
     "Najdrobniejsze srebro.",
     "Gładsze niż GHEL 21. Do jedwabistych, bardzo drobnych metalików."),
    ("GHEL 30", "Perła biała", "perly", "biel", "",
     "Biała perła.",
     "Dodaje biały, perłowy połysk w binderze efektowym."),
    ("GHEL 31", "Perła żółta", "perly", "żółty", "",
     "Żółta perła.",
     "Ciepły perłowy błysk. Do złotawych efektów."),
    ("GHEL 32", "Perła czerwona", "perly", "czerwony", "",
     "Czerwona perła.",
     "Czerwony perłowy połysk."),
    ("GHEL 33", "Perła niebieska", "perly", "niebieski", "",
     "Niebieska perła.",
     "Niebieski perłowy połysk."),
    ("GHEL 34", "Perła fioletowa", "perly", "fiolet", "",
     "Fioletowa perła.",
     "Fioletowy perłowy połysk."),
    ("GHEL 35", "Perła zielona", "perly", "zielony", "",
     "Zielona perła.",
     "Zielony perłowy połysk."),
    ("PP 40", "Fluor żółty", "fluor", "żółty", "",
     "Żółty pigment fluorescencyjny.",
     "Świeci w świetle dziennym. Nie zastępuje pasteli GHEL. Do kolorów ostrzegawczych."),
    ("PP 41", "Fluor żółtopomarańczowy", "fluor", "pomarańcz", "",
     "Żółtopomarańczowy pigment fluorescencyjny.",
     "Między żółtym PP 40 a pomarańczowym PP 42."),
    ("PP 42", "Fluor pomarańczowy", "fluor", "pomarańcz", "",
     "Pomarańczowy pigment fluorescencyjny.",
     "Do pomarańczowych kolorów fluorescencyjnych."),
    ("PP 43", "Fluor czerwonopomarańczowy", "fluor", "czerwony", "",
     "Czerwonopomarańczowy pigment fluorescencyjny.",
     "Między pomarańczem PP 42 a czerwienią PP 44."),
    ("PP 44", "Fluor czerwony", "fluor", "czerwony", "",
     "Czerwony pigment fluorescencyjny.",
     "Do czerwonych kolorów fluorescencyjnych."),
    ("PP 45", "Fluor różowy", "fluor", "czerwony", "",
     "Różowy pigment fluorescencyjny.",
     "Chłodniejszy niż czerwień PP 44."),
    ("PP 46", "Fluor niebieski", "fluor", "niebieski", "",
     "Niebieski pigment fluorescencyjny.",
     "Do niebieskich kolorów fluorescencyjnych."),
    ("PP 47", "Fluor zielony", "fluor", "zielony", "",
     "Zielony pigment fluorescencyjny.",
     "Do zielonych kolorów fluorescencyjnych."),
]


def slugify(sku: str, name: str) -> str:
    raw = f"{sku} {name}".lower()
    for src, dst in (
        ("ł", "l"), ("ś", "s"), ("ć", "c"), ("ń", "n"), ("ó", "o"),
        ("ą", "a"), ("ę", "e"), ("ż", "z"), ("ź", "z"),
    ):
        raw = raw.replace(src, dst)
    return re.sub(r"[^a-z0-9]+", "-", raw).strip("-")


def products_from(rows: list[tuple], prefix: str) -> list[dict]:
    products = []
    for i, row in enumerate(rows, start=1):
        if len(row) == 6:
            sku, name, cat, rodzina, short, description = row
            ziarno = ""
        else:
            sku, name, cat, rodzina, ziarno, short, description = row
        products.append(
            {
                "id": prefix + "-" + sku.lower().replace(" ", "-"),
                "sku": sku,
                "kod_receptury": sku.replace(" ", ""),
                "name": f"{sku} {name}",
                "name_pl": name,
                "category": cat,
                "rodzina": rodzina,
                "ziarno": ziarno,
                "short": short,
                "description": description,
                "image_file": "",
                "slug": slugify(sku, name),
                "sort": i,
            }
        )
    return products


def write_csv(path: Path, products: list[dict], cat_name: dict[str, str], root_name: str) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        writer.writerow([
            "Active", "Name", "Categories", "Price tax excluded",
            "Reference", "Short description", "Description", "Visibility",
        ])
        for product in products:
            writer.writerow([
                1,
                product["name"],
                f"{root_name}/{cat_name[product['category']]}",
                "",
                product["sku"],
                product["short"],
                f"<p>{product['description']}</p>",
                "both",
            ])


def dump(stem: str, payload: dict, root_name: str) -> None:
    skus = [p["sku"] for p in payload["products"]]
    if len(skus) != len(set(skus)):
        raise SystemExit(f"zduplikowany kod w {stem}")
    json_path = SKLEP / f"{stem}.json"
    csv_path = SKLEP / f"{stem}-prestashop.csv"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cat_name = {c["id"]: c["name"] for c in payload["categories"]}
    write_csv(csv_path, payload["products"], cat_name, root_name)
    print(f"{len(payload['products'])} -> {json_path.name}, {csv_path.name}")


def main() -> None:
    SKLEP.mkdir(parents=True, exist_ok=True)
    dump(
        "pigmenty-mobihel-akryl",
        {
            "sklep": "autocolor.pl",
            "przeznaczenie": "Dane katalogowe produktów do sklepu autocolor.pl.",
            "system": "MOBIHEL 2K akryl MIX",
            "zrodlo_lista": "Karta TDS MOBIHEL 2K Acrylic Enamel MIX: 30 pigmentów UNI, kody 101–131 bez 106",
            "zrodlo_opisy": "Nazwy katalogowe składników i noty krycia z karty produktu akrylu 2K",
            "uwaga": (
                "Lakier jednowarstwowy 2K, nie baza. Opis mówi o kierunku koloru i kryciu, nie o flopie. "
                "Samodzielnie kryją MIX 101, 108, 112, 113 i 116. Tonery 120–125 mają obniżoną moc. "
                "MIX 106 nie wchodzi w aktualny zestaw 30 składników. Ceny nie są uzupełnione."
            ),
            "image_placeholder": "/assets/images/products/product-placeholder.svg",
            "image_dir": "public/assets/images/pigmenty",
            "categories": [
                {"id": "kolory", "name": "Kolory"},
                {"id": "tonery", "name": "Tonery obniżonej mocy"},
            ],
            "products": products_from(AKRYL, "mh2k"),
        },
        "Pigmenty MOBIHEL 2K akryl",
    )
    dump(
        "pigmenty-gravihel",
        {
            "sklep": "autocolor.pl",
            "przeznaczenie": "Dane katalogowe produktów do sklepu autocolor.pl.",
            "system": "GRAVIHEL",
            "zrodlo_lista": "Karta TDS GRAVIHEL Pastes: 31 past oraz 8 proszków fluorescencyjnych",
            "zrodlo_opisy": "Nazwy i rola past z karty TDS. Pasty barwią binder, nie są gotowym lakierem.",
            "uwaga": (
                "31 past: 20 pasteli, 5 aluminium, 6 pereł, plus 8 proszków fluorescencyjnych. "
                "Pasty są wysoko stężone i wchodzą do binderów GRAVIHEL. "
                "Ceny nie są uzupełnione. Proszek fosforyzujący z opisu systemu nie ma kodu na karcie past, więc go tu nie ma."
            ),
            "image_placeholder": "/assets/images/products/product-placeholder.svg",
            "image_dir": "public/assets/images/pigmenty",
            "categories": [
                {"id": "pigmenty", "name": "Pigmenty"},
                {"id": "aluminium", "name": "Aluminium"},
                {"id": "perly", "name": "Perła"},
                {"id": "fluor", "name": "Fluorescencyjne"},
            ],
            "products": products_from(GRAVIHEL, "gh"),
        },
        "Pasty GRAVIHEL",
    )


if __name__ == "__main__":
    main()
