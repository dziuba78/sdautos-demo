<?php
/**
 * Katalog tonerów Nexa Autocolor 2K.
 * Dane: config/pigmenty-autocolor-2k.json
 * Zdjęcie: public/assets/images/pigmenty/{SKU}.webp|jpg|jpeg|png
 * albo pole image_file w JSON.
 */
$site = require dirname(__DIR__) . '/config/site.php';
$catalog = json_decode(
    file_get_contents(dirname(__DIR__) . '/config/pigmenty-autocolor-2k.json'),
    true
);
$categories = [];
foreach ($catalog['categories'] as $cat) {
    $categories[$cat['id']] = $cat['name'];
}

$imageDir = __DIR__ . '/assets/images/pigmenty';
$imageUrl = '/assets/images/pigmenty/';
$placeholder = $catalog['image_placeholder'] ?? '/assets/images/products/product-placeholder.svg';

/**
 * @param array<string, mixed> $product
 */
function pigment_image(array $product, string $imageDir, string $imageUrl, string $placeholder): string
{
    $explicit = trim((string) ($product['image_file'] ?? ''));
    if ($explicit !== '') {
        $base = basename(str_replace('\\', '/', $explicit));
        if ($base !== '' && is_file($imageDir . DIRECTORY_SEPARATOR . $base)) {
            return $imageUrl . rawurlencode($base);
        }
    }

    $stems = [];
    foreach (['sku', 'kod_receptury'] as $key) {
        $stem = trim((string) ($product[$key] ?? ''));
        if ($stem !== '' && !in_array($stem, $stems, true)) {
            $stems[] = $stem;
        }
    }
    foreach ($stems as $stem) {
        foreach (['webp', 'jpg', 'jpeg', 'png'] as $ext) {
            $file = $stem . '.' . $ext;
            if (is_file($imageDir . DIRECTORY_SEPARATOR . $file)) {
                return $imageUrl . rawurlencode($file);
            }
        }
    }

    return $placeholder;
}

$pageTitle = 'Pigmenty Autocolor 2K — SDAUTOS';
$pageDescription = 'Tonery Nexa Autocolor 2K: kolory, czerń i biel, metaliki, perły i efekty specjalne. Opisy z karty tinting guide, przygotowane pod zdjęcia produktów.';
$canonicalPath = '/pigmenty-autocolor.php';
$activeNav = 'pigmenty';
require dirname(__DIR__) . '/includes/head.php';
require dirname(__DIR__) . '/includes/header.php';
?>
<main id="main">
  <header class="page-hero">
    <div class="container-sda">
      <h1>Pigmenty Autocolor 2K</h1>
      <p>
        <?= count($catalog['products']) ?> tonerów Nexa Autocolor 2K.
        Opis mówi, jak toner zmienia światło i flop. Ceny nie są jeszcze podane — zapytanie idzie do kontaktu.
        Zdjęcie pojawia się samo po wrzuceniu pliku
        <code>public/assets/images/pigmenty/KOD.webp</code>
        (dopuszczalne też jpg i png), na przykład <code>P420-905.webp</code>.
      </p>
    </div>
  </header>
  <section class="section section--light" data-products>
    <div class="container-sda">
      <div class="product-filters" role="group" aria-label="Filtr grupy tonerów">
        <button type="button" class="chip is-active" data-filter="all" aria-pressed="true">Wszystkie</button>
        <?php foreach ($catalog['categories'] as $cat): ?>
          <button type="button" class="chip" data-filter="<?= htmlspecialchars($cat['id'], ENT_QUOTES, 'UTF-8') ?>" aria-pressed="false">
            <?= htmlspecialchars($cat['name'], ENT_QUOTES, 'UTF-8') ?>
          </button>
        <?php endforeach; ?>
      </div>

      <div class="product-grid">
        <?php foreach ($catalog['products'] as $product): ?>
          <?php
            $catName = $categories[$product['category']] ?? '';
            $meta = $catName;
            if (!empty($product['ziarno'])) {
                $meta .= ' · ziarno ' . $product['ziarno'];
            }
            if (($product['moc'] ?? '') === 'RT') {
                $meta .= ' · obniżona moc';
            }
            $image = pigment_image($product, $imageDir, $imageUrl, $placeholder);
            $recipeNote = ($product['kod_receptury'] ?? '') !== ($product['sku'] ?? '')
                ? 'W recepturze: ' . $product['kod_receptury'] . '.'
                : '';
          ?>
          <article
            class="product-card"
            id="<?= htmlspecialchars($product['slug'], ENT_QUOTES, 'UTF-8') ?>"
            data-category="<?= htmlspecialchars($product['category'], ENT_QUOTES, 'UTF-8') ?>"
          >
            <div class="product-card__media">
              <img
                src="<?= htmlspecialchars($image, ENT_QUOTES, 'UTF-8') ?>"
                alt="<?= htmlspecialchars($product['name'], ENT_QUOTES, 'UTF-8') ?>"
                width="800"
                height="600"
                loading="lazy"
                decoding="async"
              >
            </div>
            <div class="product-card__body">
              <p class="product-card__cat"><?= htmlspecialchars($meta, ENT_QUOTES, 'UTF-8') ?></p>
              <h2 class="product-card__title"><?= htmlspecialchars($product['name'], ENT_QUOTES, 'UTF-8') ?></h2>
              <p class="product-card__text"><?= htmlspecialchars($product['description'], ENT_QUOTES, 'UTF-8') ?></p>
              <?php if ($recipeNote !== ''): ?>
                <p class="product-card__text"><?= htmlspecialchars($recipeNote, ENT_QUOTES, 'UTF-8') ?></p>
              <?php endif; ?>
              <a class="btn-sda btn-sda--primary" href="/kontakt.php?temat=<?= rawurlencode('Zapytanie: ' . $product['name']) ?>">Zapytaj o toner</a>
            </div>
          </article>
        <?php endforeach; ?>
      </div>
    </div>
  </section>
</main>
<?php require dirname(__DIR__) . '/includes/footer.php'; ?>
