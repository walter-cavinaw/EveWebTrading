#!/usr/bin/env python
#
#the main script that runs the tornado server. Run this to start the server.

import threading
import tornado.wsgi
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.options import options
import torndb
from settings import settings

from CDASimulator.VirtualExchange import VirtualExchange
from CDASimulator.ExchangeObjects.Company import Company
from Handlers import ChartSocketHandler, MainHandler, UserSocketHandler, LoginHandler, LogoutHandler, \
    HomeHandler, RegisterHandler, PortfolioHandler, StockHandler, SearchHandler, SearchAPIHandler


# Global configurations and routing goes here
class Application(tornado.web.Application):
    def __init__(self):
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)
        handlers = [
            (r"/", HomeHandler),
            # Homepage is routed here
            (r"/portfolio", PortfolioHandler),
            (r"/trade", MainHandler),
            # Requests to get/post order data are routed here
            (r"/usersocket", UserSocketHandler),
            # Chart data
            (r"/stock/(.*)", StockHandler),
            (r"/search/(.*)", SearchHandler),
            (r"/search_api", SearchAPIHandler),
            (r"/chartsocket", ChartSocketHandler),
            (r"/auth/login", LoginHandler),
            (r"/auth/logout", LogoutHandler),
            (r"/auth/register", RegisterHandler),
            # potentially get rid of this
            (r'.*', HomeHandler),
        ]
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
