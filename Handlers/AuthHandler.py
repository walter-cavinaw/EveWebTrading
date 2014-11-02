from BaseHandler import BaseHandler


class LoginHandler(BaseHandler):

    def get(self):
        return self.render('login.html')

    def post(self):
        print self.get_argument("name")
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/trade")


class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))