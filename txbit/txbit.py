import hashlib
import hmac
import json
import requests

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
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getCurrencies():
        res = Txbit.request('public/getcurrencies')
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getMarketSummaries():
        res = Txbit.request('public/getmarketsummaries')
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getExchangePairs():
        res = Txbit.getMarketSummaries()
        res.result = [pair['MarketName'] for pair in res.result]
        return res

    def getOrderBook(market, bookType='both'):
        params = {'market': market, 'type': bookType}
        res = Txbit.request('public/getorderbook', params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getTicker(market):
        params = {'market': market}
        res = Txbit.request('public/getticker', params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getMarketHistory(market):
        params = {'market': market}
        res = Txbit.request('public/getmarkethistory', params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getSystemStatus():
        res = Txbit.request('public/getsystemstatus')
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getCurrencyInformation(currency):
        params = {'currency': currency}
        res = Txbit.request('public/getcurrencyinformation', params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getCurrencyBalanceSheet(currency):
        params = {'currency': currency}
        res = Txbit.request('public/getcurrencybalancesheet', params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

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
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getBalanceFor(self, currency):
        path = 'account/getbalance'
        params = { 'currency': currency }
        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getDepositAddress(self, currency):
        path = 'account/getdepositaddress'
        params = { 'currency': currency }
        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def withdraw(self, currency, quantity, address, paymentid = None):
        path = 'account/withdraw'
        params = {'currency': currency, 'quantity': quantity, 'address': address}

        if paymentid is not None:
            params['paymentid'] = paymentid

        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getOrder(self, uuid):
        path = 'account/getorder'
        params = { 'uuid': uuid }
        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getOrderHistory(self, market = None):
        path = 'account/getorderhistory'
        params = {}

        if market is not None:
            params['market'] = market

        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getWithdrawlHistory(self, currency = None):
        path = 'account/getwithdrawalhistory'
        params = { }

        if currency is not None:
            params['currency'] = currency

        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getDepositHistory(self, currency = None):
        path = 'account/getdeposithistory'
        params = { }

        if currency is not None:
            params['currency'] = currency

        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    ## MARKET FUNCTIONS ---------------

    def buyLimit(self, market, quantity, rate):
        path = 'market/buylimit'
        params = {'market': market, 'quantity': quantity, 'rate': rate}
        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def sellLimit(self, market, quantity, rate):
        path = 'market/selllimit'
        params = {'market': market, 'quantity': quantity, 'rate': rate}
        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def cancel(self, uuid):
        path = 'market/cancel'
        params = {'uuic': uuic}
        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getOpenOrders(self, market = None):
        path = 'getopenorders'
        params = {}

        if market is not None:
            params['market'] = market

        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)
