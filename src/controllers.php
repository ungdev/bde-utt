<?php

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\RedirectResponse;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;
use GuzzleHttp\Client;
use GuzzleHttp\Exception\GuzzleException;

Request::setTrustedProxies(array('127.0.0.1'));

$app['dolibarr'] = new Dolibarr($app);
$app['etupay.decrypt']= $app->protect(function (string $payload) use ($app)
{
    $crypt = new \Illuminate\Encryption\Encrypter(base64_decode($app['etupay.key']), 'AES-256-CBC');
    $payload = json_decode($crypt->decrypt($payload));
    if ($payload && !is_null($payload->service_data))
        return $payload;

    return null;
});

/**
 * Login middleware
 */

$login_required = function (Request $request, \Silex\Application $app) {
    if(!$app['session']->has('user'))
    {
        $app['session']->getFlashBag()->add('error', $app['translator']->trans('error.no_connected'));
        return new RedirectResponse($app['url_generator']->generate('home'));
    }
};

$api_hmac = function (Request $request, \Silex\Application $app) {
    $query_param = $request->query->all();
    unset($query_param['key']);
    unset($query_param['expiration']);
    asort($query_param);
    $payload = json_encode([$request->getPathInfo(),$query_param]);
    $hmac = hash_hmac('sha256', $payload, $app['app_key']);

    if($request->query->get('key', '') !=  $hmac)
        return $app->json(['error' => 'You must be authentificated.'], 401);

    if($request->query->get('expiration', time()) <  time())
        return $app->json(['error' => 'Token expired.'], 403);

};

$refresh_profil = function (Request $request, \Silex\Application $app) {
    if($app['session']->has('dolibarr'))
    {
        $temp = $dolibarr = $app['dolibarr']->getMemberByLogin($app['session']->get('dolibarr')['login']);
        if($temp) {
            $app['session']->set('dolibarr', $temp);
            $app['session']->set('subscription_active', $temp['subscription_active']);
        }
    }
};
/**
 * API
 */

$app->get('/api/v1/members/', function (Request $request) use ($app) {
    $members = $app['dolibarr']->getMemberAtDate($request->query->get('dateend', null));
    $return = [];
    foreach ($members as $member)
    {
        if($member['datefin'] > $request->query->get('dateend', time())) {
            switch ($request->query->get('algo', 'md5')) {
                case 'md5':
                    $return[] = md5($member['email']);
                    break;
                case 'sha1':
                    $return[] = sha1($member['email']);
                    break;
            }
        }
    }
    return $app->json($return, 200);
})->bind('api_members')->before($api_hmac);

$app->get('/api/v1/user/profile', function (Request $request) use ($app) {
    $client = new Client([
        'base_uri' => 'https://etu.utt.fr',
        'auth' => [
            $app['etuutt.id'],
            $app['etuutt.secret']
        ]
    ]);
    try {
        $refresh = $client->post('/api/oauth/token', [ 'form_params' => [
            'grant_type' => 'refresh_token',
            'refresh_token' => $app['session']->get('user.etuRefreshToken')
        ]]);
        $json = json_decode($refresh->getBody()->getContents(), true)['response'];
        $app['session']->set('user.etuRefreshToken', $json['refresh_token']);
    
        $url = '/api/public/users/image/' . $app['session']->get('user')['login'] . '_official.jpg?access_token=' . $json['access_token'];
        $avatar = $client->get($url);
    } catch (GuzzleException $e) {
        return new Response('Unable to access profile picture', 403);
    }
    $response = new Response($avatar->getBody(), 200);
    $response->headers->set('Content-Type', 'image/jpeg');
    return $response;
})->before($login_required);

/**
 * Controllers
 */

$app->get('/', function () use ($app) {
    return new RedirectResponse($app['url_generator']->generate('home'));
})->bind('default');

$app->get('/{_locale}', function () use ($app) {
    return $app['twig']->render('cover.html.twig', array());
})->bind('home')
->assert('_locale', '[a-zA-Z]{2}');

// changement de langue
$app->get('/langue/{locale}', function ($locale) use ($app) {
    $app['translator']->setLocale($locale);
    return $app['twig']->render('cover.html.twig', array());
})->bind('lang');

