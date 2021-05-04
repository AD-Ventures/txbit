# Txbit [![Build Status](https://travis-ci.com/AD-Ventures/txbit.svg?branch=main)](https://travis-ci.com/AD-Ventures/txbit) ![Last Commit](https://img.shields.io/github/last-commit/AD-Ventures/txbit) ![Python Version](https://img.shields.io/badge/python-3.4%2B-green)  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/AD-Ventures/txbit/blob/main/LICENSE)


A Python3 wrapper for the [Txbit API](https://apidocs.txbit.io/#txbit-io-api)

## Installation

```bash
pip3 install txbit
```

## Usage

Methods in the txbit package retrun a `TxbitReponse` object containing three attributes aligning with txbit API response (success, message, result).

```python
import txbit

request = txbit.PublicClient().getMarkets() # TxbitResponse object
request.success  # returns True
request.message  # returns ''
request.result  # returns a list of market dictionaries
```
## Public API

The Txbit API is split into three groups (Public, Market, and Account). The Public group provides information about markets and does not require authentication.

```python
pubClient = txbit.PublicClient()  # initalize the object
```
Methods of the PublicClient class, and related documentation, below: 

* `pubClient.getMarkets()` - https://apidocs.txbit.io/#public-getmarkets
* `pubClient.getCurrencies()` - https://apidocs.txbit.io/#public-getcurrencies
* `pubClient.getTicker(market)` - https://apidocs.txbit.io/#public-getticker
* `pubClient.getMarketSummaries()` - https://apidocs.txbit.io/#public-getmarketsummaries
* `pubClient.getMarketSummary(market)` - https://apidocs.txbit.io/#public-getmarketsummary
* `pubClient.getOrderBook(market, bookType='both')` - https://apidocs.txbit.io/#public-getorderbook
* `pubClient.getMarketHistory(market)` - https://apidocs.txbit.io/#public-getmarkethistory
* `pubClient.getSystemStatus()` - https://apidocs.txbit.io/#public-getsystemstatus
* `pubClient.getCurrencyInformation(currency)` - https://apidocs.txbit.io/#public-getcurrencyinformation
* `pubClient.getCurrencyBalanceSheet(currency)` - https://apidocs.txbit.io/#public-getcurrencybalancesheet

## Authenticated API

The other two groups (Market and Account) require authentication for access/use. 

* **Market** - Used for setting and canceling orders. The **ALLOW TRADING** permission must be set up on the key(s) being used.
* **Acount** - Used for account related functions such as balances, withdrawals and deposit addresses. The **ALLOW READING** permission must be set up on the key(s) being used.

This wrapper handles most of teh authentication process, so the only thing that needs to be supplied is an API Key and Secret with proper permissions. We recommend saving your key and secret as variables (`APIKEY = XXX` and `SECRET=XXX`) in a separate python file named `secrets.py` and importing it such as the example below.

To create and manage your API keys go to **Profile** > **Settings** > **API Keys** on the Txbit.io site.

```python
from secrets import APIKEY, SECRET  # import api key and secret

authClient = txbit.AuthenticatedClient(APIKEY, SECRET)
```
Methods of the Authenticated Client class, and related documentation, below: 

### Market API

 * `authClient.buyLimit(market, quantity, rate)` - https://apidocs.txbit.io/#market-buylimit
 * `authClient.sellLimit(market, quantity, rate)` - https://apidocs.txbit.io/#market-selllimit
 * `authClient.cancel(uuid)` - https://apidocs.txbit.io/#market-cancel
 * `authClient.getOpenOrders(market=None)` - https://apidocs.txbit.io/#market-getopenorders

### Account API

 * `authClient.getBalances()` - https://apidocs.txbit.io/#account-getbalances
 * `authClient.getBalance(currency)` - https://apidocs.txbit.io/#account-getbalance
 * `authClient.getDepositAddress(currency)` - https://apidocs.txbit.io/#account-getdepositaddress
 * `authClient.withdraw(currency, quantity,  address, paymentid=None)` - https://apidocs.txbit.io/#account-withdraw
 * `authClient.getOrder(uuid)` - https://apidocs.txbit.io/#account-getorder
 * `authClient.getOrderHistory(market=None)` - https://apidocs.txbit.io/#account-getorderhistory
 * `authClient.getWithdrawlHistory(currency=None)` - https://apidocs.txbit.io/#account-getwithdrawalhistory
 * `authClient.getDepositHistory(currency=None)` - https://apidocs.txbit.io/#account-getdeposithistory

## Support

For any help or questions, please open an issue on GitHub.

## License

[MIT](https://github.com/AD-Ventures/txbit/blob/master/LICENSE)
