# -*- coding: utf-8 -*-
"""Katalog sklepowy tonerów Nexa Autocolor 2K z tint chart (RMTT1002).

Źródło charakterystyk: nexa-autocolor-2k-tint-chart-guide.pdf.
Opisy po polsku, pod kartę produktu. Zdjęcia dopina strona po nazwie pliku.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "config" / "pigmenty-autocolor-2k.json"

# sku, nazwa EN, kategoria, rodzina, ziarno, moc, para, kod w recepturze, krotki, opis
ROWS: list[tuple] = [
    (
        "P420-905", "Yellow Oxide", "tonery", "żółty", "", "standard", "", "P420-905",
        "Kryjący tlenek żółty. Ciepła, ziemista żółć o mocnym kryciu.",
        "Toner tlenkowy do bazy Autocolor 2K. Dodaje ciepłą żółć i silnie kryje, przytłumiając czystość tonu. Do solidów i korekt, w których potrzebna jest żółć tlenkowa, a nie czysta organiczna.",
    ),
    (
        "P429-972", "HS Bright Amber", "tonery", "pomarańcz", "", "HS", "", "P429-972",
        "Jasna, czysta pomarańcz HS. Głównie kolory solid.",
        "Jaśniejsza i czystsza niż tlenki żółte P420-982 i P420-983. Wysoka moc do nasyconych pomarańczy w kolorach solid.",
    ),
    (
        "P420-982", "Trans Oxide Yellow", "tonery", "żółty", "", "standard", "", "P420-982",
        "Transparentny tlenek żółty. Ciemniejszy flop niż P420-983.",
        "Żółć tlenkowa bez mocnego krycia. Pogłębia flop mocniej niż Strong Yellow. Do metalików i pereł, gdy żółć ma zejść w ciemniejszy cień.",
    ),
    (
        "P420-983", "Strong Yellow", "tonery", "żółty", "", "standard", "", "P420-983",
        "Żółty o pomarańczowym odcieniu, czystszy niż tlenek P420-982.",
        "Do receptur, w których flop ma zejść w zielony ton. Czystsze światło niż transparentny tlenek żółty.",
    ),
    (
        "P420-903", "RT Medium Pale Yellow", "tonery", "żółty", "", "RT", "", "P420-903RT",
        "Blada żółć o zielonkawym flopie. Toner RT, obniżona moc.",
        "Rozjaśnia mieszankę w stronę bladego, lekko zielonkawego żółtego. Obniżona siła barwienia do precyzyjnej korekty małych ilości.",
    ),
    (
        "P429-937", "HS Pale Yellow", "tonery", "żółty", "", "HS", "", "P429-937",
        "Żółty o zielonym odcieniu, zielony także na flopie.",
        "Chłodna, blada żółć HS. Przesuwa ton w zieleń i na świetle, i w cieniu.",
    ),
    (
        "P420-975", "Bronze Green", "tonery", "zielony", "", "standard", "", "P420-975",
        "Złocista zieleń na świetle, żółty odcień na flopie.",
        "Ciepła zieleń z żółtym cieniem. Do brązowo-zielonych i złotych zieleni, nie do chłodnego błękitnozielonego.",
    ),
    (
        "P425-954", "HS Blue Green", "tonery", "zielony", "", "HS", "", "P425-954",
        "Zieleń o niebieskim odcieniu.",
        "Chłodna zieleń HS. Odciąga ton od żółtozielonego w stronę błękitu.",
    ),
    (
        "P425-922", "HS Lagoon Blue", "tonery", "niebieski", "", "HS", "", "P425-922",
        "Zielonkawy niebieski z zielonym flopem. Do metalików i pereł.",
        "Przesuwa błękit w zieleń także w cieniu. Na karcie oznaczony do receptur metalik i perła.",
    ),
    (
        "P420-930", "Lake Blue", "tonery", "niebieski", "", "standard", "", "P420-930",
        "Niebieski o czerwonym odcieniu.",
        "Cieplejszy błękit, przesunięty w stronę fioletu. Korekta niebieskiego w czerwień.",
    ),
    (
        "P420-952", "Fast Blue", "tonery", "niebieski", "", "standard", "", "P420-952",
        "Niebieski o środkowym odcieniu.",
        "Neutralny błękit. Korekta tonu bez silnego zejścia w zieleń albo w czerwień.",
    ),
    (
        "P425-956", "HS Super Blue", "tonery", "niebieski", "", "HS", "", "P425-956",
        "Niebieski środkowy: zielone światło, czerwony flop.",
        "Na wprost chłodniejszy, w cieniu cieplejszy. Do metalików, w których kąt ma zmienić odcień.",
    ),
    (
        "P425-957", "HS Fast Blue", "tonery", "niebieski", "", "HS", "P420-910", "P425-957",
        "Wysokowydajny transparentny niebieski. Pełna moc odpowiednika RT Deep Blue.",
        "Ten sam kierunek co P420-910. Wchodzi, gdy udział niebieskiego przekracza 10%.",
    ),
    (
        "P420-910", "RT Deep Blue", "tonery", "niebieski", "", "RT", "P425-957", "P420-910RT",
        "Wysokowydajny transparentny niebieski w obniżonej mocy (RT).",
        "Do małych dodatków głębokiego błękitu. Powyżej 10% udziału przejdź na P425-957 HS Fast Blue.",
    ),
    (
        "P420-942", "Transoxide Red", "tonery", "czerwony", "", "standard", "", "P420-942",
        "Złotobrązowy transparentny tlenek czerwony, żółty flop.",
        "Czystsze światło oraz jaśniejszy i bardziej żółty cień niż brąz P420-978. Transparentny: buduje głębię bez mocnego krycia.",
    ),
    (
        "P429-973", "HS Bright Orange", "tonery", "pomarańcz", "", "HS", "", "P429-973",
        "Pomarańcz o czerwonym odcieniu.",
        "Ciepła, czerwona pomarańcz HS. Do korekty tonu w stronę czerwonej pomarańczy.",
    ),
    (
        "P420-907", "Red Oxide", "tonery", "czerwony", "", "standard", "P420-908", "P420-907",
        "Tlenek czerwony o niebieskim odcieniu. Pełna moc.",
        "Kryjący toner tlenkowy, pełna siła pary z RT Russet (P420-908). Wchodzi, gdy udział tlenku przekracza 10%.",
    ),
    (
        "P420-908", "RT Russet", "tonery", "czerwony", "", "RT", "P420-907", "P420-908RT",
        "Tlenek czerwony o niebieskim odcieniu, obniżona moc (RT).",
        "Do niewielkich dodatków rdzawego tlenku. Powyżej 10% użyj P420-907 Red Oxide.",
    ),
    (
        "P420-926", "Super Red", "tonery", "czerwony", "", "standard", "", "P420-926",
        "Czysta czerwień, bez tlenkowego przytłumienia.",
        "Czysty czerwony ton do korekt, w których czerwień ma zostać czysta.",
    ),
    (
        "P420-978", "Brown", "tonery", "brąz", "", "standard", "", "P420-978",
        "Ciemny brąz z bardziej żółtym flopem niż P429-923.",
        "Ściemnia i ociepla, szczególnie w cieniu. Żółtszy flop niż bordo HS Bright Maroon.",
    ),
    (
        "P425-919", "HS Clean Red Violet", "tonery", "fiolet", "", "HS", "", "P425-919",
        "Średni fiolet z głębokim flopem.",
        "Czysty czerwono-fioletowy ton. Mocno pogłębia cień.",
    ),
    (
        "P425-941", "HS Strong Red", "tonery", "czerwony", "", "HS", "", "P425-941",
        "Czysta, wysokowydajna czerwień. Głównie kolory solid.",
        "Silna siła barwienia i czysty czerwony ton. Podstawowa czerwień do solidów.",
    ),
    (
        "P425-971", "HS Brilliant Red", "tonery", "czerwony", "", "HS", "", "P425-971",
        "Czysta czerwień o żółtym tonie.",
        "Ciepła, jaskrawa czerwień w stronę pomarańczu, bez brudzenia flopu.",
    ),
    (
        "P429-923", "HS Bright Maroon", "tonery", "czerwony", "", "HS", "", "P429-923",
        "Transparentne bordo o środkowym odcieniu, ciemny flop.",
        "Ściemnia i czerwieni w cieniu, bez silnego krycia.",
    ),
    (
        "P429-980", "HS Speed Red", "tonery", "czerwony", "", "HS", "", "P429-980",
        "Jasna, czysta czerwień do solidów, zwykle powyżej 20% udziału.",
        "Silna czerwień solid. Do receptur, w których czerwień jest głównym składnikiem, a nie tylko korektą.",
    ),
    (
        "P420-920", "Violet", "tonery", "fiolet", "", "standard", "", "P420-920",
        "Czysty fiolet, czerwieńszy niż Lake Blue, z brudnym żółtym flopem.",
        "Czyste światło i cieplejszy, brudniejszy cień. Bardziej czerwony niż P420-930.",
    ),
    (
        "P425-921", "HS Claret", "tonery", "fiolet", "", "HS", "", "P425-921",
        "Czysta magenta o niebieskim tonie. Czystsza i jaśniejsza niż P429-976.",
        "Chłodny, czysty czerwono-fiolet. Jaśniejszy punkt odniesienia dla RT Burgundy i HS Red Violet.",
    ),
    (
        "P429-961", "HS Clean Magenta", "tonery", "fiolet", "", "HS", "", "P429-961",
        "Czysty fiolet o niebieskim tonie, ciemniejszy flop niż HS Claret.",
        "Chłodna magenta. Głębszy cień niż P425-921.",
    ),
    (
        "P429-976", "HS Red Violet", "tonery", "fiolet", "", "HS", "P420-960", "P429-976",
        "Fiolet o niebieskim odcieniu. Pełna moc odpowiednika RT Burgundy.",
        "Brudniejsze światło i ciemniejszy flop niż HS Claret (P425-921). Wchodzi powyżej 10% zamiast P420-960.",
    ),
    (
        "P420-960", "RT Burgundy", "tonery", "fiolet", "", "RT", "P429-976", "P420-960RT",
        "Fiolet o niebieskim odcieniu w obniżonej mocy (RT).",
        "Brudniejsze światło i ciemniejszy flop niż P425-921. Powyżej 10% użyj P429-976 HS Red Violet.",
    ),
    (
        "P420-933", "Blue Black", "czern-biel", "czerń", "", "standard", "", "P420-933",
        "Czerń o niebieskim odcieniu. Jaśniejszy i bardziej niebieski flop niż HS Black.",
        "Ściemnia z chłodnym, niebieskim cieniem. Lżejsza na flopie niż P425-948.",
    ),
    (
        "P425-900", "HS Super White", "czern-biel", "biel", "", "HS", "P420-902", "P425-900",
        "Mocna biel HS. Pełna moc odpowiednika RT Pale White.",
        "Silnie rozjaśnia. Ten sam kierunek co P420-902. Stosować, gdy udział bieli przekracza 10%.",
    ),
    (
        "P420-902", "RT Pale White", "czern-biel", "biel", "", "RT", "P425-900", "P420-902RT",
        "Mocna biel w obniżonej mocy (RT).",
        "Do małych dodatków rozjaśniających. Powyżej 10% przejdź na P425-900 HS Super White.",
    ),
    (
        "P425-948", "HS Black", "czern-biel", "czerń", "", "HS", "P420-904", "P425-948",
        "Czerń HS o żółtym odcieniu. Ciemniejszy flop niż Blue Black.",
        "Pełna moc pary z RT Transparent Black (P420-904). Ciemniejszy cień niż P420-933. Powyżej 10% zamiast tonera RT.",
    ),
    (
        "P420-904", "RT Transparent Black", "czern-biel", "czerń", "", "RT", "P425-948", "P420-904RT",
        "Czerń o żółtym odcieniu w obniżonej mocy, transparentniejsza.",
        "Ciemniejszy flop niż Blue Black (P420-933). Do małych ściemnień. Powyżej 10% użyj P425-948 HS Black.",
    ),
    (
        "P425-950", "HS Jet Black", "czern-biel", "czerń", "", "HS", "", "P425-950",
        "Czerń o żółtym odcieniu, ciemniejszy flop niż HS Black.",
        "Głębszy, cieplejszy cień niż P425-948. Do kolorów, które mają zejść mocniej w kąt.",
    ),
    (
        "P426-HE03", "Graphite Flake", "czern-biel", "grafit", "", "standard", "", "P426-HE03",
        "Grafitowy płatek. Subtelny niebieski ton na świetle, rozjaśnia flop.",
        "Nie jest konwencjonalną czernią. Uspokaja i rozjaśnia cień, dodając chłodny ton na wprost.",
    ),
    (
        "P429-967", "HS Deep Angle Black", "czern-biel", "czerń", "", "HS", "", "P429-967",
        "Czerń o żółtym odcieniu z najciemniejszym flopem w palecie 2K.",
        "Najgłębszy cień spośród czerni Autocolor 2K. Ściemnia duży kąt obserwacji.",
    ),
    (
        "P425-984", "HS Medium Fine Aluminium", "metaliki", "aluminium", "drobne", "HS", "", "P425-984",
        "Drobny, jasny metalik. Ciemniejszy flop niż średnie aluminium P425-986.",
        "Rozjaśnia światło i pogłębia cień względem średniego aluminium. Ziarno drobne.",
    ),
    (
        "P425-985", "HS Fine Aluminium", "metaliki", "aluminium", "drobne", "HS", "", "P425-985",
        "Drobny metalik: ciemne światło, jasny flop.",
        "Drobne ziarno. Na wprost ciemniejszy, w cieniu jaśniejszy niż grubsze aluminium.",
    ),
    (
        "P425-986", "HS Medium Aluminium", "metaliki", "aluminium", "średnie", "HS", "", "P425-986",
        "Średnie aluminium. Ciemniejszy flop niż drobne P425-985.",
        "Grubsze ziarno niż Fine. Cień schodzi mocniej.",
    ),
    (
        "P425-987", "Medium Coarse Aluminium", "metaliki", "aluminium", "średnie", "standard", "", "P425-987",
        "Średnio grube aluminium. Ciemniejszy flop niż drobne P425-985.",
        "Wyraźniejsze ziarno niż Fine, z ciemniejszym cieniem. Na karcie ziarno średnie.",
    ),
    (
        "P425-988", "HS Coarse Aluminium", "metaliki", "aluminium", "grube", "HS", "", "P425-988",
        "Grube aluminium: jaśniejsze światło, ciemniejszy flop niż P425-987.",
        "Mocniejszy błysk ziarna i głębszy cień. Ziarno grube.",
    ),
    (
        "P425-989", "HS Very Coarse Aluminium", "metaliki", "aluminium", "grube", "HS", "", "P425-989",
        "Bardzo grube, jasne aluminium z ciemnym flopem.",
        "Duże ziarno, silny błysk na świetle i głęboki cień.",
    ),
    (
        "P425-991", "Fine Satin Aluminium", "metaliki", "aluminium", "drobne", "standard", "", "P425-991",
        "Drobne aluminium satynowe. Ciemniejsze światło i jaśniejszy flop niż P425-984.",
        "Uspokaja błysk i rozjaśnia cień. Satynowe, drobne ziarno.",
    ),
    (
        "P425-992", "HS Shining Coarse Aluminium", "metaliki", "aluminium", "średnie", "HS", "", "P425-992",
        "Błyszczący metalik o średnim ziarnie. Ciemniejszy flop niż P425-984.",
        "Średnio jasny płatek. Na karcie ziarno średnie. Ciemniejszy cień niż drobne Medium Fine.",
    ),
    (
        "P425-998", "HS Coarse Silver Dollar Aluminium", "metaliki", "aluminium", "grube", "HS", "", "P425-998",
        "Grube aluminium typu silver dollar. Czystsze światło i ciemniejszy flop niż P425-992.",
        "Jasne, grube ziarno o czystszym błysku i głębszym cieniu niż Shining Coarse.",
    ),
    (
        "VM4370", "Super Fine Liquid Metal", "metaliki", "liquid metal", "drobne", "standard", "", "VM4370",
        "Bardzo drobne płatki liquid metal, efekt stopionego metalu.",
        "Próżniowe płatki o lustrzanym połysku. Ziarno drobne. Osobny efekt optyczny, nie klasyczne aluminium.",
    ),
    (
        "P426-HE04", "Gold Flash", "metaliki", "aluminium barwione", "średnie", "standard", "", "P426-HE04",
        "Średni złoty płatek aluminiowy.",
        "Barwione ziarno. Dodaje złoty błysk, nie jest tonerem konwencjonalnym.",
    ),
    (
        "P426-HE05", "Orange Flash", "metaliki", "aluminium barwione", "średnie", "standard", "", "P426-HE05",
        "Pomarańczowy płatek aluminiowy, ziarno średnie.",
        "Barwione aluminium. Pomarańczowy refleks na ziarnie.",
    ),
    (
        "P426-HE07", "Blue Flash", "metaliki", "aluminium barwione", "średnie", "standard", "", "P426-HE07",
        "Organiczny niebieski płatek aluminiowy, ziarno średnie.",
        "Barwione ziarno. Niebieski błysk metaliku.",
    ),
    (
        "P420-938", "Tone Controller", "flop", "korekta", "", "standard", "", "P420-938",
        "Pogrubia wygląd ziarna i rozjaśnia flop.",
        "Kontroler tonu metaliku. Uspokaja zbyt ciemny, płaski cień i daje wrażenie grubszego płatka.",
    ),
    (
        "P426-HE02", "Blue Frost", "flop", "korekta", "", "standard", "", "P426-HE02",
        "W metalikach dodaje żółć na świetle i jasnoniebieski ton na flopie.",
        "Korekta flopu w stronę chłodnego błękitu, przy żółtszym świetle.",
    ),
    (
        "P426-PP05", "White Pearl", "perly", "perła", "średnie", "standard", "", "P426-PP05",
        "Czysta biała perła. Jaśniejsze światło i ciemniejszy flop niż Fine White Pearl.",
        "Ziarno średnie. Rozjaśnia perłę i pogłębia cień względem drobnej P426-PP06.",
    ),
    (
        "P426-PP06", "Fine White Pearl", "perly", "perła", "drobne", "standard", "", "P426-PP06",
        "Drobna biała perła. Brudniejsze światło, jaśniejszy flop niż P426-PP05.",
        "Drobniejsze ziarno. Uspokaja kontrast światło/cień.",
    ),
    (
        "P426-PP07", "Blue Pearl", "perly", "perła", "średnie", "standard", "", "P426-PP07",
        "Niebieskie światło, żółty flop. Grubsza niż Fine Blue Pearl.",
        "Perła ze zmianą kąta: błękit na wprost, żółć w cieniu. Ziarno średnie.",
    ),
    (
        "P426-PP08", "Red Pearl", "perly", "perła", "średnie", "standard", "", "P426-PP08",
        "Czerwona mika, grubsza niż Fine Russet Pearl.",
        "Czerwony efekt perłowy, wyraźniejsze ziarno niż P426-PP62.",
    ),
    (
        "P426-PP09", "Gold Pearl", "perly", "perła", "średnie", "standard", "", "P426-PP09",
        "Złote światło, niebieskawy flop.",
        "Złota perła z chłodniejszym cieniem. Ziarno średnie.",
    ),
    (
        "P426-PP10", "Copper Pearl", "perly", "perła", "średnie", "standard", "", "P426-PP10",
        "Miedziane światło, na flopie ciemna miedź.",
        "Perła ze zmianą kąta w stronę ciemnej miedzi. Ziarno średnie.",
    ),
    (
        "P426-PP60", "White Satin Pearl", "perly", "perła", "drobne", "standard", "", "P426-PP60",
        "Drobna biała perła satynowa.",
        "Subtelne białe ziarno. Uspokaja błysk.",
    ),
    (
        "P426-PP61", "Fine Red Pearl", "perly", "perła", "drobne", "standard", "", "P426-PP61",
        "Interferencyjna czerwona mika z zielonym flopem.",
        "Czerwień na świetle, zieleń w cieniu. Ziarno drobne.",
    ),
    (
        "P426-PP62", "Fine Russet Pearl", "perly", "perła", "drobne", "standard", "", "P426-PP62",
        "Czerwona mika, drobniejsza niż Red Pearl.",
        "Russet perłowy o drobniejszym ziarnie niż P426-PP08.",
    ),
    (
        "P426-PP63", "Fine Blue Pearl", "perly", "perła", "drobne", "standard", "", "P426-PP63",
        "Niebieskie światło, żółty flop. Drobniejsza niż Blue Pearl.",
        "Ten sam kąt co P426-PP07, spokojniejsze ziarno.",
    ),
    (
        "P426-PP64", "Medium Violet Pearl", "perly", "perła", "średnie", "standard", "", "P426-PP64",
        "Liliowe światło, zielony flop.",
        "Fioletowa perła z zielonym cieniem. Ziarno średnie.",
    ),
    (
        "P426-PP65", "Medium Green Pearl", "perly", "perła", "średnie", "standard", "", "P426-PP65",
        "Zielone światło, czerwonawy flop.",
        "Zielona perła z ciepłym cieniem. Ziarno średnie.",
    ),
    (
        "P426-PP68", "Orange Pearl", "perly", "perła", "średnie", "standard", "", "P426-PP68",
        "Czyste pomarańczowe światło, zielony flop.",
        "Czysta pomarańcz perłowa z chłodniejszym cieniem. Ziarno średnie.",
    ),
    (
        "P440-FX51", "Silver Flair", "efekty", "efekt", "średnie", "standard", "", "P440-FX51",
        "Tęczowy efekt, szczególnie w srebrnych kolorach przy mocnym świetle.",
        "Wielobarwny refleks na srebrze. Ziarno średnie. Efekt wychodzi przy intensywnym świetle.",
    ),
    (
        "P435-GF37", "Silver Glass", "efekty", "szkło", "grube", "standard", "", "P435-GF37",
        "Srebrne płatki szkła pokryte metalem. Iskra widoczna w słońcu.",
        "Jasne kolory z intensywną iskrą. Efekt szczególnie widoczny w ostrym słońcu. Ziarno grube.",
    ),
    (
        "P433-XR10", "Crystal Silver", "efekty", "xirallic", "średnie", "standard", "", "P433-XR10",
        "Iskrzący biały Xirallic. Grubszy i jaśniejszy niż biała perła P426-PP05.",
        "Krystaliczny srebrny efekt. Ziarno średnie, mocniejsza iskra niż klasyczna perła.",
    ),
    (
        "P433-XR11", "Sunbeam Gold", "efekty", "xirallic", "średnie", "standard", "", "P433-XR11",
        "Iskrzący złoty Xirallic, jaśniejszy i grubszy niż Gold Pearl.",
        "Złota iskra, wyraźniejsza niż P426-PP09. Ziarno średnie.",
    ),
    (
        "P433-XR12", "Radiant Red", "efekty", "xirallic", "średnie", "standard", "", "P433-XR12",
        "Iskrzący czerwony Xirallic, jaśniejszy niż Red Pearl.",
        "Czerwona iskra, grubsza i jaśniejsza niż P426-PP08. Ziarno średnie.",
    ),
    (
        "P433-XR13", "Galaxy Blue", "efekty", "xirallic", "średnie", "standard", "", "P433-XR13",
        "Iskrzący niebieski Xirallic, jaśniejszy niż Blue Pearl.",
        "Niebieska iskra, grubsza i jaśniejsza niż P426-PP07. Ziarno średnie.",
    ),
    (
        "P433-XR14", "Stellar Green", "efekty", "xirallic", "średnie", "standard", "", "P433-XR14",
        "Iskrzący zielony Xirallic, jaśniejszy niż Medium Green Pearl.",
        "Zielona iskra, grubsza i jaśniejsza niż P426-PP65. Ziarno średnie.",
    ),
    (
        "P433-XR15", "Solaris Red", "efekty", "xirallic", "średnie", "standard", "", "P433-XR15",
        "Iskrzący magenta-czerwony Xirallic, jaśniejszy niż Fine Red Pearl.",
        "Magenta z iskrą, grubsza i jaśniejsza niż P426-PP61. Ziarno średnie.",
    ),
    (
        "P433-XR16", "Fireside Copper", "efekty", "xirallic", "średnie", "standard", "", "P433-XR16",
        "Iskrzący miedziany Xirallic, jaśniejszy niż Copper Pearl.",
        "Miedziana iskra, grubsza i jaśniejsza niż P426-PP10. Ziarno średnie.",
    ),
    (
        "P433-XR17", "Cosmic Turquoise", "efekty", "xirallic", "średnie", "standard", "", "P433-XR17",
        "Iskrzący morski błękit, płatek Xirallic.",
        "Turkusowy efekt o wyraźnej iskrze. Ziarno średnie.",
    ),
    (
        "P433-XR18", "Amethyst Dream", "efekty", "xirallic", "średnie", "standard", "", "P433-XR18",
        "Iskrzący fioletowy Xirallic, jaśniejszy niż Medium Violet Pearl.",
        "Fioletowa iskra, grubsza i jaśniejsza niż P426-PP64. Ziarno średnie.",
    ),
    (
        "P434-CS31", "Autumn Mystery", "efekty", "colorstream", "średnie", "standard", "", "P434-CS31",
        "Colorstream: kąt od czerwieni przez złoto i brąz do zieleni.",
        "Pomarańczowy płatek krzemionkowy. Barwa zmienia się z kątem patrzenia: czerwień, złoto, brąz, zieleń.",
    ),
    (
        "P434-CS32", "Viola Fantasy", "efekty", "colorstream", "średnie", "standard", "", "P434-CS32",
        "Colorstream: kąt fiolet, srebro, zieleń, błękit.",
        "Biały płatek krzemionkowy. Kąt przechodzi od fioletu przez srebro i zieleń do błękitu.",
    ),
    (
        "P434-CS33", "Arctic Fire", "efekty", "colorstream", "średnie", "standard", "", "P434-CS33",
        "Colorstream: od turkusu przez srebro do czerwieni.",
        "Płatek krzemionkowy. Kąt od subtelnego turkusu przez błyszczące srebro do czerwieni.",
    ),
    (
        "P434-CS34", "Tropic Sunrise", "efekty", "colorstream", "średnie", "standard", "", "P434-CS34",
        "Colorstream: zieleń, srebro, czerwonawa pomarańcz.",
        "Płatek krzemionkowy. Kąt przechodzi od zieleni przez srebro do czerwonawej pomarańczy.",
    ),
    (
        "P434-CS35", "Lapis Sunlight", "efekty", "colorstream", "średnie", "standard", "", "P434-CS35",
        "Colorstream: złoto, zieleń, błękit.",
        "Płatek krzemionkowy. Kąt przechodzi od złota przez zieleń do błękitu.",
    ),
    (
        "VM4987", "Cyan to Purple", "efekty", "chromaflair", "średnie", "standard", "", "VM4987",
        "ChromaFlair: cyjan przechodzi w fiolet.",
        "Płatek zmieniający barwę z kątem. Dodaje przesunięcie koloru, nie krycie. Ziarno średnie.",
    ),
    (
        "VM4988", "Silver to Green", "efekty", "chromaflair", "średnie", "standard", "", "VM4988",
        "ChromaFlair: srebro przechodzi w zieleń.",
        "Płatek zmieniający barwę z kątem. Ziarno średnie.",
    ),
    (
        "VM4989", "Green to Purple", "efekty", "chromaflair", "średnie", "standard", "", "VM4989",
        "ChromaFlair: zieleń przechodzi w fiolet.",
        "Płatek zmieniający barwę z kątem. Ziarno średnie.",
    ),
    (
        "VM4990", "Blue to Red", "efekty", "chromaflair", "średnie", "standard", "", "VM4990",
        "ChromaFlair: błękit przechodzi w czerwień.",
        "Płatek zmieniający barwę z kątem. Ziarno średnie.",
    ),
    (
        "VM4991", "Magenta to Gold", "efekty", "chromaflair", "średnie", "standard", "", "VM4991",
        "ChromaFlair: magenta przechodzi w złoto.",
        "Płatek zmieniający barwę z kątem. Ziarno średnie.",
    ),
    (
        "VM4994", "Gold to Silver", "efekty", "chromaflair", "średnie", "standard", "", "VM4994",
        "ChromaFlair: złoto przechodzi w srebro.",
        "Płatek zmieniający barwę z kątem. Ziarno średnie.",
    ),
    (
        "VM4995", "Red to Gold", "efekty", "chromaflair", "średnie", "standard", "", "VM4995",
        "ChromaFlair: czerwień przechodzi w złoto.",
        "Płatek zmieniający barwę z kątem. Ziarno średnie.",
    ),
]


def slugify(sku: str, name: str) -> str:
    raw = f"{sku} {name}".lower()
    raw = raw.replace("ł", "l").replace("ś", "s").replace("ć", "c")
    raw = re.sub(r"[^a-z0-9]+", "-", raw).strip("-")
    return raw


def main() -> None:
    skus = [row[0] for row in ROWS]
    if len(skus) != len(set(skus)):
        raise SystemExit("zduplikowany kod")
    products = []
    for i, row in enumerate(ROWS, start=1):
        sku, name_en, cat, rodzina, ziarno, moc, para, kod_rec, short, description = row
        products.append(
            {
                "id": "ac-" + sku.lower(),
                "sku": sku,
                "kod_receptury": kod_rec,
                "name": f"{sku} {name_en}",
                "name_en": name_en,
                "category": cat,
                "rodzina": rodzina,
                "ziarno": ziarno,
                "moc": moc,
                "para": para,
                "short": short,
                "description": description,
                "image_file": "",
                "slug": slugify(sku, name_en),
                "sort": i,
            }
        )
    payload = {
        "system": "Nexa Autocolor 2K",
        "zrodlo": "nexa-autocolor-2k-tint-chart-guide.pdf",
        "zrodlo_nr": "RMTT1002, 5/18",
        "uwaga": (
            "Opisy techniczne pod kartę sklepu, na podstawie charakterystyki tint chart. "
            "Ceny i pojemności nie pochodzą z karty. "
            "Zdjęcie: wrzuć plik do public/assets/images/pigmenty/ "
            "nazwany kodem, np. P420-905.webp (albo .jpg, .jpeg, .png). "
            "Można też wpisać nazwę pliku w image_file. Puste pole = placeholder."
        ),
        "image_placeholder": "/assets/images/products/product-placeholder.svg",
        "image_dir": "public/assets/images/pigmenty",
        "categories": [
            {"id": "tonery", "name": "Tonery kolorowe"},
            {"id": "czern-biel", "name": "Czerń i biel"},
            {"id": "metaliki", "name": "Metaliki"},
            {"id": "perly", "name": "Perły"},
            {"id": "efekty", "name": "Efekty specjalne"},
            {"id": "flop", "name": "Korekta flopu"},
        ],
        "products": products,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(products)} -> {OUT}")


if __name__ == "__main__":
    main()
