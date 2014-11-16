EveWebTrading
=============

Initially designed to create an exchange on which trading stocks is possible using a continuous double auction.

At first this was to be used as a trading engine for sales and trading competitions
but it's uses could be extended to anything that functions as an exchange.

It uses python's tornado framework, along with websockets to push data to the endpoint in real time.

Requirements
------------

Must have python 2.7

tornado

jsonpickle

mysqldb (for windows use a binary installer)

torndb

py-bcrypt (The easiest way to install is to use the wheel @ https://bitbucket.org/alexandrul/py-bcrypt/downloads)


Will Include:
-------------

real time stock data (based on fake stocks traded on the exchange)

News data (modeled after news events that occur around real stocks)

Best bids and asks from the order book.

Portfolio Information regarding security holdings (real or fake stocks).
