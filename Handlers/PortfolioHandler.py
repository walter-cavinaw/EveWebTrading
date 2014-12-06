from BaseHandler import BaseHandler
import logging
import jsonpickle

class PortfolioHandler(BaseHandler):

    def get(self):

        db = self.db
        userEmail = self.get_secure_cookie("user")

        stockQuery = "SELECT * FROM users u, user_follows_stocks s WHERE u.email = %s AND u.id = s.userid"
        stocks = db.query(stockQuery, userEmail)
        logging.info(stocks)

        portfolios = [

        ]

        self.render("portfolio.html", jsonpickle=jsonpickle, stocks=stocks, portfolios=portfolios)