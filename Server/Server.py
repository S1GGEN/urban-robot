# -*- coding: utf-8 -*-
import socketserver
import json
import time

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

connection_threads = []

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

help_text = "\n HERE IS SOME HELP: \n Available commands: \n login <username> \n message <message>"  # TODO: finalize help_text


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

        connection_threads.append(self)

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
        if not self.validate_user():
            if username in connected_users:
                self.error('Username already in use!')
            else:
                user = {
                    'ip': self.ip,
                    'port': self.port
                }
                connected_users[username] = user

                self.send_to_all('server', 'info', username + ' logged in')
                self.send_response('server', 'history', messages)

                # DEBUG LOG:
                print(str(connected_users))
        else:
            self.error('You are already logged in! \n Log out to log in with another username')

    def logout(self):
        username = self.validate_user()
        if username in connected_users:
            del connected_users[username]
            self.send_response('server', 'info', username + " logged out")

            # DEBUG LOG:
            print(connected_users)
        else:
            self.error('You cannot log out, as you are not logged in!!')  # TODO: will this ever be relevant?

    def message(self, payload):
        username = self.validate_user()
        if username:
            messages.append({'timestamp': time.time(), 'sender': username, 'content': payload['content']})
            self.send_to_all('server', 'info', payload['content'])
        else:
            self.error('You cannot send messages, as you are not logged in!')

    def send_to_all(self, sender, type, content):
        for thread in connection_threads:
            if thread.validate_user():
                thread.send_response(sender, type, content)

    def names(self):
        username = self.validate_user()

        if username:
            response_string = 'Connected users: \n'
            for username in connected_users.keys():
                response_string += username + '\n'
            self.send_response('server', 'info', response_string)
        else:
            self.error('You cannot see names, as you are not logged in!')

    def help(self):
        self.send_response('server', 'info', help_text)

    def error(self, error_message):
        self.send_response('server', 'error', error_message)

    def validate_user(self):
        for user in connected_users.keys():
            if self.ip == connected_users[user]['ip'] and self.port == connected_users[user]['port']:
                return user
        return False

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
    HOST, PORT = 'localhost', 9999
    print('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()