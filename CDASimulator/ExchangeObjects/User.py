#!/usr/bin/python
from CDASimulator.ExchangeObjects import PortfolioElement


class User(object):

    def __init__(self, identity):
        self.id = identity
        self.portfolio = []
        self.cash = 0

    def set_cash(self, cash):
        self.cash = cash

    def set_portfolio(self, portfolio):
        self.portfolio = portfolio

    def get_id(self):
        return self.id

    def get_cash(self):
        return self.cash

    def get_portfolio(self):
        return self.portfolio

    def change_portfolio(self, transaction, is_buyer):
        stock_ticker = transaction.get_stock().get_ticker()
        if is_buyer:
            transaction_size = transaction.get_size()
        else:
            transaction_size = -transaction.get_size()
        for element in self.portfolio:
            if element.get_ticker() == stock_ticker:
                element.add_quantity(transaction_size)
                return
        self.portfolio.append(PortfolioElement(stock_ticker, transaction_size))