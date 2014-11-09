#!/usr/bin/env python
#
#the main script that runs the tornado server. Run this to start the server.

import os.path
import threading
import tornado.wsgi
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.options import define, options
import torndb

from CDASimulator.VirtualExchange import VirtualExchange
from CDASimulator.ExchangeObjects.Company import Company
from Handlers import ChartSocketHandler, MainHandler, UserSocketHandler, LoginHandler, LogoutHandler, \
    HomeHandler, RegisterHandler, PortfolioHandler


define("port", default=8888, help="run on the given port", type=int)
define("mysql_host", default="localhost:3306", help="eve database host")
define("mysql_database", default="eve", help="database/schema name: eve")
define("mysql_user", default="eve_server", help="eve server login id")
define("mysql_password", default="evetrading2014", help="eve server password")


# Global configurations and routing goes here
class Application(tornado.web.Application):
    def __init__(self):
        LoginHandler.set_db(torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password))
        handlers = [
            (r"/", HomeHandler),
            # Homepage is routed here
            (r"/portfolio", PortfolioHandler),
            (r"/trade", MainHandler),
            # Requests to get/post order data are routed here
            (r"/usersocket", UserSocketHandler),
            # Chart data
            (r"/chartsocket", ChartSocketHandler),
            (r"/auth/login", LoginHandler),
            (r"/auth/logout", LogoutHandler),
            (r"/auth/register", RegisterHandler),
            # potentially get rid of this
            (r'.*', HomeHandler),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/auth/login",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    companies = [Company("fake company", 3000, "FAKE")]
    eve = VirtualExchange(companies)
    ex_thread = threading.Thread(target=eve.run_exchange)
    ex_thread.start()
    tornado.options.parse_command_line()
    UserSocketHandler.set_exchange(eve)
    tornado_app = Application()
    app = tornado_app
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    ex_thread.join()


if __name__ == "__main__":
    main()
