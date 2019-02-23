<?php

use Silex\Provider\MonologServiceProvider;
use Silex\Provider\WebProfilerServiceProvider;

// include the prod configuration
require __DIR__.'/prod.php';

// enable the debug mode
$app['debug'] = true;

$app->register(new MonologServiceProvider(), array(
    'monolog.logfile' => __DIR__.'/../var/logs/silex_dev.log',
));

$app->register(new WebProfilerServiceProvider(), array(
    'profiler.cache_dir' => __DIR__.'/../var/cache/profiler',
));


$app['dolikey'] = 'e432ada9a9857310041b6d3d69064261';
$app['etupay.id'] = 14;
$app['etupay.key'] = '0FrcAOHY2CQqhE28/D4pzMOnixo3cedQjCFUbsBJT8c=';
$app['etuutt.id'] = '49531438000';
$app['etuutt.secret'] = 'df310aa7bf70c90f8e434b20bd2091e9';

/*
$app['swiftmailer.options'] = array(
    'host' => '127.0.0.1',
    'port' => '1025',
    'username' => null,
    'password' => null,
    'encryption' => null,
    'auth_mode' => null
);*/