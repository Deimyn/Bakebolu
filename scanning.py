from os import error
import socket
import threading

from smbclient import smbclient
import options
import ipaddress
from concurrent.futures import ThreadPoolExecutor
import sys
from smbprotocol.connection import Connection
from smbprotocol.session import Session
from smbprotocol.tree import TreeConnect

from services.ftp import FtpService
from services.http import HttpService
from services.mysql import MySqlService
from services.smb import SmbService
from services.ssh import SshService
from services.telnet import TelnetService


def scan_network(ip_netw: ipaddress.IPv4Network, ports: list[int]) -> list[dict]:
    out = []
    for ip_addr in ip_netw.hosts():
        if options.VERBOSE:
            print(f"[+] {ip_addr}")
        else:
            sys.stdout.write(f"\r[*] Scanning address: {ip_addr}")
            sys.stdout.flush()
        out.append({
            "ip": ip_addr,
            # Makes the correct structure
            "open_ports": [{"port": port, "service": ""} for port in scan_ports(ip_addr, ports)]
        })

    sys.stdout.write("\r" + " " * 50 + "\r")
    sys.stdout.flush()

    return out

def scan_ports(ip_addr: ipaddress.IPv4Address, ports: list[int]) -> list[int]:
    """Returns a list of open ports."""
    results = []
    # Using a lock to safely append to the list while on multiple threads
    lock = threading.Lock()

    def scan_port(port): 
        """Scan a single port and detect its service."""
        if is_port_open(ip_addr, port):
            with lock:
                results.append(port)

    # Using ThreadPoolExecutor to limit the number of threads allowed 
    with ThreadPoolExecutor(max_workers=options.MAX_THREADS) as executor:
        for port in ports:
            executor.submit(scan_port, port)

    return results

def is_port_open(
        ip_addr: ipaddress.IPv4Address,
        port: int,
        ) -> bool:
    """Returns True if a port is open"""

    socket_type = socket.SOCK_STREAM
    sock = socket.socket(socket.AF_INET, socket_type)
    sock.settimeout(0.5)  # Set a timeout for faster response
    result = sock.connect_ex((str(ip_addr), port))
    sock.close()

    if options.VERBOSE:
        print(f"[+] {port} : {'opened' if result == 0 else 'closed'}")

    return result == 0

def detect_service(ip_addr: ipaddress.IPv4Address, port: int):
    """Attempt to detect the service running on any given port."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            sock.connect((str(ip_addr), port))

            # Attempt to read initial banner
            try:
                banner = sock.recv(1024)
                if banner:
                    banner_decoded = banner.decode(errors="ignore").strip()
                    if "SSH" in banner_decoded.upper():
                        return SshService(ip_addr, port)
                    if "FTP" in banner_decoded.upper():
                        return FtpService(ip_addr, port)
                    if "TELNET" in banner_decoded.upper():
                        return TelnetService(ip_addr, port)
                    if "MySQL" in banner_decoded.upper():
                        return MySqlService(ip_addr, port)
                    if "mysql_native_password" in banner_decoded.lower() or "caching_sha2_password" in banner_decoded.lower() or "sha256_password" in banner_decoded.lower():
                        return MySqlService(ip_addr, port) 
                    if "HTTP" in banner_decoded.upper() or "<HTML>" in banner_decoded.upper():
                        return HttpService(ip_addr, port) 
                    # Telnet IAC sequences
                    if banner.startswith(b'\xff\xfd') or banner.startswith(b'\xff\xfb'):
                        return TelnetService(ip_addr, port)
                    return f"Banner Detected: {banner_decoded}"
            except socket.timeout:
                pass  

            # Fallback: Send an HTTP-like request and analyze response
            sock.sendall(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
            response = sock.recv(1024).decode(errors="ignore")
            if "HTTP" in response:
                return HttpService(ip_addr, port)
            if "Not Implemented" in response:
                return HttpService(ip_addr, port)

            return "Unknown Service"
    except socket.timeout:
        return "No Response (Timeout)"
    except ConnectionRefusedError:
        return "Connection Refused"
    except Exception as e:
        return f"Error: {str(e)}"