$app->get('/{_locale}/dashboard', function () use ($app) {
    return $app['twig']->render('dashboard/home.html.twig', array());
})->bind('dashboard')
    ->before($login_required)
    ->before($refresh_profil);

/**
 * EtuPay Callback
 */
$app->post('etupay/callback', function (Request $request) use ($app) {
    if($request->request->has('payload'))
        $payload = $request->request->get('payload');
    else if($request->query->has('payload'))
        $payload = $request->query->get('payload');

    if(!isset($payload))
        return new Response('Unexpected query', 402);

    $data = $app['etupay.decrypt']($payload);
    if(!$data)
        return new Response('Incorrect payload', 402);

    $data_service = explode('#', $data->service_data);
    $user = $app['dolibarr']->getMemberByLogin($data_service[0]);

    if(!in_array($data_service[1],array_keys($app['cotisations'])))
        return new Response('Incorrect cotisation', 200);

    if($data->step != 'PAID')
        return new Response('No paid', 200);

    //Création de la cotisation
    $return = $app['dolibarr']->createSubscriptionById($user['id'], $app['cotisations'][$data_service[1]]['start'], $app['cotisations'][$data_service[1]]['end'], $data->amount/100, 'EtuPay #'.$data->transaction_id);

    return new Response('OK');

})->bind('etupay_callback');

$app->get('/etupay/return', function () use ($app) {
    $app['session']->getFlashBag()->add('info', $app['translator']->trans('transaction.willbeproceded'));
    return new RedirectResponse($app['url_generator']->generate('home'));
});
/**
 * Membership Letter
 */
$app->get('dashboard/lettre/{id}', function ($id, Request $request) use ($app) {
    $subscription = $app['dolibarr']->getSubscriptionById($id);
    if($subscription && $subscription['fk_adherent']==$app['session']->get('dolibarr')['id']) {
        $user = $app['dolibarr']->getMemberById($subscription['fk_adherent']);
        $options = new \Dompdf\Options();
        $options->set('defaultFont', 'Courier');
        $options->set('isRemoteEnabled', TRUE);

        $pdf = new \Dompdf\Dompdf($options);
        $template = $app['twig']->loadTemplate('letter/membership.html.twig');
        $html = $template->renderBlock('letter', [
            'request' => $request,
            'app'   =>  $app,
            'subscription'  =>  $subscription,
            'user'  => $user]);
        $pdf->loadHtml($html);
        $pdf->setPaper('A4');
        $pdf->render();
        return new Response($pdf->stream('justificatif_adhesion_'.intval($subscription['id'].'.pdf')));
    } else {
        $app['session']->getFlashBag()->add('error', $app['translator']->trans('error.happening'));
        return new RedirectResponse($app['url_generator']->generate('home'));
    }
})->bind('lettre')->before($login_required);

/**
 * Cotisations
 */

$app->get('/{_locale}/dashboard/cotiser', function () use ($app) {
    return $app['twig']->render('cotiser/index.html.twig', array());
})->bind('cotiser')->before($login_required);

$app->post('/{_locale}/dashboard/cotiser', function (Request $request) use ($app) {
    if(!in_array($request->request->get('cotisations'), ['year', 'automne', 'printemp']))
    {
        $app['session']->getFlashBag()->add('error', $app['translator']->trans('error.happening'));
        return new RedirectResponse($app['url_generator']->generate('home'));
    }

    $choice = $request->request->get('cotisations');

    //EtuPay implentation
    $crypt = new \Illuminate\Encryption\Encrypter(base64_decode($app['etupay.key']), 'AES-256-CBC');
    $payload =  $crypt->encrypt(json_encode([
        'type' => 'checkout',
        'amount'=> intval($app['cotisations'][$choice]['price'])*100,
        'client_mail' => $app['session']->get('dolibarr')['email'],
        'firstname' => $app['session']->get('dolibarr')['firstname'],
        'lastname' => $app['session']->get('dolibarr')['lastname'],
        'description' => 'Cotisation au BDE UTT',
        'articles' => [[
            'name' => ($choice=='year'?'Cotisation d\'une année':'Cotisation du semestre: '.ucfirst($choice)),
            'price' => intval($app['cotisations'][$choice]['price'])*100,
            'quantity'   => 1
        ]],
        'service_data' => $app['session']->get('dolibarr')['login'].'#'.$choice,
    ]));

    return new RedirectResponse('https://etupay.utt.fr/initiate?service_id='.$app['etupay.id'].'&payload='.$payload);

})->bind('postCotiser')->before($login_required);

