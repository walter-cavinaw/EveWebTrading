#!/usr/bin/python

import socket
from ProcessThread import ProcessThread
from ClientThread import ClientThread

def main():
    t = ProcessThread()
    t.start()
    s = socket.socket()          # Create a socket object
    host = socket.gethostname()  # Get local machine name
    port = 12345                 # Reserve a port for your service.
    s.bind((host, port))         # Bind to the port
    print "Listening on port {p}...".format(p=port)

    s.listen(5)                   # Now wait for client connection.
    while True:
        try:
            client, addr = s.accept()
            ct = ClientThread(client, t)
            ct.start()
        except KeyboardInterrupt:
            print
            print "Stop."
            break
        except socket.error, msg:
            print "Socket error! %s" % msg
            break
    #
    cleanup(t)


def cleanup(t):
    t.stop()
    t.join()

#########################################################

if __name__ == "__main__":
    main()