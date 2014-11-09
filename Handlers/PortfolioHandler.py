from BaseHandler import BaseHandler
import jsonpickle

class PortfolioHandler(BaseHandler):

    def get(self):
        portfolios = [

        ]
        stocks = [
            {"ticker": "DIS"},
            {"ticker": "TSLA"},
            {"ticker": "WFS"},
            {"ticker": "AAPL"},
            {"ticker": "GOOG"},
            {"ticker": "SCTY"},
            {"ticker": "FB"},
            {"ticker": "NFLX"},
            {"ticker": "TWTR"},
            {"ticker": "BAC"},
            {"ticker": "COST"},
        ]
        self.render("portfolio.html", jsonpickle=jsonpickle, stocks=stocks, portfolios=portfolios)