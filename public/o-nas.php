<?php
$site = require dirname(__DIR__) . '/config/site.php';
$pageTitle = 'O nas — SDAUTOS';
$pageDescription = 'Poznaj SDAUTOS — lakiernictwo samochodowe, materiały lakiernicze i doradztwo. Dane firmowe do uzupełnienia.';
$canonicalPath = '/o-nas.php';
$activeNav = 'o-nas';
require dirname(__DIR__) . '/includes/head.php';
require dirname(__DIR__) . '/includes/header.php';
require dirname(__DIR__) . '/includes/schema-local-business.php';
?>
<main id="main">
  <header class="page-hero">
    <div class="container-sda">
      <h1>O nas</h1>
      <p>SDAUTOS — lakiernictwo, materiały i wyposażenie dla profesjonalnych lakierników.</p>
    </div>
  </header>
  <section class="section section--light">
    <div class="container-sda">
      <div class="card-grid">
        <article class="card-sda">
          <h2 class="card-sda__title">Doświadczenie</h2>
          <p class="card-sda__text">Opis doświadczenia i historii firmy: <span class="placeholder-data">[DO UZUPEŁNIENIA]</span>. Nie publikujemy tu wymyślonych lat działalności ani liczb.</p>
        </article>
        <article class="card-sda">
          <h2 class="card-sda__title">Zakres usług</h2>
          <p class="card-sda__text">Lakiernictwo samochodowe, przygotowanie do lakierowania, sprzedaż materiałów i narzędzi, doradztwo produktowe i technologiczne.</p>
        </article>
        <article class="card-sda">
          <h2 class="card-sda__title">Jakość</h2>
          <p class="card-sda__text">Priorytetem jest poprawny proces i materiały dopasowane do naprawy. Szczegóły standardów jakości: <span class="placeholder-data">[DO UZUPEŁNIENIA]</span>.</p>
        </article>
        <article class="card-sda">
          <h2 class="card-sda__title">Technologia</h2>
          <p class="card-sda__text">Stosowane systemy i technologie lakiernicze: <span class="placeholder-data">[DO UZUPEŁNIENIA]</span>.</p>
        </article>
        <article class="card-sda">
          <h2 class="card-sda__title">Obsługa klienta</h2>
          <p class="card-sda__text">Doradztwo przy doborze materiałów i wsparcie w zakresie procesu. Kontakt: <a href="/kontakt.php">formularz</a>.</p>
        </article>
      </div>
    </div>
  </section>
</main>
<?php require dirname(__DIR__) . '/includes/footer.php'; ?>
