import string
import random
import logging
import MySQLdb
import configparser
from random import randrange
from pydock import DockerManager

class Management:

    def __init__(self):
        logging.basicConfig(filename='generate.log', level=logging.INFO)
        logging.info("Management Generator initial.")
        self.cf = configparser.ConfigParser()
        self.cf.read('config.ini')
        logging.info("Load database...")
        self.db = MySQLdb.connect(self.cf['database']['url'], 
            self.cf['database']['user'], self.cf['database']['password'], self.cf['database']['dbname'])

    def random(self, size):
        ws_size = 10
        ws_entry = []
        wls = []
        for i in range(0, size, 1):
            cp_inx = randrange(1, ws_size)
            ''' insert script to web service '''
        print('Finish...')
    
    def random_key(self, length=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))