from txbit import Txbit, TxbitResponse
import unittest

class TestTxbit(unittest.TestCase):
#     def test_error(self):
#         with self.assertRaises(TypeError):
#             call_error_function()

    endpoint = 'https://api.txbit.io/api/'

    def test_endpoint(self):
        self.assertEqual(self.endpoint, Txbit.endpoint)

    def test_expandPathToUrl(self):
        path = 'test/case'
        url = Txbit.expandPathToUrl(path)
        self.assertEqual(url, self.endpoint + path)

    def test_expandPathToUrl_params(self):
        path = 'test/case'
        params = {
            'param1': 'test1',\
            'param2': 'test2'\
        }
        url = Txbit.expandPathToUrl(path, params)

        expected_url = self.endpoint + path + '?'

        for key in params:
            expected_url += key + "=" + params[key] + "&"

        self.assertEqual(url, expected_url)

    def test_request_bad(self):
        path = 'test/case'
        res = Txbit.request(path)

        self.assertFalse(res.ok)
        self.assertEqual(404, res.status_code)

    def test_getMarkets(self):
        res = Txbit.getMarkets()
        self.assertTrue(res.success)

    def test_getCurrencies(self):
        res = Txbit.getCurrencies()
        self.assertTrue(res.success)

    def test_getMarketSummaries(self):
        res = Txbit.getMarketSummaries()
        self.assertTrue(res.success)

    def test_getExchangePairs(self):
        res = Txbit.getExchangePairs()
        self.assertTrue(res.success)

    def test_getOrderBook(self):
        res = Txbit.getOrderBook('BAN/BTC')
        self.assertTrue(res.success)

    def test_getTicker(self):
        res = Txbit.getTicker('BAN/BTC')
        self.assertTrue(res.success)

    def test_getMarketHistory(self):
        res = Txbit.getMarketHistory('BAN/BTC')
        self.assertTrue(res.success)



if __name__ == '__main__':
    unittest.main()
