#!/usr/bin/python

import Queue
from threading import Thread
import sys

from CDASimulator.OrderTypes import LimitOrder, MarketOrder, MidPointOrder
from VirtualExchange import VirtualExchange


class ProcessThread(Thread):
    def __init__(self):
        super(ProcessThread, self).__init__()
        self.running = True
        self.q = Queue.Queue()
        self.eve = VirtualExchange()

    def add(self, data):
        self.q.put(data)

    def stop(self):
        self.running = False

    def run(self):
        q = self.q
        while self.running:
            try:
                # block for 1 second only:
                value = q.get(block=True, timeout=1)
                self.process(value)
            except Queue.Empty:
                sys.stdout.write('.')
                sys.stdout.flush()
        #
        if not q.empty():
            print "Elements left in the queue:"
            while not q.empty():
                print q.get()

    def process(self, value):
        request_type = value[0]            # o/stok/ord/b/0xffffffff(size)/waltercavi/0xffffffff (limit)
        print request_type
        if request_type == "O":
            stock = value[2:6]
            order_type = value[7:10]
            is_buy = value[11]
            if is_buy == "B":
                is_buy = True
            else:
                is_buy = False
            quantity = int(value[13:23], 0)
            origin = value[24:34]
            if order_type == "LMT":
                limit = int(value[35:45], 0)
                self.eve.place_order(LimitOrder(stock, quantity, limit, origin, is_buy))
            elif order_type == "MKT":
                self.eve.place_order(MarketOrder(stock, quantity, origin, is_buy))
            elif order_type == "MID":
                self.eve.place_order(MidPointOrder(stock, quantity, quantity, origin, is_buy)) # Some how the mid-point for this order needs to be determined
        elif request_type == "C":
            stock = value[2:6]
            order_type = value[7:10]
            is_buy = value[11]
            if is_buy == "B":
                is_buy = True
            else:
                is_buy = False
        if self.eve.fake_engine.get_stock().get_last_transaction():
            print self.eve.fake_engine.get_stock().get_last_transaction().get_price()