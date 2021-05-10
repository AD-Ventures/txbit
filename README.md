# Txbit [![Build Status](https://travis-ci.com/AD-Ventures/txbit.svg?branch=main)](https://travis-ci.com/AD-Ventures/txbit) ![Last Commit](https://img.shields.io/github/last-commit/AD-Ventures/txbit) ![Python Version](https://img.shields.io/badge/python-3.4%2B-green)  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/AD-Ventures/txbit/blob/main/LICENSE)


A Python3 wrapper for the [Txbit API](https://apidocs.txbit.io/#txbit-io-api)

This is an unofficial wrapper with no affiliation with Txbit, use at your own risk.

*Note: requests are limited to 10 per second per IP address*

## Installation

```bash
pip3 install txbit
```

## Usage

Methods in the txbit package retrun a `TxbitReponse` object containing three attributes aligning with txbit API response (success, message, result).

```python
import txbit

txbit = txbit.Txbit()  # initalize the object

request = txbit.getMarkets()  # use one of the object's methods to make an API call
request.success  # returns True
request.message  # returns ''
request.result  # returns a list of market dictionaries
```
## Public API

The Txbit API is split into three groups (Public, Market, and Account). The Public group provides information about markets and does not require authentication with an API Key and Secret. An exception will be raised if trying to use the non-public methods without supplying a APIKey and Secret.

```python
txbit = txbit.Txbit()  # no API Key and Secret supplied if only using public methods
```
Methods of the PublicClient class, and related documentation, below: 

* `txbit.getMarkets()` - https://apidocs.txbit.io/#public-getmarkets
* `txbit.getCurrencies()` - https://apidocs.txbit.io/#public-getcurrencies
* `txbit.getTicker(market)` - https://apidocs.txbit.io/#public-getticker
* `txbit.getMarketSummaries()` - https://apidocs.txbit.io/#public-getmarketsummaries
* `txbit.getMarketSummary(market)` - https://apidocs.txbit.io/#public-getmarketsummary
* `txbit.getOrderBook(market, bookType='both')` - https://apidocs.txbit.io/#public-getorderbook
* `txbit.getMarketHistory(market)` - https://apidocs.txbit.io/#public-getmarkethistory
* `txbit.getSystemStatus()` - https://apidocs.txbit.io/#public-getsystemstatus
* `txbit.getCurrencyInformation(currency)` - https://apidocs.txbit.io/#public-getcurrencyinformation
* `txbit.getCurrencyBalanceSheet(currency)` - https://apidocs.txbit.io/#public-getcurrencybalancesheet

## Authenticated API

The other two groups (Market and Account) require authentication for access/use. 

* **Market** - Used for setting and canceling orders. The **ALLOW TRADING** permission must be set up on the key(s) being used.
* **Acount** - Used for account related functions such as balances, withdrawals and deposit addresses. The **ALLOW READING** permission must be set up on the key(s) being used.

This wrapper handles most of the authentication process, so the only thing that needs to be supplied is an API Key and Secret with proper permissions. We recommend saving your key and secret as variables (`APIKEY = XXX` and `SECRET=XXX`) in a separate python file named `secrets.py` and importing it such as the example below.

To create and manage your API keys go to **Profile** > **Settings** > **API Keys** on the Txbit.io site.

```python
from secrets import APIKEY, SECRET  # import api key and secret

txbit = txbit.Txbit(APIKEY, SECRET)  # this time supplying a API Key and Secret
```
Methods of the Authenticated Client class, and related documentation, below: 

### Market API

 * `txbit.buyLimit(market, quantity, rate)` - https://apidocs.txbit.io/#market-buylimit
 * `txbit.sellLimit(market, quantity, rate)` - https://apidocs.txbit.io/#market-selllimit
 * `txbit.cancel(uuid)` - https://apidocs.txbit.io/#market-cancel
 * `txbit.getOpenOrders(market=None)` - https://apidocs.txbit.io/#market-getopenorders

### Account API

 * `txbit.getBalances()` - https://apidocs.txbit.io/#account-getbalances
 * `txbit.getBalance(currency)` - https://apidocs.txbit.io/#account-getbalance
 * `txbit.getDepositAddress(currency)` - https://apidocs.txbit.io/#account-getdepositaddress
 * `txbit.withdraw(currency, quantity,  address, paymentid=None)` - https://apidocs.txbit.io/#account-withdraw
 * `txbit.getOrder(uuid)` - https://apidocs.txbit.io/#account-getorder
 * `txbit.getOrderHistory(market=None)` - https://apidocs.txbit.io/#account-getorderhistory
 * `authClient.getWithdrawlHistory(currency=None)` - https://apidocs.txbit.io/#account-getwithdrawalhistory
 * `authClient.getDepositHistory(currency=None)` - https://apidocs.txbit.io/#account-getdeposithistory

## Support

For any help or questions, please open an issue on GitHub.

## License

[MIT](https://github.com/AD-Ventures/txbit/blob/master/LICENSE)
