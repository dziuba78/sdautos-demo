<?php
/**
 * Katalog produktów — demo pod przyszły PrestaShop 9
 */
$site = require dirname(__DIR__) . '/config/site.php';
$productsData = json_decode(
    file_get_contents(dirname(__DIR__) . '/config/products.demo.json'),
    true
);
$categories = [];
foreach ($productsData['categories'] as $cat) {
    $categories[$cat['id']] = $cat['name'];
}

$pageTitle = 'Produkty — katalog demo SDAUTOS';
$pageDescription = 'Demonstracyjny katalog produktów SDAUTOS. Architektura przygotowana pod integrację z PrestaShop 9.';
$canonicalPath = '/produkty.php';
$activeNav = 'produkty';
require dirname(__DIR__) . '/includes/head.php';
require dirname(__DIR__) . '/includes/header.php';
?>
<main id="main">
  <header class="page-hero">
    <div class="container-sda">
      <h1>Produkty</h1>
      <p>Katalog demonstracyjny. Brak płatności i prawdziwych cen — dane z pliku JSON, łatwe do wymiany na API PrestaShop 9.</p>
    </div>
  </header>
  <section class="section section--light" data-products>
    <div class="container-sda">
      <div class="product-filters" role="group" aria-label="Filtr kategorii">
        <button type="button" class="chip is-active" data-filter="all" aria-pressed="true">Wszystkie</button>
        <?php foreach ($productsData['categories'] as $cat): ?>
          <button type="button" class="chip" data-filter="<?= htmlspecialchars($cat['id'], ENT_QUOTES, 'UTF-8') ?>" aria-pressed="false">
            <?= htmlspecialchars($cat['name'], ENT_QUOTES, 'UTF-8') ?>
          </button>
        <?php endforeach; ?>
      </div>

      <div class="product-grid">
        <?php foreach ($productsData['products'] as $product): ?>
          <article
            class="product-card"
            id="<?= htmlspecialchars($product['slug'], ENT_QUOTES, 'UTF-8') ?>"
            data-category="<?= htmlspecialchars($product['category'], ENT_QUOTES, 'UTF-8') ?>"
          >
            <div class="product-card__media">
              <img
                src="<?= htmlspecialchars($product['image'], ENT_QUOTES, 'UTF-8') ?>"
                alt="<?= htmlspecialchars($product['name'], ENT_QUOTES, 'UTF-8') ?>"
                width="800"
                height="600"
                loading="lazy"
                decoding="async"
              >
            </div>
            <div class="product-card__body">
              <p class="product-card__cat"><?= htmlspecialchars($categories[$product['category']] ?? '', ENT_QUOTES, 'UTF-8') ?></p>
              <h2 class="product-card__title"><?= htmlspecialchars($product['name'], ENT_QUOTES, 'UTF-8') ?></h2>
              <p class="product-card__text"><?= htmlspecialchars($product['short'], ENT_QUOTES, 'UTF-8') ?></p>
              <a class="btn-sda btn-sda--primary" href="/kontakt.php?temat=<?= rawurlencode('Zapytanie: ' . $product['name']) ?>">Zobacz produkt</a>
            </div>
          </article>
        <?php endforeach; ?>
      </div>
    </div>
  </section>
</main>
<?php require dirname(__DIR__) . '/includes/footer.php'; ?>
