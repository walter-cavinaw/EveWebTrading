#!/usr/bin/python


import time

from CDASimulator.ExchangeObjects import Transaction
from CDASimulator.OrderTypes import MarketOrder
from OrderQueue import OrderQueue, PriorityOrderQueue


class MatchingEngine(object):

    def __init__(self, stock, **kwds):
        self.stock = stock
        self.ask_heap = PriorityOrderQueue()
        self.bid_heap = PriorityOrderQueue()
        self.buy_market_queue = OrderQueue()
        self.sell_market_queue = OrderQueue()
        self.spread = 0
        super(MatchingEngine, self).__init__(**kwds)

    def get_stock(self):
        return self.stock

    def process_order(self, order):
        order.set_timestamp(time.time())
        if order.get_buy():
            if type(order) is not MarketOrder:
                order = (-order.get_limit(), order.get_timestamp(), order)
                self.match_limit(self.ask_heap, self.sell_market_queue, order, self.bid_heap)
            elif not self.match_market(self.ask_heap, order):
                self.buy_market_queue.put((order.get_timestamp(), order))
        else:
            if type(order) is not MarketOrder:
                self.match_limit(self.bid_heap, self.buy_market_queue, (order.get_limit(), order.get_timestamp(), order), self.ask_heap)
            elif not self.match_market(self.bid_heap, order):
                self.sell_market_queue.put((order.get_timestamp(), order))
        #self.calculate_spread()

    def match_market(self, heap, new_order):
        while not heap.empty():
            order = heap.get()
            if self.complete_transaction(order[2], new_order):
                if order[2].remaining_shares() > 0:
                    heap.put(order)
                return True
        else:
            return False

    def complete_transaction(self, order, new_order):
        order_shares = order.remaining_shares()
        new_order_shares = new_order.remaining_shares()
        if order_shares > new_order_shares:
            new_order.set_remaining_shares(0)
            order.set_remaining_shares(order_shares - new_order_shares)
            self.announce_transaction(order, new_order, new_order_shares)
            return True
        elif order_shares == new_order_shares:
            new_order.set_remaining_shares(0)
            order.set_remaining_shares(0)
            self.announce_transaction(order, new_order, order_shares)
            return True
        elif order_shares < new_order_shares:
            new_order.set_remaining_shares(new_order_shares - order_shares)
            order.set_remaining_shares(0)
            self.announce_transaction(order, new_order, order_shares)
            return False

    def match_limit(self, limit_heap, market_heap, new_order, altered_heap):
        if not limit_heap.empty():
            self.spread = limit_heap.queue[0][0] + new_order[0]
        while not limit_heap.empty() and self.spread <= 0 and not market_heap.empty():
            limit_order = limit_heap.get()
            market_order = market_heap.get()
            priority_order = self.calculate_priority(limit_order, market_order)
            if priority_order == limit_order:
                priority_heap = limit_heap
                priority_pass = priority_order[2]
                market_heap.put(market_order)
            else:
                priority_heap = market_heap
                priority_pass = priority_order[1]
                limit_heap.put(limit_order)
            if self.complete_transaction(priority_pass, new_order[2]):
                if priority_pass.remaining_shares() > 0:
                    priority_heap.put(priority_order)
                return True
            if not limit_heap.empty():
                self.spread = limit_heap.queue[0][0] + new_order[0]
        while not limit_heap.empty() and self.spread <= 0:
            priority_order = limit_heap.get()
            if self.complete_transaction(priority_order[2], new_order[2]):
                if priority_order[2].remaining_shares() > 0:
                    limit_heap.put(priority_order)
                return True
            if not limit_heap.empty():
                self.spread = limit_heap.queue[0][0] + new_order[0]
        while not market_heap.empty():
            priority_order = market_heap.get()
            if self.complete_transaction(priority_order[1], new_order[2]):
                if priority_order[1].remaining_shares() > 0:
                    market_heap.put(priority_order)
                return True
        altered_heap.put(new_order)

    def cancel_order(self, order):
        is_buy = order.get_buy()
        if is_buy:
            if order is type(MarketOrder):
                queue = self.buy_market_queue
            else:
                queue = self.bid_heap
        else:
            if order is type(MarketOrder):
                queue = self.sell_market_queue
            else:
                queue = self.ask_heap
        queue.cancel_order(order)

    def announce_transaction(self, order1, order2, size):
        # make a transaction between the two orders and put it in the stock transactions
        if order1.get_buy():
            buyer = order1
            seller = order2
        else:
            buyer = order2
            seller = order1
        if type(order2) is MarketOrder or type(order1) is MarketOrder:
            price = order1.get_limit()
        else:
            price = buyer.get_limit()/2.0 + seller.get_limit()/2.0
        self.stock.append_transaction(Transaction(size, price, buyer.get_origin(),
                                                          seller.get_origin(), time.time(), self.stock))

    def calculate_priority(self, limit_order, market_order):
        if limit_order[1] < market_order[0]:
            return limit_order
        else:
            return market_order

    def calculate_spread(self):
        if not self.bid_heap.empty() and not self.ask_heap.empty():
            self.spread = self.bid_heap.queue[0][0] + self.ask_heap.queue[0][0]

    def get_spread(self):
        return self.spread

    def get_bid(self):
        if not self.bid_heap.empty():
            return self.bid_heap.queue.queue[0][2].get_limit()
        else:
            return -1

    def get_ask(self):
        if not self.ask_heap.empty():
            return self.ask_heap.queue[0][2].get_limit()
        else:
            return -1

