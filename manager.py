import sys
import configparser
from Repository import Repository

class Manager:

    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read('config.ini')

    def execute(self):
        print("host:{}, user:{}, password:{}".format(self.cf['database']['url'],
            self.cf['database']['user'], self.cf['database']['password']))

def main():
    m = Manager()
    m.execute()

if __name__ == "__main__":
    main()
