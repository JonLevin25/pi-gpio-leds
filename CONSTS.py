PORT = 8888
ACTIONS_PATH = r"/leds"
DISCOVERY_PATH = r"/actions/discover"
SERVER_IP = "192.168.1.106"

ACTIONS_REMOTE_URL = f"ws://{SERVER_IP}:{PORT}{ACTIONS_PATH}"
ACTIONS_DISCOVERY_URL = f"http://{SERVER_IP}:{PORT}{DISCOVERY_PATH}"


class HTTP_Headers:
    Key_ContentType = "Content-Type"
    Val_AppJson = "application/json"
