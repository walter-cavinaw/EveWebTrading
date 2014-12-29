from BaseHandler import BaseHandler
import logging
import json
import tornado.escape
from sql_queries import queries
from helpers import date_handler


class PortfolioHandler(BaseHandler):

    def get(self):

        portfolios = []
        stocks_query = queries.folio_stocks_query
        db = self.db
        db.reconnect()
        userEmail = self.get_secure_cookie("user")

        if userEmail:
            db_stocks = db.query(stocks_query, userEmail, 'default')
        else:
            db_stocks = db.query(stocks_query, 'dev@test.com', 'default')
        stocks = json.dumps(db_stocks, default=date_handler)
        self.render("portfolio.html", stocks=stocks, portfolios=portfolios)

    def post(self):
        user = self.get_current_user()
        stock = tornado.escape.json_decode(self.request.body)['stock']
        if user and stock:
            db = self.db
            db.reconnect()
            query = queries.add_stock_query
            try:
                db.execute(query, user, 'default', stock)
            except:
                logging.error("Error adding stock to portfolio")
                self.send_error(400)