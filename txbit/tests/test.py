from txbit import Txbit
import unittest

class TestTxbit(unittest.TestCase):
    endpoint = 'https://api.txbit.io/api/'
    txbit = Txbit()

    def test_endpoint(self):
        self.assertEqual(self.endpoint, self.txbit.endpoint)

    def test_expandPathToUrl(self):
        path = 'test/case'
        url = self.txbit.__expandPathToUrl__(path)
        self.assertEqual(url, self.endpoint + path)

    def test_expandPathToUrl_params(self):
        path = 'test/case'
        params = {
            'param1': 'test1',\
            'param2': 'test2'\
        }
        url = self.txbit.__expandPathToUrl__(path, params)

        expected_url = self.endpoint + path + '?'

        for key in params:
            expected_url += key + "=" + params[key] + "&"

        self.assertEqual(url, expected_url)

    def test_getMarkets(self):
        res = self.txbit.getMarkets()
        self.assertTrue(res.success)

    def test_getCurrencies(self):
        res = self.txbit.getCurrencies()
        self.assertTrue(res.success)

    def test_getTicker(self):
        res = self.txbit.getTicker('BAN/BTC')
        self.assertTrue(res.success)

    def test_getTicker_bad(self):
        res = self.txbit.getTicker('BAN')

        self.assertFalse(res.success)
        self.assertEqual("INVALID_MARKET", res.message)

    def test_getMarketSummaries(self):
        res = self.txbit.getMarketSummaries()
        self.assertTrue(res.success)

    def test_getMarketSummary(self):
        res = self.txbit.getMarketSummary('BAN/BTC')
        self.assertTrue(res.success)

    def test_getOrderBook(self):
        res = self.txbit.getOrderBook('BAN/BTC')
        self.assertTrue(res.success)

    def test_getMarketHistory(self):
        res = self.txbit.getMarketHistory('BAN/BTC')
        self.assertTrue(res.success)

    def test_getSystemStatus(self):
        res = self.txbit.getSystemStatus()
        self.assertTrue(res.success)

    def test_getCurrencyInformation(self):
        res = self.txbit.getCurrencyInformation('BTC')
        self.assertTrue(res.success)

    def test_getCurrencyBalanceSheet(self):
        res = self.txbit.getCurrencyBalanceSheet('BTC')
        self.assertTrue(res.success)

if __name__ == '__main__':
    unittest.main()
