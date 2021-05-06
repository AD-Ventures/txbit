import hashlib
import hmac
import json


import requests


from time import time


class TxbitResponse:
    """A class to handle responses from calls to the Txbit API"""
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
    """A class to interact with the Txbit API

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
    _expandPathToUrl(path, params={}):
       adds onto the base url for specific methods
    _publicRequest(path, params={}):
       public call for Public Methods
    _athenticatedRequest(path, params={}):
       authenticated call with APIKey and Secret for Market and Account methods

    Notes
    -----
    Market methods need 'ALLOW TRADING' permission set up on the APIKey
    Account methods need 'ALLOW READING' permission set up on the APIKey
    """
    endpoint = 'https://api.txbit.io/api/'

    def __init__(self, APIKey=None, Secret=None):
        self.APIKey = APIKey
        self.Secret = Secret

    def _expandPathToUrl(self, path, params={}):
        """adds onto the base url for specific methods"""
        url = self.endpoint + path
        url += '?' if params else ''
        return url + '&'.join([key + '=' + str(params[key]) for key in params])

    def _publicRequest(self, path, params={}):
        """public call for Public Methods"""
        url = self._expandPathToUrl(path, params)
        res = requests.get(url)

        return TxbitResponse(res.ok and res.json()['success'],
                             res.json()['message'],
                             res.json()['result'])

    def _authenticatedRequest(self, path, params={}):
        """authenticated call with APIKey and Secret for Market and Account methods"""
        if self.APIKey is None or self.Secret is None:
            raise ValueError('APIKey and Secret must be supplied to use this methods')

        params['apikey'] = self.APIKey
        params['nonce'] = str(int(time()))

        url = self._expandPathToUrl(path, params)
        apisign = hmac.new(bytes(self.Secret, 'utf-8'),
                           bytes(url, 'utf-8'),
                           hashlib.sha512).hexdigest().upper()
        headers = {'apisign': apisign}

        res = requests.get(url, headers=headers)

        return TxbitResponse(res.ok and res.json()['success'],
                             res.json()['message'],
                             res.json()['result'])

    ## PUBLIC FUNCTIONS ---------------

    def getMarkets(self):
        """get the open and available trading markets along with other meta data"""
        return self._publicRequest('public/getmarkets')

    def getCurrencies(self):
        """get all supported assets along with other meta data"""
        return self._publicRequest('public/getcurrencies')

    def getTicker(self, market):
        """get current tick values for a market"""
        params = {'market': market}
        return self._publicRequest('public/getticker', params)

    def getMarketSummaries(self):
        """get the last 24 hour summary of all active markets"""
        return self._publicRequest('public/getmarketsummaries')

    def getMarketSummary(self, market):
        """get the last 24 hour summary of a specific market"""
        params = {'market': market}
        return self._publicRequest('public/getmarketsummary', params)

    def getOrderBook(self, market, bookType='both'):
        """get the orderbook for a given market"""
        params = {'market': market, 'type': bookType}
        return self._publicRequest('public/getorderbook', params)

    def getMarketHistory(self, market):
        """get the latest trades that have occurred for a specific market"""
        params = {'market': market}
        return self._publicRequest('public/getmarkethistory', params)

    def getSystemStatus(self):
        """get the system related status for all currencies"""
        return self._publicRequest('public/getsystemstatus')

    def getCurrencyInformation(self, currency):
        """get specific information and metadata about the listed currency"""
        params = {'currency': currency}
        return self._publicRequest('public/getcurrencyinformation', params)

    def getCurrencyBalanceSheet(self, currency):
        """get solvency information for listed currencies"""
        params = {'currency': currency}
        return self._publicRequest('public/getcurrencybalancesheet', params)

    ## MARKET FUNCTIONS ---------------

    def buyLimit(self, market, quantity, rate):
        """place a Buy Limit order in a specific market"""
        params = {'market': market, 'quantity': quantity, 'rate': rate}
        return self._authenticatedRequest('market/buylimit', params)

    def sellLimit(self, market, quantity, rate):
        """place a Sell Limit order in a specific market"""
        params = {'market': market, 'quantity': quantity, 'rate': rate}
        return self._authenticatedRequest('market/selllimit', params)

    def cancel(self, uuid):
        """cancel a buy or sell order"""
        params = {'uuic': uuic}
        return self._authenticatedRequest('market/cancel', params)

    def getOpenOrders(self, market=None):
        """get all orders that you currently have opened"""
        params = {}

        if market is not None:
            params['market'] = market

        return self._authenticatedRequest('market/getopenorders', params)

    ## ACOUNT FUNCTIONS ---------------

    def getBalances(self):
        """get all balances from your account"""
        return self._authenticatedRequest('account/getbalances')

    def getBalance(self, currency):
        """get the balance from your account for a specific asset"""
        params = {'currency': currency}
        return self._authenticatedRequest('account/getbalance', params)

    def getDepositAddress(self, currency):
        """get or generate an address for a specific currency

        Notes
        -----
        will return ADDRESS_GENERATING until one is available
        """
        params = {'currency': currency}
        return self._authenticatedRequest('account/getdepositaddress', params)

    def withdraw(self, currency, quantity, address, paymentid=None):
        """withdraw funds from your account

        Notes
        -----
        you must account for txfee
        """
        params = {'currency': currency, 'quantity': quantity, 'address': address}

        if paymentid is not None:
            params['paymentid'] = paymentid

        return self._authenticatedRequest('account/withdraw', params)

    def getOrder(self, uuid):
        """get a single order by uuid"""
        params = {'uuid': uuid}
        return self._authenticatedRequest('account/getorder', params)

    def getOrderHistory(self, market=None):
        """get your order history"""
        params = {}

        if market is not None:
            params['market'] = market

        return self._authenticatedRequest('account/getorderhistory', params)

    def getWithdrawlHistory(self, currency=None):
        """get your withdrawal history"""
        params = {}

        if currency is not None:
            params['currency'] = currency

        return self._authenticatedRequest('account/getwithdrawalhistory', params)

    def getDepositHistory(self, currency=None):
        """get your deposit history"""
        params = {}

        if currency is not None:
            params['currency'] = currency

        return self._authenticatedRequest('account/getdeposithistory', params)
