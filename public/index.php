<?php
/**
 * Strona główna SDAUTOS — demo
 */
$site = require dirname(__DIR__) . '/config/site.php';
$productsData = json_decode(
    file_get_contents(dirname(__DIR__) . '/config/products.demo.json'),
    true
);
$categories = [];
foreach ($productsData['categories'] as $cat) {
    $categories[$cat['id']] = $cat['name'];
}
$homeProducts = array_slice($productsData['products'], 0, 6);

$pageTitle = 'SDAUTOS — Lakiernictwo samochodowe i materiały lakiernicze';
$pageDescription = 'SDAUTOS: lakiernictwo samochodowe, przygotowanie powierzchni, materiały lakiernicze oraz wyposażenie dla profesjonalistów. Oferta demonstracyjna.';
$canonicalPath = '/index.php';
$activeNav = 'home';

require dirname(__DIR__) . '/includes/head.php';
require dirname(__DIR__) . '/includes/header.php';
require dirname(__DIR__) . '/includes/schema-local-business.php';
?>

<main id="main">
  <!-- HERO -->
  <section class="hero" aria-labelledby="hero-heading">
    <div class="hero__media" aria-hidden="true">
      <img
        src="/assets/images/hero/hero-workshop.webp"
        alt="Lakiernik pracujący przy samochodzie w warsztacie — zdjęcie demonstracyjne"
        width="1920"
        height="1080"
        fetchpriority="high"
        decoding="async"
      >
    </div>
    <div class="hero__overlay" aria-hidden="true"></div>
    <div class="container-sda hero__content">
      <p class="hero__brand">SD<span>AUTOS</span></p>
      <h1 id="hero-heading" class="hero__title">Lakiernictwo samochodowe i materiały lakiernicze</h1>
      <p class="hero__text">
        Precyzyjne naprawy lakiernicze, sprawdzone materiały i doradztwo technologiczne
        dla warsztatów oraz klientów indywidualnych.
      </p>
      <div class="btn-group-sda">
        <a class="btn-sda btn-sda--primary" href="#oferta">Poznaj ofertę</a>
        <a class="btn-sda btn-sda--ghost" href="/kontakt.php">Skontaktuj się z nami</a>
      </div>
    </div>
  </section>

  <!-- OFERTA -->
  <section id="oferta" class="section section--light" aria-labelledby="oferta-title">
    <div class="container-sda">
      <p class="section__eyebrow">Oferta</p>
      <h2 id="oferta-title" class="section__title">Główne obszary działalności</h2>
      <p class="section__lead">
        Kompleksowe wsparcie w zakresie lakiernictwa, materiałów i wyposażenia warsztatu.
      </p>
      <div class="card-grid">
        <article class="card-sda">
          <svg class="card-sda__icon" viewBox="0 0 48 48" aria-hidden="true"><path fill="currentColor" d="M8 34h32v4H8zm4-18 8-8 4 4-8 8H12v-4zm18.5 2.5 4-4 4 4-4 4-4-4zM14 28h12l10-10 4 4-10 10H14v-4z"/></svg>
          <h3 class="card-sda__title">Lakiernictwo samochodowe</h3>
          <p class="card-sda__text">Usługi naprawcze i przygotowanie powierzchni pod profesjonalne lakierowanie.</p>
          <ul>
            <li>naprawy lakiernicze</li>
            <li>przygotowanie powierzchni</li>
            <li>lakierowanie elementów</li>
            <li>dobór koloru</li>
            <li>korekty lakiernicze</li>
          </ul>
          <p class="mt-3 mb-0"><a href="/lakiernictwo.php">Szczegóły usług</a></p>
        </article>
        <article class="card-sda">
          <svg class="card-sda__icon" viewBox="0 0 48 48" aria-hidden="true"><path fill="currentColor" d="M10 8h20l8 8v24H10V8zm18 2v6h6l-6-6zM14 22h20v2H14zm0 6h20v2H14zm0 6h14v2H14z"/></svg>
          <h3 class="card-sda__title">Materiały lakiernicze</h3>
          <p class="card-sda__text">Asortyment materiałów do przygotowania, aplikacji i zabezpieczenia powłok.</p>
          <ul>
            <li>lakiery, podkłady, szpachle</li>
            <li>bezbarwne i rozcieńczalniki</li>
            <li>materiały ścierne</li>
            <li>taśmy, folie, akcesoria</li>
          </ul>
          <p class="mt-3 mb-0"><a href="/materialy.php">Zobacz materiały</a></p>
        </article>
        <article class="card-sda">
          <svg class="card-sda__icon" viewBox="0 0 48 48" aria-hidden="true"><path fill="currentColor" d="M28 6v10h10L28 6zM12 8h14v12h12v20H12V8zm6 18h16v2H18zm0 6h12v2H18z"/></svg>
          <h3 class="card-sda__title">Wyposażenie lakiernika</h3>
          <p class="card-sda__text">Narzędzia i akcesoria wspierające codzienną pracę w lakierni.</p>
          <ul>
            <li>pistolety lakiernicze</li>
            <li>narzędzia warsztatowe</li>
            <li>akcesoria aplikacyjne</li>
            <li>wyposażenie stanowiska</li>
          </ul>
          <p class="mt-3 mb-0"><a href="/produkty.php">Przeglądaj produkty</a></p>
        </article>
      </div>
    </div>
  </section>

  <!-- PRODUKTY (demo sklepu) -->
  <section id="produkty" class="section section--panel" aria-labelledby="produkty-title">
    <div class="container-sda">
      <p class="section__eyebrow">Sklep — demo</p>
      <h2 id="produkty-title" class="section__title">Produkty</h2>
      <p class="section__lead">
        Demonstracyjna prezentacja katalogu. Docelowo możliwa integracja z PrestaShop 9
        (ceny, stany, warianty i koszyk).
      </p>
      <div class="product-grid">
        <?php foreach ($homeProducts as $product): ?>
          <article class="product-card">
            <div class="product-card__media">
              <img
                src="<?= htmlspecialchars($product['image'], ENT_QUOTES, 'UTF-8') ?>"
                alt="<?= htmlspecialchars($product['name'], ENT_QUOTES, 'UTF-8') ?>"
                width="800"
                height="600"
                loading="lazy"
                decoding="async"
              >
            </div>
            <div class="product-card__body">
              <p class="product-card__cat"><?= htmlspecialchars($categories[$product['category']] ?? $product['category'], ENT_QUOTES, 'UTF-8') ?></p>
              <h3 class="product-card__title"><?= htmlspecialchars($product['name'], ENT_QUOTES, 'UTF-8') ?></h3>
              <p class="product-card__text"><?= htmlspecialchars($product['short'], ENT_QUOTES, 'UTF-8') ?></p>
              <a class="btn-sda btn-sda--primary" href="/produkty.php#<?= htmlspecialchars($product['slug'], ENT_QUOTES, 'UTF-8') ?>">Zobacz produkt</a>
            </div>
          </article>
        <?php endforeach; ?>
      </div>
      <p class="mt-4 mb-0"><a class="btn-sda btn-sda--ghost" href="/produkty.php">Pełny katalog demo</a></p>
    </div>
  </section>

  <!-- DOBÓR LAKIERU -->
  <section id="dobor-lakieru" class="section section--dark" aria-labelledby="dobor-title">
    <div class="container-sda color-finder">
      <div>
        <p class="section__eyebrow">Narzędzie</p>
        <h2 id="dobor-title" class="section__title">Dobór lakieru</h2>
        <p class="section__lead">
          Miejsce pod przyszłą wyszukiwarkę koloru: kod farby, marka, model oraz system lakierniczy.
          Na etapie demo pola są nieaktywne — architektura gotowa do podłączenia bazy kolorów.
        </p>
        <a class="btn-sda btn-sda--primary" href="/dobor-lakieru.php">Znajdź kod koloru</a>
      </div>
      <div class="color-finder__panel" aria-label="Podgląd przyszłego formularza doboru">
        <h3 class="card-sda__title mt-0">Wyszukiwanie koloru — podgląd</h3>
        <div class="color-finder__fields">
          <div>
            <label class="form-label-sda" for="demo-code">Kod koloru</label>
            <input class="form-control-sda" id="demo-code" type="text" placeholder="np. kod z tabliczki" disabled>
          </div>
          <div>
            <label class="form-label-sda" for="demo-brand">Marka samochodu</label>
            <select class="form-select-sda" id="demo-brand" disabled>
              <option>[DO UZUPEŁNIENIA]</option>
            </select>
          </div>
          <div>
            <label class="form-label-sda" for="demo-model">Model</label>
            <input class="form-control-sda" id="demo-model" type="text" disabled>
          </div>
          <div>
            <label class="form-label-sda" for="demo-system">System lakierniczy</label>
            <select class="form-select-sda" id="demo-system" disabled>
              <option>[DO UZUPEŁNIENIA]</option>
            </select>
          </div>
        </div>
        <p class="form-hint">Funkcja demonstracyjna — bez połączenia z bazą kolorów.</p>
      </div>
    </div>
  </section>

  <!-- REALIZACJE -->
  <section id="realizacje" class="section section--light" aria-labelledby="realizacje-title">
    <div class="container-sda" data-gallery>
      <p class="section__eyebrow">Portfolio</p>
      <h2 id="realizacje-title" class="section__title">Nasze realizacje</h2>
      <p class="section__lead">
        Galeria demonstracyjna ze zdjęciami stockowymi branży lakierniczej.
        Docelowo zastąp własnymi realizacjami (przed / po, elementy, proces).
      </p>
      <div class="gallery-grid">
        <button type="button" class="gallery-item" data-gallery-item
          data-full="/assets/images/gallery/before-01.webp"
          data-caption="Przygotowanie / naprawa karoserii — zdjęcie demonstracyjne"
          data-alt="Samochód w trakcie naprawy blacharsko-lakierniczej">
          <img src="/assets/images/gallery/before-01.webp" alt="Samochód w trakcie naprawy blacharsko-lakierniczej" width="1200" height="900" loading="lazy" decoding="async">
          <span class="gallery-item__caption">Przygotowanie</span>
        </button>
        <button type="button" class="gallery-item" data-gallery-item
          data-full="/assets/images/gallery/after-01.webp"
          data-caption="Efekt po lakierowaniu / polerowaniu — zdjęcie demonstracyjne"
          data-alt="Błyszcząca powłoka lakiernicza samochodu">
          <img src="/assets/images/gallery/after-01.webp" alt="Błyszcząca powłoka lakiernicza samochodu" width="1200" height="900" loading="lazy" decoding="async">
          <span class="gallery-item__caption">Po wykończeniu</span>
        </button>
        <button type="button" class="gallery-item" data-gallery-item
          data-full="/assets/images/gallery/part-01.webp"
          data-caption="Praca na elemencie karoserii — zdjęcie demonstracyjne"
          data-alt="Lakierowanie elementu karoserii">
          <img src="/assets/images/gallery/part-01.webp" alt="Lakierowanie elementu karoserii" width="1200" height="900" loading="lazy" decoding="async">
          <span class="gallery-item__caption">Element</span>
        </button>
        <button type="button" class="gallery-item" data-gallery-item
          data-full="/assets/images/gallery/process-01.webp"
          data-caption="Proces pracy w lakierni — zdjęcie demonstracyjne"
          data-alt="Proces pracy blacharsko-lakierniczej">
          <img src="/assets/images/gallery/process-01.webp" alt="Proces pracy blacharsko-lakierniczej" width="1200" height="900" loading="lazy" decoding="async">
          <span class="gallery-item__caption">Proces</span>
        </button>
      </div>
      <dialog class="gallery-dialog" data-gallery-dialog aria-label="Podgląd realizacji">
        <div class="gallery-dialog__inner">
          <div data-gallery-media></div>
          <p data-gallery-caption></p>
          <button type="button" class="btn-sda btn-sda--primary gallery-dialog__close" data-gallery-close>Zamknij</button>
        </div>
      </dialog>
      <p class="mt-4 mb-0"><a href="/realizacje.php">Więcej realizacji</a></p>
    </div>
  </section>

  <!-- DLACZEGO SDAUTOS -->
  <section id="dlaczego" class="section section--panel" aria-labelledby="dlaczego-title">
    <div class="container-sda">
      <p class="section__eyebrow">Przewagi</p>
      <h2 id="dlaczego-title" class="section__title">Dlaczego SDAUTOS</h2>
      <p class="section__lead">Najważniejsze obszary, na których budujemy współpracę z klientami.</p>
      <div class="feature-list">
        <article class="feature-item">
          <h3>Profesjonalne podejście</h3>
          <p>Uporządkowany proces od diagnozy, przez przygotowanie, aż po wykończenie powłoki.</p>
        </article>
        <article class="feature-item">
          <h3>Materiały lakiernicze</h3>
          <p>Dobór materiałów dopasowanych do technologii naprawy i wymagań warsztatu.</p>
        </article>
        <article class="feature-item">
          <h3>Doradztwo</h3>
          <p>Wsparcie w zakresie produktów i technologii lakierniczych — bez narzucania zbędnych rozwiązań.</p>
        </article>
        <article class="feature-item">
          <h3>Kompleksowa obsługa</h3>
          <p>Usługi, materiały i wyposażenie w jednym miejscu — wygodniej dla lakierni i klienta.</p>
        </article>
        <article class="feature-item">
          <h3>Jakość wykonania</h3>
          <p>Nacisk na dokładność przygotowania powierzchni i powtarzalność efektu lakierniczego.</p>
        </article>
        <article class="feature-item">
          <h3>Dla profesjonalistów</h3>
          <p>Oferta skierowana do warsztatów oraz klientów oczekujących technicznego standardu pracy.</p>
        </article>
      </div>
    </div>
  </section>

  <!-- O NAS -->
  <section id="o-nas" class="section section--light" aria-labelledby="onas-title">
    <div class="container-sda">
      <p class="section__eyebrow">Firma</p>
      <h2 id="onas-title" class="section__title">O nas</h2>
      <p class="section__lead">
        SDAUTOS działa w obszarze lakiernictwa samochodowego oraz dystrybucji materiałów
        i narzędzi dla lakierników. Poniższe punkty opisują strukturę prezentacji firmy —
        konkretne dane uzupełnimy po ich dostarczeniu.
      </p>
      <div class="card-grid">
        <article class="card-sda">
          <h3 class="card-sda__title">Doświadczenie</h3>
          <p class="card-sda__text"><span class="placeholder-data">[DO UZUPEŁNIENIA]</span> — opis doświadczenia zespołu i historii firmy.</p>
        </article>
        <article class="card-sda">
          <h3 class="card-sda__title">Zakres usług</h3>
          <p class="card-sda__text">Lakiernictwo, przygotowanie do lakierowania, sprzedaż materiałów i wyposażenia, doradztwo technologiczne.</p>
        </article>
        <article class="card-sda">
          <h3 class="card-sda__title">Jakość i technologia</h3>
          <p class="card-sda__text">Stawiamy na poprawny proces technologiczny i materiały adekwatne do rodzaju naprawy. <span class="placeholder-data">[DO UZUPEŁNIENIA: certyfikaty / systemy]</span></p>
        </article>
        <article class="card-sda">
          <h3 class="card-sda__title">Obsługa klienta</h3>
          <p class="card-sda__text">Jasna komunikacja, doradztwo produktowe i wsparcie na etapie doboru rozwiązań. <span class="placeholder-data">[DO UZUPEŁNIENIA]</span></p>
        </article>
      </div>
      <p class="mt-4 mb-0"><a href="/o-nas.php">Więcej o firmie</a></p>
    </div>
  </section>

  <!-- KONTAKT -->
  <section id="kontakt" class="section section--dark" aria-labelledby="kontakt-title">
    <div class="container-sda contact-layout">
      <div>
        <p class="section__eyebrow">Kontakt</p>
        <h2 id="kontakt-title" class="section__title">Skontaktuj się z nami</h2>
        <p class="section__lead">
          Formularz działa w trybie demonstracyjnym — nie wysyła wiadomości do prawdziwego odbiorcy.
        </p>
        <ul class="contact-details">
          <li><strong>Adres</strong><?= sda_display_text($site['contact']['address']) ?>, <?= sda_display_text(trim($site['contact']['postal_code'] . ' ' . $site['contact']['city'])) ?></li>
          <li><strong>Telefon</strong><?= sda_phone_link($site['contact']['phone']) ?></li>
          <li><strong>E-mail</strong><?= sda_email_link($site['contact']['email']) ?></li>
          <li><strong>Godziny</strong><?= sda_display_text($site['contact']['hours']) ?></li>
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
          <input class="form-control-sda" type="text" id="subject" name="subject" required>
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
            <span>Wyrażam zgodę na przetworzenie danych w celu odpowiedzi na zapytanie. Polityka: <a href="/polityka-prywatnosci.php">link</a>. Treść zgody — <span class="placeholder-data">[DO UZUPEŁNIENIA]</span>.</span>
          </label>
          <p class="form-error" data-error role="alert"></p>
        </div>
        <!-- Honeypot antyspamowy -->
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
