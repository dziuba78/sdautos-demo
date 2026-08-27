<?php
/**
 * Schema.org LocalBusiness — placeholdery bez wymyślonych danych
 * @var array $site
 */
$c = $site['contact'];
$schema = [
    '@context' => 'https://schema.org',
    '@type' => 'AutomotiveBusiness',
    'name' => $site['site_name'],
    'description' => $site['tagline'],
    'url' => rtrim($site['base_url'], '/'),
    'image' => rtrim($site['base_url'], '/') . '/assets/images/og-default.webp',
    'address' => [
        '@type' => 'PostalAddress',
        'streetAddress' => $c['address'],
        'postalCode' => $c['postal_code'],
        'addressLocality' => $c['city'],
        'addressCountry' => 'PL',
    ],
    'telephone' => '+48' . preg_replace('/\s+/', '', $c['phone']),
    'email' => $c['email'],
    // openingHoursSpecification — uzupełnić po otrzymaniu godzin
];
?>
<script type="application/ld+json">
<?= json_encode($schema, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT) ?>
</script>
