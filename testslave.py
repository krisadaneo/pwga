import time
import sys
import socket
import logging
import configparser
from random import randrange
from threading import Thread
from Repository import Repository

def main(ip, port, data):
    print("call run_slave ->{},{},{}".format(ip, port, data))
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            s.sendall(data.encode('utf8','strict'))
            rs = s.recv(4096)
            s.close()
            print("Slave Response :{}".format(rs))
    except Exception as e:
        print("Run Slave Error.{}".format(e))

if __name__ == "__main__":
    ip = "172.17.0.1"
    port = 9011 
    data = 'STOP|FOUND\r\n'
    main(ip, port, data)


