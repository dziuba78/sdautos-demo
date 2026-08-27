<?php
/**
 * Pomocnicze funkcje prezentacji danych kontaktowych
 */

/**
 * Czy wartość to jeszcze placeholder do uzupełnienia
 */
function sda_is_placeholder(?string $value): bool
{
    if ($value === null || $value === '') {
        return true;
    }
    return str_contains($value, '[DO UZUPEŁNIENIA]');
}

/**
 * Tekst z klasą placeholder tylko gdy dane nieuzupełnione
 */
function sda_display_text(?string $value): string
{
    $value = (string) $value;
    $class = sda_is_placeholder($value) ? ' class="placeholder-data"' : '';
    return '<span' . $class . '>' . htmlspecialchars($value, ENT_QUOTES, 'UTF-8') . '</span>';
}

/**
 * Link tel: — zwykły tekst, gdy brak numeru
 */
function sda_phone_link(?string $phone): string
{
    $phone = (string) $phone;
    if (sda_is_placeholder($phone)) {
        return sda_display_text($phone);
    }
    $href = 'tel:' . preg_replace('/\s+/', '', $phone);
    return '<a href="' . htmlspecialchars($href, ENT_QUOTES, 'UTF-8') . '">'
        . htmlspecialchars($phone, ENT_QUOTES, 'UTF-8') . '</a>';
}

/**
 * Link mailto:
 */
function sda_email_link(?string $email): string
{
    $email = (string) $email;
    if (sda_is_placeholder($email)) {
        return sda_display_text($email);
    }
    return '<a href="mailto:' . htmlspecialchars($email, ENT_QUOTES, 'UTF-8') . '">'
        . htmlspecialchars($email, ENT_QUOTES, 'UTF-8') . '</a>';
}
