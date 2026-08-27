<?php
$site = require dirname(__DIR__) . '/config/site.php';
$pageTitle = 'Realizacje — SDAUTOS';
$pageDescription = 'Galeria realizacji SDAUTOS — demonstracyjne placeholdery przed/po, elementy i proces pracy.';
$canonicalPath = '/realizacje.php';
$activeNav = 'realizacje';
require dirname(__DIR__) . '/includes/head.php';
require dirname(__DIR__) . '/includes/header.php';
?>
<main id="main">
  <header class="page-hero">
    <div class="container-sda">
      <h1>Nasze realizacje</h1>
      <p>Galeria demonstracyjna ze zdjęciami stockowymi. Zastąp własnymi realizacjami SDAUTOS.</p>
    </div>
  </header>
  <section class="section section--light">
    <div class="container-sda" data-gallery>
      <div class="gallery-grid">
        <?php
        $items = [
          ['before-01.webp', 'Przygotowanie', 'Przygotowanie / naprawa karoserii — zdjęcie demonstracyjne'],
          ['after-01.webp', 'Po wykończeniu', 'Efekt po lakierowaniu — zdjęcie demonstracyjne'],
          ['part-01.webp', 'Element', 'Praca na elemencie karoserii — zdjęcie demonstracyjne'],
          ['process-01.webp', 'Proces', 'Proces pracy w lakierni — zdjęcie demonstracyjne'],
          ['polish-01.webp', 'Polerowanie', 'Polerowanie powłoki — zdjęcie demonstracyjne'],
          ['booth-01.webp', 'Warsztat', 'Prace lakiernicze w warsztacie — zdjęcie demonstracyjne'],
        ];
        foreach ($items as [$file, $label, $caption]):
          $src = '/assets/images/gallery/' . $file;
        ?>
          <button type="button" class="gallery-item" data-gallery-item
            data-full="<?= htmlspecialchars($src, ENT_QUOTES, 'UTF-8') ?>"
            data-caption="<?= htmlspecialchars($caption, ENT_QUOTES, 'UTF-8') ?>"
            data-alt="<?= htmlspecialchars($caption, ENT_QUOTES, 'UTF-8') ?>">
            <img src="<?= htmlspecialchars($src, ENT_QUOTES, 'UTF-8') ?>" alt="<?= htmlspecialchars($caption, ENT_QUOTES, 'UTF-8') ?>" width="1200" height="900" loading="lazy" decoding="async">
            <span class="gallery-item__caption"><?= htmlspecialchars($label, ENT_QUOTES, 'UTF-8') ?></span>
          </button>
        <?php endforeach; ?>
      </div>
      <dialog class="gallery-dialog" data-gallery-dialog aria-label="Podgląd realizacji">
        <div class="gallery-dialog__inner">
          <div data-gallery-media></div>
          <p data-gallery-caption></p>
          <button type="button" class="btn-sda btn-sda--primary gallery-dialog__close" data-gallery-close>Zamknij</button>
        </div>
      </dialog>
    </div>
  </section>
</main>
<?php require dirname(__DIR__) . '/includes/footer.php'; ?>
