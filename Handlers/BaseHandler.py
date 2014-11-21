import tornado.web


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        user = self.get_secure_cookie("user")
        if not user:
            return None
        else:
            return user

    @property
    def db(self):
        return self.application.db