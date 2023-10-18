<?php

// configure your app for the production environment
$app['debug'] = false;
define('DOMPDF_ENABLE_AUTOLOAD', false);

$app['twig.path'] = array(__DIR__.'/../templates');
$app['twig.options'] = array('cache' => __DIR__.'/../var/cache/twig');

$app->register(new \Silex\Provider\MonologServiceProvider(), array(
    'monolog.logfile' => 'php://stderr',
    'monolog.level' => \Monolog\Logger::WARNING,
));

$app['etuutt.id'] = getenv('ETUUTT_ID');
$app['etuutt.secret'] = getenv('ETUUTT_SECRET');
$app['dolikey'] = getenv('DOLIKEY');

$temp['cotisations'] = [
        'automne' => [
            'start' => '01 september ',
            'last'   =>  5,
            'price' =>  15
        ],
        'printemp' => [
            'start' => '01 february ',
            'last'   =>  8,
            'price' =>  15
        ],
        'year' => [
            'last'   =>  13,
            'price' =>  30
        ]
];

//Calcul des dates de fin
if(date('n') == 1)
    $temp['cotisations']['automne']['start'] .= (date('Y') - 1);
else
    $temp['cotisations']['automne']['start'] .= date('Y');

if(date('n') >= 8)
    $temp['cotisations']['printemp']['start'] .= (date('Y') + 1);
else
    $temp['cotisations']['printemp']['start'] .= date('Y');

$temp['cotisations.actuel']['actuel'] = ((strtotime('now') < strtotime($temp['cotisations']['automne']['start']))? 'printemp':'automne');

$temp['cotisations']['printemp']['end'] = strtotime($temp['cotisations']['printemp']['start'].' +'.$temp['cotisations']['printemp']['last'].' months');
$temp['cotisations']['automne']['end'] = strtotime($temp['cotisations']['automne']['start'].' +'.$temp['cotisations']['automne']['last'].' months');

if(date('n') > 6)
    $temp['cotisations']['year']['start'] = $temp['cotisations']['automne']['start'];
else
    $temp['cotisations']['year']['start'] = $temp['cotisations']['printemp']['start'];
$temp['cotisations']['year']['end'] = strtotime($temp['cotisations']['year']['start'].' +'.$temp['cotisations']['year']['last'].' months');

//Calcul des dates de début actualisé
foreach ($temp['cotisations'] as $month=>$value)
{
    if(strtotime('now') > strtotime($temp['cotisations'][$month]['start']))
        $temp['cotisations'][$month]['start'] = date('d F Y');
}

$app['cotisations'] = $temp['cotisations'];

$app['app_key'] = getenv('APP_KEY');

$app['etupay.id'] = getenv('ETUPAY_ID');
$app['etupay.key'] = getenv('ETUPAY_KEY');
$app['lang.flags'] = [
    'fr'    => 'fr',
    'en'    => 'gb',
    'cn'    =>  'cn'
];

$app['locale'] = 'fr';

$app['swiftmailer.options'] = array(
    'host' => 'smtp.utt.fr',
    'port' => '25',
    'username' => null,
    'password' => null,
    'encryption' => null,
    'auth_mode' => null
);