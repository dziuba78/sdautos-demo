# Integracja z PrestaShop 9 (plan)

Demo **nie** integruje się jeszcze z PrestaShop. Poniżej rekomendowana ścieżka bez przepisywania frontu.

## Cele docelowe

- produkty, kategorie, ceny, stany magazynowe,
- zdjęcia i warianty,
- koszyk i zamówienia.

## Rekomendowane podejścia

### A) PrestaShop jako sklep + witryna marketingowa osobno (proste)

- Obecna witryna zostaje landingiem / contentem.
- Sklep PS9 pod subdomeną lub ścieżką (`sklep.sdautos…` / `/sklep`).
- Header ma już slot koszyka prowadzący do katalogu — podmienić na URL PS.

### B) Headless / API (elastyczne)

- Front pobiera produkty z Webservice / API PrestaShop.
- Zastąpić `config/products.demo.json` klientem API.
- Zachować karty produktów i filtry; dodać cenę, dostępność, ID PS.

### C) Motyw PrestaShop oparty o ten design system (spójność brandu)

- Przenieść tokeny CSS i komponenty do motywu PS9.
- Najwięcej pracy frontowej, pełna spójność UX sklepu.

## Mapowanie danych (demo → PS)

| Demo JSON | PrestaShop |
|-----------|------------|
| `id` / `slug` | `id_product` / `link_rewrite` |
| `name` | `name` |
| `category` | `id_category` / kategorie |
| `short` | `description_short` |
| `image` | image API / URL generowany |

## Bezpieczeństwo integracji

- Klucz API wyłącznie po stronie serwera (`.env`), nigdy w JS przeglądarki.
- Ograniczyć uprawnienia klucza Webservice do minimum.
- Cache’ować odpowiedzi katalogu (TTL), nie odpytywać API przy każdym odświeżeniu bez potrzeby.

## Etapy wdrożenia (propozycja)

1. Uzupełnić katalog w PS9 (kategorie jak w demo).
2. Wybrać model A/B/C.
3. Podmienić źródło produktów.
4. Podłączyć koszyk / checkout w PS.
5. Przenieść CTA „Zobacz produkt” na karty PS.
6. Testy synchronizacji stanów i cen.
