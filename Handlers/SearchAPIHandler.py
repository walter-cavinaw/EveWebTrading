from BaseHandler import BaseHandler
import logging
import json
from helpers import date_handler


class SearchAPIHandler(BaseHandler):

    def get(self):
        snippet = self.get_argument("matching", "").lower()
        # the static variable SearchAPIHandler.stocks is set in tornado_main
        stocks = SearchAPIHandler.stocks
        # filter the stocks by checking whether the snippet matches the ticker or name of stock
        results = [item for item in stocks if (snippet in item['ticker'].lower() or snippet in item['name'].lower())]
        # turn it into json string; date handler converts the date from a py object ot a string date
        results = json.dumps(results, default=date_handler)
        logging.info(results)
        return self.write(results)