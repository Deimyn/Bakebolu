from ipaddress import IPv4Address
import options
from services.service import Service
from colorama import Fore, Style
import telnetlib
import sys

class TelnetService(Service):
    def __init__(self, ip_addr: IPv4Address, port: int) -> None:
        super().__init__("Telnet", ip_addr, port)

    def connect(self, username: str, password: str) -> bool:
        try:
            with telnetlib.Telnet(str(self.ip_addr), self.port, timeout=5) as tn:
                prompt = tn.read_until(b"login:", timeout=3)
                if b"login:" in prompt:
                    tn.write(username.encode("utf-8") + b"\n")

                prompt = tn.read_until(b"Password:", timeout=3)
                if b"Password:" in prompt:
                    tn.write(password.encode("utf-8") + b"\n")

                response = tn.read_until(b"$", timeout=3).decode(errors="ignore")

                if "Login incorrect" not in response and response.strip():
                    return True
                return False

        except Exception as e:
            if options.VERBOSE:
                sys.stdout.write("\r" + " " * 50 + "\r")
                sys.stdout.flush()
                print(f"    [TELNET ERROR] {e}")
            return False

    def try_login(self) -> bool:
        if self.connect("root", "root"):
            print(Fore.GREEN + f"    ({self.port} - {self.name}) Default credentials found: root:root" + Style.RESET_ALL)
            return True
        return False
