<?php
$site = require dirname(__DIR__) . '/config/site.php';
$pageTitle = 'Dobór lakieru — SDAUTOS';
$pageDescription = 'Demonstracyjna wyszukiwarka kodu koloru SDAUTOS. Miejsce pod przyszłą bazę kolorów i systemy lakiernicze.';
$canonicalPath = '/dobor-lakieru.php';
$activeNav = 'materialy';
require dirname(__DIR__) . '/includes/head.php';
require dirname(__DIR__) . '/includes/header.php';
?>
<main id="main">
  <header class="page-hero">
    <div class="container-sda">
      <h1>Dobór lakieru</h1>
      <p>Znajdź kod koloru — funkcja demonstracyjna. Pola przygotowane pod przyszłą bazę danych kolorów.</p>
    </div>
  </header>
  <section class="section section--dark">
    <div class="container-sda color-finder">
      <div>
        <h2 class="section__title">Jak szukać kodu koloru</h2>
        <ol class="section__lead list-steps">
          <li>Zlokalizuj tabliczkę znamionową / naklejkę z kodem koloru w pojeździe.</li>
          <li>Sprawdź dokumentację pojazdu, jeśli kod jest nieczytelny.</li>
          <li>Wpisz kod oraz markę / model (gdy funkcja będzie aktywna).</li>
          <li>W razie wątpliwości skontaktuj się z nami — pomożemy dobrać rozwiązanie.</li>
        </ol>
        <p class="form-hint">Instrukcje szczegółowe dla konkretnych marek: <span class="placeholder-data">[DO UZUPEŁNIENIA]</span></p>
      </div>
      <form class="color-finder__panel" action="/dobor-lakieru.php" method="get" aria-label="Wyszukiwanie koloru (demo)">
        <h2 class="card-sda__title mt-0">Znajdź kod koloru</h2>
        <div class="color-finder__fields">
          <div>
            <label class="form-label-sda" for="color-code">Kod koloru</label>
            <input class="form-control-sda" id="color-code" name="code" type="text" placeholder="Wpisz kod" disabled>
          </div>
          <div>
            <label class="form-label-sda" for="car-brand">Marka samochodu</label>
            <select class="form-select-sda" id="car-brand" name="brand" disabled>
              <option value="">[DO UZUPEŁNIENIA]</option>
            </select>
          </div>
          <div>
            <label class="form-label-sda" for="car-model">Model</label>
            <input class="form-control-sda" id="car-model" name="model" type="text" disabled>
          </div>
          <div>
            <label class="form-label-sda" for="paint-system">Producent systemu lakierniczego</label>
            <select class="form-select-sda" id="paint-system" name="system" disabled>
              <option value="">[DO UZUPEŁNIENIA]</option>
            </select>
          </div>
        </div>
        <button class="btn-sda btn-sda--primary" type="button" disabled title="Funkcja niedostępna w demo">Szukaj (wkrótce)</button>
        <p class="form-hint mt-3">To jest placeholder. Po podłączeniu bazy kolorów formularz zostanie aktywowany.</p>
        <p class="mb-0"><a class="btn-sda btn-sda--ghost" href="/kontakt.php">Skontaktuj się w sprawie koloru</a></p>
      </form>
    </div>
  </section>
</main>
<?php require dirname(__DIR__) . '/includes/footer.php'; ?>
