from BaseHandler import BaseHandler
import logging
import jsonpickle
from sql_queries import queries

class PortfolioHandler(BaseHandler):

    def get(self):

        stocks = []
        portfolios = []
        stocks_query = queries.folio_stocks_query
        db = self.db
        userEmail = self.get_secure_cookie("user")

        if userEmail:
            stocks = db.query(stocks_query, userEmail, 'default')
            logging.info(stocks)

        else:
            stocks = db.query(stocks_query, 'dev@test.com', 'default')

        self.render("portfolio.html", jsonpickle=jsonpickle, stocks=stocks, portfolios=portfolios)