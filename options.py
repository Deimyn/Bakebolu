import ipaddress


def initialize():
    global VERBOSE
    global TARGET_NETWORK
    global START_PORT
    global END_PORT
    global MAX_THREADS
    global USERNAME
    global PASSWORD_FILE_PATH

    VERBOSE = False
    # /32 mask is equivalent to 1 ip address
    TARGET_NETWORK = ipaddress.IPv4Network("127.0.0.1/32")
    START_PORT = 0
    END_PORT = 9999
    MAX_THREADS = 100
    USERNAME = None
    PASSWORD_FILE_PATH = None
