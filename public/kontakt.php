<?php
$site = require dirname(__DIR__) . '/config/site.php';
$pageTitle = 'Kontakt — SDAUTOS';
$pageDescription = 'Skontaktuj się z SDAUTOS. Formularz demonstracyjny — bez wysyłki do prawdziwego odbiorcy.';
$canonicalPath = '/kontakt.php';
$activeNav = 'kontakt';
$prefillSubject = isset($_GET['temat']) ? trim((string) $_GET['temat']) : '';
require dirname(__DIR__) . '/includes/head.php';
require dirname(__DIR__) . '/includes/header.php';
?>
<main id="main">
  <header class="page-hero">
    <div class="container-sda">
      <h1>Kontakt</h1>
      <p>Napisz do nas. W demo wiadomość nie trafia do prawdziwej skrzynki — tylko walidacja i komunikat.</p>
    </div>
  </header>
  <section class="section section--dark">
    <div class="container-sda contact-layout">
      <div>
        <h2 class="section__title">Dane kontaktowe</h2>
        <ul class="contact-details">
          <li><strong>Adres</strong><?= sda_display_text($site['contact']['address']) ?>, <?= sda_display_text(trim($site['contact']['postal_code'] . ' ' . $site['contact']['city'])) ?></li>
          <li><strong>Telefon</strong><?= sda_phone_link($site['contact']['phone']) ?></li>
          <li><strong>E-mail</strong><?= sda_email_link($site['contact']['email']) ?></li>
          <li><strong>Godziny otwarcia</strong><?= sda_display_text($site['contact']['hours']) ?></li>
          <li><strong>NIP</strong><?= sda_display_text($site['contact']['nip']) ?></li>
        </ul>
      </div>
      <form class="form-sda" method="post" action="/api/contact-demo.php" data-contact-form novalidate>
        <div class="form-field" data-field="name">
          <label class="form-label-sda" for="name">Imię</label>
          <input class="form-control-sda" type="text" id="name" name="name" autocomplete="name" required>
          <p class="form-error" data-error role="alert"></p>
        </div>
        <div class="form-field" data-field="email">
          <label class="form-label-sda" for="email">E-mail</label>
          <input class="form-control-sda" type="email" id="email" name="email" autocomplete="email" required>
          <p class="form-error" data-error role="alert"></p>
        </div>
        <div class="form-field" data-field="phone">
          <label class="form-label-sda" for="phone">Telefon</label>
          <input class="form-control-sda" type="tel" id="phone" name="phone" autocomplete="tel">
          <p class="form-error" data-error role="alert"></p>
        </div>
        <div class="form-field" data-field="subject">
          <label class="form-label-sda" for="subject">Temat</label>
          <input class="form-control-sda" type="text" id="subject" name="subject" value="<?= htmlspecialchars($prefillSubject, ENT_QUOTES, 'UTF-8') ?>" required>
          <p class="form-error" data-error role="alert"></p>
        </div>
        <div class="form-field" data-field="message">
          <label class="form-label-sda" for="message">Wiadomość</label>
          <textarea class="form-textarea-sda" id="message" name="message" required></textarea>
          <p class="form-error" data-error role="alert"></p>
        </div>
        <div class="form-field" data-field="consent">
          <label class="form-check-sda">
            <input type="checkbox" name="consent" value="1" required>
            <span>Wyrażam zgodę na przetworzenie danych w celu odpowiedzi. Szczegóły: <a href="/polityka-prywatnosci.php">polityka prywatności</a>. Treść prawna zgody: <span class="placeholder-data">[DO UZUPEŁNIENIA]</span>.</span>
          </label>
          <p class="form-error" data-error role="alert"></p>
        </div>
        <div class="visually-hidden-sda" aria-hidden="true">
          <label for="website">Strona WWW</label>
          <input type="text" id="website" name="website" tabindex="-1" autocomplete="off">
        </div>
        <input type="hidden" name="csrf_token" value="<?= htmlspecialchars(bin2hex(random_bytes(16)), ENT_QUOTES, 'UTF-8') ?>">
        <button class="btn-sda btn-sda--primary" type="submit">Wyślij wiadomość (demo)</button>
        <div data-form-status hidden></div>
      </form>
    </div>
  </section>
</main>
<?php require dirname(__DIR__) . '/includes/footer.php'; ?>
