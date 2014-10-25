import logging
import tornado.escape
import tornado.ioloop
import tornado.websocket


class ChartSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = []
    data = []
    cache_size = 200

    # temporary loop index
    loopIndex = 0

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
        lines = [line.rstrip() for line in f]
        lineCount = len(lines)

        # temporary method to send a line of data every 2 seconds
        def sendChartData():
            indexToRead = ChartSocketHandler.loopIndex
            logging.info(indexToRead)
            if indexToRead == 0:
                indexToRead = 88
                ChartSocketHandler.loopIndex = 88
            if indexToRead > 1:
                message_arr = lines[indexToRead].split(",")
                message = {"date": message_arr[0],
                           "open": message_arr[1],
                           "high": message_arr[2],
                           "low": message_arr[3],
                           "close": message_arr[4],
                           "volume": message_arr[5]
                          }
                logging.info(message)
                ChartSocketHandler.send_updates(message)
                # iterate the loop index
                ChartSocketHandler.loopIndex -= 1

        chart_loop = tornado.ioloop.IOLoop.instance()
        schedule = tornado.ioloop.PeriodicCallback(sendChartData, 2000, io_loop=chart_loop)
        schedule.start()