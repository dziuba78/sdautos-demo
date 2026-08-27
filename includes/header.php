<?php
/**
 * Nagłówek witryny — logo, menu, CTA, sloty telefon/koszyk
 * @var array $site
 * @var string $activeNav
 */

$activeNav = $activeNav ?? '';
$phone = $site['contact']['phone'] ?? '[DO UZUPEŁNIENIA]';
$phoneHref = ($phone !== '[DO UZUPEŁNIENIA]') ? 'tel:' . preg_replace('/\s+/', '', $phone) : '#kontakt';
?>
<header class="site-header" role="banner">
  <div class="container-sda site-header__inner">
    <a class="brand" href="/index.php" aria-label="SDAUTOS — strona główna">
      <span class="brand__mark">SD<span>AUTOS</span></span>
    </a>

    <nav class="d-none d-lg-block" aria-label="Menu główne">
      <ul class="nav-desktop">
        <?php foreach ($site['nav'] as $item): ?>
          <li>
            <a
              href="<?= htmlspecialchars($item['href'], ENT_QUOTES, 'UTF-8') ?>"
              data-nav-link
              class="<?= $activeNav === $item['id'] ? 'is-active' : '' ?>"
              <?= $activeNav === $item['id'] ? 'aria-current="page"' : '' ?>
            ><?= htmlspecialchars($item['label'], ENT_QUOTES, 'UTF-8') ?></a>
          </li>
        <?php endforeach; ?>
      </ul>
    </nav>

    <div class="header-actions">
      <!-- Slot na telefon — widoczny gdy uzupełniony lub jako placeholder -->
      <a class="header-phone" href="<?= htmlspecialchars($phoneHref, ENT_QUOTES, 'UTF-8') ?>" aria-label="Zadzwoń">
        <span class="visually-hidden-sda">Telefon: </span><?= htmlspecialchars($phone, ENT_QUOTES, 'UTF-8') ?>
      </a>

      <!-- Slot na przyszły koszyk PrestaShop -->
      <a class="header-cart" href="/produkty.php" aria-label="Koszyk — wkrótce (demo)" title="Koszyk — placeholder pod PrestaShop">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M6 6h15l-1.5 9h-12L6 6Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>
          <path d="M6 6 5 3H2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
          <circle cx="9" cy="20" r="1.3" fill="currentColor"/>
          <circle cx="18" cy="20" r="1.3" fill="currentColor"/>
        </svg>
      </a>

      <a class="btn-sda btn-sda--primary d-none d-md-inline-flex" href="/kontakt.php">Kontakt</a>

      <button
        class="nav-toggle"
        type="button"
        data-nav-toggle
        aria-controls="mobileNav"
        aria-expanded="false"
        aria-label="Otwórz menu"
      >
        <span class="nav-toggle__bars" aria-hidden="true">
          <span></span><span></span><span></span>
        </span>
      </button>
    </div>
  </div>
</header>

<div class="offcanvas offcanvas-end offcanvas-sda" tabindex="-1" id="mobileNav" aria-labelledby="mobileNavLabel">
  <div class="offcanvas-header">
    <h2 class="offcanvas-title" id="mobileNavLabel">Menu</h2>
    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas" aria-label="Zamknij menu"></button>
  </div>
  <div class="offcanvas-body">
    <nav aria-label="Menu mobilne">
      <ul class="nav-mobile">
        <?php foreach ($site['nav'] as $item): ?>
          <li>
            <a
              href="<?= htmlspecialchars($item['href'], ENT_QUOTES, 'UTF-8') ?>"
              data-nav-link
              class="<?= $activeNav === $item['id'] ? 'is-active' : '' ?>"
            ><?= htmlspecialchars($item['label'], ENT_QUOTES, 'UTF-8') ?></a>
          </li>
        <?php endforeach; ?>
      </ul>
    </nav>
    <div class="mt-4">
      <a class="btn-sda btn-sda--primary w-100" href="/kontakt.php">Skontaktuj się</a>
    </div>
  </div>
</div>
