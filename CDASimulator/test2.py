#!/usr/bin/python

import wx
from VirtualExchange import VirtualExchange
from FirstInterface import QuoteInterface
import thread

eve = VirtualExchange()
thread.start_new_thread(eve.run_exchange, ())

app = wx.App()
QuoteInterface(None, "EVE", eve)
app.MainLoop()
