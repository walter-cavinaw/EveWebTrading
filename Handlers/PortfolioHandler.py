from BaseHandler import BaseHandler
import logging
import json
import tornado.escape
from sql_queries import queries
from helpers import date_handler


class PortfolioHandler(BaseHandler):

    def get(self, portfolioName):

        stocks_query = queries.folio_stocks_query
        folio_query = queries.folio_query
        db = self.db
        db.reconnect()
        userEmail = self.get_secure_cookie("user")

        # Get all portfolios that belong to the current user
        portfolios = db.query(folio_query, userEmail)
        logging.info(portfolios)

        # Check if a portfolio was specified in the url
        # Show the specified portfolio
        if portfolioName != None:
            logging.info("Requesting portfolio with name " + portfolioName)
            if userEmail:
                db_stocks = db.query(stocks_query, userEmail, portfolioName)
            else:
                db_stocks = db.query(stocks_query, 'dev@test.com', portfolioName)
            stocks = json.dumps(db_stocks, default=date_handler)
            self.render("portfolio.html", stocks=stocks, portfolios=portfolios)

        # Else, show the default portfolio
        else:
            logging.info("No portfolio selected, redirecting to default portfolio")
            self.redirect(self, "/portfolio/default")

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