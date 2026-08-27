/**
 * Formularz kontaktowy — tryb demo (bez prawdziwej wysyłki)
 */

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function initContactForm() {
  const form = document.querySelector('[data-contact-form]');
  if (!form) return;

  const status = form.querySelector('[data-form-status]');
  const submitBtn = form.querySelector('[type="submit"]');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    clearErrors(form);
    if (status) {
      status.hidden = true;
      status.textContent = '';
      status.className = '';
    }

    const data = new FormData(form);
    const errors = validate(data);

    if (Object.keys(errors).length > 0) {
      showErrors(form, errors);
      const firstInvalid = form.querySelector('.is-invalid input, .is-invalid select, .is-invalid textarea');
      firstInvalid?.focus();
      return;
    }

    if (submitBtn) submitBtn.disabled = true;

    try {
      const response = await fetch(form.action || '/api/contact-demo.php', {
        method: 'POST',
        body: data,
        headers: { Accept: 'application/json' },
      });

      const payload = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(payload.message || 'Nie udało się wysłać formularza demonstracyjnego.');
      }

      form.reset();
      if (status) {
        status.hidden = false;
        status.className = 'form-success';
        status.textContent =
          payload.message ||
          'Dziękujemy. To jest demonstracyjny komunikat — wiadomość nie została wysłana do prawdziwego odbiorcy.';
      }
    } catch (err) {
      if (status) {
        status.hidden = false;
        status.className = 'form-error';
        status.textContent = err.message || 'Wystąpił błąd. Spróbuj ponownie.';
      }
    } finally {
      if (submitBtn) submitBtn.disabled = false;
    }
  });
}

function validate(data) {
  const errors = {};
  const name = String(data.get('name') || '').trim();
  const email = String(data.get('email') || '').trim();
  const phone = String(data.get('phone') || '').trim();
  const subject = String(data.get('subject') || '').trim();
  const message = String(data.get('message') || '').trim();
  const consent = data.get('consent');

  if (name.length < 2) errors.name = 'Podaj imię (min. 2 znaki).';
  if (!EMAIL_RE.test(email)) errors.email = 'Podaj prawidłowy adres e-mail.';
  if (phone && phone.replace(/\D/g, '').length < 9) errors.phone = 'Podaj prawidłowy numer telefonu.';
  if (subject.length < 3) errors.subject = 'Podaj temat wiadomości.';
  if (message.length < 10) errors.message = 'Wiadomość powinna mieć co najmniej 10 znaków.';
  if (!consent) errors.consent = 'Wymagana jest zgoda na przetworzenie danych.';

  // Honeypot — boty wypełniają ukryte pole
  if (String(data.get('website') || '').trim() !== '') {
    errors.website = 'Wykryto niedozwolone pole.';
  }

  return errors;
}

function showErrors(form, errors) {
  Object.entries(errors).forEach(([field, message]) => {
    const wrap = form.querySelector(`[data-field="${field}"]`);
    if (!wrap) return;
    wrap.classList.add('is-invalid');
    const err = wrap.querySelector('[data-error]');
    if (err) err.textContent = message;
  });
}

function clearErrors(form) {
  form.querySelectorAll('.form-field').forEach((wrap) => {
    wrap.classList.remove('is-invalid');
    const err = wrap.querySelector('[data-error]');
    if (err) err.textContent = '';
  });
}
