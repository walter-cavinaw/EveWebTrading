#!/usr/bin/env python
#
#the main script that runs the tornado server. Run this to start the server.

import os.path
import threading

import django
import django.core.handlers.wsgi
import tornado.wsgi
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.options import define, options

from CDASimulator.VirtualExchange import VirtualExchange
from CDASimulator.ExchangeObjects.Company import Company
from Handlers.ChartSocketHandler import ChartSocketHandler
from Handlers.MainHandler import MainHandler
from Handlers.UserSocketHandler import UserSocketHandler
from Handlers.AuthHandler import LoginHandler


define("port", default=8888, help="run on the given port", type=int)
django.setup()

# Global configurations and routing goes here
class Application(tornado.web.Application):
    def __init__(self):
        wsgi_app = tornado.wsgi.WSGIContainer(
        django.core.handlers.wsgi.WSGIHandler())
        handlers = [
            # Homepage is routed here
            (r"/trade", MainHandler),
            # Requests to get/post order data are routed here
            (r"/usersocket", UserSocketHandler),
            (r"/chartsocket", ChartSocketHandler),
            (r"/auth/login", LoginHandler),
            (r'.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
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
