from ipaddress import IPv4Address
import options
from services.service import Service
from colorama import Fore, Style
import mysql.connector

class MySqlService(Service):
    def __init__(self, ip_addr: IPv4Address, port: int) -> None:
        super().__init__("MySql", ip_addr, port)

    def connect(self, username: str, password: str) -> bool:
        try:
            mysql.connector.connect(user=username, password=password, host=format(self.ip_addr), port=self.port)
            return True
        except Exception as e:
            if options.VERBOSE:
                print(f"    [MYSQL ERROR] : {e}")
            return False

    def try_login(self):
        if self.connect("root", "root"):
            print(Fore.GREEN + f"    ({self.port}) Default credentials found: root:root" + Style.RESET_ALL)
            return True
        return False

