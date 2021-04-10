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
    """A class to interact with the Txbit.io API

    Attributes
    ----------
    endpoint : str
        the base url for API calls
    APIKey : str
        key for working with the Market and Account methods
    Secret : str
        secret for working with the Market and Account methods

    Methods
    -------
    expandPathToUrl(path, params={}):
       adds onto the base url for specific methods
    request(path, params={}):
        uses `expandPathToUrl()` to make the API call
    authenticatedRequest(path, params={})
        authenticated API call with APIKey and Secret for Market and Account methods
    getMarkets():
        get the open and available trading markets along with other meta data
    getCurrencies():
        get all supported assets along with other meta data
    getMarketSummaries():
        get the last 24 hour summary of all active markets
    getExchangePairs():
        get list of all pairs that form markets
    getSystemStatus():
        get the system related status for all currencies
    getOrderBook(market, bookType='both'):
        get the orderbook for a given market
    getTicker(market):
        get current tick values for a market
    getMarketHistory(market):
        get the latest trades that have occurred for a specific market
    getCurrencyInformation(currency):
        get specific information and metadata about the listed currency
    getCurrencyBalanceSheet(currency):
        get solvency information for listed currencies
    getBalances():
        get all balances from your account
    getBalanceFor(currency):
        get the balance from your account for a specific asset
    getDepositAddress(currency):
        get or generate an address for a specific currency
    withdraw(currency, quantity, address, paymentid=None):
        withdraw funds from your account
    getOrder(uuic):
        get a single order by uuid
    getOrderHistory(market):
        get your order history
    getWithdrawlHistory(currency):
        get your withdrawal history
    getDepositHistory(currency):
        get your deposit history
    butLimit(market, quantity, rate):
        place a Buy Limit order in a specific market
    sellLimit(market, quantity, rate):
        place a Sell Limit order in a specific market
    cancel(uuid):
        cancel a buy or sell order
    getOpenOrders(market):
        get all orders that you currently have opened

    Notes
    -----
    Public methods can be run without supplying APIKey or Secret
    Market and Account methods need APIKey and Secret for authentification
    Market methods need 'ALLOW TRADING' permission set up on the APIKey
    Account methods need 'ALLOW READING' permission set up on the APIKey
    For more information, see: https://apidocs.txbit.io/#txbit-io-api
    """
    endpoint = 'https://api.txbit.io/api/'

    def __init__(self, APIKey, Secret):
        self.APIKey = APIKey
        self.Secret = Secret

    def expandPathToUrl(path, params={}):
        """adds onto the base url for specific methods"""
        url = Txbit.endpoint + path
        url += '?' if params else ''

        for key in params:
            url += key + '=' + params[key] + '&'

        return url

    def request(path, params={}):
        """uses `expandPathToUrl()` to make the API call"""
        url = Txbit.expandPathToUrl(path, params)
        return requests.get(url)

    def authenticatedRequest(self, path, params={}):
        """authenticated API call with APIKey and Secret for Market and Account methods"""
        params['apikey'] = self.APIKey
        params['nonce'] = str(int(time()))

        url = Txbit.expandPathToUrl(path, params)

        apisign = hmac.new(bytes(self.Secret, 'utf-8'),
                           bytes(url, 'utf-8'),
                           hashlib.sha512).hexdigest().upper()

        headers = {'apisign': apisign}
        return requests.get(url, headers=headers)

    ## PUBLIC FUNCTIONS ---------------

    def getMarkets():
        """(P) get the open and available trading markets along with other meta data"""
        res = Txbit.request('public/getmarkets')
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getCurrencies():
        """(P) get all supported assets along with other meta data"""
        res = Txbit.request('public/getcurrencies')
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getMarketSummaries():
        """(P) get the last 24 hour summary of all active markets"""
        res = Txbit.request('public/getmarketsummaries')
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getExchangePairs():
        """(P) get list of all pairs that form markets"""
        res = Txbit.getMarketSummaries()
        res.result = [pair['MarketName'] for pair in res.result]
        return res

    def getSystemStatus():
        """(P) get the system related status for all currencies"""
        res = Txbit.request('public/getsystemstatus')
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getOrderBook(market, bookType='both'):
        """(P) get the orderbook for a given market"""
        params = {'market': market, 'type': bookType}
        res = Txbit.request('public/getorderbook', params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getTicker(market):
        """(P) get current tick values for a market"""
        params = {'market': market}
        res = Txbit.request('public/getticker', params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getMarketHistory(market):
        """(P) get the latest trades that have occurred for a specific market"""
        params = {'market': market}
        res = Txbit.request('public/getmarkethistory', params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getCurrencyInformation(currency):
        """(P) get specific information and metadata about the listed currency"""
        params = {'currency': currency}
        res = Txbit.request('public/getcurrencyinformation', params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getCurrencyBalanceSheet(currency):
        """(P) get solvency information for listed currencies"""
        params = {'currency': currency}
        res = Txbit.request('public/getcurrencybalancesheet', params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    ## ACOUNT FUNCTIONS ---------------

    def getBalances(self):
        """(A) get all balances from your account"""
        path = 'account/getbalances'
        res = self.authenticatedRequest(path)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getBalanceFor(self, currency):
        """(A) get the balance from your account for a specific asset"""
        path = 'account/getbalance'
        params = {'currency': currency}
        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getDepositAddress(self, currency):
        """(A) get or generate an address for a specific currency

        Notes
        -----
        will return ADDRESS_GENERATING until one is available
        """
        path = 'account/getdepositaddress'
        params = {'currency': currency}
        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def withdraw(self, currency, quantity, address, paymentid=None):
        """(A) withdraw funds from your account

        Notes
        -----
        account for txfee
        """
        path = 'account/withdraw'
        params = {'currency': currency, 'quantity': quantity, 'address': address}

        if paymentid is not None:
            params['paymentid'] = paymentid

        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getOrder(self, uuid):
        """(A) get a single order by uuid"""
        path = 'account/getorder'
        params = {'uuid': uuid}
        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getOrderHistory(self, market=None):
        """(A) get your order history"""
        path = 'account/getorderhistory'
        params = {}

        if market is not None:
            params['market'] = market

        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getWithdrawlHistory(self, currency=None):
        """(A) get your withdrawal history"""
        path = 'account/getwithdrawalhistory'
        params = {}

        if currency is not None:
            params['currency'] = currency

        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getDepositHistory(self, currency=None):
        """(A) get your deposit history"""
        path = 'account/getdeposithistory'
        params = {}

        if currency is not None:
            params['currency'] = currency

        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    ## MARKET FUNCTIONS ---------------

    def buyLimit(self, market, quantity, rate):
        """(M) place a Buy Limit order in a specific market"""
        path = 'market/buylimit'
        params = {'market': market, 'quantity': quantity, 'rate': rate}
        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def sellLimit(self, market, quantity, rate):
        """(M) place a Sell Limit order in a specific market"""
        path = 'market/selllimit'
        params = {'market': market, 'quantity': quantity, 'rate': rate}
        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def cancel(self, uuid):
        """(M) cancel a buy or sell order"""
        path = 'market/cancel'
        params = {'uuic': uuic}
        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getOpenOrders(self, market=None):
        """(M) get all orders that you currently have opened"""
        path = 'getopenorders'
        params = {}

        if market is not None:
            params['market'] = market

        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)
