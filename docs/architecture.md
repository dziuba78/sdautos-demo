# Architektura SDAUTOS demo

## Cel architektury

Lekka, czytelna witryna marketingowa z katalogiem demo i miejscem na narzędzie doboru koloru, możliwa do utrzymania bez ciężkiego frameworka JS, z jasną ścieżką do PrestaShop 9.

## Warstwy

1. **Prezentacja** — strony PHP w `public/` + partials w `includes/`
2. **Konfiguracja** — `config/site.php`, `config/products.demo.json`
3. **Assety** — `public/assets` (CSS, JS, obrazy, ikony)
4. **Vendor** — Bootstrap 5 lokalnie (`public/vendor/bootstrap`)
5. **API demo** — `public/api/contact-demo.php` (bez wysyłki e-mail)
6. **Dokumentacja** — `docs/`

## Dlaczego PHP includes?

Bez bundlera (Webpack/Vite) partials PHP dają:

- jeden header/footer,
- poprawne SEO (HTML renderowany po stronie serwera),
- działanie bez JS dla treści,
- prosty hosting (Apache/Nginx + PHP).

## Przepływ strony głównej

Hero → Oferta → Produkty → Dobór lakieru → Realizacje → Dlaczego SDAUTOS → O nas → Kontakt

## Produkty

Źródło demo: JSON. Karty renderowane w PHP. Filtrowanie kategorii w JS.

Docelowo: zamiana źródła na API / feed PrestaShop 9 bez przepisywania layoutu kart.

## Dobór lakieru

UI + wyłączone pola + dokumentacja procesu. Interfejs gotowy pod podłączenie bazy kolorów (własnej lub zewnętrznej).

## Bezpieczeństwo (demo → produkcja)

| Obszar | Demo | Produkcja |
|--------|------|-----------|
| Formularz | walidacja FE/BE, honeypot, brak maila | SMTP, rate limit, CSRF sesyjny |
| Sekrety | `.env.example`, brak sekretów w JS | `.env` poza repo |
| XSS | `htmlspecialchars` / `strip_tags` | utrzymać escaping |
| SQL | brak DB | prepared statements |

## Wydajność

- lokalny Bootstrap (bez zbędnych pluginów),
- lazy-loading obrazów poza hero,
- SVG placeholdery (lekkie),
- CSS podzielony (tokens / main / responsive),
- JS modularny, `defer` / `type="module"`,
- ograniczone fonty (swap).

## SEO

- title, description, canonical,
- OG + Twitter Cards,
- H1/H2 semantyczne,
- alt obrazów,
- robots.txt + sitemap.xml,
- Schema.org `AutomotiveBusiness` z placeholderami.
