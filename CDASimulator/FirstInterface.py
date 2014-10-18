
#!/usr/bin/python

# A basic interface for quotes and transaction
import wx
import matplotlib

from CDASimulator.OrderTypes import LimitOrder, MarketOrder, MidPointOrder


matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas
import numpy as np
import pylab


class DataGen(object):
    """ A silly class that generates pseudo-random data for
        display in the plot.
    """
    def __init__(self, init=50):
        self.data = self.init = init

    def next(self):
        self._recalc_data()
        return self.data

    def _recalc_data(self):
        delta = np.random.uniform(-0.5, 0.5)
        r = np.random.random()

        if r > 0.9:
            self.data += delta * 3
        elif r > 0.5:
            # attraction to the initial value
            delta += (0.5 if self.init > self.data else -0.5)
            self.data += delta
        else:
            self.data += delta


class QuoteInterface(wx.Frame):
    def __init__(self, parent, title, exchange):
        super(QuoteInterface, self).__init__(parent, title=title, size=(500, 500))
        self.exchange = exchange
        self.data = [100.0]
        self.paused = False
        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):

        self.SetBackgroundColour('white')
        self.panel = wx.Panel(self)
        self.box = wx.BoxSizer(wx.VERTICAL)
        self.InitQuoteBar()
        self.init_plot()
        self.canvas = FigCanvas(self.panel, -1, self.fig)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.canvas, flag=wx.ALL, border=4)
        #hbox.Add(wx.StaticBox())
        self.box.Add(hbox, flag=wx.EXPAND)
        self.panel.SetSizerAndFit(self.box)

        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)
        self.redraw_timer.Start(100)

    def InitQuoteBar(self):
        quote_size_bar = wx.GridBagSizer(1, 7)

        quantity = wx.StaticText(self.panel, label="Quantity")
        quote_size_bar.Add(quantity, pos=(0, 0), flag=wx.LEFT|wx.ALIGN_CENTER, border=15)

        self.enter_quant = wx.TextCtrl(self.panel)
        quote_size_bar.Add(self.enter_quant, pos=(0,1), flag=wx.ALIGN_CENTER)

        limit = wx.StaticText(self.panel, label="Limit Price")
        quote_size_bar.Add(limit, pos=(0, 2), flag=wx.ALIGN_CENTER)

        self.limit_entry = wx.TextCtrl(self.panel)
        quote_size_bar.Add(self.limit_entry, pos=(0,3), flag=wx.ALIGN_CENTER)

        self.order_type = wx.ComboBox(self.panel, value="Order type",
                                 choices=['Market', 'Limit', 'MidPointPeg'])
        quote_size_bar.Add(self.order_type, pos=(0,4), flag=wx.ALIGN_CENTER)

        buy_button = wx.Button(self.panel, label="BUY")
        quote_size_bar.Add(buy_button, pos=(0,5), flag=wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON, self.on_buy_button, buy_button)

        sell_button = wx.Button(self.panel, label="SELL")
        quote_size_bar.Add(sell_button, pos=(0, 6), flag=wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON, self.on_sell_button, sell_button)

        self.box.Add(quote_size_bar, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

    def on_buy_button(self, event):
        quantity = float(self.enter_quant.GetValue())
        limit = float(self.limit_entry.GetValue())
        order_type = self.order_type.GetValue()
        if order_type == "Order type":
            print "do nothin"
        elif order_type == "Market":
            # The stock id must be obtained from somewhere
            self.exchange.insert_order(MarketOrder(self.exchange.fake_engine.get_stock().get_ticker(), quantity, "walter", True))
        elif order_type == "Limit":
            self.exchange.insert_order(LimitOrder(self.exchange.fake_engine.get_stock().get_ticker(), quantity, limit, "walter", True))
        elif order_type == "MidPointPeg":
            self.exchange.insert_order(MidPointOrder(self.exchange.fake_engine.get_stock().get_ticker(), quantity, limit, "walter", True))

        #self.exchange.insert_order()

    def on_sell_button(self, event):
        #  discover the order type and make that the Order
        quantity = float(self.enter_quant.GetValue())
        limit = float(self.limit_entry.GetValue())
        order_type = self.order_type.GetValue()
        if order_type == "Order type":
            print "do nothin"
        elif order_type == "Market":
            # The stock id must be obtained from somewhere
            self.exchange.insert_order(MarketOrder(self.exchange.fake_engine.get_stock().get_ticker(), quantity, "walter", False))
        elif order_type == "Limit":
            self.exchange.insert_order(LimitOrder(self.exchange.fake_engine.get_stock().get_ticker(), quantity, limit, "walter", False))
        elif order_type == "MidPointPeg":
            self.exchange.insert_order(MidPointOrder(self.exchange.fake_engine.get_stock().get_ticker(), quantity, limit, "walter", False))

    def init_plot(self):
        self.fig = Figure((6.0, 5.0), dpi=100)   # what is this
        self.fig.patch.set_facecolor('white')
        self.axes = self.fig.add_subplot(1,1,1)
        self.axes.set_axis_bgcolor('black')     # what is this
        self.axes.set_title('Sample Chart', size=10)    # waht is this

        pylab.setp(self.axes.get_xticklabels(), fontsize=7)  # what does this do
        pylab.setp(self.axes.get_yticklabels(), fontsize=7)   # what does this do

        self.plot_data = self.axes.plot(
            self.data,
            linewidth=1,
            color=(1,1,0),
        )[0]  # what is all this

    def draw_plot(self):
        xmax = len(self.data)
        xmin = xmax - 50 if xmax > 50 else 0
        self.data = self.data if self.data else 0
        ymax = round(max(self.data), 0) + 1
        ymin = round(min(self.data), 0) - 1
        self.axes.set_xbound(lower=xmin, upper=xmax)
        self.axes.set_ybound(lower=ymin, upper=ymax)
        self.plot_data.set_xdata(np.arange(len(self.data)))
        self.plot_data.set_ydata(np.array(self.data))

        self.canvas.draw()

    def on_redraw_timer(self, event):
        new_transaction = self.exchange.fake_company.get_stock().get_last_transaction()
        if new_transaction:
            self.data.append(new_transaction.get_price())
        self.draw_plot()


if __name__ == '__main__':
    app = wx.App()
    QuoteInterface(None, title="First Attempt", exchange="none")
    app.MainLoop()