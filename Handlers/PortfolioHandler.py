from BaseHandler import BaseHandler
import logging
import json
from sql_queries import queries

class PortfolioHandler(BaseHandler):

    def get(self):

        stocks = []
        portfolios = []
        stocks_query = queries.folio_stocks_query
        db = self.db
        db.reconnect()
        userEmail = self.get_secure_cookie("user")

        if userEmail:
            db_stocks = db.query(stocks_query, userEmail, 'default')
            logging.info(stocks)
        else:
            db_stocks = db.query(stocks_query, 'dev@test.com', 'default')
        stocks = json.dumps(db_stocks, default=self.date_handler)
        self.render("portfolio.html", stocks=stocks, portfolios=portfolios)

    @staticmethod
    def date_handler(obj):
        return obj.isoformat() if hasattr(obj, 'isoformat') else obj