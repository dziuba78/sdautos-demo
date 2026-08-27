# Wdrożenie SDAUTOS na serwer produkcyjny

Instrukcja wdrożenia lokalnego demo na hosting z PHP 8.2+.

## Wymagania serwera

- PHP **8.2+** (rozszerzenia: `json`, `filter`; opcjonalnie `mbstring`)
- Serwer WWW: **Apache** (mod_rewrite) lub **Nginx**
- HTTPS (certyfikat SSL/TLS)
- Dostęp SSH / FTP / panel hostingu (wg oferty)

## Struktura na serwerze

Document root powinien wskazywać na katalog **`public/`**:

```text
/var/www/sdautos/          # katalog projektu (poza publicznym dostępem: config, includes)
├── config/
├── includes/
├── public/                # ← DocumentRoot / vhost root
│   ├── index.php
│   ├── assets/
│   └── …
├── .env                   # lokalnie na serwerze, NIE w Git
└── …
```

Jeśli hosting pozwala tylko na `public_html` bez osobnego DocumentRoot:

1. Wgraj zawartość `public/` do `public_html/`
2. Wgraj `config/` i `includes/` **poziom wyżej** niż `public_html` (albo dostosuj ścieżki `dirname(__DIR__)` w plikach PHP)

## Checklist przed wdrożeniem

- [ ] Uzupełnić dane w `config/site.php` (`base_url` produkcyjny, godziny, NIP, REGON, social)
- [ ] Zaktualizować `public/robots.txt` i `public/sitemap.xml` (URL produkcyjny)
- [ ] Podmienić zdjęcia stock na własne realizacje
- [ ] Skopiować `.env.example` → `.env` na serwerze i uzupełnić
- [ ] Ustawić prawdziwą wysyłkę formularza (SMTP) — obecnie tryb demo
- [ ] Włączyć CSRF sesyjny w produkcji
- [ ] Sprawdzić HTTPS i przekierowanie HTTP → HTTPS

## Szybkie wdrożenie (SSH + Git)

```bash
# Na serwerze
cd /var/www
git clone https://github.com/dziuba78/sdautos-demo.git sdautos
cd sdautos
cp .env.example .env
# Edytuj config/site.php — base_url i dane firmy
```

### Apache (przykład vhost)

```apache
<VirtualHost *:443>
    ServerName www.przyklad.pl
    DocumentRoot /var/www/sdautos/public

    <Directory /var/www/sdautos/public>
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/sdautos-error.log
    CustomLog ${APACHE_LOG_DIR}/sdautos-access.log combined
</VirtualHost>
```

Plik `public/.htaccess` chroni katalogi nadrzędne i wymusza podstawowe nagłówki bezpieczeństwa.

### Nginx (przykład)

```nginx
server {
    listen 443 ssl http2;
    server_name www.przyklad.pl;
    root /var/www/sdautos/public;
    index index.php;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php8.2-fpm.sock;
    }

    location ~* \.(env|git|md)$ {
        deny all;
    }
}
```

## Wdrożenie bez Git (FTP / panel)

1. Spakuj projekt (bez `.git`, bez `.env`).
2. Wgraj pliki na serwer.
3. Ustaw DocumentRoot na `public/` (lub przenieś pliki zgodnie z ograniczeniami hostingu).
4. Ustaw uprawnienia: katalogi `755`, pliki `644`.
5. Sprawdź `https://twoja-domena/` w przeglądarce.

## Aktualizacja (po zmianach w repo)

```bash
cd /var/www/sdautos
git pull origin main
# Wyczyść cache hostingu / OPcache jeśli używane
```

## Formularz kontaktowy w produkcji

Endpoint `public/api/contact-demo.php` **nie wysyła** e-maili.

Przed produkcją:

1. Zaimplementuj wysyłkę SMTP (np. PHPMailer) z danymi z `.env`
2. Zapisz token CSRF w sesji PHP i weryfikuj `hash_equals`
3. Dodaj rate limiting (np. po IP)
4. Ustaw `CONTACT_MAIL_TO=sdautos@o2.pl` w `.env`

## Bezpieczeństwo

- Nie commituj `.env`, haseł, kluczy API
- DocumentRoot = tylko `public/`
- Wymuś HTTPS
- Regularne aktualizacje PHP
- Kopia zapasowa przed każdą większą zmianą

## Weryfikacja po wdrożeniu

- [ ] Strona główna ładuje się przez HTTPS
- [ ] Menu i podstrony działają
- [ ] CSS/JS/obrazy ładują się (ścieżki `/assets/…`)
- [ ] Formularz zwraca oczekiwany komunikat / wysyła mail
- [ ] `robots.txt` i `sitemap.xml` mają poprawny URL
- [ ] Telefon i e-mail w stopce są poprawne

## Rollback

```bash
cd /var/www/sdautos
git log --oneline -5
git checkout <hash-działającej-wersji>
```

Albo przywróć backup z panelu hostingu.
