import json

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history
            # More key:values pairs could be needed
        }

    def parse(self, data):
        try:
            payload = json.loads(data)
        except Exception as e:
            return {
                'title': 'Nothing in response',
                'message': e,
                'data': data
            }
        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            print("ELSE?")
            print(payload['response'])

    def parse_error(self, payload):
        # print("error")
        return str(payload['timestamp']) + bcolors.FAIL + ": ERROR: " + str(payload['content'] + bcolors.ENDC)

    def parse_info(self, payload):
        # print("info")
        return str(payload['timestamp']) + ": " + str(payload['content'])

    def parse_message(self, payload):
        # print("msg")
        return str(payload['timestamp']) + ": " + payload['sender'] + ": " + payload['content']

    def parse_history(self, payload):
        history_string = ""
        for message in payload['content']:
            history_string += "\n" + self.parse_message(message)
        return history_string


if __name__ == '__main__':
    """
    This is the main method

    No alterations are necessary
    """
    myParser = MessageParser()

    print(myParser.parse(payload="dsdsd"))
