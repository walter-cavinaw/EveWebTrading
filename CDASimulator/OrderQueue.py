#!/usr/bin/python

# Extends the Queue Python implementation, so that we can cancel Orders in the Queue

import Queue
import heapq


class OrderQueue(Queue.PriorityQueue):

    def cancel_order(self, new_item):
        self.mutex.acquire()
        try:
            if len(self.queue) > 0:
                for item in self.queue:
                    if new_item == item:
                        print "get here"
                        item = self.queue[-1]
                        self.queue.pop()
                        heapq.heapify(self.queue)
        finally:
            self.mutex.release()


class PriorityOrderQueue(OrderQueue):
    def _init(self, maxsize):
        self.queue = []

    def _get(self, heappop=heapq.heappop):
        return heappop(self.queue)

    def _put(self, item, heappush=heapq.heappush):
        heappush(self.queue, item)

    def _qsize(self, len=len):
        return len(self.queue)

if __name__ == '__main__':
    order_queue = OrderQueue()
    order_queue.put((5, 3, 2))
    for x in xrange(0, 6):
        order_queue.put((x, 4, 1))
    order_queue.cancel_order((5, 3, 2))
    print order_queue.qsize()