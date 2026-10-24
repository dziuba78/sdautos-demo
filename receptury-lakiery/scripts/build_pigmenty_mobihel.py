# -*- coding: utf-8 -*-
"""Katalog sklepowy bazy MOBIHEL MIX (jakość BASE).

Lista kodów i grup: poradnik barwienia Helios Communicator
(MOBIHEL, BASE, wszystkie segmenty). Przy kodzie na stronie jest próbka,
bez zdania o działaniu. Opisy flip/flop są skrótem publicznej karty
TDS Base Mix, po polsku, pod kartę produktu. Ceny nie są uzupełnione.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "sklep" / "pigmenty-mobihel-base.json"
OUT_CSV = ROOT / "sklep" / "pigmenty-mobihel-base-prestashop.csv"

# sku, nazwa, kategoria, rodzina, ziarno, krotki, opis
ROWS: list[tuple] = [
    (
        "MIX 400", "Aluminium średnie", "aluminium", "aluminium", "średnie",
        "Średni płatek nieregularny. Jasne światło, średnio ciemny flop.",
        "Aluminium cornflake o średnim ziarnie. Na wprost jasne i błyszczące, z boku szare, średnio ciemne.",
    ),
    (
        "MIX 401", "Aluminium drobne", "aluminium", "aluminium", "drobne",
        "Drobny płatek nieregularny. Jasne światło, jaśniejszy flop niż MIX 400.",
        "Drobniejsze aluminium cornflake. Światło jasne, flop jasnoszary i bledszy niż przy średnim płatku.",
    ),
    (
        "MIX 402", "Aluminium grube", "aluminium", "aluminium", "grube",
        "Grubszy płatek nieregularny. Jasne światło i ciemny flop.",
        "Średnio grube aluminium cornflake. Na wprost jasne, z boku wyraźnie ciemniejsze.",
    ),
    (
        "MIX 403", "Aluminium ekstra drobne", "aluminium", "aluminium", "ekstra drobne",
        "Najdrobniejszy płatek. Szare, brudniejsze światło i bardzo jasny flop.",
        "Najdrobniejsze aluminium w tej grupie. Z boku bardzo jasne, na wprost brudnoszare.",
    ),
    (
        "MIX 404", "Aluminium ekstra grube", "aluminium", "aluminium", "ekstra grube",
        "Bardzo gruby, błyszczący płatek. Jasne światło, ciemny flop.",
        "Grube aluminium o regularniejszym kształcie. Silny błysk na wprost i ciemny bok.",
    ),
    (
        "MIX 405", "Aluminium drobne brylantowe", "aluminium", "aluminium", "drobne",
        "Drobny srebrny dolar. Bardzo jasny błysk i bardzo ciemny flop.",
        "Drobne aluminium sferyczne. Odbicie ostre, flop i kąt środkowy zostają ciemne.",
    ),
    (
        "MIX 406", "Aluminium grube brylantowe", "aluminium", "aluminium", "grube",
        "Gruby srebrny dolar. Wysoki połysk i bardzo ciemny flop.",
        "Grubsze aluminium sferyczne. Szeroka, jasna strefa odbicia i ciemny bok.",
    ),
    (
        "MIX 407", "Aluminium drobne jasne", "aluminium", "aluminium", "drobne",
        "Cienki płatek. Jasne światło i średnio jasny, szary flop.",
        "Drobne aluminium o jasnoszarym flopie. Rozjaśnia bok bez mocnego brylantowego błysku.",
    ),
    (
        "MIX 408", "Aluminium drobne brylant jasny", "aluminium", "aluminium", "drobne",
        "Drobny płatek o wysokim brylancie i jasnym flopie.",
        "Daje jasny błysk na wprost i jasny bok. Flop bledszy niż przy MIX 405.",
    ),
    (
        "MIX 409", "Aluminium jedwabiste drobne", "aluminium", "aluminium", "ekstra drobne",
        "Bardzo drobny, regularny płatek. Jasny błysk i ciemny flop.",
        "Drobniejsze niż MIX 405. Silny kontrast: jasne światło, ciemny bok.",
    ),
    (
        "MIX 410", "Aluminium jedwabiste grubsze", "aluminium", "aluminium", "drobne",
        "Drobny regularny płatek, grubszy niż MIX 409. Jasny błysk i ciemny flop.",
        "Mniejsze ziarno niż MIX 406. Jasne odbicie przechodzi w ciemny bok.",
    ),
    (
        "MIX 411", "Aluminium premium drobne", "aluminium", "aluminium", "ekstra drobne",
        "Bardzo drobny srebrny dolar, około 7 µm. Drobniejszy niż MIX 409.",
        "Regularny, bardzo drobny płatek premium. Jasne światło i mocny kontrast z ciemnym flopem.",
    ),
    (
        "MIX 412", "Aluminium premium grube", "aluminium", "aluminium", "grube",
        "Gruby srebrny dolar premium. Wysoki połysk, flop ciemniejszy niż MIX 406.",
        "Grube aluminium sferyczne. Jasna strefa odbicia, bok błyszczący, ale ciemniejszy niż przy MIX 406.",
    ),
    (
        "MIX 413", "Szkło srebrzone", "aluminium", "efekt", "grube",
        "Płatek szklany pokryty srebrem. Iskrzący błysk z ciepłym odcieniem.",
        "Przezroczysty efekt interferencyjny. Dodaje bardzo jasny, iskrzący połysk, z ciepłym złotawym tonem.",
    ),
    (
        "MIX 415", "Aluminium złote", "aluminium", "złoto", "drobne",
        "Drobne złote aluminium. Ciemny flop.",
        "Płatek pokryty tlenkiem żelaza, żółtozłoty pod każdym kątem. Do jasnych złotych kolorów, bok ciemnieje.",
    ),
    (
        "MIX 416", "Aluminium złotopomarańczowe", "aluminium", "złoto", "drobne",
        "Ziarno barwione tlenkiem żelaza. Iskrzący pomarańcz na wprost, ciemniejszy flop.",
        "Na kącie około 15° jasny, iskrzący pomarańcz. Przy 45° i z boku pomarańcz jest ciemniejszy.",
    ),
    (
        "MIX 417", "Aluminium niebieskie", "aluminium", "niebieski", "drobne",
        "Regularny płatek w niebieskim kolorze.",
        "Aluminium o czystym niebieskim świetle i niebieskim flopie.",
    ),
    (
        "MIX 300", "Biel efektowa", "flop", "biel", "",
        "Do metalików i pereł. Światło żółknie, flop robi się mlecznoniebieski.",
        "Tylko kolory efektowe. W dużej ilości niebieski bok znika, więc udział zwykle zostaje poniżej połowy mieszanki.",
    ),
    (
        "MIX 301", "Biel", "flop", "biel", "",
        "Rozjaśnia solidy. W metaliku do około 5% rozjaśnia flop i brudzi światło.",
        "Główne rozjaśnienie kolorów bez efektu. Większy dodatek w metaliku daje mleczność i tłumi widoczność ziarna.",
    ),
    (
        "MIX 302", "Biel o wyższej mocy", "flop", "biel", "",
        "Mocniejsza biel niż MIX 301, lepsze krycie.",
        "Ten sam kierunek co MIX 301, wyższe stężenie. Do solidów, gdy biel ma kryć mocniej.",
    ),
    (
        "MIX 495", "Dodatek flopu", "flop", "flop", "",
        "Ściemnia i brudzi światło, rozjaśnia bok. Ziarno wygląda grubiej.",
        "Tylko kolory efektowe, zwykle do 20%. W słońcu twarz ciemnieje, w cieniu blednie. Bok jaśnieje bez mlecznego brudu białej. Głębokiego flopu pod bardzo ostrym kątem rozjaśnia słabo.",
    ),
    (
        "MIX 420", "Perła biała gruba", "perly", "biel", "grube",
        "Gruba srebrnobiała perła. Grubsza niż MIX 421 i MIX 422.",
        "Biały perłowy połysk o średnio dużym ziarnie. Światło i bok zostają srebrnobiałe.",
    ),
    (
        "MIX 421", "Perła biała drobna", "perly", "biel", "drobne",
        "Drobna srebrnobiała perła. Drobniejsza niż MIX 420, grubsza niż MIX 422.",
        "Jedwabisty biały połysk. Do jaśniejszych pereł, gdy MIX 420 jest za gruba.",
    ),
    (
        "MIX 422", "Perła biała ekstra drobna", "perly", "biel", "ekstra drobne",
        "Najdrobniejsza biała perła z tej trójki.",
        "Bardzo drobne ziarno, srebrnobiałe światło i blady bok.",
    ),
    (
        "MIX 430", "Perła żółta", "perly", "żółty", "średnie",
        "Żółta perła o średnim ziarnie. Żółte światło, niebieskawy kąt środkowy.",
        "W efekcie daje żółty błysk. Na białym podkładzie bok wpada w błękit, na czarnym w brudną żółć.",
    ),
    (
        "MIX 440", "Perła miedziana", "perly", "miedź", "średnie",
        "Kryjąca perła miedziana o średnim ziarnie.",
        "Ciepły miedziany połysk. Światło jasnoczerwone, bok zostaje miedziany.",
    ),
    (
        "MIX 450", "Perła czerwona drobna", "perly", "czerwony", "drobne",
        "Drobna czerwona perła do malinowego błysku.",
        "W kolorach efektowych dodaje malinowy połysk. Ziarno drobniejsze niż MIX 451.",
    ),
    (
        "MIX 451", "Perła czerwona gruba", "perly", "czerwony", "grube",
        "Grubsza czerwona perła niż MIX 450. Miedzianoczerwony błysk.",
        "Do efektów, w których czerwona perła ma być grubsza i bardziej miedziana.",
    ),
    (
        "MIX 452", "Perła czerwonobrązowa", "perly", "czerwony", "średnie",
        "Przezroczysta czerwona perła o średnim ziarnie.",
        "Na białym podkładzie daje zielonkawy odcień, na czarnym brudnoczerwony flop.",
    ),
    (
        "MIX 453", "Perła bordowa", "perly", "czerwony", "średnie",
        "Kryjąca czerwona perła, bardziej niebieska niż MIX 450.",
        "Przesuwa czerwoną perłę w stronę bordo i błękitu.",
    ),
    (
        "MIX 460", "Perła fioletowa", "perly", "fiolet", "średnie",
        "Przezroczysta fioletowa perła o średnim ziarnie.",
        "Na białym podkładzie wpada w zieleń, na czarnym w brudny fiolet.",
    ),
    (
        "MIX 461", "Perła fioletowo-zielona", "perly", "kolorstream", "średnie",
        "Colorstream. Przelew od fioletu przez srebro i zieleń do błękitu.",
        "Bardzo przezroczysta perła o mocnej zmianie koloru z kątem.",
    ),
    (
        "MIX 470", "Perła niebieska", "perly", "niebieski", "grube",
        "Średnio gruba niebieska perła. Niebieskozielone światło, jasnożółty bok.",
        "Na białym podkładzie flop żółknie, na czarnym zostaje zielononiebieski.",
    ),
    (
        "MIX 471", "Perła niebieska drobniejsza", "perly", "niebieski", "drobne",
        "Przezroczysta niebieska perła z czerwonym odcieniem. Drobniejsza niż MIX 470.",
        "Na białym podkładzie bok żółty, na czarnym brudnoniebieski.",
    ),
    (
        "MIX 472", "Perła niebieska ekstra drobna", "perly", "niebieski", "ekstra drobne",
        "Bardzo drobna niebieska perła z czerwonym odcieniem. Drobniejsza niż MIX 471.",
        "Na białym podkładzie flop żółty, na czarnym czerwononiebieski.",
    ),
    (
        "MIX 480", "Perła niebieskozielona", "perly", "zielony", "średnie",
        "Niebieskozielona perła o średnim ziarnie i żółtozielonym flopie.",
        "Chłodna zieleń na wprost, z boku żółknie.",
    ),
    (
        "MIX 481", "Perła zielona", "perly", "zielony", "drobne",
        "Przezroczysta zielona perła, drobniejsza niż MIX 480.",
        "Na białym podkładzie bok czerwienieje, na czarnym zostaje brudna zieleń.",
    ),
    (
        "MIX 500", "Xirallic biały", "perly", "xirallic", "grube",
        "Gruby biały ksyrallic. Wyższy połysk i bielszy ton niż MIX 420.",
        "Duży przezroczysty kryształ. Do efektów, w których biała perła ma iskrzyć mocniej.",
    ),
    (
        "MIX 501", "Xirallic żółty", "perly", "xirallic", "grube",
        "Gruby żółty ksyrallic.",
        "Na białym podkładzie flop wpada w błękit, na czarnym w brudną żółć.",
    ),
    (
        "MIX 502", "Xirallic miedziany", "perly", "xirallic", "grube",
        "Kryjący, gruby ksyrallic w kolorze miedzi.",
        "Miedziany błysk na świetle i z boku, mocniejszy niż klasyczna perła MIX 440.",
    ),
    (
        "MIX 503", "Xirallic czerwony", "perly", "xirallic", "grube",
        "Kryjący, gruby czerwony ksyrallic.",
        "Jasnoczerwony błysk na wprost i z boku.",
    ),
    (
        "MIX 504", "Xirallic niebieski", "perly", "xirallic", "grube",
        "Gruby przezroczysty niebieski ksyrallic.",
        "Na białym podkładzie bok żółknie, na czarnym zostaje zielononiebieski.",
    ),
    (
        "MIX 505", "Xirallic zielony", "perly", "xirallic", "grube",
        "Gruby przezroczysty zielony ksyrallic.",
        "Na białym podkładzie flop czerwienieje, na czarnym jest brudnozielony.",
    ),
    (
        "MP01", "Proszek Colorstream ciepły", "perly", "proszek", "drobne",
        "Przelew od czerwieni przez złoto i brąz do zieleni.",
        "Bardzo przezroczysty proszek. Do ciepłych, jesiennych i ciemnych kolorów z delikatną zmianą odcienia.",
    ),
    (
        "MP02", "Proszek Xirallic czerwony", "perly", "proszek", "drobne",
        "Czyste czerwone odbicie, zielony bok.",
        "Brylantowa perła proszkowa. Na wprost czysta czerwień, z boku zieleń.",
    ),
    (
        "MP03", "Proszek Colorstream turkus", "perly", "proszek", "drobne",
        "Przelew od turkusu przez srebrny brylant do metalicznej czerwieni.",
        "Bardzo przezroczysty proszek o mocnej zmianie koloru z kątem.",
    ),
    (
        "MP04", "Proszek Iriodin brąz", "perly", "proszek", "drobne",
        "Klasyczna perła z tlenkiem żelaza. Przelew z zieleni w czerwień.",
        "Brązowy odcień miki. Z kątem schodzi od zieleni do czerwieni.",
    ),
    (
        "MP05", "Proszek Xirallic biały drobny", "perly", "proszek", "ekstra drobne",
        "Perłowo-biały brylant o drobnej strukturze. Jedwabistszy niż MIX 500.",
        "Czystszy biały ton niż drobne perły MIX 421 i MIX 422.",
    ),
    (
        "MP06", "Proszek Iriodin zielony", "perly", "proszek", "drobne",
        "Zielona perła interferencyjna. Przelew z zieleni w czerwień, czystsza niż MIX 481.",
        "Do zielonego efektu, gdy klasyczna perła MIX 481 jest za brudna.",
    ),
    (
        "MP07", "Proszek Xirallic niebieskozielony", "perly", "proszek", "drobne",
        "Czysty przelew z niebieskiej zieleni w zieleń, wysoki połysk.",
        "Bardzo przezroczysty. Najczyściej pracuje w niebieskich kolorach.",
    ),
    (
        "MP08", "Proszek Colorstream złoto-błękit", "perly", "proszek", "drobne",
        "Przelew od złota przez srebrną zieleń do żywego błękitu.",
        "Bardzo przezroczysty proszek o mocnej zmianie odcienia z kątem.",
    ),
    (
        "MP09", "Proszek Iriodin złoto-czerwień", "perly", "proszek", "drobne",
        "Mika z tlenkiem żelaza i tytanu. Przelew ze złotej żółci w czerwień.",
        "Metaliczna perła proszkowa o ciepłym przelewie.",
    ),
    (
        "MP10", "Proszek Colorstream fiolet", "perly", "proszek", "drobne",
        "Przelew od fioletu przez srebrzystą szarość do zieleni i błękitu.",
        "Bardzo przezroczysty proszek. Bliski kierunkowi MIX 461, w formie proszku.",
    ),
    (
        "MP11", "Proszek Iriodin niebieski", "perly", "proszek", "drobne",
        "Niebieska perła interferencyjna. Przelew z błękitu w żółć, czystsza niż MIX 470.",
        "Do niebieskiego efektu, gdy klasyczna perła MIX 470 jest za brudna.",
    ),
    (
        "MP12", "Proszek perłowy", "perly", "proszek", "",
        "Pigment proszkowy z grupy Perła w poradniku MOBIHEL BASE.",
        "Kod jest na liście poradnika. Opublikowana karta TDS urywa opisy proszków na MP11, więc przelewu MP12 tu nie dopisuję.",
    ),
    (
        "MIX 308", "Żółcień zielonkawa", "pigmenty", "żółty", "",
        "Żółtozielony, z ciemnym żółtawym flopem.",
        "W niebieskich już kilka procent zabiera czerwień z boku: flop ciemnieje i schodzi w zieleń.",
    ),
    (
        "MIX 310", "Żółcień słoneczna", "pigmenty", "żółty", "",
        "Mocniejsza, lepiej kryjąca wersja MIX 311. Flop mocniejszy niż światło.",
        "Żółtozielony o wyższym stężeniu. W efektach zmiana z boku jest wyraźniejsza niż na wprost.",
    ),
    (
        "MIX 311", "Żółcień jasna", "pigmenty", "żółty", "",
        "Czysta, przezroczysta żółć o zielonym odcieniu. Bardziej transparentna niż MIX 310.",
        "Mały dodatek w metaliku daje zielonkawy flop, duży — żywo żółty bok.",
    ),
    (
        "MIX 312", "Żółcień czerwonawa", "pigmenty", "żółty", "",
        "Jasna, czysta żółć z czerwonym odcieniem.",
        "Głównie żółtopomarańczowe, zielone i żółtobrązowe. W efekcie tylko śladowo, żeby bok został jasnożółty.",
    ),
    (
        "MIX 313", "Żółcień", "pigmenty", "żółty", "",
        "Przezroczysta, czysta żółć z czerwonawym odcieniem.",
        "W metaliku mała ilość daje jasnożółty flop.",
    ),
    (
        "MIX 314", "Pomarańcz", "pigmenty", "pomarańcz", "",
        "Kryjący pomarańcz do czystych czerwieni i pomarańczy solid.",
        "Mały dodatek w kolorze efektowym rozjaśnia bok w stronę jasnego pomarańczu.",
    ),
    (
        "MIX 315", "Ochra", "pigmenty", "żółty", "",
        "Brudna żółć do jasnych żółci, beżów i brązów.",
        "W efekcie mała ilość daje mlecznożółty flop.",
    ),
    (
        "MIX 316", "Żółcień złocista", "pigmenty", "żółty", "",
        "Przezroczysty żółty tlenek. Ciemny flop, ciepły brązowo-złoty ton.",
        "Do efektów z brązowym połyskiem i beżów, zwłaszcza gdy bok ma zejść w zieleń. Duża transparentność ściemnia flop.",
    ),
    (
        "MIX 317", "Pomarańcz brylantowy", "pigmenty", "pomarańcz", "",
        "Czysty, przezroczysty pomarańcz z czerwonym odcieniem.",
        "Do czystych pomarańczy i czerwieni. Mała ilość daje żywy pomarańczowy bok.",
    ),
    (
        "MIX 320", "Czerwień miedziana przezroczysta", "pigmenty", "czerwony", "",
        "Czysta przezroczysta czerwień o brązowym odcieniu. Ciemny flop.",
        "W efektach buduje żywą miedź. Czystsza i bardziej żółta niż MIX 321.",
    ),
    (
        "MIX 321", "Czerwień miedziana", "pigmenty", "czerwony", "",
        "Przezroczysty tlenek czerwony do miedzianych efektów. Ciemny flop.",
        "Mniej żółta niż MIX 320. Bok zostaje ciemny, czerwonawo-miedziany.",
    ),
    (
        "MIX 322", "Czerwień cyklamen", "pigmenty", "czerwony", "",
        "Średnia czerwień z niebieskim odcieniem. Czyste światło, ciemnożółty flop.",
        "Głównie czyste czerwone solidy. W metaliku używana rzadko.",
    ),
    (
        "MIX 323", "Czerwień brązowa", "pigmenty", "czerwony", "",
        "Kryjąca, brudna czerwień brązowa do kości słoniowej, beżów i brązów.",
        "W efekcie tylko mało: mlecznoczerwony flop.",
    ),
    (
        "MIX 324", "Czerwień purpurowa", "pigmenty", "czerwony", "",
        "Przezroczysta czerwień o żółtym odcieniu. Czyste światło, ciemnożółty flop.",
        "Czystsza i bardziej żółta niż MIX 326. Do czerwonych efektów.",
    ),
    (
        "MIX 325", "Czerwień", "pigmenty", "czerwony", "",
        "Jasna, żywa czerwień z pomarańczowym odcieniem.",
        "Głównie czyste czerwone solidy. Mały dodatek w efekcie daje jasnoczerwony flop.",
    ),
    (
        "MIX 326", "Czerwień ciemna", "pigmenty", "czerwony", "",
        "Półtransparentna ciemna czerwień z brązem. W efekcie żółknie bok.",
        "Do średnich i ciemnych czerwieni. Światło czerwonobrązowe.",
    ),
    (
        "MIX 327", "Czerwień ciemna przezroczysta", "pigmenty", "czerwony", "",
        "Bardziej przezroczysta i nieco bardziej żółta niż MIX 326. Ciemny flop.",
        "Lepsza do metalików niż MIX 326, bo mniej kryje i głębiej ściemnia bok.",
    ),
    (
        "MIX 328", "Czerwień brylantowa", "pigmenty", "czerwony", "",
        "Żywa czerwień z niebieskim odcieniem.",
        "Z bielą albo aluminium daje czyste róże. Brudniejsza niż MIX 330, czystsza niż MIX 329.",
    ),
    (
        "MIX 329", "Bordo", "pigmenty", "czerwony", "",
        "Półtransparentny, czysty purpur. W efekcie bok bardziej czerwony niż światło.",
        "Do malinowego odcienia w solidach i metalikach.",
    ),
    (
        "MIX 330", "Róż", "pigmenty", "czerwony", "",
        "Przezroczysta czerwień o malinowym odcieniu.",
        "Z bielą albo srebrem daje żywy róż. Często w czystych czerwonych solidach.",
    ),
    (
        "MIX 331", "Fiolet", "pigmenty", "fiolet", "",
        "Czysty niebieski fiolet. Głęboki czerwononiebieski efekt.",
        "W niebieskich dodaje czerwieni, w czerwonych błękitu. W pozostałych buduje fiolet.",
    ),
    (
        "MIX 332", "Fiolet niebieski słabszy", "pigmenty", "fiolet", "",
        "Słabsza wersja MIX 331, ten sam kierunek.",
        "Do jasnych solidów i efektów, gdy fiolet ma być tylko lekką korektą.",
    ),
    (
        "MIX 341", "Błękit stalowy", "pigmenty", "niebieski", "",
        "Przezroczysty, brudny ciemny błękit z mocną czerwienią. W efekcie czerwony flop.",
        "Światło brudnoniebieskie, bok bladoczerwononiebieski.",
    ),
    (
        "MIX 342", "Błękit brylantowy", "pigmenty", "niebieski", "",
        "Bardzo czysty, przezroczysty ciemny błękit.",
        "W efekcie światło niebieskie, flop niebieski z lekką czerwienią. Dodaje czystości niebieskim.",
    ),
    (
        "MIX 343", "Błękit", "pigmenty", "niebieski", "",
        "Przezroczysty ciemny błękit o zielonym odcieniu. Stabilny na kącie.",
        "Gdy flop ma zostać niebieskozielony, a nie złamać się w fiolet.",
    ),
    (
        "MIX 344", "Błękit przezroczysty", "pigmenty", "niebieski", "",
        "Na wprost bardziej zielony niż MIX 343, flop łamie się w czerwonofiolet.",
        "Mały dodatek może zostawić niebieskozielony bok. Większy ostro schodzi we fiolet, mocniej niż MIX 341.",
    ),
    (
        "MIX 345", "Błękit królewski", "pigmenty", "niebieski", "",
        "Przezroczysty ciemny błękit o fioletowym odcieniu.",
        "W efektach daje mocno czerwony, fioletowy flop.",
    ),
    (
        "MIX 346", "Błękit oceanu", "pigmenty", "niebieski", "",
        "Brylantowy przezroczysty błękit. Zielone światło, wyraźnie czerwony flop.",
        "Do metalików, w których kąt ma zmienić błękit z zieleni w czerwień.",
    ),
    (
        "MIX 351", "Zieleń ciemna", "pigmenty", "zielony", "",
        "Przezroczysta zieleń o niebieskim odcieniu. Ciemny flop, podobny pod każdym kątem.",
        "Chłodna zieleń do solidów i efektów, bez mocnego zejścia w żółć.",
    ),
    (
        "MIX 352", "Zieleń", "pigmenty", "zielony", "",
        "Przezroczysta zieleń o żółtym odcieniu. Bardzo jasny, żywy zielony flop.",
        "Żółtozielony bok trudno później zabrać. Do jasnych, czystych zieleni.",
    ),
    (
        "MIX 361", "Czerń głęboka", "pigmenty", "czerń", "",
        "Półtransparentna czerń o brązowożółtym odcieniu. W efekcie ciemny flop.",
        "Gdy w kolorze nie ma bieli, pogłębia ton. Bok schodzi w ciemną, żółtawą czerń.",
    ),
    (
        "MIX 362", "Czerń niebieskawa", "pigmenty", "czerń", "",
        "Czerń o niebieskim odcieniu. W efekcie nie ściemnia boku.",
        "Chłodniejsza niż MIX 361. Flop zostaje czarnoszary, bez głębokiego załamania.",
    ),
    (
        "MIX 363", "Czerń słabsza", "pigmenty", "czerń", "",
        "Słabsza pigmentacja niż MIX 362. Ten sam chłodny kierunek.",
        "Ściemnia i szarzeje kolor, gdy pełna czerń byłaby za mocna.",
    ),
    (
        "MIX 364", "Czerń brązowa", "pigmenty", "czerń", "",
        "Głęboka czerń o brązowym odcieniu. Ciemniejsza niż MIX 361, bardzo ciemny flop.",
        "Do ciemnych kolorów, w których bok ma zejść mocniej niż przy MIX 361.",
    ),
    (
        "MIX 365", "Czerń antracyt", "pigmenty", "czerń", "",
        "Półtransparentny grafit tylko do efektów. Miękki, niebieskawy flop.",
        "Daje dymny, jedwabisty wygląd i wrażenie przygaszonego, starszego lakieru.",
    ),
    (
        "MIX 366", "Czerń głęboka ekstra", "pigmenty", "czerń", "",
        "Głęboka czerń o niebieskim odcieniu. Flop ciemniejszy niż światło.",
        "Gdy MIX 361 i MIX 364 nie dają dość głębokiej czerni.",
    ),
    (
        "MIX 367", "Czerń super głęboka", "pigmenty", "czerń", "",
        "Głęboka czerń o neutralnym szaroniebieskim odcieniu.",
        "Do nasyconych czerni, bez żółtego zaciągnięcia MIX 361.",
    ),
    (
        "MIX 368", "Czerń głęboka neutralna", "pigmenty", "czerń", "",
        "Czerń o bardziej neutralnym odcieniu. Mniej czerwona niż MIX 361.",
        "Z boku mniej żółknie niż MIX 361.",
    ),
    (
        "MIX 369", "Czerń ekstra", "pigmenty", "czerń", "",
        "Nasycona, głęboka czerń. W efekcie neutralny szarozielony bok, bez czerwieni.",
        "Do głębokich czerni solid i efekt. Flop zostaje głęboki.",
    ),
    (
        "MIX 822", "Czerwień malinowa", "pigmenty", "czerwony", "",
        "Nasycona, czysta, przezroczysta czerwień z lekkim błękitem.",
        "Światło czerwone, flop niebieskoczerwony.",
    ),
    (
        "MIX 825", "Czerwień o wyższej mocy", "pigmenty", "czerwony", "",
        "Mocniejszy odpowiednik MIX 325. Nie do kolorów efektowych.",
        "Do czystych czerwonych solidów, gdy MIX 325 jest za słaba.",
    ),
    (
        "MIX 828", "Magenta", "pigmenty", "fiolet", "",
        "Przezroczysta, nasycona magenta. Światło i flop niebieskoczerwone.",
        "Przesuwa kolor w czystą magentę, bez brązowego przytłumienia.",
    ),
]


def slugify(sku: str, name: str) -> str:
    raw = f"{sku} {name}".lower()
    for src, dst in (
        ("ł", "l"), ("ś", "s"), ("ć", "c"), ("ń", "n"), ("ó", "o"),
        ("ą", "a"), ("ę", "e"), ("ż", "z"), ("ź", "z"),
    ):
        raw = raw.replace(src, dst)
    return re.sub(r"[^a-z0-9]+", "-", raw).strip("-")


def main() -> None:
    skus = [row[0] for row in ROWS]
    if len(skus) != len(set(skus)):
        raise SystemExit("zduplikowany kod")
    products = []
    for i, row in enumerate(ROWS, start=1):
        sku, name, cat, rodzina, ziarno, short, description = row
        products.append(
            {
                "id": "mh-" + sku.lower().replace(" ", "-"),
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
    payload = {
        "sklep": "autocolor.pl",
        "przeznaczenie": "Dane katalogowe produktów do sklepu autocolor.pl.",
        "system": "MOBIHEL MIX BASE",
        "zrodlo_lista": "Helios Refinish Communicator, poradnik barwienia, system MOBIHEL, jakość BASE",
        "zrodlo_opisy": "Karta TDS MOBIHEL Base Mix: charakterystyka światła i flopu, skrócona po polsku",
        "uwaga": (
            "Lista kodów i grup pochodzi z otwartego poradnika barwienia. "
            "Przy kodzie na stronie jest próbka koloru, bez zdania o działaniu. "
            "Opisy mówią, jak składnik zmienia światło i flop. "
            "Ceny i stany magazynowe nie są uzupełnione. "
            "MP12 jest na liście poradnika; karta TDS nie podaje jego przelewu."
        ),
        "image_placeholder": "/assets/images/products/product-placeholder.svg",
        "image_dir": "public/assets/images/pigmenty",
        "categories": [
            {"id": "aluminium", "name": "Aluminium"},
            {"id": "flop", "name": "Modyfikatory flopa"},
            {"id": "perly", "name": "Perła"},
            {"id": "pigmenty", "name": "Pigmenty"},
        ],
        "products": products,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    cat_name = {c["id"]: c["name"] for c in payload["categories"]}
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        writer.writerow([
            "Active",
            "Name",
            "Categories",
            "Price tax excluded",
            "Reference",
            "Short description",
            "Description",
            "Visibility",
        ])
        for product in products:
            category = f"Pigmenty MOBIHEL BASE/{cat_name[product['category']]}"
            description = f"<p>{product['description']}</p>"
            writer.writerow([
                1,
                product["name"],
                category,
                "",
                product["sku"],
                product["short"],
                description,
                "both",
            ])
    print(f"{len(products)} -> {OUT_JSON}")
    print(f"{len(products)} -> {OUT_CSV}")


if __name__ == "__main__":
    main()
