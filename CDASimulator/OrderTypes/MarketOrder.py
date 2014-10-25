#!/usr/bin/python

from Order import Order


class MarketOrder(Order):

    def __init__(self, stock=None, size=None, origin=None, buy=None, **kwds):
        super(MarketOrder, self).__init__(stock, size, origin, buy, **kwds)