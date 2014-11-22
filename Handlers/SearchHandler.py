from BaseHandler import BaseHandler
import tornado.escape as esc
import logging


class SearchHandler(BaseHandler):

    def get(self, ticker):
        return self.render('search.html')

    def post(self):
        #check if it is a stock
        url = "/stock/" + self.get_argument("ticker")
        self.redirect(url)
