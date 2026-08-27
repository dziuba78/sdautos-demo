/**
 * Prosta galeria z dialogiem (bez ciężkich bibliotek)
 */

export function initGallery() {
  const root = document.querySelector('[data-gallery]');
  if (!root) return;

  const dialog = root.querySelector('[data-gallery-dialog]');
  const dialogMedia = root.querySelector('[data-gallery-media]');
  const dialogCaption = root.querySelector('[data-gallery-caption]');
  const closeBtn = root.querySelector('[data-gallery-close]');

  if (!dialog || !dialogMedia) return;

  root.querySelectorAll('[data-gallery-item]').forEach((item) => {
    item.addEventListener('click', () => {
      const src = item.getAttribute('data-full') || '';
      const caption = item.getAttribute('data-caption') || '';
      const alt = item.getAttribute('data-alt') || caption || 'Podgląd realizacji';

      dialogMedia.innerHTML = '';
      if (src.endsWith('.svg') || src.includes('placeholder')) {
        const img = document.createElement('img');
        img.src = src;
        img.alt = alt;
        img.width = 1200;
        img.height = 900;
        dialogMedia.appendChild(img);
      } else {
        const img = document.createElement('img');
        img.src = src;
        img.alt = alt;
        img.width = 1200;
        img.height = 900;
        dialogMedia.appendChild(img);
      }

      if (dialogCaption) dialogCaption.textContent = caption;
      if (typeof dialog.showModal === 'function') {
        dialog.showModal();
      }
    });
  });

  closeBtn?.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', (event) => {
    if (event.target === dialog) dialog.close();
  });
}
