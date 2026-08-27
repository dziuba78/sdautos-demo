/**
 * Nawigacja mobilna i aktywny stan menu
 */

export function initNavigation() {
  const toggle = document.querySelector('[data-nav-toggle]');
  const offcanvasEl = document.getElementById('mobileNav');
  if (!toggle || !offcanvasEl || typeof bootstrap === 'undefined') {
    highlightActiveLinks();
    return;
  }

  const offcanvas = bootstrap.Offcanvas.getOrCreateInstance(offcanvasEl);

  toggle.addEventListener('click', () => {
    offcanvas.toggle();
  });

  offcanvasEl.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => offcanvas.hide());
  });

  highlightActiveLinks();
}

function highlightActiveLinks() {
  const path = window.location.pathname.replace(/\/$/, '') || '/index.php';
  const current = path.endsWith('.php') ? path : `${path}/index.php`;

  document.querySelectorAll('[data-nav-link]').forEach((link) => {
    const href = link.getAttribute('href') || '';
    const normalized = href.replace(/\/$/, '');
    if (normalized === current || (current.endsWith('/index.php') && normalized.endsWith('/index.php'))) {
      link.classList.add('is-active');
      link.setAttribute('aria-current', 'page');
    }
  });
}
