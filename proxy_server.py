#! python
#
# Proxy Server - Server
# Reference:
# https://pymotw.com/2/SocketServer/
import logging
# import sys
import socket
import socketserver
import sys


logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')


class ProxyRequestHandler(socketserver.BaseRequestHandler):
    # This is the request handler class for the server
    # It is instantiated once per connection to the server and must override
    # the "handle()" method to implement communication to the client

    def __init__(self, request, client_address, server):

        self.logger = logging.getLogger('ProxyRequestHandler')
        self.logger.debug('__init__')
        socketserver.BaseRequestHandler.__init__(
            self, request, client_address, server
        )
        return

    def handle(self):
        # Overriding the handle method of the Request handler to insert custom
        # logic. The request from the lhost is received, sent to the server,
        # server response is received, then passed back to the client

        # Unsure at this point if establishing self.data as an empty binary
        # var is necessary or not
        self.data = b''

        while True:
            # This is the receive loop - it receives based on the buffer size
            # until it receives less data than the buffer size (at which point
            # the transmission should be done).
            part = self.request.recv(server.buffer)
            self.data += part
            if len(part) < server.buffer:
                break

        # TODO: Need message handler logic here to pass off the lhost message
        #       for later processing
        self.lhost_data_handler(self.client_address, self.data)

        # Sending message from lhost to rhost
        try:

            response = self.rhost_handler(
                server.remote_address, server.buffer, self.data
            )

        except Exception as e:
            self.logger.critical(f"An exception occurred - exiting: {e}")
            sys.exit(1)

        # Sending back the same date but upper-case to the local client
        self.request.sendall(response)

    def lhost_data_handler(self, lhost, data):
        self.logger.debug('Handling local host data')
        self.logger.debug(f"{lhost[0]} wrote {data}")
        self.logger.debug(f"Transmission length: {len(data)}")

    def rhost_handler(self, rhost, buffer, data):
        self.logger.debug(f"Attempting connection to {rhost[0]}:{rhost[1]}")
        # Create a temporary socket to send data to and receive data from rhost
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as remote:
            remote.connect(rhost)
            remote.sendall(data)

            rdata = b''

            # Receive back from the server
            while True:
                part = remote.recv(buffer)
                rdata += part
                if len(part) < buffer:
                    break

            remote.close()

            return rdata


class ProxyServer(socketserver.TCPServer):
    # This is the server

    def __init__(
        self, server_address, handler_class=ProxyRequestHandler, buffer=1024,
        remote_address=("127.0.0.1", 54321)
    ):
        self.logger = logging.getLogger('ProxyServer')
        self.buffer = buffer
        self.remote_address = remote_address
        self.logger.debug(f'__init__\nbuffer: {self.buffer}')
        socketserver.TCPServer.__init__(self, server_address, handler_class)

    def server_activate(self):
        self.logger.info(
            f"Listening on {self.server_address[0]}:"
            f"{self.server_address[0]}"
        )
        socketserver.TCPServer.server_activate(self)


if __name__ == "__main__":

    logger = logging.getLogger('Test_Output')

    local = ("localhost", 9999)

    remote = ("localhost", 54321)

    # Create the server, binding to localhost on port 9999
    with ProxyServer(local, ProxyRequestHandler, 8, remote) as server:
        try:
            # Activate the server; this will keep running until given a
            # keyboard
            # interrupt (Ctrl + C)
            server.serve_forever()
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt - shutting down")
