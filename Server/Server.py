# -*- coding: utf-8 -*-
import socketserver
import json
import time

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""
connected_users = {
    'Sigurd': {
        'ip': '127.0.0.1',
        'port': 133769
    },
    'Sigurd2': {
        'ip': '127.0.0.1',
        'port': 420420
    },
    'Sigurd3': {
        'ip': '127.0.0.1',
        'port': 691337
    }
}

messages = [
    {
      "message": "message0",
      "sender": "user0",
      "timestamp": "1490105373.0190203"
    },
    {
      "message": "message1",
      "sender": "user1",
      "timestamp": "1490105373.0190203"
    },
    {
      "message": "message2",
      "sender": "user2",
      "timestamp": "1490105373.0190203"
    }
]

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
            'help': self.help
            # More key:values pairs may be needed (rooms etc)
        }

        self.possible_requests_with_arguments = {
            'login': self.login,
            'msg': self.message
        }

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            if True:  # received_string != b'': TODO: Check if this really is useful at all
                # DEBUG LOG:
                print('received: ' + str(received_string))

                try:
                    payload = json.loads(received_string.decode())
                    self.choose_response(payload)
                except json.decoder.JSONDecodeError:
                    print('Invalid JSON')

    def choose_response(self, payload):

        if payload['request'] in self.possible_requests:
            if payload['request'] in self.possible_requests_with_arguments:
                return self.possible_requests[payload['request']](payload)
            else:
                return self.possible_requests[payload['request']]()
        else:
            raise ValueError("Invalid request")

    def login(self, payload):
        username = payload['content']
        if username in connected_users:
            self.error('Username already in use!')
        else:
            user = {
                'ip': self.ip,
                'port': self.port
            }
            connected_users[username] = user

            self.send_response('server', 'history', messages)
            self.send_response('server', 'error', username + ' logged in')

            # DEBUG LOG:
            print(username + " logged in")
            print(str(connected_users))

    def logout(self):
        username = 'test_user'  # TODO: Find user from ip and port
        if username in connected_users:
            del connected_users[username]
        else:
            self.error('Cannot log out, user is not logged in!')

    def message(self, payload):
        username = 'test_user'  # TODO: Find user from ip and port
        messages.append({'timestamp': time.time(), 'sender': username, 'content': payload['content']})
        self.send_response(username, 'message', payload['content'])

    def names(self):
        # TODO: Check if user is logged in, shouldn't be able to see names otherwise
        response_string = 'Connected users: \n'
        for username in connected_users.keys():
            response_string += username + '\n'
        self.send_response('server', 'info', 'connected users: ' + response_string)
        pass

    def help(self):
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
        self.connection.sendall(json_data.encode('ascii'))  # TODO: verifisere når Client/MessageReceiver er på plass

        # DEBUG LOG:
        print('sending: ' + str(json_data))


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
    HOST, PORT = 'localhost', 9998
    print('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
