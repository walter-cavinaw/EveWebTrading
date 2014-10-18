#!/usr/bin/python

from threading import Thread


class ClientThread(Thread):
    def __init__(self, client, process_thread):
        super(ClientThread, self).__init__()
        self.process_thread = process_thread
        self.client = client
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            # o/stok/ord/b/0xffffffff(size)/waltercavi/0xffffffff(limit)
            data = self.client.recv(45)
            if data:
                self.process_thread.add(data)
                # self.client.send("Order Received")
                if data[0] == "Q":
                    self.client.close()
                    self.stop()

