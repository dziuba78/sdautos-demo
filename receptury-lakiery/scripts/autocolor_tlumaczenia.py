# -*- coding: utf-8 -*-
"""Polskie opisy działania tonerów Nexa Autocolor 2K (tint chart).

Nazwy katalogowe (Pale White, HS Super White itd.) zostają po angielsku.
Kody pigmentów i czynnik E nie są zmieniane. Tłumaczone są tylko opisy
dobarwiania: światło (face), flop (cień), ziarno, krycie, czystość tonu.
"""
from __future__ import annotations

# kod → nazwa katalogowa EN, opis EN (z PDF, uzupełniony), opis PL
TINT: dict[str, dict[str, str]] = {
    "P192-475": {
        "nazwa": "REGULATOR BAZY",
        "en": "Base blender / reducer. Does not shift hue; adjusts viscosity and application of the mixing base.",
        "pl": "Regulator bazy — rozcieńcza i ułatwia aplikację mieszanki, bez zmiany odcienia. Nie jest tonerem kolorystycznym.",
    },
    "P192-528": {
        "nazwa": "REGULATOR UŁOŻENIA ZIARNA",
        "en": "Grain / flake orientation controller. Settles metallic flake layout.",
        "pl": "Regulator ułożenia ziarna — poprawia orientację płatków metalicznych, uspokaja układ ziarna na powierzchni.",
    },
    "P192-5600": {
        "nazwa": "REGULATOR FLOPU",
        "en": "Flop controller. Adjusts the light-to-dark travel (face vs flop).",
        "pl": "Regulator flopu — koryguje różnicę światło/cień, uspokaja lub pogłębia flop (cień) w metalikach i perłach.",
    },
    "P420-902RT": {
        "nazwa": "RT Pale White",
        "en": "Strong white. If more than 10% use P425-900.",
        "pl": "Mocna biel — silnie rozjaśnia. Toner RT (obniżona moc). Jeżeli udział przekracza 10%, użyj P425-900.",
    },
    "P420-903RT": {
        "nazwa": "RT Medium Pale Yellow",
        "en": "Pale yellow with a greenish yellow flop.",
        "pl": "Bladożółty z zielonkawożółtym flopem (cień). Toner RT — rozjaśnia w stronę bladego żółtego.",
    },
    "P420-904RT": {
        "nazwa": "RT Transparent Black",
        "en": "Yellow-shade black, darker flop than P420-933. If more than 10% use P425-948.",
        "pl": "Czerń o żółtym odcieniu, ciemniejszy flop niż P420-933. Toner RT, transparentniejszy niż pełna czerń. Jeżeli udział przekracza 10%, użyj P425-948.",
    },
    "P420-905": {
        "nazwa": "Yellow Oxide",
        "en": "Opaque yellow oxide.",
        "pl": "Kryjący tlenek żółty. Dodaje żółć tlenkową (ciepłą, ziemistą), silne krycie, przytłumia czystość tonu.",
    },
    "P420-907": {
        "nazwa": "Red Oxide",
        "en": "Red oxide. Full-strength counterpart of RT Russet P420-908RT.",
        "pl": "Tlenek czerwony (rdzawy). Kryjący toner tlenkowy; pełna moc odpowiednika RT Russet (P420-908RT).",
    },
    "P420-908RT": {
        "nazwa": "RT Russet",
        "en": "Blue shade red oxide. If more than 10% use P420-907.",
        "pl": "Tlenek czerwony o niebieskim odcieniu. Toner RT. Jeżeli udział przekracza 10%, użyj P420-907.",
    },
    "P420-910RT": {
        "nazwa": "RT Deep Blue",
        "en": "High strength transparent blue. If more than 10% use P425-957.",
        "pl": "Wysokowydajny transparentny niebieski. Toner RT. Jeżeli udział przekracza 10%, użyj P425-957.",
    },
    "P420-920": {
        "nazwa": "Violet",
        "en": "Clean violet with a dirty yellow flop, redder than P420-930.",
        "pl": "Czysty fiolet z brudnym żółtym flopem; bardziej czerwony niż P420-930. Czyste światło (face), cieplejszy/brudniejszy cień.",
    },
    "P420-926": {
        "nazwa": "Super Red",
        "en": "Clean red.",
        "pl": "Czysta czerwień. Dodaje czysty czerwony ton (bez tlenkowego przytłumienia).",
    },
    "P420-930": {
        "nazwa": "Lake Blue",
        "en": "Red shade blue.",
        "pl": "Niebieski o czerwonym odcieniu. Przesuwa ton w stronę czerwono-niebieskiego (cieplejszy błękit).",
    },
    "P420-933": {
        "nazwa": "Blue Black",
        "en": "Blue-shade black, lighter and bluer flop than P425-948.",
        "pl": "Czerń o niebieskim odcieniu; jaśniejszy i bardziej niebieski flop niż P425-948. Ściemia z niebieskim cieniem.",
    },
    "P420-938": {
        "nazwa": "Tone Controller",
        "en": "Gives a more coarse flake appearance and lightens the flop.",
        "pl": "Kontroler tonu — daje wrażenie grubszego ziarna i rozjaśnia flop (cień). Uspokaja zbyt ciemny/płaski cień metaliku.",
    },
    "P420-942": {
        "nazwa": "Transoxide Red",
        "en": "Golden brown transparent red oxide with a yellow shade flop. Cleaner face, lighter and yellower flop than P420-978.",
        "pl": "Złotobrązowy transparentny tlenek czerwony z żółtym flopem. Czystsze światło (face), jaśniejszy i bardziej żółty flop niż P420-978.",
    },
    "P420-952": {
        "nazwa": "Fast Blue",
        "en": "Mid-shade blue.",
        "pl": "Niebieski o środkowym odcieniu. Neutralny błękit do korekty tonu bez silnego przesunięcia w zieleń lub czerwień.",
    },
    "P420-960RT": {
        "nazwa": "RT Burgundy",
        "en": "Blue shade violet, dirtier face and darker flop than P425-921. If more than 10% use P429-976.",
        "pl": "Fiolet o niebieskim odcieniu; brudniejsze światło (face) i ciemniejszy flop niż P425-921. Toner RT. Jeżeli udział przekracza 10%, użyj P429-976.",
    },
    "P420-975": {
        "nazwa": "Bronze Green",
        "en": "Golden green face, yellow shade flop.",
        "pl": "Złocista zieleń na świetle (face), żółty odcień na flopie. Ciepła zieleń z żółtym cieniem.",
    },
    "P420-978": {
        "nazwa": "Brown",
        "en": "Dark brown with a yellower flop than P429-923.",
        "pl": "Ciemny brąz z bardziej żółtym flopem niż P429-923. Ściemia i ociepla, szczególnie w cieniu.",
    },
    "P420-982": {
        "nazwa": "Trans Oxide Yellow",
        "en": "Transparent yellow oxide with a darker flop than P420-983.",
        "pl": "Transparentny tlenek żółty z ciemniejszym flopem niż P420-983. Żółć tlenkowa bez silnego krycia, pogłębia cień.",
    },
    "P420-983": {
        "nazwa": "Strong Yellow",
        "en": "Orange shade yellow, can be used when a green tone flop is needed. Cleaner than P420-982.",
        "pl": "Żółty o pomarańczowym odcieniu; stosować, gdy potrzebny zielony flop. Czystszy niż P420-982.",
    },
    "P425-900": {
        "nazwa": "HS Super White",
        "en": "Strong HS white. Full-strength counterpart of RT Pale White P420-902RT.",
        "pl": "Mocna biel HS — silnie rozjaśnia recepturę. Pełna moc odpowiednika RT Pale White (P420-902RT).",
    },
    "P425-919": {
        "nazwa": "HS Clean Red Violet",
        "en": "Medium violet with deep flop.",
        "pl": "Średni fiolet z głębokim flopem. Czysty czerwono-fioletowy ton, mocno pogłębia cień.",
    },
    "P425-921": {
        "nazwa": "HS Claret",
        "en": "Clean blue tone magenta, cleaner and lighter than P429-976.",
        "pl": "Czysta magenta o niebieskim tonie; czystsza i jaśniejsza niż P429-976. Czysty, chłodny czerwono-fiolet.",
    },
    "P425-922": {
        "nazwa": "HS Lagoon Blue",
        "en": "Green shade blue with a green flop. Used in metallic/pearl formulations.",
        "pl": "Zielonawy niebieski z zielonym flopem. Do receptur metalik/perła — przesuwa błękit w zieleń, także w cieniu.",
    },
    "P425-941": {
        "nazwa": "HS Strong Red",
        "en": "Clean, high strength red used primarily in solid colours.",
        "pl": "Czysta, wysokowydajna czerwień — głównie kolory solid. Silna siła barwienia, czysty czerwony ton.",
    },
    "P425-948": {
        "nazwa": "HS Black",
        "en": "HS black. Full-strength counterpart of RT Transparent Black P420-904RT.",
        "pl": "Czerń HS. Ściemia światło i flop. Pełna moc odpowiednika RT Transparent Black (P420-904RT).",
    },
    "P425-950": {
        "nazwa": "HS Jet Black",
        "en": "Yellow-shade black, darker flop than P425-948.",
        "pl": "Czerń o żółtym odcieniu, ciemniejszy flop niż P425-948. Głębszy, cieplejszy cień niż standardowa czerń HS.",
    },
    "P425-954": {
        "nazwa": "HS Blue Green",
        "en": "Blue shade green.",
        "pl": "Zieleń o niebieskim odcieniu. Chłodna zieleń — przesuwa ton od żółtozielonego w stronę błękitu.",
    },
    "P425-956": {
        "nazwa": "HS Super Blue",
        "en": "Mid-shade blue with green face and red tone flop.",
        "pl": "Niebieski środkowy z zielonym światłem (face) i czerwonym flopem. Na świetle chłodniejszy, w cieniu cieplejszy.",
    },
    "P425-957": {
        "nazwa": "HS Fast Blue",
        "en": "High strength blue. Full-strength counterpart of RT Deep Blue P420-910RT.",
        "pl": "Wysokowydajny niebieski HS. Pełna moc odpowiednika RT Deep Blue (P420-910RT).",
    },
    "P425-971": {
        "nazwa": "HS Brilliant Red",
        "en": "Clean yellow tone red.",
        "pl": "Czysta czerwień o żółtym tonie. Ciepła, jaskrawa czerwień (w stronę pomarańczu), bez brudzenia flopu.",
    },
    "P425-984": {
        "nazwa": "HS Medium Fine Aluminium",
        "en": "Fine bright metallic with darker flop than P425-986.",
        "pl": "Drobny, jasny metalik z ciemniejszym flopem niż P425-986. Rozjaśnia światło, pogłębia cień względem średniego aluminium.",
    },
    "P425-985": {
        "nazwa": "HS Fine Aluminium",
        "en": "Fine metallic with a dark face and light flop.",
        "pl": "Drobny metalik z ciemnym światłem (face) i jasnym flopem. Drobne ziarno: ciemniejszy na wprost, jaśniejszy w cieniu.",
    },
    "P425-986": {
        "nazwa": "HS Medium Aluminium",
        "en": "Medium metallic with a darker flop than P425-985.",
        "pl": "Średni metalik z ciemniejszym flopem niż P425-985. Grubsze ziarno niż Fine — ciemniejszy cień.",
    },
    "P425-987": {
        "nazwa": "Medium Coarse Aluminium",
        "en": "Medium metallic with a darker flop than P425-985.",
        "pl": "Średnio grube aluminium z ciemniejszym flopem niż P425-985. Wyraźniejsze ziarno, ciemniejszy cień.",
    },
    "P425-988": {
        "nazwa": "HS Coarse Aluminium",
        "en": "Brighter face, darker flop than P425-987.",
        "pl": "Grube aluminium: jaśniejsze światło (face), ciemniejszy flop niż P425-987. Mocniejszy błysk ziarna, głębszy cień.",
    },
    "P425-989": {
        "nazwa": "HS Very Coarse Aluminium",
        "en": "Very coarse, bright aluminium with a dark flop.",
        "pl": "Bardzo grube, jasne aluminium z ciemnym flopem. Duże ziarno, silny błysk na świetle, głęboki cień.",
    },
    "P425-991": {
        "nazwa": "Fine Satin Aluminium",
        "en": "Fine aluminium. Darker face and lighter flop than P425-984.",
        "pl": "Drobne aluminium satynowe. Ciemniejsze światło i jaśniejszy flop niż P425-984. Uspokaja błysk, rozjaśnia cień.",
    },
    "P425-992": {
        "nazwa": "HS Shining Coarse Aluminium",
        "en": "Medium bright metallic with a darker flop than P425-984.",
        "pl": "Średnio jasny, błyszczący grubszy metalik z ciemniejszym flopem niż P425-984.",
    },
    "P425-998": {
        "nazwa": "HS Coarse Silver Dollar Aluminium",
        "en": "Bright coarse aluminium. Cleaner face and darker flop than P425-992.",
        "pl": "Jasne grube aluminium typu silver dollar. Czystsze światło i ciemniejszy flop niż P425-992.",
    },
    "P425-EB02": {
        "nazwa": "KONWERTER BAZY DO KOMÓR SILNIKA",
        "en": "Engine-bay base converter. Not a colour toner.",
        "pl": "Konwerter bazy do komór silnika — zmienia bazę pod aplikację w komorze silnika. Nie jest tonerem kolorystycznym.",
    },
    "P426-HE02": {
        "nazwa": "Blue Frost",
        "en": "Used in metallic colours to add yellow to the face and light blue tone to the flop.",
        "pl": "W metalikach dodaje żółć na świetle (face) i jasnoniebieski ton na flopie. Koryguje flop w stronę chłodnego błękitu.",
    },
    "P426-HE03": {
        "nazwa": "Graphite Flake",
        "en": "Subtle blue tone on face, lightens flop.",
        "pl": "Subtelny niebieski ton na świetle (face), rozjaśnia flop. Grafitowe ziarno — uspokaja i rozjaśnia cień.",
    },
    "P426-HE04": {
        "nazwa": "Gold Flash",
        "en": "Medium gold aluminium flake.",
        "pl": "Średni złoty płatek aluminiowy. Dodaje złoty błysk ziarna (nie toner konwencjonalny).",
    },
    "P426-HE05": {
        "nazwa": "Orange Flash",
        "en": "Orange aluminium flake.",
        "pl": "Pomarańczowy płatek aluminiowy. Dodaje pomarańczowy refleks na ziarnie.",
    },
    "P426-HE07": {
        "nazwa": "Blue Flash",
        "en": "Organic blue coloured aluminium flake.",
        "pl": "Organiczny niebieski płatek aluminiowy. Barwione ziarno — niebieski błysk metaliku.",
    },
    "P426-HE08": {
        "nazwa": "BLUE ALUMINIUM",
        "en": "Blue coloured aluminium flake.",
        "pl": "Niebieskie aluminium — barwiony płatek metaliczny, dodaje niebieski refleks na ziarnie.",
    },
    "P426-PP05": {
        "nazwa": "White Pearl",
        "en": "Clean white. Brighter face, darker flop than P426-PP06.",
        "pl": "Czysta biel perłowa. Jaśniejsze światło (face), ciemniejszy flop niż P426-PP06. Rozjaśnia perły, pogłębia cień względem Fine White Pearl.",
    },
    "P426-PP06": {
        "nazwa": "Fine White Pearl",
        "en": "Dirtier face and lighter flop than P426-PP05.",
        "pl": "Drobna biała perła. Brudniejsze światło i jaśniejszy flop niż P426-PP05. Drobniejsze ziarno, uspokaja kontrast światło/cień.",
    },
    "P426-PP07": {
        "nazwa": "Blue Pearl",
        "en": "Blue face, yellow flop. Coarser than P426-PP63.",
        "pl": "Niebieskie światło (face), żółty flop. Grubsza niż P426-PP63. Perła z travel: błękit na wprost, żółć w cieniu.",
    },
    "P426-PP08": {
        "nazwa": "Red Pearl",
        "en": "Red mica, coarser than P426-PP62.",
        "pl": "Czerwona mika, grubsza niż P426-PP62. Dodaje czerwony efekt perłowy, wyraźniejsze ziarno.",
    },
    "P426-PP09": {
        "nazwa": "Gold Pearl",
        "en": "Gold face, bluish tone flop.",
        "pl": "Złote światło (face), niebieskawy flop. Złota perła z chłodniejszym cieniem.",
    },
    "P426-PP10": {
        "nazwa": "Copper Pearl",
        "en": "Copper face, travels to dark copper tone on the flop.",
        "pl": "Miedziane światło (face), na flopie przechodzi w ciemną miedź. Perła z travel miedzianym.",
    },
    "P426-PP60": {
        "nazwa": "White Satin Pearl",
        "en": "Fine white flake.",
        "pl": "Drobne białe ziarno perłowe (satyna). Subtelna biała perła, uspokaja błysk.",
    },
    "P426-PP61": {
        "nazwa": "Fine Red Pearl",
        "en": "Interference red mica with a green flop.",
        "pl": "Interferencyjna czerwona mika z zielonym flopem. Czerwień na świetle, zieleń w cieniu.",
    },
    "P426-PP62": {
        "nazwa": "Fine Russet Pearl",
        "en": "Red mica. Finer than P426-PP08.",
        "pl": "Czerwona mika, drobniejsza niż P426-PP08. Russet perłowy o drobniejszym ziarnie.",
    },
    "P426-PP63": {
        "nazwa": "Fine Blue Pearl",
        "en": "Blue face, yellow flop. Finer than P426-PP07.",
        "pl": "Niebieskie światło, żółty flop. Drobniejsza niż P426-PP07. Ten sam travel co Blue Pearl, spokojniejsze ziarno.",
    },
    "P426-PP64": {
        "nazwa": "Medium Violet Pearl",
        "en": "Lilac face, green flop.",
        "pl": "Liliowe światło (face), zielony flop. Fioletowa perła z zielonym cieniem.",
    },
    "P426-PP65": {
        "nazwa": "Medium Green Pearl",
        "en": "Green face, reddish tone flop.",
        "pl": "Zielone światło (face), czerwonawy flop. Zielona perła z ciepłym cieniem.",
    },
    "P426-PP68": {
        "nazwa": "Orange Pearl",
        "en": "Clean orange face, green tone flop.",
        "pl": "Czyste pomarańczowe światło (face), zielony flop. Czysta pomarańcz perłowa z chłodniejszym cieniem.",
    },
    "P429-914": {
        "nazwa": "HS CLEAN BLUE VIOLET",
        "en": "Clean blue-shade violet HS toner.",
        "pl": "Czysty fiolet o niebieskim odcieniu (HS). Chłodny, czysty ton — korekta w stronę niebieskiego fioletu.",
    },
    "P429-917": {
        "nazwa": "HS GREEN GOLD",
        "en": "Green-gold HS toner.",
        "pl": "Złoto-zielony toner HS. Dodaje złocistą zieleń na świetle, ciepły zielonożółty ton.",
    },
    "P429-923": {
        "nazwa": "HS Bright Maroon",
        "en": "Mid-shade transparent maroon, dark flop.",
        "pl": "Transparentny bordo o środkowym odcieniu, ciemny flop. Ściemia i czerwieni w cieniu, bez silnego krycia.",
    },
    "P429-932": {
        "nazwa": "HS CLEAN ORGANIC ORANGE",
        "en": "Clean organic orange HS toner.",
        "pl": "Czysta organiczna pomarańcz HS. Nasycony, czysty ton pomarańczowy (nie tlenkowy).",
    },
    "P429-937": {
        "nazwa": "HS Pale Yellow",
        "en": "Green shade yellow with a green shade flop.",
        "pl": "Żółty o zielonym odcieniu, z zielonym flopem. Chłodna, blada żółć — rozjaśnia w stronę zieleni.",
    },
    "P429-961": {
        "nazwa": "HS Clean Magenta",
        "en": "Clean blue tone violet, darker flop than P425-921.",
        "pl": "Czysty fiolet o niebieskim tonie, ciemniejszy flop niż P425-921. Chłodna magenta, głębszy cień.",
    },
    "P429-967": {
        "nazwa": "HS Deep Angle Black",
        "en": "Yellow-shade black, darkest flop.",
        "pl": "Czerń o żółtym odcieniu, najciemniejszy flop. Najgłębszy cień spośród czerni 2K — ściemia kąt duży.",
    },
    "P429-972": {
        "nazwa": "HS Bright Amber",
        "en": "Bright orange used primarily in solid colours. Cleaner than P420-982 and P420-983.",
        "pl": "Jasna pomarańcz, głównie kolory solid. Czystsza niż P420-982 i P420-983.",
    },
    "P429-973": {
        "nazwa": "HS Bright Orange",
        "en": "Red shade orange.",
        "pl": "Pomarańcz o czerwonym odcieniu. Ciepła, czerwona pomarańcz do korekty tonu.",
    },
    "P429-976": {
        "nazwa": "HS Red Violet",
        "en": "Red violet HS. Full-strength counterpart of RT Burgundy P420-960RT.",
        "pl": "Fiolet czerwony HS. Pełna moc odpowiednika RT Burgundy (P420-960RT).",
    },
    "P429-980": {
        "nazwa": "HS Speed Red",
        "en": "Bright clean red, used primarily in solid colours above 20%.",
        "pl": "Jasna, czysta czerwień — głównie kolory solid, zwykle powyżej 20% udziału. Silna, czysta czerwień solid.",
    },
    "P429-981": {
        "nazwa": "Transparent Gold",
        "en": "Transparent gold toner.",
        "pl": "Transparentne złoto. Dodaje złoty ton bez silnego krycia; ociepla światło, słabiej buduje flop.",
    },
    "P433-XR10": {
        "nazwa": "Crystal Silver",
        "en": "Sparkle bright white effect, coarser appearance and brighter than P426-PP05.",
        "pl": "Iskrzący, jasny biały efekt Xirallic; grubsze ziarno i jaśniejszy niż P426-PP05.",
    },
    "P433-XR11": {
        "nazwa": "Sunbeam Gold",
        "en": "Sparkle bright gold effect, coarser appearance and brighter than P426-PP09.",
        "pl": "Iskrzący, jasny złoty efekt Xirallic; grubsze ziarno i jaśniejszy niż P426-PP09.",
    },
    "P433-XR12": {
        "nazwa": "Radiant Red",
        "en": "Sparkle bright red effect, coarser appearance and brighter than P426-PP08.",
        "pl": "Iskrzący, jasny czerwony efekt Xirallic; grubsze ziarno i jaśniejszy niż P426-PP08.",
    },
    "P433-XR13": {
        "nazwa": "Galaxy Blue",
        "en": "Sparkle bright blue effect, coarser appearance and brighter than P426-PP07.",
        "pl": "Iskrzący, jasny niebieski efekt Xirallic; grubsze ziarno i jaśniejszy niż P426-PP07.",
    },
    "P433-XR14": {
        "nazwa": "Stellar Green",
        "en": "Sparkle bright green effect, coarser appearance and brighter than P426-PP65.",
        "pl": "Iskrzący, jasny zielony efekt Xirallic; grubsze ziarno i jaśniejszy niż P426-PP65.",
    },
    "P433-XR15": {
        "nazwa": "Solaris Red",
        "en": "Sparkle bright magenta red effect, coarser appearance and brighter than P426-PP61.",
        "pl": "Iskrzący, jasny magenta-czerwony efekt Xirallic; grubsze ziarno i jaśniejszy niż P426-PP61.",
    },
    "P433-XR16": {
        "nazwa": "Fireside Copper",
        "en": "Sparkle bright copper effect, coarser appearance and brighter than P426-PP10.",
        "pl": "Iskrzący, jasny miedziany efekt Xirallic; grubsze ziarno i jaśniejszy niż P426-PP10.",
    },
    "P433-XR17": {
        "nazwa": "Cosmic Turquoise",
        "en": "Sparkle bright unique marine blue flake pigment.",
        "pl": "Iskrzący, unikalny morski błękit (turkus) — płatek Xirallic o wyraźnej iskrze.",
    },
    "P433-XR18": {
        "nazwa": "Amethyst Dream",
        "en": "Sparkle bright violet effect, coarser appearance and brighter than P426-PP64.",
        "pl": "Iskrzący, jasny fioletowy efekt Xirallic; grubsze ziarno i jaśniejszy niż P426-PP64.",
    },
    "P434-CS31": {
        "nazwa": "Autumn Mystery",
        "en": "Special effect orange silica flake that creates a unique red to gold to bronze to green colour travel.",
        "pl": "Efektowy pomarańczowy płatek krzemionkowy Colorstream: unikalny travel czerwony → złoty → brąz → zieleń.",
    },
    "P434-CS32": {
        "nazwa": "Viola Fantasy",
        "en": "Special effect white silica flake that creates a unique violet to silver to green to blue colour travel.",
        "pl": "Efektowy biały płatek krzemionkowy Colorstream: unikalny travel fiolet → srebro → zieleń → błękit.",
    },
    "P434-CS33": {
        "nazwa": "Arctic Fire",
        "en": "Special effect silica flake that creates a unique colour travel from subtle turquoise through brilliant silver to red.",
        "pl": "Efektowy płatek krzemionkowy Colorstream: travel od subtelnego turkusu przez błyszczące srebro do czerwieni.",
    },
    "P434-CS34": {
        "nazwa": "Tropic Sunrise",
        "en": "Special effect silica flake that creates a unique colour travel from green to silver to reddish orange.",
        "pl": "Efektowy płatek krzemionkowy Colorstream: travel zieleń → srebro → czerwonawa pomarańcz.",
    },
    "P434-CS35": {
        "nazwa": "Lapis Sunlight",
        "en": "Special effect silica flake that creates a unique colour travel from gold to green to blue.",
        "pl": "Efektowy płatek krzemionkowy Colorstream: travel złoto → zieleń → błękit.",
    },
    "P435-GF37": {
        "nazwa": "Silver Glass",
        "en": "Silver metal-coated glass flakes, used to create bright colours with intense sparkle and flare. The effect is particularly evident in bright sunlight.",
        "pl": "Srebrne płatki szkła pokryte metalem — jasne kolory z intensywną iskrą i flare. Efekt szczególnie widoczny w ostrym słońcu.",
    },
    "P440-FX20": {
        "nazwa": "CHROMAFLAIR CYAN TO PURPLE",
        "en": "Colour shifting flake. Colour shifts from cyan through purple.",
        "pl": "Płatek zmieniający barwę (ChromaFlair): travel cyjan → fiolet. Dodaje kątowe przesunięcie koloru, nie krycie.",
    },
    "P440-FX21": {
        "nazwa": "CHROMAFLAIR SILVER TO GREEN",
        "en": "Colour shifting flake. Colour shifts from silver through green.",
        "pl": "Płatek zmieniający barwę (ChromaFlair): travel srebro → zieleń.",
    },
    "P440-FX22": {
        "nazwa": "CHROMAFLAIR GREEN TO PURPLE",
        "en": "Colour shifting flake. Colour shifts from green through purple.",
        "pl": "Płatek zmieniający barwę (ChromaFlair): travel zieleń → fiolet.",
    },
    "P440-FX23": {
        "nazwa": "CHROMAFLAIR BLUE TO RED",
        "en": "Colour shifting flake. Colour shifts from blue through red.",
        "pl": "Płatek zmieniający barwę (ChromaFlair): travel błękit → czerwień.",
    },
    "P440-FX24": {
        "nazwa": "CHROMAFLAIR MAGENTA TO GOLD",
        "en": "Colour shifting flake. Colour shifts from magenta through gold.",
        "pl": "Płatek zmieniający barwę (ChromaFlair): travel magenta → złoto.",
    },
    "P440-FX25": {
        "nazwa": "CHROMAFLAIR GOLD TO SILVER",
        "en": "Colour shifting flake. Colour shifts from gold through silver.",
        "pl": "Płatek zmieniający barwę (ChromaFlair): travel złoto → srebro.",
    },
    "P440-FX26": {
        "nazwa": "CHROMAFLAIR RED TO GOLD",
        "en": "Colour shifting flake. Colour shifts from red through gold.",
        "pl": "Płatek zmieniający barwę (ChromaFlair): travel czerwień → złoto.",
    },
    "P440-FX51": {
        "nazwa": "Silver Flair",
        "en": "Exhibits a unique rainbow multi coloured effect, particularly in silver colours under intense light source.",
        "pl": "Tęczowy, wielobarwny efekt (rainbow), szczególnie w srebrnych kolorach przy intensywnym świetle.",
    },
    "P440-LM01": {
        "nazwa": "LIQUID METAL SUPER FINE",
        "en": "Vacuumized metal flakes with a unique optical effect similar to a molten metal appearance.",
        "pl": "Próżniowe płatki metalu (liquid metal) o efekcie stopionego metalu. Bardzo drobne ziarno, lustrzany połysk.",
    },
    "P450-EC50": {
        "nazwa": "BRILLIANT RED",
        "en": "Brilliant red effect / toner.",
        "pl": "Jaskrawa czerwień (toner EC). Dodaje czysty, intensywny czerwony ton.",
    },
    "VM4370": {
        "nazwa": "Super Fine Liquid Metal",
        "en": "Vacuumized metal flakes that have a unique optical effect similar to a molten metal appearance.",
        "pl": "Próżniowe płatki metalu — unikalny efekt optyczny jak stopiony metal. Bardzo drobne ziarno, lustrzany połysk.",
    },
    "VM4987": {
        "nazwa": "Cyan to Purple",
        "en": "Colour shifting flake. Colour shifts from cyan through purple.",
        "pl": "Płatek zmieniający barwę: travel cyjan → fiolet.",
    },
    "VM4988": {
        "nazwa": "Silver to Green",
        "en": "Colour shifting flake. Colour shifts from silver through green.",
        "pl": "Płatek zmieniający barwę: travel srebro → zieleń.",
    },
    "VM4989": {
        "nazwa": "Green to Purple",
        "en": "Colour shifting flake. Colour shifts from green through purple.",
        "pl": "Płatek zmieniający barwę: travel zieleń → fiolet.",
    },
    "VM4990": {
        "nazwa": "Blue to Red",
        "en": "Colour shifting flake. Colour shifts from blue through red.",
        "pl": "Płatek zmieniający barwę: travel błękit → czerwień.",
    },
    "VM4991": {
        "nazwa": "Magenta to Gold",
        "en": "Colour shifting flake. Colour shifts from magenta through gold.",
        "pl": "Płatek zmieniający barwę: travel magenta → złoto.",
    },
    "VM4994": {
        "nazwa": "Gold to Silver",
        "en": "Colour shifting flake. Colour shifts from gold through silver.",
        "pl": "Płatek zmieniający barwę: travel złoto → srebro.",
    },
    "VM4995": {
        "nazwa": "Red to Gold",
        "en": "Colour shifting flake. Colour shifts from red through gold.",
        "pl": "Płatek zmieniający barwę: travel czerwień → złoto.",
    },
}


