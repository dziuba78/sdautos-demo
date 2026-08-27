<?php
/**
 * Wspólny <head> — SEO, CSS, fonty
 * @var array $site
 * @var string $pageTitle
 * @var string $pageDescription
 * @var string $canonicalPath
 * @var string $ogType
 * @var string $activeNav
 */

if (!isset($site)) {
    $site = require dirname(__DIR__) . '/config/site.php';
}

require_once dirname(__DIR__) . '/includes/helpers.php';

$pageTitle = $pageTitle ?? ($site['site_name'] . ' — ' . $site['tagline']);
$pageDescription = $pageDescription ?? 'SDAUTOS — profesjonalne lakiernictwo samochodowe, materiały lakiernicze oraz wyposażenie dla lakierników. [DO UZUPEŁNIENIA]';
$canonicalPath = $canonicalPath ?? '/index.php';
$ogType = $ogType ?? 'website';
$activeNav = $activeNav ?? '';
$baseUrl = rtrim($site['base_url'], '/');
$canonical = $baseUrl . $canonicalPath;
?>
<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title><?= htmlspecialchars($pageTitle, ENT_QUOTES, 'UTF-8') ?></title>
  <meta name="description" content="<?= htmlspecialchars($pageDescription, ENT_QUOTES, 'UTF-8') ?>">
  <link rel="canonical" href="<?= htmlspecialchars($canonical, ENT_QUOTES, 'UTF-8') ?>">
  <meta name="robots" content="index, follow">

  <!-- Open Graph -->
  <meta property="og:type" content="<?= htmlspecialchars($ogType, ENT_QUOTES, 'UTF-8') ?>">
  <meta property="og:locale" content="pl_PL">
  <meta property="og:site_name" content="<?= htmlspecialchars($site['site_name'], ENT_QUOTES, 'UTF-8') ?>">
  <meta property="og:title" content="<?= htmlspecialchars($pageTitle, ENT_QUOTES, 'UTF-8') ?>">
  <meta property="og:description" content="<?= htmlspecialchars($pageDescription, ENT_QUOTES, 'UTF-8') ?>">
  <meta property="og:url" content="<?= htmlspecialchars($canonical, ENT_QUOTES, 'UTF-8') ?>">
  <meta property="og:image" content="<?= htmlspecialchars($baseUrl . '/assets/images/og-default.webp', ENT_QUOTES, 'UTF-8') ?>">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="<?= htmlspecialchars($pageTitle, ENT_QUOTES, 'UTF-8') ?>">
  <meta name="twitter:description" content="<?= htmlspecialchars($pageDescription, ENT_QUOTES, 'UTF-8') ?>">
  <meta name="twitter:image" content="<?= htmlspecialchars($baseUrl . '/assets/images/og-default.webp', ENT_QUOTES, 'UTF-8') ?>">

  <!-- Fonty self-hosted -->
  <link rel="preload" href="/assets/fonts/barlow-condensed-600.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/source-sans-3-400.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/css/fonts.css">

  <link rel="stylesheet" href="/vendor/bootstrap/css/bootstrap.min.css">
  <link rel="stylesheet" href="/assets/css/tokens.css">
  <link rel="stylesheet" href="/assets/css/main.css">
  <link rel="stylesheet" href="/assets/css/responsive.css">

  <link rel="icon" href="/assets/icons/favicon.svg" type="image/svg+xml">
</head>
<body>
<a class="skip-link" href="#main">Przejdź do treści</a>
