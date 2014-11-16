import tornado.web
from BaseHandler import BaseHandler


class MainHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render("trade.html")
