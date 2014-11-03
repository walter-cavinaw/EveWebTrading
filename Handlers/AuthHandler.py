from BaseHandler import BaseHandler
import logging


class LoginHandler(BaseHandler):

    database = None

    @classmethod
    def set_db(cls, db):
        cls.database = db

    def get(self):
        logging.info(self.get_argument("next"))
        return self.render('login.html', next=self.get_argument("next", "/"))

    def post(self):
        logging.info(self.get_argument("next"))
        # these strings need to be checked for random values. They can only be a-z, 0-9, @ and dot.
        email = self.get_argument("user_email")
        # this can only have a-z, 0-9, -,_, etc. Nothing that could mess up the query below.
        pwd = self.get_argument("password")
        query = "SELECT * FROM users WHERE id = %s AND pass = %s"
        user = LoginHandler.database.get(query, email, pwd)
        if user:
            self.set_secure_cookie("user", email)
            self.redirect(self.get_argument("next", "/"))
        else:
            self.render("login.html")


class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))