<?php
$site = require dirname(__DIR__) . '/config/site.php';
$pageTitle = 'Lakiernictwo samochodowe — SDAUTOS';
$pageDescription = 'Usługi lakiernictwa samochodowego SDAUTOS: naprawy, przygotowanie powierzchni, lakierowanie, dobór koloru i korekty.';
$canonicalPath = '/lakiernictwo.php';
$activeNav = 'lakiernictwo';
require dirname(__DIR__) . '/includes/head.php';
require dirname(__DIR__) . '/includes/header.php';
?>
<main id="main">
  <header class="page-hero">
    <div class="container-sda">
      <h1>Lakiernictwo samochodowe</h1>
      <p>Profesjonalne naprawy i przygotowanie powierzchni pod trwałe, estetyczne powłoki lakiernicze.</p>
    </div>
  </header>
  <section class="section section--light">
    <div class="container-sda card-grid">
      <article class="card-sda">
        <h2 class="card-sda__title">Naprawy lakiernicze</h2>
        <p class="card-sda__text">Usuwanie uszkodzeń powłoki i lokalne naprawy elementów karoserii zgodnie z procesem technologicznym.</p>
      </article>
      <article class="card-sda">
        <h2 class="card-sda__title">Przygotowanie powierzchni</h2>
        <p class="card-sda__text">Szlifowanie, odtłuszczanie, maskowanie i przygotowanie podkładów pod lakierowanie.</p>
      </article>
      <article class="card-sda">
        <h2 class="card-sda__title">Lakierowanie elementów</h2>
        <p class="card-sda__text">Aplikacja lakierów bazowych i bezbarwnych na elementach oraz — w zależności od zakresu — na większych powierzchniach.</p>
      </article>
      <article class="card-sda">
        <h2 class="card-sda__title">Dobór koloru</h2>
        <p class="card-sda__text">Identyfikacja i dobór koloru z uwzględnieniem kodu oraz warunków aplikacji. <a href="/dobor-lakieru.php">Narzędzie doboru</a> (demo).</p>
      </article>
      <article class="card-sda">
        <h2 class="card-sda__title">Korekty lakiernicze</h2>
        <p class="card-sda__text">Korekty wykończenia i prace poprawkowe mające na celu wyrównanie wyglądu powłoki.</p>
      </article>
    </div>
    <div class="container-sda mt-4">
      <a class="btn-sda btn-sda--dark" href="/kontakt.php">Zapytaj o usługę</a>
    </div>
  </section>
</main>
<?php require dirname(__DIR__) . '/includes/footer.php'; ?>
