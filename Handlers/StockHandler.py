from BaseHandler import BaseHandler
import tornado.escape as esc
import logging


class StockHandler(BaseHandler):

    def get(self, ticker):
        logging.info(ticker)
        return self.render('stock.html', stock=ticker)
