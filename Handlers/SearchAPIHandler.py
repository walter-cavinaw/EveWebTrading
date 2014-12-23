from BaseHandler import BaseHandler
import logging
import json
from sql_queries import queries
from helpers import date_handler


class SearchAPIHandler(BaseHandler):
    initialized = False

    def init(self):
        SearchAPIHandler.initialized = True
        db = self.db
        db.reconnect()
        query = queries.all_stocks
        SearchAPIHandler.stocks = db.query(query)

    def get(self):
        if not SearchAPIHandler.initialized:
            self.init()
        snippet = self.get_argument("matching", "")
        dicts = SearchAPIHandler.stocks
        results = [item for item in dicts if (snippet in item['ticker'] or snippet in item['name'])]
        results = json.dumps(results, default=date_handler)
        logging.info(results)
        # get query for finding matches in the database
        # return all potential matches to function
        # return all matches to the client as json like: ticker, name, dataset, startdate
        return self.write(results)