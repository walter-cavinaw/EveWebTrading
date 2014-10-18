#!/usr/bin/python


class Transaction(object):

    total_transactions = 0

    def __init__(self, size, price, buyer, seller, timestamp, stock, **kwds):
        self.timestamp = timestamp
        self.stock = stock
        self.size = size
        self.price = price
        self.buyer = buyer
        self.seller = seller
        Transaction.total_transactions += 1
        super(Transaction, self).__init__(**kwds)

    def get_buyer(self):
        return self.buyer

    def get_seller(self):
        return self.seller

    def get_price(self):
        return self.price

    def get_size(self):
        return self.size

    def get_stock(self):
        return self.stock

    def __str__(self):
        return "quantity:"+self.size.__str__()+", Price:"+self.price.__str__()+", Buyer: "+self.buyer.__str__()
