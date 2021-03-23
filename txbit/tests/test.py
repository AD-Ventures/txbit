from txbit import Txbit, TxbitResponse
import unittest

class TestTxbit(unittest.TestCase):
#     def test_error(self):
#         with self.assertRaises(TypeError):
#             benchmark_env(foo)

    def test_expandPathToUrl(self):
        url = Txbit.expandPathToUrl('test/case')
        self.assertEqual(url, 'https://api.txbit.io/api/test/case?')

if __name__ == '__main__':
    unittest.main()
