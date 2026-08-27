# Instalacja i uruchomienie lokalne

## 1. Wymagania

- System: Windows / macOS / Linux
- PHP 8.2 lub nowszy
- Przeglądarka Chromium / Firefox / Safari / Edge

Sprawdzenie PHP:

```bash
php -v
```

Jeśli komenda nie działa w nowym terminalu po instalacji, zamknij i otwórz terminal ponownie (odświeżenie PATH).

## 2. Instalacja projektu

Sklonuj lub skopiuj katalog `sdautos-demo`. Zależności npm/composer **nie są wymagane** w demo — Bootstrap jest już w `public/vendor`.

Opcjonalnie:

```bash
cp .env.example .env
```

## 3. Uruchomienie

Z katalogu głównego projektu:

```bash
php -S localhost:8000 -t public
```

## 4. Adres lokalny

- Strona: http://localhost:8000/
- Kontakt API (demo): http://localhost:8000/api/contact-demo.php

## 5. Zatrzymanie

W terminalu z uruchomionym serwerem: `Ctrl+C`.

## Typowe problemy

| Problem | Rozwiązanie |
|---------|-------------|
| `php` nieznane | Doinstaluj PHP 8.2 i dodaj do PATH; nowy terminal |
| Biała strona | Sprawdź logi PHP; włącz `display_errors` tylko lokalnie |
| Brak stylów | Upewnij się, że serwer startuje z `-t public` |
| Formularz nie działa | Serwer musi obsługiwać PHP (nie czysty `python -m http.server`) |
