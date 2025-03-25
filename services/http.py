from ipaddress import IPv4Address
from services.service import Service

class HttpService(Service):
    def __init__(self, ip_addr: IPv4Address, port: int) -> None:
        super().__init__("HTTP", ip_addr, port)

    # Cannot connect to a http service
    def connect(self, username, password=None):
        return False

    # Cannot login to an http service
    def try_login(self) -> bool:
        return False

    # if cannot login, cannot bruteforce either
    def bruteforce(self) -> bool:
        return False
