from BaseHandler import BaseHandler


class HomeHandler(BaseHandler):

    def get(self):
        self.render("home.html")
