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

import django
import django.core.handlers.wsgi
import tornado.wsgi
import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import uuid
import threading
from CDASimulator.VirtualExchange import VirtualExchange
from CDASimulator.ExchangeObjects.Company import Company

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
django.setup()

# Global configurations and routing goes here
class Application(tornado.web.Application):
    def __init__(self):
        wsgi_app = tornado.wsgi.WSGIContainer(
        django.core.handlers.wsgi.WSGIHandler())
        handlers = [
            # Homepage is routed here
            (r"/", MainHandler),
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
            xsrf_cookies=True,
            debug=options.debug,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", messages=UserSocketHandler.cache)


class ChartSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = []
    data = []
    cache_size = 200

    # temporary loop index
    loopIndex = 0;

    def open(self):
        print("Chart websocket opened")
        ChartSocketHandler.waiters.add(self)

    def on_close(self):
        ChartSocketHandler.waiters.remove(self)

    @classmethod
    def update_cache(cls, message):
        cls.cache.append(message)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]

    @classmethod
    def send_updates(cls, message):
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(message)
            except:
                logging.error("Error sending message", exc_info=True)


    def on_message(self, message):
        logging.info("Message from client: " + message)
        parsed = tornado.escape.json_decode(message)
        ticker = parsed["ticker"]
        logging.info("Client is requesting live data for ticker " + ticker);

        # read data.csv
        f = open("static/data.csv")
        lines = f.readlines()
        lineCount = len(lines)

        # temporary method to send a line of data every 2 seconds
        def sendChartData():
            indexToRead = ChartSocketHandler.loopIndex%lineCount
            if indexToRead == 0:
                indexToRead = 1
            print(lines[indexToRead])
            ChartSocketHandler.send_updates(lines[indexToRead])
            # iterate the loop index
            ChartSocketHandler.loopIndex += 1

        chart_loop = tornado.ioloop.IOLoop.instance()
        schedule = tornado.ioloop.PeriodicCallback(sendChartData, 2000, io_loop = chart_loop)
        schedule.start()

    @classmethod
    def update_data(cls, datap):
        cls.data.append(datap)
        cls.send_updates(cls.data)
        print(cls.data)

class UserSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = []
    data = []
    cache_size = 200

    @classmethod
    def set_exchange(self, exchange):
        self.exchange = exchange

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        logging.info("user websocket opened")
        logging.info(self.exchange)
        UserSocketHandler.waiters.add(self)

    def on_close(self):
        UserSocketHandler.waiters.remove(self)

    @classmethod
    def update_cache(cls, message):
        cls.cache.append(message)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]

    @classmethod
    def send_updates(cls, message):
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(message)
            except:
                logging.error("Error sending message", exc_info=True)


    def on_message(self, message):
        logging.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)
        try:
            order = {
                "trade": parsed["trade"],
                "type": parsed["type"],
                "ticker": parsed["ticker"],
                "shares": int(parsed["shares"]),
                "price": int(parsed["price"]),
                "id": str(uuid.uuid4()),
                }
            order['html'] = tornado.escape.to_basestring(
               self.render_string("message.html", message=order))
            # Check the order parameters some more: is the ticker valid
            #                Are the prices and share amounts reasonable
            # Then send the order through to get processed

            # UserSocketHandler.update_cache(chat)
            # UserSocketHandler.send_updates(chat)
        except:
            logging.error("Error when parsing Order data", exc_info=False)
            error_notify = {"type": "notification"}
            error_notify["html"] = tornado.escape.to_basestring(
                self.render_string("error.html", message="Order was not inputted correctly.")
            )
            UserSocketHandler.send_updates(error_notify)

    @classmethod
    def update_data(cls, datap):
        cls.data.append(datap)
        cls.send_updates(cls.data)
        print(cls.data)

def main():
    companies = [Company("fake company", 3000, "FAKE")]
    eve = VirtualExchange(companies)
    ex_thread = threading.Thread(target=eve.run_exchange)
    ex_thread.start()
    tornado.options.parse_command_line()
    wsgi_app = tornado.wsgi.WSGIContainer(
    django.core.handlers.wsgi.WSGIHandler())
    UserSocketHandler.set_exchange(eve)
    tornado_app = tornado.web.Application(
    [
    (r"/trade", MainHandler),
    (r"/usersocket", UserSocketHandler),
    (r"/chartsocket", ChartSocketHandler),
    (r'.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app))
    ],
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        login_url="/auth/login",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
    )
    app = tornado_app
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    ex_thread.join()


if __name__ == "__main__":
    main()
