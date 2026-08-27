# SDAUTOS — lokalne demo strony WWW

Profesjonalne demo witryny firmy **SDAUTOS** (lakiernictwo samochodowe, materiały lakiernicze, wyposażenie, doradztwo).

Projekt jest przygotowany do testów lokalnych, uzupełnienia danych firmowych, akceptacji, a następnie wdrożenia produkcyjnego i integracji z PrestaShop 9.

> To jest **wersja demonstracyjna**. Nie publikuj automatycznie i nie wypychaj na GitHub bez świadomej decyzji.

## Cel

- prezentacja oferty i wizerunku SDAUTOS,
- lokalne demo bez publikacji w Internecie,
- solidna baza pod SEO, bezpieczeństwo i Core Web Vitals,
- architektura pod przyszły sklep PrestaShop 9.

## Technologie

- HTML5 (semantyczny)
- CSS3 (design system + responsywność)
- JavaScript ES6 modules
- Bootstrap 5.3 (lokalnie w `public/vendor`)
- PHP 8.2 (includes + endpoint demo formularza)
- SVG (logo tekstowe, placeholdery grafik)

**Bez** React / Vue / Next.js — celowo, dla wydajności, SEO i prostoty utrzymania.

## Wymagania

- PHP **8.2+** (`php -v`)
- Nowoczesna przeglądarka
- (opcjonalnie) Git

## Instalacja i uruchomienie

Szczegóły: [docs/installation.md](docs/installation.md)

```bash
cd sdautos-demo
php -S localhost:8000 -t public
```

Otwórz: [http://localhost:8000](http://localhost:8000)

Zatrzymanie serwera: `Ctrl+C`

## Struktura katalogów

```text
sdautos-demo/
├── public/                 # Document root (strony, assets, SEO)
├── includes/               # Partial PHP (head, header, footer, schema)
├── config/                 # Konfiguracja witryny + produkty demo (JSON)
├── docs/                   # Dokumentacja PL
├── tests/                  # Checklista testów
├── .env.example
├── .gitignore
├── README.md
└── LICENSE
```

Assety CSS/JS/obrazy są w `public/assets/`, aby działały z `php -S -t public` bez dodatkowego routera.

## Dane do uzupełnienia

Wyszukaj w projekcie frazę **`[DO UZUPEŁNIENIA]`**.

Główne miejsca:

| Co | Gdzie |
|----|--------|
| Adres, telefon, e-mail, godziny, NIP, REGON | `config/site.php` |
| URL produkcyjny | `config/site.php` → `base_url`, `public/robots.txt`, `public/sitemap.xml` |
| Social media | `config/site.php` → `social` |
| Treści O nas / zgody RODO | strony + placeholdery w formularzu |
| Logo docelowe | zamień znak tekstowy w `includes/header.php` / `footer.php` |
| Zdjęcia realizacji / produktów | `public/assets/images/` |
| Fonty WOFF2 (opcjonalnie) | `public/assets/fonts/` + `fonts.css` |

## Dokumentacja

- [Architektura](docs/architecture.md)
- [Instalacja](docs/installation.md)
- [Rozwój](docs/development.md)
- [Wdrożenie na serwer](docs/deployment.md)
- [Integracja PrestaShop 9](docs/prestashop-integration.md)
- [Kredyty zdjęć](docs/image-credits.md)

## Git (bez automatycznego push)

```bash
cd sdautos-demo
git init
git add .
git commit -m "Initial SDAUTOS demo"
```

### Podłączenie GitHub

Repozytorium: https://github.com/dziuba78/sdautos-demo

```bash
git remote add origin https://github.com/dziuba78/sdautos-demo.git
git branch -M main
git push -u origin main
```

## Wdrożenie produkcyjne (później)

1. Uzupełnij dane firmowe i media.
2. Ustaw `base_url`, canonical, sitemap, robots.
3. Włącz prawdziwą wysyłkę formularza (SMTP) + CSRF sesyjny.
4. Skonfiguruj HTTPS, nagłówki bezpieczeństwa, kopie zapasowe.
5. Zaplanuj integrację PrestaShop 9 (patrz dokumentacja).

## Licencja

Zobacz plik [LICENSE](LICENSE).
