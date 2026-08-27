# Audyt po implementacji (2026-08-27)

## Wynik smoke testów

- Wszystkie strony HTML/PHP: **HTTP 200**
- `robots.txt`, `sitemap.xml`, CSS, JS, Bootstrap: **200**
- API formularza demo: **200** + JSON `ok:true` (po poprawce mbstring)
- Index: 1× H1, title, description, canonical, OG, Schema.org — OK

## Problemy znalezione i naprawione

1. **`mb_strlen` niedostępne** w domyślnym PHP Windows → polyfill `sda_len` / `sda_cut` w `contact-demo.php`
2. Assety przeniesione do **`public/assets`** (wymagane przez `php -S -t public`)
3. Usunięte zbędne **inline styles** na stronach prawnych / doborze lakieru
4. Preload fontów dopiero po pobraniu plików `.woff2`
5. **`config/site.php` bez `<?php`** → `require` zwracało `1`, błędy w kontakcie/stopce — dodano tag PHP

## Uwagi pozostałe (świadome, nieblokujące)

- CSRF w demo sprawdza format tokena (bez sesji) — przed produkcją: sesja + `hash_equals`
- Bootstrap ~227 KB CSS — akceptowalne; można później tree-shakować
- Placeholdery `[DO UZUPEŁNIENIA]` celowo widoczne
- Brak prawdziwych zdjęć — lokalne SVG
- Schema.org zawiera placeholdery adresu/telefonu — uzupełnić przed indeksacją produkcyjną

## Rozmiary (orientacyjnie)

| Zasób | Rozmiar |
|-------|---------|
| Własny CSS (suma) | ~23 KB |
| Własny JS (suma) | ~8 KB |
| Bootstrap CSS | ~227 KB |
| Bootstrap JS | ~79 KB |
| Fonty WOFF2 (4 pliki) | ~74 KB |

## Następne kroki

1. Przegląd wizualny w przeglądarce (mobile + desktop)
2. Uzupełnienie danych firmy
3. Akceptacja demo
4. Commit Git (na życzenie)
5. Push GitHub (na życzenie)
