#!/usr/bin/python

import thread

from CDASimulator.OrderTypes import LimitOrder
from VirtualExchange import VirtualExchange


eve = VirtualExchange()
stock = eve.fake_stock
print "do we get here"
thread.start_new_thread(eve.run_exchange, ())
print " do we get here"
eve.insert_order(LimitOrder(stock, 100, 50, "walter b1", True))
eve.insert_order(LimitOrder(stock, 100, 51, "walter b2", True))
eve.insert_order(LimitOrder(stock, 100, 52, "walter b3", True))
eve.insert_order(LimitOrder(stock, 100, 53, "walter b4", True))
eve.insert_order(LimitOrder(stock, 100, 54, "walter s1", False))
eve.insert_order(LimitOrder(stock, 100, 50, "walter s2", False))
eve.insert_order(LimitOrder(stock, 100, 50, "walter s3", False))
eve.insert_order(LimitOrder(stock, 100, 50, "walter s4", False))
while not eve.order_queue.empty():
    pass
eve.end_exchange()
for t in stock.transactions:
    print t.__str__()
if not stock.transactions:
    print "List is empty"
#app = wx.App()
#interface = QuoteInterface(None, "First Attempt with exchange", eve)
#app.MainLoop()
