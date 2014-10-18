#!/usr/bin/python

from Order import Order


class MarketOrder(Order):

    def __init__(self, stock, size, origin, buy, **kwds):
        super(MarketOrder, self).__init__(stock, size, origin, buy, **kwds)