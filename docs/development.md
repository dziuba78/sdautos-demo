# Rozwój projektu SDAUTOS

## Zasady

- Nie wymyślaj danych firmowych — używaj `[DO UZUPEŁNIENIA]`.
- Nie commituj `.env`, sekretów, kluczy API.
- Preferuj małe, czytelne pliki zamiast monolitu.
- Komentarze w kodzie po polsku.

## Gdzie edytować treści

| Treść | Plik |
|-------|------|
| Nazwa, kontakt, menu, social | `config/site.php` |
| Produkty demo | `config/products.demo.json` |
| Sekcje strony głównej | `public/index.php` |
| Style / design system | `public/assets/css/` |
| Zachowania UI | `public/assets/js/` |
| SEO head | `includes/head.php` |
| Schema.org | `includes/schema-local-business.php` |

## Design system

Tokeny w `tokens.css`: kolory, typografia, odstępy, promienie.

Kierunek wizualny: grafit + stalowy niebieski, typografia techniczna (Barlow Condensed + Source Sans 3).

## Testowanie lokalne

1. Uruchom `php -S localhost:8000 -t public`
2. Sprawdź checklistę w `tests/checklist.md`
3. Przetestuj szerokości: 320, 375, 390, 414, 768, 1024, 1280, 1440, 1920

## Git — workflow rekomendowany

```bash
git checkout -b feature/opis-zmiany
# zmiany…
git add .
git commit -m "Krótki opis dlaczego"
# push dopiero po akceptacji
```

## Przed produkcją

- [ ] Uzupełnić dane firmy
- [ ] Podmienić logo i zdjęcia
- [ ] Ustawić URL produkcyjny (canonical, sitemap, robots, OG)
- [ ] Włączyć prawdziwy backend formularza + CSRF sesyjny
- [ ] Dodać politykę prywatności / cookies / zgody (treść prawna)
- [ ] Skonfigurować HTTPS i nagłówki bezpieczeństwa
- [ ] Zaplanować PrestaShop 9 (patrz `prestashop-integration.md`)
