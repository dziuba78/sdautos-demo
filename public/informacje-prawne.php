<?php
$site = require dirname(__DIR__) . '/config/site.php';
$pageTitle = 'Informacje prawne — SDAUTOS';
$pageDescription = 'Informacje prawne i dane rejestrowe SDAUTOS — placeholdery do uzupełnienia.';
$canonicalPath = '/informacje-prawne.php';
$activeNav = '';
require dirname(__DIR__) . '/includes/head.php';
require dirname(__DIR__) . '/includes/header.php';
?>
<main id="main">
  <header class="page-hero">
    <div class="container-sda"><h1>Informacje prawne</h1></div>
  </header>
  <section class="section section--light">
    <div class="container-sda prose">
      <h2>Dane podmiotu</h2>
      <ul>
        <li>Nazwa: <?= htmlspecialchars($site['site_name'], ENT_QUOTES, 'UTF-8') ?></li>
        <li>Adres: <?= sda_display_text($site['contact']['address']) ?>, <?= sda_display_text(trim($site['contact']['postal_code'] . ' ' . $site['contact']['city'])) ?></li>
        <li>Telefon: <?= sda_phone_link($site['contact']['phone']) ?></li>
        <li>E-mail: <?= sda_email_link($site['contact']['email']) ?></li>
        <li>NIP: <?= sda_display_text($site['contact']['nip']) ?></li>
        <li>REGON: <?= sda_display_text($site['contact']['regon']) ?></li>
        <li>KRS / CEIDG: <span class="placeholder-data">[DO UZUPEŁNIENIA]</span></li>
      </ul>
      <h2>Wyłączenie odpowiedzialności</h2>
      <p>Treści na stronie demo mają charakter informacyjny i mogą ulec zmianie. Oferta produktowa oraz ceny pojawią się po integracji ze sklepem.</p>
    </div>
  </section>
</main>
<?php require dirname(__DIR__) . '/includes/footer.php'; ?>
