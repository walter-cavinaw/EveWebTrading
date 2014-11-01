import tornado.auth
import tornado.web


class LoginHandler(tornado.web.RequestHandler):

    def get(self):
        return self.render('login.html')