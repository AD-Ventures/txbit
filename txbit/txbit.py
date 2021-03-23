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
        url = Txbit.endpoint + path
        url += '?' if params else ''

        for key in params:
            url += key + "=" + params[key] + "&"

        return url

    def request(path, params = {}):
        url = Txbit.expandPathToUrl(path, params)
        return requests.get(url)

    ## PUBLIC FUNCTIONS ---------------
    def getMarkets():
        res = Txbit.request('public/getmarkets')
        result = { m['MarketCurrency']: m for m in res.json()['result'] } if res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getCurrencies():
        res = Txbit.request('public/getcurrencies')
        result = { m['Currency']: m for m in res.json()['result'] } if res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getMarketSummaries():
        res = Txbit.request('public/getmarketsummaries')
        result = { m['MarketName']: m for m in res.json()['result'] } if res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getExchangePairs():
        res = Txbit.getMarketSummaries()
        res.result = [res.result[m]['MarketName'] for m in res.result]
        return res

    def getOrderBook(market, bookType='both'):
        params = { 'market': market, 'type': bookType}
        res = Txbit.request('public/getorderbook', params)
        result = { market: res.json()['result'] } if res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getTicker(market):
        params = { 'market': market}
        res = Txbit.request('public/getticker', params)
        result = { market: res.json()['result'] } if res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getMarketHistory(market):
        params = { 'market': market}
        res = Txbit.request('public/getmarkethistory', params)
        result = { market: res.json()['result'] } if res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getSystemStatus():
        res = Txbit.request('public/getsystemstatus')
        result = { 'status': res.json()['result'] } if res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getCurrencyInformation(currency):
        params = { 'currency': currency}
        res = Txbit.request('public/getcurrencyinformation')
        result = { currency: res.json()['result'] } if res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getCurrencyBalanceSheet(currency):
        params = { 'currency': currency}
        res = Txbit.request('public/getcurrencybalancesheet')
        result = { currency: res.json()['result'] } if res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)


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
        return requests.get(url, headers=headers)

    def getBalances(self):
        path = 'account/getbalances'
        res = self.authenticatedRequest(path)
        result = res.json()['result'] if res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getBalanceFor(self, currency):
        path = 'account/getbalance'
        params = { 'currency': currency }
        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)
