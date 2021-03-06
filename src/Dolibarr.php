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

    public function getMemberAtDate($date = null)
    {
        if(!$date)
            $date = time();
        $sqlfilters = '(t.datefin:>:'.$date.')';
        try {
            $response = $this->client->get('api/index.php/members?sortfield=t.rowid&sortorder=ASC&limit=99999999999999999&sqlfilters=t.datefin%20%3E%20'.$date);
        } catch (GuzzleException $e) {
            return null;
        }
        $json = json_decode($response->getBody()->getContents(), true);

        if(isset($json['error']))
            return null;
        else return $json;

    }
    public function getMembers()
    {
        $url = 'https://picsou.uttnetgroup.fr/api/index.php/members?limit=500&DOLAPIKEY='.$this->app['dolikey'].'&page=';
        $page = 0;

        $resp = [];
        while($data_temp = @file_get_contents($url.$page))
        {
            $resp = array_merge($resp, json_decode($data_temp, true));
            $page++;
        }

        return $resp;
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
            $response = $this->client->post('api/index.php/subscriptions', [
                'form_params' => [
                    'dateh' => strtotime($start),
                    'fk_adherent' => $id,
                    'datef'  =>  $end,
                    'note' =>  'Adhésion en ligne ('.$payment.')',
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