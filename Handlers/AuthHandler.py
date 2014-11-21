from BaseHandler import BaseHandler
import tornado.escape as esc
import logging
import bcrypt
import torndb


class RegisterHandler(BaseHandler):

    def get(self):
        return self.render("register.html")

    def post(self):
        email = self.get_argument("user_email")
        pwd = self.get_argument("password")
        confirmPwd = self.get_argument("confirmPassword")

        if pwd == confirmPwd:
            db = self.db
            query = "SELECT * FROM users WHERE id = %s"
            user = db.get(query, email)
            if not user:
                hashedPwd = bcrypt.hashpw(pwd, bcrypt.gensalt())
                logging.info("Hashed password: " + hashedPwd)
                query = "INSERT INTO users (id, pass) VALUES (%s, %s)"
                db.reconnect()
                db.insert(query, email, hashedPwd)
                self.redirect("/auth/login")
            else:
                error_msg = self.render_string('error.html', message="This user already exists")
                self.render("register.html", notification=error_msg)
        else:
            error_msg = self.render_string('error.html', message="The passwords don't match")
            self.render("register.html", notification=error_msg)


class LoginHandler(BaseHandler):

    def get(self):
        next_arg = esc.url_escape(self.get_argument("next", "/"))
        logging.info(next_arg)
        return self.render('login.html', next=next_arg)

    def post(self):
        next_arg = esc.url_escape(self.get_argument("next", "/"))
        logging.info(next_arg)
        db = self.db
        db.reconnect()
        # these strings need to be checked for random values. They can only be a-z, 0-9, @ and dot.
        email = self.get_argument("user_email")
        # this can only have a-z, 0-9, -,_, etc. Nothing that could mess up the query below.
        pwd = self.get_argument("password")
        query = "SELECT * FROM users WHERE id = %s"
        user = db.get(query, email)
        if user:
            # get hashed password from user
            userRow = torndb.Row(user)
            hashedPwd = userRow.__getattr__("pass")
            if bcrypt.hashpw(pwd, hashedPwd) == hashedPwd:
                self.set_secure_cookie("user", email)
                self.redirect(self.get_argument("next", "/"))
            else:
                # password is incorrect
                error_msg = self.render_string('error.html', message="Login Credentials were incorrect")
                self.render("login.html", notification=error_msg, next=next_arg)
        else:
            # user does not exist
            error_msg = self.render_string('error.html', message="Login Credentials were incorrect")
            self.render("login.html", notification=error_msg, next=next_arg)

class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))