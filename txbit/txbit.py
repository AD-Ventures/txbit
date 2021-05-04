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
    """A general class to use as the base for other Txbit.io API classes

    Attributes
    ----------
    endpoint : str
        the base url for API calls

    Methods
    -------
    expandPathToUrl(path, params={}):
       adds onto the base url for specific methods
    request(path, params={}):
        uses `expandPathToUrl()` to make the API call
    """
    endpoint = 'https://api.txbit.io/api/'

    def expandPathToUrl(self, path, params={}):
        """adds onto the base url for specific methods"""
        url = self.endpoint + path
        url += '?' if params else ''

        for key in params:
            url += key + '=' + params[key] + '&'

        return url

    def request(self, path, params={}):
        """uses `expandPathToUrl()` to make the API call"""
        url = self.expandPathToUrl(path, params)
        return requests.get(url)



class PublicClient(Txbit):
    """A class to interact with the Txbit.io API Public Functions"""

    def __init__(self):
        pass

    def getMarkets(self):
        """get the open and available trading markets along with other meta data"""
        res = self.request('public/getmarkets')
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getCurrencies(self):
        """get all supported assets along with other meta data"""
        res = self.request('public/getcurrencies')
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getTicker(self, market):
        """get current tick values for a market"""
        params = {'market': market}
        res = self.request('public/getticker', params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getMarketSummaries(self):
        """get the last 24 hour summary of all active markets"""
        res = self.request('public/getmarketsummaries')
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getMarketSummary(self, market):
        """get the last 24 hour summary of a specific market"""
        params = {'market': market}
        res = self.request('public/getmarketsummary', params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getOrderBook(self, market, bookType='both'):
        """get the orderbook for a given market"""
        params = {'market': market, 'type': bookType}
        res = self.request('public/getorderbook', params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getMarketHistory(self, market):
        """get the latest trades that have occurred for a specific market"""
        params = {'market': market}
        res = self.request('public/getmarkethistory', params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getSystemStatus(self):
        """get the system related status for all currencies"""
        res = self.request('public/getsystemstatus')
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getCurrencyInformation(self, currency):
        """get specific information and metadata about the listed currency"""
        params = {'currency': currency}
        res = self.request('public/getcurrencyinformation', params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getCurrencyBalanceSheet(self, currency):
        """get solvency information for listed currencies"""
        params = {'currency': currency}
        res = self.request('public/getcurrencybalancesheet', params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)


class AuthenticatedClient(Txbit):
    """A class to interact with the Txbit.io API Market and Account methods

    Attributes
    ----------
    APIKey : str
        key for working with the Market and Account methods
    Secret : str
        secret for working with the Market and Account methods

    Notes
    -----
    Market methods need 'ALLOW TRADING' permission set up on the APIKey
    Account methods need 'ALLOW READING' permission set up on the APIKey
    """

    def __init__(self, APIKey, Secret):
        self.APIKey = APIKey
        self.Secret = Secret

    def authenticatedRequest(self, path, params={}):
        """authenticated API call with APIKey and Secret for Market and Account methods"""
        params['apikey'] = self.APIKey
        params['nonce'] = str(int(time()))

        url = self.expandPathToUrl(path, params)

        apisign = hmac.new(bytes(self.Secret, 'utf-8'),
                           bytes(url, 'utf-8'),
                           hashlib.sha512).hexdigest().upper()

        headers = {'apisign': apisign}
        return requests.get(url, headers=headers)

    ## MARKET FUNCTIONS ---------------

    def buyLimit(self, market, quantity, rate):
        """place a Buy Limit order in a specific market"""
        path = 'market/buylimit'
        params = {'market': market, 'quantity': quantity, 'rate': rate}
        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def sellLimit(self, market, quantity, rate):
        """place a Sell Limit order in a specific market"""
        path = 'market/selllimit'
        params = {'market': market, 'quantity': quantity, 'rate': rate}
        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def cancel(self, uuid):
        """cancel a buy or sell order"""
        path = 'market/cancel'
        params = {'uuic': uuic}
        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getOpenOrders(self, market=None):
        """get all orders that you currently have opened"""
        path = 'market/getopenorders'
        params = {}

        if market is not None:
            params['market'] = market

        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    ## ACOUNT FUNCTIONS ---------------

    def getBalances(self):
        """get all balances from your account"""
        path = 'account/getbalances'
        res = self.authenticatedRequest(path)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getBalance(self, currency):
        """get the balance from your account for a specific asset"""
        path = 'account/getbalance'
        params = {'currency': currency}
        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getDepositAddress(self, currency):
        """get or generate an address for a specific currency

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
        """withdraw funds from your account

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
        """get a single order by uuid"""
        path = 'account/getorder'
        params = {'uuid': uuid}
        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getOrderHistory(self, market=None):
        """get your order history"""
        path = 'account/getorderhistory'
        params = {}

        if market is not None:
            params['market'] = market

        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getWithdrawlHistory(self, currency=None):
        """get your withdrawal history"""
        path = 'account/getwithdrawalhistory'
        params = {}

        if currency is not None:
            params['currency'] = currency

        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)

    def getDepositHistory(self, currency=None):
        """get your deposit history"""
        path = 'account/getdeposithistory'
        params = {}

        if currency is not None:
            params['currency'] = currency

        res = self.authenticatedRequest(path, params)
        result = res.json()['result'] if res.ok and res.json()['success'] else res.status_code
        return TxbitResponse(res.ok and res.json()['success'], "", result)
