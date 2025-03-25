# RWU-Python-Project

The aim of this project is to make a machine / network port scanner. And then try default credentials with the open ports.

## Files

- `main.py` : Entrypoint of the program
- `cli.py` : Handle the user input on the cli
- `options.py` : Holds global variables to be accessible from all files
- `scanning.py` : Contains all the scanning functions
- `services/service.py` : Base Class for all services to inherit
- `services/*.py` : All the services with the approptiate functions

- `test_lab` : Docker network containing 3 machines with open ports to test the program on
- `test_lab/ftp_server` : custom build for anonymous ftp login

## Test Lab

Start the lab using `docker compose up -d --build`. And stop `docker compose down --remove-orphan`

## Required Libraries

 - paramiko
 - colorama
 - mysql-connector
 - smbprotocol
