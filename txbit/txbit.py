import hashlib
import hmac
import json
import requests
import urllib.parse

from time import time

class TxbitResponse:
    def __init__(self, success, message, result):
        self.success = success
        self.message = message
        self.result = result

    def __str__(self):
        d = {
            'success': self.success,\
            'message': self.message,\
            'result': self.result
        }
        return str(json.dumps(d, indent = 4))

class Txbit:
    endpoint = 'https://api.txbit.io/api/'

    def __init__(self, APIKey, Secret):
        self.APIKey = APIKey
        self.Secret = Secret

    def expandPathToUrl(path, params = {}):
        url = Txbit.endpoint + path + '?'

        for key in params:
            url += key + "=" + params[key] + "&"

        return url

    def request(path, params = {}):
        url = Txbit.expandPathToUrl(path, params)
        r = requests.get(url)
        return TxbitResponse(r.ok, "", r.json()['result'] if r.ok else r.status_code)

    ## PUBLIC FUNCTIONS ---------------
    def getMarkets():
        res = Txbit.request('public/getmarkets')
        return { m['MarketCurrency']: m for m in res.result } if res.success else res.result

    def getCurrencies():
        res = Txbit.request('public/getcurrencies')
        return { m['Currency']: m for m in res.result } if res.success else res.result

    def getMarketSummaries():
        res = Txbit.request('public/getmarketsummaries')
        return { m['MarketName']: m for m in res.result } if res.success else res.result

    def getExchangePairs():
        markets = Txbit.getMarketSummaries()
        return [markets[m]['MarketName'] for m in markets]

    def getOrderBook(market, bookType='both'):
        params = { 'market': market, 'type': bookType}
        res = Txbit.request('public/getorderbook', params)
        return { market: res } if res.success else res.result

    def getTicker(market):
        params = { 'market': market}
        res = Txbit.request('public/getticker', params)
        return { market: res } if res.success else res.result

    def getMarketHistory(market):
        params = { 'market': market}
        res = Txbit.request('public/getmarkethistory', params)
        return { market: res } if res.success else res.result

    def getSystemStatus():
        res = Txbit.request('public/getsystemstatus')
        return { 'status': res } if res.success else res.result

    def getCurrencyInformation(currency):
        params = { 'currency': currency}
        res = Txbit.request('public/getcurrencyinformation')
        return { currency: res } if res.success else res.result

    def getCurrencyBalanceSheet(currency):
        params = { 'currency': currency}
        res = Txbit.request('public/getcurrencybalancesheet')
        return { currency: res } if res.success else res.result


    ## MARKET FUNCTIONS ---------------
    '''
    --- TODO --- Outstanding Market Functions
    /account/getdepositaddress
    /account/withdraw
    /account/getorder
    /account/getorderhistory
    /account/getwithdrawalhistory
    /account/getdeposithistory
    '''

    ## ACOUNT FUNCTIONS ---------------

    def authenticatedRequest(self, path, params = {}):
        params['apikey'] = self.APIKey
        params['nonce'] = str(int(time()))

        url = Txbit.expandPathToUrl(path, params)

        apisign = hmac.new(bytes(self.Secret, 'utf-8'),
                           bytes(url, 'utf-8'),
                           hashlib.sha512).hexdigest().upper()

        headers = { 'apisign': apisign }

        r = requests.get(url, headers=headers)
        return TxbitResponse(r.ok, "", r.json()['result'] if r.ok else r.status_code)


    def getBalances(self):
        path = 'account/getbalances'
        return self.authenticatedRequest(path)

    def getBalanceFor(self, currency):
        path = 'account/getbalance'
        params = { 'currency': currency }
        return self.authenticatedRequest(path, params)
