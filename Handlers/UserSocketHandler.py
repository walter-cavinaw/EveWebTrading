import logging
import uuid
import tornado.escape
import tornado.websocket


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