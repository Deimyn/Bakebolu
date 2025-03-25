from ipaddress import IPv4Address
from colorama import Fore, Style
import sys

import options

class Service:
    def __init__(self, name: str, ip_addr: IPv4Address, port: int) -> None:
        self._name = name
        self._ip_addr = ip_addr
        self._port = port

    # Connect method to be implemented for each service
    def connect(self, username: str, password: str) -> bool:
        raise NotImplementedError("connect method should be implemented for each service individually")

    # Try login method to be implemented for each service
    # Should try default credentials, anonymous login, ...
    def try_login(self) -> bool:
        raise NotImplementedError("try_login method should be implemented for each service individually")

    # Getters
    @property
    def name(self):
        return self._name

    @property
    def port(self):
        return self._port

    @property
    def ip_addr(self):
        return self._ip_addr

    def __str__(self) -> str:
        return f"{self.ip_addr}:{self.port} -> {self.name}"

    def bruteforce(self) -> bool:
        attempt_count = 0

        username = options.USERNAME
        wordlist_path = options.PASSWORD_FILE_PATH

        if not wordlist_path or not username:
            raise Exception("An error occured, password wordlist path and username should not be empty")

        try:
            with open(wordlist_path, "r") as wordlist:
                passwords = wordlist.readlines()
                total_attempts = len(passwords)
                for password in passwords:
                    password = password.strip()
                    attempt_count += 1
                    sys.stdout.write(f"\r    [*] Bruteforce Attempts: {attempt_count}/{total_attempts}")
                    sys.stdout.flush()
                    if self.connect(username, password):
                        sys.stdout.write("\r" + " " * 50 + "\r")  # Overwrite with spaces
                        sys.stdout.flush()
                        print(Fore.GREEN + f"    ({self.port} - {self.name}) Brute-force success: {username}/{password}" + Style.RESET_ALL)
                        return True
            sys.stdout.write("\r" + " " * 50 + "\r")  # Overwrite with spaces
            sys.stdout.flush()
            print(f"    ({self.port} - {self.name}) Brute-force attempt finished, no valid credentials found.")
        except FileNotFoundError:
            print("    [ERROR] Wordlist file not found at", wordlist_path)
        
        return False

    # All the commented code below is related to brute-force Multi-threading
    # For the moment, it causes a lot of issues so we keep an non threaded approach

    # def worker(self, username: str, total_attempts: int):
    #     """ Worker thread function to test passwords from the queue """
    #     while not self.queue.empty() and not self.found:
    #         password = self.queue.get()
    #         attempt_count = total_attempts - self.queue.qsize()

    #         # Print progress safely
    #         with self.lock:
    #             sys.stdout.write(f"\r\t[*] Bruteforce Attempts: {attempt_count}/{total_attempts}")
    #             sys.stdout.flush()

    #         if self.connect(username, password):
    #             sys.stdout.write("\r" + " " * 50 + "\r")
    #             sys.stdout.flush()
    #             print(Fore.GREEN + f"\t[+] Brute-force success: {username}/{password}" + Style.RESET_ALL)
    #             self.found = True
    #             self.queue.queue.clear()
    #             break  

    #         self.queue.task_done()

    # def bruteforce(self):
    #     """ Multi-threaded brute-force attack """

    #     username = options.USERNAME
    #     wordlist_path = options.PASSWORD_FILE_PATH

    #     if not wordlist_path:
    #         raise Exception("An error occured, password wordlist path should not be empty")

    #     try:
    #         with open(wordlist_path, "r") as wordlist:
    #             passwords = [line.strip() for line in wordlist if line.strip()]
    #             total_attempts = len(passwords)

    #             if total_attempts == 0:
    #                 print(Fore.RED + "\t[ERROR] Wordlist is empty!" + Style.RESET_ALL)
    #                 return False

    #             for password in passwords:
    #                 self.queue.put(password)

    #     except FileNotFoundError:
    #         print(Fore.RED + f"\t[ERROR] Wordlist file not found at {wordlist_path}" + Style.RESET_ALL)
    #         return False

    #     # Create and start worker threads
    #     threads = []
    #     for _ in range(min(1, self.queue.qsize())):
    #         thread = threading.Thread(target=self.worker, args=(username, total_attempts))
    #         thread.start()
    #         threads.append(thread)

    #     # Wait for all threads to finish
    #     for thread in threads:
    #         thread.join()

    #     sys.stdout.write("\r" + " " * 50 + "\r")
    #     sys.stdout.flush()

    #     if not self.found:
    #         print(f"\t({self.port}) Brute-force attempt finished, no valid credentials found.")

    #     return self.found

