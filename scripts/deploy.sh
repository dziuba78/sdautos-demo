#!/usr/bin/env bash
# Prosty skrypt wdrożeniowy SDAUTOS (SSH na serwerze)
# Użycie: ./scripts/deploy.sh
# Wymaga: git, ustawiony remote, DocumentRoot = public/

set -euo pipefail

APP_DIR="${APP_DIR:-/var/www/sdautos}"
BRANCH="${BRANCH:-main}"

cd "$APP_DIR"

echo "==> Pobieranie zmian ($BRANCH)…"
git fetch origin
git checkout "$BRANCH"
git pull --ff-only origin "$BRANCH"

echo "==> Uprawnienia…"
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;

if [[ -f .env ]]; then
  chmod 600 .env || true
fi

echo "==> Gotowe. Sprawdź stronę w przeglądarce (HTTPS)."
echo "    Pamiętaj o aktualizacji config/site.php (base_url) przy pierwszym wdrożeniu."
