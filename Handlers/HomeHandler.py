from BaseHandler import BaseHandler
import jsonpickle

class HomeHandler(BaseHandler):

    def get(self):
        portfolios = [

        ]
        stocks = [
            {"ticker": "AAPL"},
            {"ticker": "GOOG"},
            {"ticker": "FB"},
            {"ticker": "NFLX"},
            {"ticker": "TWTR"},
            {"ticker": "BAC"},
            {"ticker": "COST"},
        ]
        self.render("home.html", jsonpickle=jsonpickle, stocks=stocks, portfolios=portfolios)