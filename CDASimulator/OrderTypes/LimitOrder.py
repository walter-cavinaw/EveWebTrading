#!/usr/bin/python

from Order import Order


class LimitOrder(Order):

    def __init__(self, stock=None, size=None, limit=None, origin=None, buy=None, **kwds):
        super(LimitOrder, self).__init__(stock, size, origin, buy, **kwds)
        self.limit = limit

    def set_limit(self, limit):
        self.limit = limit

    def get_limit(self):
        return self.limit
