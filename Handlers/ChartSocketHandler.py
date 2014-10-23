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