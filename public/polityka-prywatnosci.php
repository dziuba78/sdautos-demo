<?php
$site = require dirname(__DIR__) . '/config/site.php';
$pageTitle = 'Polityka prywatności — SDAUTOS';
$pageDescription = 'Polityka prywatności SDAUTOS — treść demonstracyjna do uzupełnienia przez administratora danych.';
$canonicalPath = '/polityka-prywatnosci.php';
$activeNav = '';
require dirname(__DIR__) . '/includes/head.php';
require dirname(__DIR__) . '/includes/header.php';
?>
<main id="main">
  <header class="page-hero">
    <div class="container-sda"><h1>Polityka prywatności</h1></div>
  </header>
  <section class="section section--light">
    <div class="container-sda prose">
      <p>Niniejsza strona zawiera szablon polityki prywatności. Przed publikacją produkcyjną uzupełnij dane administratora i podstawy prawne.</p>
      <h2>Administrator danych</h2>
      <p>
        <?= htmlspecialchars($site['site_name'], ENT_QUOTES, 'UTF-8') ?>,
        <?= htmlspecialchars($site['contact']['address'], ENT_QUOTES, 'UTF-8') ?>,
        <?= htmlspecialchars(trim($site['contact']['postal_code'] . ' ' . $site['contact']['city']), ENT_QUOTES, 'UTF-8') ?>,
        e-mail: <?= sda_email_link($site['contact']['email']) ?>.
        NIP: <?= sda_display_text($site['contact']['nip']) ?>.
      </p>
      <h2>Zakres przetwarzanych danych</h2>
      <p>W ramach formularza kontaktowego mogą być przetwarzane: imię, e-mail, telefon, treść wiadomości oraz dane techniczne połączenia.</p>
      <h2>Cel i podstawa</h2>
      <p><span class="placeholder-data">[DO UZUPEŁNIENIA: cele, podstawy prawne art. 6 RODO]</span></p>
      <h2>Okres przechowywania</h2>
      <p><span class="placeholder-data">[DO UZUPEŁNIENIA]</span></p>
      <h2>Prawa osoby</h2>
      <p>Prawo dostępu, sprostowania, usunięcia, ograniczenia, przenoszenia, sprzeciwu oraz skargi do PUODO — szczegóły: <span class="placeholder-data">[DO UZUPEŁNIENIA]</span>.</p>
    </div>
  </section>
</main>
<?php require dirname(__DIR__) . '/includes/footer.php'; ?>
