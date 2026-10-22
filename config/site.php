<?php
/**
 * Konfiguracja witryny SDAUTOS — dane demonstracyjne
 * Pola oznaczone [DO UZUPEŁNIENIA] należy uzupełnić przed produkcją.
 */

return [
    'site_name' => 'SDAUTOS',
    'tagline' => 'Lakiernictwo samochodowe i materiały lakiernicze',
    'base_url' => 'http://localhost:8000', // [DO UZUPEŁNIENIA] URL produkcyjny
    'locale' => 'pl_PL',
    'language' => 'pl',

    // Dane kontaktowe
    'contact' => [
        'company' => 'SDAUTOS',
        'address' => 'Rdziostów 85',
        'postal_code' => '33-393',
        'city' => 'Rdziostów',
        'phone' => '788 488 521',
        'email' => 'sdautos@o2.pl',
        'hours' => '[DO UZUPEŁNIENIA]',
        'nip' => '[DO UZUPEŁNIENIA]',
        'regon' => '[DO UZUPEŁNIENIA]',
    ],

    // Social media — placeholdery (pusty href = brak linku)
    'social' => [
        'facebook' => '#',  // [DO UZUPEŁNIENIA]
        'instagram' => '#', // [DO UZUPEŁNIENIA]
        'linkedin' => '#',  // [DO UZUPEŁNIENIA]
        'youtube' => '#',   // [DO UZUPEŁNIENIA]
    ],

    // Nawigacja główna
    'nav' => [
        ['label' => 'Strona główna', 'href' => '/index.php', 'id' => 'home'],
        ['label' => 'Lakiernictwo', 'href' => '/lakiernictwo.php', 'id' => 'lakiernictwo'],
        ['label' => 'Materiały lakiernicze', 'href' => '/materialy.php', 'id' => 'materialy'],
        ['label' => 'Produkty', 'href' => '/produkty.php', 'id' => 'produkty'],
        ['label' => 'Pigmenty 2K', 'href' => '/pigmenty-autocolor.php', 'id' => 'pigmenty'],
        ['label' => 'O nas', 'href' => '/o-nas.php', 'id' => 'o-nas'],
        ['label' => 'Realizacje', 'href' => '/realizacje.php', 'id' => 'realizacje'],
        ['label' => 'Kontakt', 'href' => '/kontakt.php', 'id' => 'kontakt'],
    ],
];
