<?php
$site = require dirname(__DIR__) . '/config/site.php';
$pageTitle = 'Polityka cookies — SDAUTOS';
$pageDescription = 'Informacje o plikach cookies na stronie SDAUTOS — treść demonstracyjna.';
$canonicalPath = '/cookies.php';
$activeNav = '';
require dirname(__DIR__) . '/includes/head.php';
require dirname(__DIR__) . '/includes/header.php';
?>
<main id="main">
  <header class="page-hero">
    <div class="container-sda"><h1>Polityka cookies</h1></div>
  </header>
  <section class="section section--light">
    <div class="container-sda prose">
      <p>Wersja demo nie ustawia marketingowych cookies ani skryptów analitycznych stron trzecich.</p>
      <h2>Czym są cookies</h2>
      <p>To niewielkie pliki zapisywane w przeglądarce. Mogą być niezbędne do działania strony lub opcjonalne.</p>
      <h2>Cookies używane w demo</h2>
      <p>Obecnie strona demo nie wymaga cookies do podstawowego działania. Po wdrożeniu produkcyjnym lista zostanie uzupełniona: <span class="placeholder-data">[DO UZUPEŁNIENIA]</span>.</p>
      <h2>Zarządzanie</h2>
      <p>Możesz ograniczyć cookies w ustawieniach przeglądarki. Szczegóły narzędzi zgody: <span class="placeholder-data">[DO UZUPEŁNIENIA]</span>.</p>
    </div>
  </section>
</main>
<?php require dirname(__DIR__) . '/includes/footer.php'; ?>