def _norm(code: str) -> str:
    return "".join(str(code).split()).upper()


def lookup_tint(code: str) -> dict[str, str] | None:
    n = _norm(code)
    hit = TINT.get(n)
    if hit:
        return hit
    if n.endswith("RT"):
        return TINT.get(n[:-2])
    return TINT.get(n + "RT")


def apply_autocolor_tint(rows: list[dict]) -> None:
    """Nadpisuje opisy Autocolor polskim tekstem technicznym; nazwy katalogowe EN zostają."""
    for rec in rows:
        if rec.get("system") != "AUTOCOLOR":
            continue
        hit = lookup_tint(rec.get("nr_pigmentu", "")) or lookup_tint(
            rec.get("nr_bazowy", "")
        )
        if not hit:
            rec.setdefault("opis_en", rec.get("opis") or "")
            rec.setdefault("opis_dzialania_pl", rec.get("opis") or "")
            continue
        rec["opis_en"] = hit["en"]
        rec["opis"] = hit["pl"]
        rec["opis_dzialania_pl"] = hit["pl"]
        rec["procedura_dobarwiania"] = hit["pl"]
        clean_name = hit.get("nazwa") or ""
        if clean_name:
            rec["nazwa_pdf"] = clean_name
            # Zostaw polskie nazwy z katalogu ODS (regulatory itd.)
            if rec.get("zrodlo_nazwy") == "PDF_AUTOCOLOR":
                rec["nazwa"] = clean_name
            elif not rec.get("nazwa"):
                rec["nazwa"] = clean_name