/**
 * Login with EtuUTT
 */
$app->get('/login', function () use ($app) {
    return $app->redirect('https://etu.utt.fr/api/oauth/authorize?client_id='.$app['etuutt.id'].'&scopes=private_user_account private_user_organizations public_user_account&response_type=code&state=xyz');
})->bind('login');

$app->get('/{_locale}/logout', function () use ($app) {
    $app['session']->clear();
    $app['session']->getFlashBag()->add('success', $app['translator']->trans('success.logout'));
    return new RedirectResponse($app['url_generator']->generate('home'));
})->bind('logout');

$app->get('/etuutt/callback', function (Request $request) use ($app) {
    if(!$request->query->has('authorization_code'))
        return new Response('No authorisation code', 402);

    $client = new Client([
        'base_uri' => 'https://etu.utt.fr',
        'auth' => [
            $app['etuutt.id'],
            $app['etuutt.secret']
        ]
    ]);

    $params = [
        'grant_type'         => 'authorization_code',
        'authorization_code' => $request->query->get('authorization_code')
    ];
    try {
        $response = $client->post('/api/oauth/token', ['form_params' => $params]);
    } catch (GuzzleException $e) {
        // An error 400 from the server is usual when the authorization_code
        // has expired. Redirect the user to the OAuth gateway to be sure
        // to regenerate a new authorization_code for him :-)
        if ($e->hasResponse() && $e->getResponse()->getStatusCode() === 400) {
            return new RedirectResponse('/login');
        }
        return new Response('Unable to login', 402);
    }
    $json = json_decode($response->getBody()->getContents(), true);
    $access_token = $json['access_token'];
    $refresh_token = $json['refresh_token'];
    try {
        $response = $client->get('/api/private/user/account?access_token=' . $json['access_token']);
    } catch (GuzzleException $e) {
        return new Response('Unable to login', 402);
    }

    $json = json_decode($response->getBody()->getContents(), true)['data'];

    //Refresh
    $response = $client->post('/api/oauth/token', [ 'form_params' => [
        'grant_type' => 'refresh_token',
        'refresh_token' => $refresh_token
    ]]);
    $jsonRefreshToken = json_decode($response->getBody()->getContents(), true)['response'];

    try {
        $response = $client->get('/api/private/user/organizations?access_token=' . $jsonRefreshToken['access_token']);
    } catch (GuzzleException $e) {
        die($e->getMessage());
        return new Response('Unable to login', 402);
    }
    $organizations = json_decode($response->getBody()->getContents(), true)['data'];
    $user_organizations = [];
    foreach ($organizations as $orga)
    {
        $name = $orga['_embed']['organization'];
        $user_organizations[$name] = $orga['role'];
    }

    $dolibarr = $app['dolibarr']->getMemberByLogin($json['login']);
    
    $app['session']->set('user.etuRefreshToken', $jsonRefreshToken['refresh_token']);
    if($dolibarr) {
        $app['session']->set('dolibarr', $dolibarr);
        $app['session']->set('user', $json);
        $app['session']->set('organizations', $user_organizations);
        $app['session']->set('subscription_active', $dolibarr['subscription_active']);
    } else {
        $app['session']->getFlashBag()->add('error', $app['translator']->trans('error.happening'));
        return new RedirectResponse($app['url_generator']->generate('home'));
    }
    $app['session']->getFlashBag()->add('success', $app['translator']->trans('success.login'));
    return new RedirectResponse($app['url_generator']->generate('dashboard'));

})->bind('etuutt_login');

$app->error(function (\Exception $e, Request $request, $code) use ($app) {
    if ($app['debug']) {
        return;
    }

    // 404.html, or 40x.html, or 4xx.html, or error.html
    $templates = array(
        'errors/'.$code.'.html.twig',
        'errors/'.substr($code, 0, 2).'x.html.twig',
        'errors/'.substr($code, 0, 1).'xx.html.twig',
        'errors/default.html.twig',
    );

    return new Response($app['twig']->resolveTemplate($templates)->render(array('code' => $code)), $code);
});
