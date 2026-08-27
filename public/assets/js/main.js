/**
 * Punkt wejścia JS — SDAUTOS demo
 */

import { initNavigation } from './navigation.js';
import { initContactForm } from './contact-form.js';
import { initGallery } from './gallery.js';
import { initProductFilters } from './products.js';

function boot() {
  initNavigation();
  initContactForm();
  initGallery();
  initProductFilters();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', boot);
} else {
  boot();
}
