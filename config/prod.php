<?php

// configure your app for the production environment
$app['debug'] = false;

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
            'price' =>  20
        ],
        'printemp' => [
            'start' => '01 february ',
            'last'   =>  8,
            'price' =>  20
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

$app['etupay.id'] = getenv('ETUPAY_ID');
$app['etupay.key'] = getenv('ETUPAY_KEY');