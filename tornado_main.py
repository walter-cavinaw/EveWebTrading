#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

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
from Handlers.HomeHandler import HomeHandler
from Handlers.ChartSocketHandler import ChartSocketHandler
from Handlers.MainHandler import MainHandler
from Handlers.UserSocketHandler import UserSocketHandler


define("port", default=8888, help="run on the given port", type=int)
django.setup()

# Global configurations and routing goes here
class Application(tornado.web.Application):
    def __init__(self):
        wsgi_app = tornado.wsgi.WSGIContainer(
        django.core.handlers.wsgi.WSGIHandler())
        handlers = [
            (r"/", HomeHandler),
            # Homepage is routed here
            (r"/trade", MainHandler),
            # Requests to get/post order data are routed here
            (r"/usersocket", UserSocketHandler),
            (r"/chartsocket", ChartSocketHandler),
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
