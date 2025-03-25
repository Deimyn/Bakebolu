from ipaddress import IPv4Address
from services.service import Service
import smbclient

class SmbService(Service):
    def __init__(self, ip_addr: IPv4Address, port: int) -> None:
        super().__init__("Samba", ip_addr, port)

    def connect(self, username: str, password: str) -> bool:
        return False

    def try_login(self):
        return False
