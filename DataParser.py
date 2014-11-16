__author__ = 'Walter'

'''
Parse the stock data from the quandl wiki database. It is sent as an array of arrays in json.
'''
import urllib2
import json
import motor
from tornado.ioloop import IOLoop
import tornado.gen as gen

def main():
    user = "eve_server"
    pwd = "evetrading2014"
    database = "stockdata"
    uri = "mongodb://%s:%s@localhost:27017/%s" % (user, pwd, database)
    conn = motor.MotorClient(uri)
    db = conn.stockdata
    coll = db.AAPL

    query = "https://www.quandl.com/api/v1/datasets/"
    database = "WIKI/"
    dataset = "AAPL.json"
    start_date = "1980-12-12"
    end_date = "2014-11-12"
    url = query + database + dataset + "?trim_start=%s&trim_end=%s" % (start_date, end_date)
    req = urllib2.Request(url)
    opener = urllib2.build_opener()
    f = opener.open(req)
    wiki_data = json.loads(f.read())
    # the stock data is in json with key data. the data is an array of arrays with no keys.
    # within each data point array the data items are:
    # [Date,Open,High,Low,Close,Volume,Ex-Dividend,Split Ratio,Adj. Open,Adj. High,Adj. Low,Adj. Close,Adj. Volume]
    # adjusted items account for any splits or consolidations, so these will be the ones of interest

    data = wiki_data["data"]

    gen = (data_to_dict(item) for item in data)
    mongo_insert(gen, coll)
    # db.AAPL.insert(gen.next(), callback=done)
    IOLoop.instance().start()


def done(result, error):
    print "done"
    IOLoop.instance()


@gen.coroutine
def mongo_insert(gen, coll):
    yield coll.insert(gen)
    count = yield coll.count()
    print("Final count: %d" % count)
    IOLoop.instance().stop()


def data_to_dict(item):
    return {
        'date': item[0],
        'open': item[1],
        'high': item[2],
        'low': item[3],
        'close': item[4]
    }


if __name__ == "__main__":
    main()

