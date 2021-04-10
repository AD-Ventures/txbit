# Txbit [![Build Status](https://travis-ci.com/AD-Ventures/txbit.svg?branch=main)](https://travis-ci.com/AD-Ventures/txbit) ![Last Commit](https://img.shields.io/github/last-commit/AD-Ventures/txbit) ![Python Version](https://img.shields.io/badge/python-3.4%2B-green)  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/AD-Ventures/txbit/blob/main/LICENSE)


A Python3 wrapper for the Txbit API

## Installation

```bash
pip3 install txbit
```

## Usage

```python
from txbit import Txbit
from secrets import APIKEY, SECRET  # api key and secret

# public functions (no APIKEY/Secret needed)
markets = Txbit.getMarketSummaries().result

order = Txbit.getOrderBook('ETH/BTC').result

# authenticated market and account functions (require APIKEY/Secret)
t = Txbit(APIKEY, SECRET)

request = t.getBalance()

# check if the API request was successful
if request.success:
    balance = request.result
```

## Support

For any help or questions, please open an issue on GitHub.

## License

[MIT](https://github.com/AD-Ventures/txbit/blob/master/LICENSE)
