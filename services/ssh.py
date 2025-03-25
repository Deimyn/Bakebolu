from ipaddress import IPv4Address
import options
from services.service import Service
from colorama import Fore, Style
import paramiko
import os

class SshService(Service):
    def __init__(self, ip_addr: IPv4Address, port: int) -> None:
        super().__init__("SSH", ip_addr, port)
        self.wordlist_path = os.path.join(os.path.dirname(__file__), "../test_lab/", "wordlist.txt")

    def connect(self, username: str, password: str) -> bool:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(str(self.ip_addr), port=self.port, username=username, password=password, timeout=5)
            client.close()
            return True
        except paramiko.AuthenticationException:
            return False
        except paramiko.SSHException as e:
            if options.VERBOSE:
                print(f"    [SSH ERROR] {e}")
            return False
        except EOFError as e:
            if options.VERBOSE:
                print(f"    [ERROR] {e}")
            return False
        except Exception as e:
            if options.VERBOSE:
                print(f"    [ERROR] {e}")
            return False

    def try_login(self) -> bool:
        if self.connect("root", "root"):
            print(Fore.GREEN + f"    ({self.port}) Default credentials found: root:root" + Style.RESET_ALL)
            return True
        return False

