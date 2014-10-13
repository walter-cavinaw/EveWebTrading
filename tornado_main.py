#!/usr/bin/env python

# Run this with
# PYTHONPATH=. DJANGO_SETTINGS_MODULE=testsite.settings testsite/tornado_main.py
# Serves by default at
# http://localhost:8080/hello-tornado and
# http://localhost:8080/hello-django

from tornado.concurrent import Future
from tornado import gen
from tornado.options import define, options, parse_command_line

import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.web
import logging
import uuid
import os.path

# define("port", default=8080, help="run on the given port", type=int)
# define("debug", default=False, help="run in debug mode")
#
#
# class HelloHandler(tornado.web.RequestHandler):
#   def get(self):
#     # self.write('Hello from tornado')
#     self.render("base-tornado.html")
#
#
# class MessageBuffer(object):
#     def __init__(self):
#         self.waiters = set()
#         self.cache = []
#         self.cache_size = 200
#
#     def wait_for_messages(self, cursor=None):
#         # Construct a Future to return to our caller.  This allows
#         # wait_for_messages to be yielded from a coroutine even though
#         # it is not a coroutine itself.  We will set the result of the
#         # Future when results are available.
#         result_future = Future()
#         if cursor:
#             new_count = 0
#             for msg in reversed(self.cache):
#                 if msg["id"] == cursor:
#                     break
#                 new_count += 1
#             if new_count:
#                 result_future.set_result(self.cache[-new_count:])
#                 return result_future
#         self.waiters.add(result_future)
#         return result_future
#
#     def cancel_wait(self, future):
#         self.waiters.remove(future)
#         # Set an empty result to unblock any coroutines waiting.
#         future.set_result([])
#
#     def new_messages(self, messages):
#         logging.info("Sending new message to %r listeners", len(self.waiters))
#         for future in self.waiters:
#             future.set_result(messages)
#         self.waiters = set()
#         self.cache.extend(messages)
#         if len(self.cache) > self.cache_size:
#             self.cache = self.cache[-self.cache_size:]
#
#
# # Making this a non-singleton is left as an exercise for the reader.
# global_message_buffer = MessageBuffer()
#
#
# class BaseHandler(tornado.web.RequestHandler):
#     def get_current_user(self):
#         user_json = self.get_secure_cookie("chatdemo_user")
#         if not user_json: return None
#         return tornado.escape.json_decode(user_json)
#
#
# class MainHandler(BaseHandler):
#     @tornado.web.authenticated
#     def get(self):
#         self.render("chatroom.html", messages=global_message_buffer.cache)
#
#
# class MessageNewHandler(BaseHandler):
#     @tornado.web.authenticated
#     def post(self):
#         message = {
#             "id": str(uuid.uuid4()),
#             "from": self.current_user["first_name"],
#             "body": self.get_argument("body"),
#         }
#         # to_basestring is necessary for Python 3's json encoder,
#         # which doesn't accept byte strings.
#         message["html"] = tornado.escape.to_basestring(
#             self.render_string("message.html", message=message))
#         if self.get_argument("next", None):
#             self.redirect(self.get_argument("next"))
#         else:
#             self.write(message)
#         global_message_buffer.new_messages([message])
#
#
# class MessageUpdatesHandler(BaseHandler):
#     @tornado.web.authenticated
#     @gen.coroutine
#     def post(self):
#         cursor = self.get_argument("cursor", None)
#         # Save the future returned by wait_for_messages so we can cancel
#         # it in wait_for_messages
#         self.future = global_message_buffer.wait_for_messages(cursor=cursor)
#         messages = yield self.future
#         if self.request.connection.stream.closed():
#             return
#         self.write(dict(messages=messages))
#
#     def on_connection_close(self):
#         global_message_buffer.cancel_wait(self.future)
#
#
# class AuthLoginHandler(BaseHandler, tornado.auth.GoogleMixin):
#     @gen.coroutine
#     def get(self):
#         if self.get_argument("openid.mode", None):
#             user = yield self.get_authenticated_user()
#             self.set_secure_cookie("chatdemo_user",
#                                    tornado.escape.json_encode(user))
#             self.redirect("/")
#             return
#         self.authenticate_redirect(ax_attrs=["name"])
#
#
# class AuthLogoutHandler(BaseHandler):
#     def get(self):
#         self.clear_cookie("chatdemo_user")
#         self.write("You are now logged out")
#
# def main():
#   parse_command_line()
#   wsgi_app = tornado.wsgi.WSGIContainer(
#     django.core.handlers.wsgi.WSGIHandler())
#   tornado_app = tornado.web.Application(
#     [
#       (r'/hello-tornado', HelloHandler),
#       (r'/chat', MainHandler),
#       (r"/auth/login", AuthLoginHandler),
#       (r"/auth/logout", AuthLogoutHandler),
#       (r"/a/message/new", MessageNewHandler),
#       (r"/a/message/updates", MessageUpdatesHandler),
#       (r'.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
#     ],
#         cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
#         login_url="/auth/login",
#         template_path=os.path.join(os.path.dirname(__file__), "chatroom/../templates"),
#         static_path=os.path.join(os.path.dirname(__file__), "chatroom/../static"),
#         xsrf_cookies=True,
#         debug=options.debug,
#     )
#   server = tornado.httpserver.HTTPServer(tornado_app)
#   server.listen(options.port)
#   tornado.ioloop.IOLoop.instance().start()
#
# if __name__ == '__main__':
#   main()

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
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        logging.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)
        chat = {
            "id": str(uuid.uuid4()),
            "body": parsed["ticker"],
            }
        chat["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=chat))

        ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)


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
