import tornado.web
from Handlers.UserSocketHandler import UserSocketHandler

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", messages=UserSocketHandler.cache)