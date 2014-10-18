#!/usr/bin/python


class PortfolioElement(object):

    def __init__(self, stock_ticker, quantity):
        self.stock_ticker = stock_ticker
        self.quantity = quantity

    def get_stock_ticker(self):
        return self.stock_ticker

    def change_quantity(self, size):
        self.quantity = self.quantity + size
