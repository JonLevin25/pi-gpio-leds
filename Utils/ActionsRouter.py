import re


class ActionsRouter:
    """
    Handles parsing strings and mapping to actions.
    Holds a dictionary of string keys -> func(string-> void) values
    Expects a "scheme" (regex pattern with 2 capture groups - the first being the key and the second
    is a payload string that will be passed to the func
    """

    def __init__(self, scheme='(.*?):(.*)$', actions={}):
        self.scheme = scheme
        for key in actions:
            fn_value = actions[key]
            if not callable(fn_value):
                raise TypeError("ActionsRouter expects {str: function} values! ")
        self.actions = actions

    def _parse(self, message):
        match = re.match('(.*?):(.*)$', message)
        if not match:
            print('Bad scheme!')
            return (None, None)

        (key, payload) = match.groups()
        print('key: {}, payloaad: {}'.format(key, payload))
        return key, payload

    def handle(self, message):
        (key, payload) = self._parse(message)
        if key in self.actions:
            fn_handler = self.actions[key]
            fn_handler(payload)
