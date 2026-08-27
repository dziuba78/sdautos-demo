<?php
/**
 * Stopka witryny
 * @var array $site
 */
$year = (int) date('Y');
$c = $site['contact'];
?>
<footer class="site-footer" role="contentinfo">
  <div class="container-sda">
    <div class="footer-grid">
      <div>
        <a class="brand" href="/index.php" aria-label="SDAUTOS">
          <span class="brand__mark">SD<span>AUTOS</span></span>
        </a>
        <p class="mt-3">
          <?= htmlspecialchars($site['site_name'], ENT_QUOTES, 'UTF-8') ?> —
          <?= htmlspecialchars($site['tagline'], ENT_QUOTES, 'UTF-8') ?>.
          Profesjonalne usługi i materiały dla branży lakierniczej.
        </p>
        <p class="text-muted-sda mb-0">Wersja demonstracyjna — dane firmy do uzupełnienia.</p>
      </div>

      <div>
        <h2>Nawigacja</h2>
        <ul class="footer-nav">
          <?php foreach ($site['nav'] as $item): ?>
            <li>
              <a href="<?= htmlspecialchars($item['href'], ENT_QUOTES, 'UTF-8') ?>">
                <?= htmlspecialchars($item['label'], ENT_QUOTES, 'UTF-8') ?>
              </a>
            </li>
          <?php endforeach; ?>
        </ul>
      </div>

      <div>
        <h2>Kontakt</h2>
        <ul class="contact-details">
          <li>
            <strong>Adres</strong>
            <?= sda_display_text($c['address']) ?>,
            <?= sda_display_text(trim($c['postal_code'] . ' ' . $c['city'])) ?>
          </li>
          <li>
            <strong>Telefon</strong>
            <?= sda_phone_link($c['phone']) ?>
          </li>
          <li>
            <strong>E-mail</strong>
            <?= sda_email_link($c['email']) ?>
          </li>
          <li>
            <strong>Godziny</strong>
            <?= sda_display_text($c['hours']) ?>
          </li>
        </ul>
      </div>

      <div>
        <h2>Social media</h2>
        <ul class="social-list">
          <?php foreach ($site['social'] as $network => $url): ?>
            <li>
              <a href="<?= htmlspecialchars($url, ENT_QUOTES, 'UTF-8') ?>" rel="noopener noreferrer">
                <?= htmlspecialchars(ucfirst($network), ENT_QUOTES, 'UTF-8') ?>
                <span class="placeholder-data">[DO UZUPEŁNIENIA]</span>
              </a>
            </li>
          <?php endforeach; ?>
        </ul>
      </div>
    </div>

    <div class="footer-bottom">
      <p class="mb-0">© <?= $year ?> <?= htmlspecialchars($site['site_name'], ENT_QUOTES, 'UTF-8') ?>. Wszelkie prawa zastrzeżone.</p>
      <ul class="footer-legal">
        <li><a href="/polityka-prywatnosci.php">Polityka prywatności</a></li>
        <li><a href="/cookies.php">Cookies</a></li>
        <li><a href="/informacje-prawne.php">Informacje prawne</a></li>
      </ul>
    </div>
  </div>
</footer>

<script src="/vendor/bootstrap/js/bootstrap.bundle.min.js" defer></script>
<script type="module" src="/assets/js/main.js"></script>
</body>
</html>
