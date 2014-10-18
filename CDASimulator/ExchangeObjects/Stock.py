#!/usr/bin/python


class Stock(object):

    def __init__(self, company, ticker, shares, **kwds):
        self.shares = shares
        self.ticker = ticker
        self.company = company
        self.transactions = []
        super(Stock, self).__init__(**kwds)

    def set_company(self, company):
        self.company = company

    def get_company(self):
        return self.company

    def set_ticker(self, ticker):
        self.ticker = ticker

    def get_ticker(self):
        return self.ticker

    def set_shares(self, shares):
        self.shares = shares

    def get_shares(self):
        return self.shares

    def append_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_transactions(self):
        return self.transactions

    def get_last_transaction(self):
        if self.transactions:
            return self.transactions[-1]