<?php
/**
 * Endpoint demonstracyjny formularza kontaktowego
 * Nie wysyła e-maili. Waliduje dane i zwraca JSON.
 */
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'message' => 'Dozwolona jest tylko metoda POST.']);
    exit;
}

/**
 * Długość tekstu (mbstring opcjonalne — domyślne buildy Windows bywają bez mbstring)
 */
function sda_len(string $value): int
{
    return function_exists('mb_strlen') ? mb_strlen($value, 'UTF-8') : strlen($value);
}

function sda_cut(string $value, int $max): string
{
    if (function_exists('mb_substr')) {
        return mb_substr($value, 0, $max, 'UTF-8');
    }
    return substr($value, 0, $max);
}

/**
 * Pobiera i czyści pole tekstowe
 */
function field(string $key, int $max = 2000): string
{
    $raw = $_POST[$key] ?? '';
    if (!is_string($raw)) {
        return '';
    }
    $value = trim($raw);
    $value = strip_tags($value);
    if (sda_len($value) > $max) {
        $value = sda_cut($value, $max);
    }
    return $value;
}

// Honeypot
if (field('website', 100) !== '') {
    http_response_code(400);
    echo json_encode(['ok' => false, 'message' => 'Żądanie odrzucone.']);
    exit;
}

$name = field('name', 120);
$email = field('email', 180);
$phone = field('phone', 40);
$subject = field('subject', 200);
$message = field('message', 5000);
$consent = isset($_POST['consent']) && (string) $_POST['consent'] === '1';
$csrf = field('csrf_token', 64);

$errors = [];
if (sda_len($name) < 2) {
    $errors['name'] = 'Podaj imię.';
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $errors['email'] = 'Nieprawidłowy e-mail.';
}
if ($phone !== '' && !preg_match('/^[0-9+\s()-]{9,20}$/', $phone)) {
    $errors['phone'] = 'Nieprawidłowy telefon.';
}
if (sda_len($subject) < 3) {
    $errors['subject'] = 'Podaj temat.';
}
if (sda_len($message) < 10) {
    $errors['message'] = 'Wiadomość jest zbyt krótka.';
}
if (!$consent) {
    $errors['consent'] = 'Wymagana zgoda.';
}
if ($csrf === '' || !preg_match('/^[a-f0-9]{32}$/', $csrf)) {
    // W demo token jest jednorazowy z formularza (bez sesji) — sprawdzamy format.
    // Przed produkcją: sesja PHP + hash_equals.
    $errors['csrf'] = 'Nieprawidłowy token bezpieczeństwa.';
}

if ($errors !== []) {
    http_response_code(422);
    echo json_encode([
        'ok' => false,
        'message' => 'Formularz zawiera błędy.',
        'errors' => $errors,
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

// Demo: brak wysyłki e-mail / zapisu do bazy
echo json_encode([
    'ok' => true,
    'message' => 'Dziękujemy. To jest demonstracyjny komunikat — wiadomość nie została wysłana do prawdziwego odbiorcy.',
], JSON_UNESCAPED_UNICODE);
