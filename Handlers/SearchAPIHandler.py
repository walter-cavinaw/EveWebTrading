from BaseHandler import BaseHandler
import logging
import json
from helpers import date_handler


class SearchAPIHandler(BaseHandler):

    def get(self):
        snippet = self.get_argument("matching", "")
        stocks = SearchAPIHandler.stocks
        results = [item for item in stocks if (snippet in item['ticker'] or snippet in item['name'])]
        results = json.dumps(results, default=date_handler)
        logging.info(results)
        # get query for finding matches in the database
        # return all potential matches to function
        # return all matches to the client as json like: ticker, name, dataset, startdate
        return self.write(results)