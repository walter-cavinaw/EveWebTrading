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
"""Simplified chat demo for websockets.

Authentication, error handling, etc are left as an exercise for the reader :)
"""
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

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
django.setup()

class Application(tornado.web.Application):
    def __init__(self):
        wsgi_app = tornado.wsgi.WSGIContainer(
        django.core.handlers.wsgi.WSGIHandler())
        handlers = [
            (r"/", MainHandler),
            (r"/chatsocket", ChatSocketHandler),
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

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("base-tornado.html")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", messages=ChatSocketHandler.cache)

class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = []
    data = []
    cache_size = 200

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        ChatSocketHandler.waiters.remove(self)

    @classmethod
    def update_cache(cls, chat):
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]

    @classmethod
    def send_updates(cls, chat):
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                print(chat)
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        logging.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)
        chat = {
            "id": str(uuid.uuid4()),
            "body": parsed["price"],
            }
        chat["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=chat))

        #self.serpdate_data(int(parsed["price"]))

        ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)

    @classmethod
    def update_data(cls, datap):
        cls.data.append(datap)
        cls.send_updates(cls.data)
        print(cls.data)

def main():
    tornado.options.parse_command_line()
    wsgi_app = tornado.wsgi.WSGIContainer(
    django.core.handlers.wsgi.WSGIHandler())
    tornado_app = tornado.web.Application(
    [
    (r"/test", TestHandler),
    (r"/chat", MainHandler),
    (r"/chatsocket", ChatSocketHandler),
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


if __name__ == "__main__":
    main()
