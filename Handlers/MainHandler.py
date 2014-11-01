import tornado.web
from Handlers.UserSocketHandler import UserSocketHandler


class MainHandler(tornado.web.RequestHandler):

    # @tornado.web.authenticated
    def get(self):
        self.render("index.html")
