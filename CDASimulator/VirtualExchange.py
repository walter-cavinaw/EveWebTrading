#!/usr/bin/python

import Queue
import threading

from CDASimulator.ExchangeObjects import Company
from MatchingEngine import MatchingEngine


class VirtualExchange(object):

    def __init__(self):
        super(VirtualExchange, self).__init__()
        self.engine_list = []
        self.fake_company = Company("Fake Company", "FAKE", 3000000000)

        self.fake_engine = MatchingEngine(self.fake_company.get_stock())
        self.engine_list.append((self.fake_engine, threading.Semaphore()))

        self.order_queue = Queue.Queue()

        self.num_order = 0

        self.start = True

        self.cv = threading.Condition()

    # this method is probably not neccessary for networking implementation
    def run_exchange(self):
        while self.start:
            self.cv.acquire()
            while self.order_queue.empty():
                self.cv.wait()
            # this next method can be done in parallel
            self.place_order(self.order_queue.get()[1])
            self.cv.release()

    # this method is probably not necessary for networking implementation
    def insert_order(self, order):
        if self.assert_is_order(order):
            self.cv.acquire()
            self.num_order += 1
            self.order_queue.put((self.num_order, order))
            self.cv.notify()
            self.cv.release()

    def place_order(self, order):
        if self.assert_is_order(order):
            for engine_and_semaphore in self.engine_list:
                if order.get_stock_ticker() == engine_and_semaphore[0].get_stock().get_ticker():
                    engine_and_semaphore[1].acquire()
                    engine_and_semaphore[0].process_order(order)
                    engine_and_semaphore[1].release()
                    return True

    def place_cancel(self, order):
        if self.assert_is_order(order):
            for engine_and_semaphore in self.engine_list:
                if order.get_stock_ticker() == engine_and_semaphore[0].get_stck().get_ticker():
                    engine_and_semaphore[1].acquire()
                    engine_and_semaphore[0].cancel_order(order)
                    engine_and_semaphore[1].release()
                    return True

    def assert_is_order(self, order):
        return True


