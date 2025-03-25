import argparse
import ipaddress
import re
import options


def initialize():
    parser = argparse.ArgumentParser(description="Bakebolu")

    # Target ip address or network to scan
    parser.add_argument("target_ip",
                        type=ip_addr_or_network_validator,
                        help="Ip address or network to scan")

    # Port range to scan 0-9999 default
    parser.add_argument("-p", "--port-range",
                        type=port_range_validator,
                        default=(0, 9999),
                        help="Port range to scan, e.g. 0-9999")

    # Verbose flag
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="Enable verbose output")

    # Maximum thread amount
    parser.add_argument("-T", "--max-threads",
                        type=max_threads_validator,
                        default=100,
                        help="Maximum number of threads allowed")

    # username
    parser.add_argument("-u", "--user",
                        default=None,
                        help="Username to test on bruteforcing")

    # password wordlist
    parser.add_argument("-w", "--wordlist",
                        default=None,
                        help="Password wordlist to use on bruteforcing")

    args = parser.parse_args()

    if (args.user and not args.wordlist) or (args.wordlist and not args.user):
        raise argparse.ArgumentTypeError(
                "You must specify a wordlist if you specify a username and inversely")
    else:
        options.USERNAME = args.user
        options.PASSWORD_FILE_PATH = args.wordlist

    options.VERBOSE = args.verbose
    options.START_PORT, options.END_PORT = args.port_range
    options.MAX_THREADS = args.max_threads


def max_threads_validator(threads):
    try:
        threads = int(threads)
    except:
        raise argparse.ArgumentTypeError("Maximum number of threads should be an integer")
    if threads <= 0:
        raise argparse.ArgumentTypeError("Maximum number of threads should be positive")
    return threads

def ip_addr_or_network_validator(
        address,
        pat=re.compile(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}(\/(\d|[12]\d|3[0-2]))?$")):
    """Regex to validate the given ip address"""
    # Regex taken from here https://stackoverflow.com/questions/5284147/validating-ipv4-addresses-with-regexp?page=1&tab=scoredesc#tab-top
    # And added optional / at the end (from 0 going to 32, based on CIDR)
    if not pat.match(address):
        raise argparse.ArgumentTypeError("invalid ip address or network")
    if "/" not in address:
        address = f"{address}/32"

    try:
        # Strict = False to allow any address from the network as the base address
        options.TARGET_NETWORK = ipaddress.IPv4Network(address, strict=False)
    except:
        raise argparse.ArgumentTypeError("Invalid address or network given")


def port_range_validator(port_range, pat=re.compile(r"^(\d+)-(\d+)$")):
    """Regex to validate the given port range"""
    match = pat.match(port_range)

    if not match:
        raise argparse.ArgumentTypeError("invalid port range")

    # Extract the port from the regex
    start_port, end_port = int(match.group(1)), int(match.group(2))

    # Check that given range is valid
    if not (0 <= start_port <= 65535 and
            0 <= end_port <= 65535 and
            start_port <= end_port):
        raise argparse.ArgumentTypeError(
                "Ports must be between 0 and 65535, and start must be <= end")

    return (start_port, end_port)
