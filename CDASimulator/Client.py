#!/usr/bin/python

import socket

client_socket = socket.socket()

client_socket.connect((socket.gethostname(), 12345))

count = 5
while count > 0:
    # o/stok/ord/b/0xffffffff(size)/waltercavi/0xffffffff
    client_socket.sendall("O/FAKE/LMT/B/0x00000010/waltercavi/0x00000010")
    #data = client_socket.recv(20)
    #print data
    count -= 1


client_socket.send("Q")
client_socket.close()