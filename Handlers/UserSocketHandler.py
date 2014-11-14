import logging
import uuid
import tornado.web
import tornado.escape
import tornado.websocket
from CDASimulator.OrderTypes import Order, LimitOrder, MarketOrder, MidPointOrder


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
        logging.info(self.get_secure_cookie("user"))
        if self.get_secure_cookie("user"):
            logging.info("user websocket opened")
            UserSocketHandler.waiters.add(self)
        else:
            logging.info("user not authenticated")
            self.close()

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
        logging.info("got message %r from user %r", message, self.get_secure_cookie("user"))
        parsed = tornado.escape.json_decode(message)
        try:
            order = {
                "trade": parsed["trade"],
                "type": parsed["type"],
                "ticker": parsed["ticker"],
                "shares": int(parsed["shares"]),
                "id": str(uuid.uuid4()),
                "user": self.get_secure_cookie("user"),
                }
            if 'price' in parsed:
                order["price"] = float(parsed["price"])
            else:
                order['price'] = None
            # Check the order parameters some more: is the ticker valid
            #                Are the prices and share amounts reasonable
            ex_order = UserSocketHandler.create_order(order)
            self.exchange.assert_is_order(ex_order)

            # Then send the order through to get processed

            # UserSocketHandler.update_cache(chat)
            # UserSocketHandler.send_updates(chat)
            success_notify = {"type": "notification",
                              "html": tornado.escape.to_basestring(
                                  self.render_string("success.html", message=ex_order.__str__()))
                              }
            UserSocketHandler.send_updates(success_notify)
        except:
            logging.error("Error when parsing Order data", exc_info=True)
            error_notify = {"type": "notification"}
            error_notify["html"] = tornado.escape.to_basestring(
                self.render_string("error.html", message="Order was not inputted correctly.")
            )
            UserSocketHandler.send_updates(error_notify)

    @classmethod
    def create_order(cls, order):
        type = order["type"]
        trade = order["trade"]
        size = order["shares"]
        ticker = order["ticker"]
        price = order["price"]
        ex_order = Order()
        if type == "Market":
            ex_order = MarketOrder()
        elif type == "Limit":
            ex_order = LimitOrder()
        elif type == "MidPoint":
            ex_order = MidPointOrder()
        if trade == "Buy":
            ex_order.set_buy(True)
        elif trade == "Sell":
            ex_order.set_buy(False)
        ex_order.set_size(size)
        ex_order.set_stock_ticker(ticker)
        if price is not None:
            ex_order.set_limit(price)
        return ex_order


