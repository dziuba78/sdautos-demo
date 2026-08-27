<?php
$site = require dirname(__DIR__) . '/config/site.php';
$pageTitle = 'Materiały lakiernicze — SDAUTOS';
$pageDescription = 'Materiały lakiernicze SDAUTOS: lakiery, podkłady, szpachle, bezbarwne, rozcieńczalniki, ścierne, taśmy, folie i akcesoria.';
$canonicalPath = '/materialy.php';
$activeNav = 'materialy';
require dirname(__DIR__) . '/includes/head.php';
require dirname(__DIR__) . '/includes/header.php';
?>
<main id="main">
  <header class="page-hero">
    <div class="container-sda">
      <h1>Materiały lakiernicze</h1>
      <p>Asortyment materiałów do przygotowania, aplikacji i zabezpieczenia powłok. Marki i parametry — do uzupełnienia.</p>
    </div>
  </header>
  <section class="section section--light">
    <div class="container-sda">
      <div class="card-grid">
        <?php
        $items = [
          'Lakiery' => 'Lakiery bazowe i systemy kolorystyczne — szczegóły asortymentu [DO UZUPEŁNIENIA].',
          'Podkłady' => 'Podkłady wypełniające i adhezyjne do przygotowania powierzchni.',
          'Szpachle' => 'Szpachle do napraw karoserii i wyrównywania powierzchni.',
          'Bezbarwne' => 'Lakiery bezbarwne zabezpieczające i nadające połysk / strukturę.',
          'Rozcieńczalniki' => 'Rozcieńczalniki i dodatki procesowe dopasowane do systemu.',
          'Materiały ścierne' => 'Papiery, dyski i materiały do obróbki międzywarstwowej.',
          'Taśmy i folie' => 'Materiały maskujące do precyzyjnego zabezpieczenia powierzchni.',
          'Akcesoria lakiernicze' => 'Akcesoria wspierające aplikację i utrzymanie czystości procesu.',
        ];
        foreach ($items as $title => $text): ?>
          <article class="card-sda">
            <h2 class="card-sda__title"><?= htmlspecialchars($title, ENT_QUOTES, 'UTF-8') ?></h2>
            <p class="card-sda__text"><?= htmlspecialchars($text, ENT_QUOTES, 'UTF-8') ?></p>
          </article>
        <?php endforeach; ?>
      </div>
      <p class="mt-4 mb-0">
        <a class="btn-sda btn-sda--dark" href="/produkty.php">Przejdź do katalogu demo</a>
      </p>
    </div>
  </section>
</main>
<?php require dirname(__DIR__) . '/includes/footer.php'; ?>
