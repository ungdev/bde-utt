<?php

use GuzzleHttp\Client;
use GuzzleHttp\Exception\GuzzleException;

class Dolibarr
{
    protected $app;
    protected $client;

    public function __construct(&$app)
    {
        $this->app = &$app;
        $this->client = new Client([
            'base_uri' => 'https://picsou.uttnetgroup.fr/',
            'headers' => ['DOLAPIKEY' => $app['dolikey']]
        ]);
    }

    public function getMemberByLogin($login)
    {
        try {
            $response = $this->client->get('api/index.php/members', [
                'query' => [
                    'sqlfilters' => "(t.login:=:'" . $login . "')"
                ]
            ]);
        } catch (GuzzleException $e) {
            return null;
        }
        $json = json_decode($response->getBody()->getContents(), true)[0];

        // Test subscription
        $json['subscription_active'] = ($json['last_subscription_date'] && $json['datefin'] && (time() >= strtotime($json['last_subscription_date']) ) && (time() <= $json['datefin']));
        if(isset($json['error']))
            return null;
        else return $json;
    }

    public function getMemberByEmail($mail)
    {
        try {
            $response = $this->client->get('api/index.php/members', [
                'query' => [
                    'sqlfilters' => "(t.email:=:'" . $mail . "')"
                ]
            ]);
        } catch (GuzzleException $e) {
            return null;
        }
        $json = json_decode($response->getBody()->getContents(), true)[0];

        // Test subscription
        $json['subscription_active'] = ($json['last_subscription_date'] && $json['datefin'] && (time() >= strtotime($json['last_subscription_date']) ) && (time() <= $json['datefin']));

        if(isset($json['error']))
            return null;
        else return $json;
    }

    public function getMemberById($id)
    {
        try {
            $response = $this->client->get('api/index.php/members/'.intval($id));
        } catch (GuzzleException $e) {
            return null;
        }
        $json = json_decode($response->getBody()->getContents(), true);

        // Test subscription
        $json['subscription_active'] = ($json['last_subscription_date'] && $json['datefin'] && (time() >= strtotime($json['last_subscription_date']) ) && (time() <= $json['datefin']));

        if(isset($json['error']))
            return null;
        else return $json;
    }

    public function getMembers()
    {
        try {
            $response = $this->client->get('api/index.php/members/');
        } catch (GuzzleException $e) {
            return null;
        }
        $json = json_decode($response->getBody()->getContents(), true);

        if(isset($json['error']))
            return null;
        else return $json;
    }

    public function getSubscriptionsById($id)
    {
        try {
            $response = $this->client->get('api/index.php/members/'.intval($id).'/subscriptions');
        } catch (GuzzleException $e) {
            return null;
        }
        $json = json_decode($response->getBody()->getContents(), true);

        if(isset($json['error']))
            return null;
        else return $json;
    }

    public function getSubscriptionById($id)
    {
        try {
            $response = $this->client->get('api/index.php/subscriptions/'.intval($id));
        } catch (GuzzleException $e) {
            return null;
        }
        $json = json_decode($response->getBody()->getContents(), true);

        if(isset($json['error']))
            return null;
        else return $json;
    }

    public function createSubscriptionById($id, $start, $end, $amount, $payment=null)
    {
        try {
            $response = $this->client->post('api/index.php/members/'.$id.'/subscriptions', [
                'form_params' => [
                    'start_date' => strtotime($start),
                    'end_date'  =>  $end,
                    'label' =>  'Adhésion en ligne ('.$payment.')',
                    'amount'    =>  $amount
                ]
            ]);
        } catch (GuzzleException $e) {
            return null;
        }
        $json = json_decode($response->getBody()->getContents(), true);

        if(isset($json['error']))
            return null;
        else return $json;
    }

    public function _request()
    {
        /**
        try {
            $response = $client->get('/api/private/user/account?access_token=' . $json['access_token']);
        } catch (GuzzleException $e) {
            abort(500);
        }
        $json = json_decode($response->getBody()->getContents(), true)['data'];
         **/
    }
}