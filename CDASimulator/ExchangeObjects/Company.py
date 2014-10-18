#!/usr/bin/python

from Stock import Stock


class Company(object):
    def __init__(self, name, ticker, shares, **kwds):
        self.name = name
        self.shares = shares
        self.stock = Stock(self, ticker, shares)
        super(Company, self).__init__(**kwds)

    def get_stock(self):
        return self.stock

    def set_name(self, name):   # name must be a string
        self.name = name

    def get_name(self):
        return self.name

    def set_shares(self, shares):
        self.shares = shares

    def get_shares(self):
        return self.shares