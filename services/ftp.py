from ipaddress import IPv4Address
import options
from services.service import Service
from colorama import Fore, Style
import ftplib

class FtpService(Service):
    def __init__(self, ip_addr: IPv4Address, port: int) -> None:
        super().__init__("FTP", ip_addr, port)

    def connect(self, username: str, password: str) -> bool:
        try:
            ftp = ftplib.FTP()
            ftp.connect(str(self.ip_addr), self.port, timeout=5)
            ftp.login(username, password)
            ftp.quit()
            return True
        except ftplib.error_perm:
            return False  # Invalid login credentials
        except Exception as e:
            if options.VERBOSE:
                print(f"    [FTP ERROR] {e}")
            return False

    def try_login(self) -> bool:
        try:
            ftp = ftplib.FTP()
            ftp.connect(str(self.ip_addr), self.port, timeout=5)
            response = ftp.login("Anonymous", "")
            print(Fore.GREEN + f"    ({self.port} - {self.name}) Anonymous login successful: {response}" + Style.RESET_ALL)
            ftp.quit()
            return True
        except Exception as e:
            if options.VERBOSE:
                print(f"    [FTP ERROR] {e}")
            return False
