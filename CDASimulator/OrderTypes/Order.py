#!/usr/bin/python


class Order(object):
    type = "Order"

    def __init__(self, stock_ticker=None, size=None, origin=None, buy=None, **kwds):
        self.origin = origin
        self.stock_ticker = stock_ticker
        self.size = size
        self.remaining = size
        self.is_buy = buy
        super(Order, self).__init__(**kwds)

    def set_stock_ticker(self, stock_ticker):
        self.stock_ticker = stock_ticker

    def set_size(self, size):
        self.size = size

    def set_buy(self, buy):
        self.is_buy = buy

    def set_origin(self, origin):
        self.origin = origin

    def set_remaining_shares(self, remaining):
        self.remaining = remaining

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def remaining_shares(self):
        return self.remaining

    def get_timestamp(self):
        return self.timestamp

    def get_size(self):
        return self.size

    def get_stock_ticker(self):
        return self.stock_ticker

    def get_origin(self):
        return self.origin

    def get_buy(self):
        return self.is_buy

    def __str__(self):
        ret = self.type + ": "
        if self.is_buy:
            ret += "Buy "
        else:
            ret += "Sell "
        ret += str(self.size) + " " + self.stock_ticker
        return ret
