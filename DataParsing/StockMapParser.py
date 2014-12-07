import csv
import urllib2
import MySQLdb


def main():

    mydb = MySQLdb.connect(host='localhost',
    user='eve_server',
    passwd='evetrading2014',
    db='eve')
    cursor = mydb.cursor()
    api_url = "http://www.quandl.com/api/v2/datasets.csv?query=*&source_code=WIKI&per_page=300&page={kwarg}&auth_token=nb1EsCSBc7fgbiRCLwYh"

    for page in range(1, 12):
        pass_url = api_url.format(kwarg=page)
        req = urllib2.Request(pass_url)
        opener = urllib2.build_opener()
        f = opener.open(req)
        stock_map = csv.reader(f)

        for row in stock_map:
            ticker = row[0][5:]
            name = row[1].split(' (', 1)[0]
            if name[0] == '(':
                name =''
            param = (ticker, name, row[0], row[2])
            cursor.execute("INSERT INTO stocks(ticker, name, dataset, startdate) VALUES(%s, %s, %s, %s)", param)

    mydb.commit()
    mydb.close()


if __name__ == '__main__':
    main()