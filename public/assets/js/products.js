/**
 * Filtrowanie kategorii produktów (demo)
 */

export function initProductFilters() {
  const root = document.querySelector('[data-products]');
  if (!root) return;

  const chips = root.querySelectorAll('[data-filter]');
  const cards = root.querySelectorAll('[data-category]');

  chips.forEach((chip) => {
    chip.addEventListener('click', () => {
      const filter = chip.getAttribute('data-filter') || 'all';

      chips.forEach((c) => {
        c.classList.toggle('is-active', c === chip);
        c.setAttribute('aria-pressed', c === chip ? 'true' : 'false');
      });

      cards.forEach((card) => {
        const cat = card.getAttribute('data-category');
        const show = filter === 'all' || filter === cat;
        card.hidden = !show;
      });
    });
  });
}
