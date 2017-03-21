# -*- coding: utf-8 -*-
import socketserver
import json
import time

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""
connected_users = {}

messages = []

help_text = "HERE IS SOME HELP: \n Available commands: \n login <username> \n message <message>"  # TODO: finalize help_text


class ClientHandler(socketserver.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        self.possible_requests = {
            'login': self.login,
            'logout': self.logout,
            'msg': self.message,
            'names': self.names,
            'help': self.help,
            'error': self.error
            # More key:values pairs are needed

        }

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            if received_string != b'':
                print(received_string)
                try:
                    payload = json.loads(received_string.decode())
                    self.choose_response(payload)
                except json.decoder.JSONDecodeError:
                    print('Invalid JSON')
                    # TODO: Add handling of received payload from client

    def choose_response(self, payload):

        if payload['request'] in self.possible_requests:
            return self.possible_requests[payload['request']](payload)
        else:
            raise ValueError("Invalid request")

    def login(self, payload):
        if payload['content'] in connected_users:
            self.error('Username already in use!')
        else:
            user = {
                'ip': self.ip,
                'port': self.port
            }
            connected_users[payload['content']] = user
            self.send_response('server', 'info', payload['content'] + ' logged in')

    def logout(self, payload):
        if payload['content'] in connected_users:
            # TODO: Check if user is trying to log out someone else
            del connected_users[payload['content']]
        else:
            self.error('Cannot log out, user is not logged in!')

    def message(self, payload):
        # TODO: Check if user is logged in, can't send message otherwise
        self.send_response('username', 'message', payload['content'])

    def names(self, payload):
        # TODO: Check if user is logged in, shouldn't be able to see names otherwise
        self.send_response('server', 'info', 'conncected users: ' + str(connected_users.keys()))
        pass

    def help(self, payload):
        self.send_response('server', 'info', help_text)
        pass

    def error(self, error_message):
        self.send_response('error', 'server', error_message)

    def send_response(self, username, response_code, response_data):
        response = {
            'timestamp': time.time(),
            'sender': username,
            'response': response_code,  # Should be 'error', 'info, 'message' or 'history'
            'content': response_data
        }
        json_data = json.dumps(response)
        self.connection.sendall(json_data.encode('ascii'))  # TODO: verifisere når client sin MessageReceiver er på plass


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9999
    print('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()