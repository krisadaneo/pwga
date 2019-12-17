import string
import random
import logging
import MySQLdb
import configparser
from random import randrange
from pydock import DockerManager

class Params(object):

    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.type = type
    
    def __str__(self):
        return "id:{}, name:{}, type:{}".format(self.id, self.name, str(self.type))

class WsEntry(object):

    def __init__(self, id, url):
        self.id = id
        self.url = url
        self.params = []
        self.reps = []
    
    def __str__(self):
        str = "id:{}, url:{}\n".format(self.id, self.url)
        str += "\tparams:\n"
        for prs in self.params:
            str += "\t\t[{}]\n".format(prs)
        str += "\treturn:\n"
        for rps in self.reps:
            str += "\t\t[{}]\n".format(rps)
        return str 

class Management:

    def __init__(self):
        logging.basicConfig(filename='generate.log', level=logging.INFO)
        logging.info("Management Generator initial.")
        self.cf = configparser.ConfigParser()
        self.cf.read('config.ini')
        logging.info("Load database...")
        self.db = MySQLdb.connect(self.cf['database']['url'], 
            self.cf['database']['user'], self.cf['database']['password'], self.cf['database']['dbname'])
        self.ws = []

    def init_data(self):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM T_WS_ENTRY")
        cursor.execute("DELETE FROM T_WS_PARAM")
        self.db.commit()

    def gen_ws(self, size):
        size = int(self.cf['management']['ws_no'])
        ws_id_size = self.cf['management']['ws_id_size']
        cursor = self.db.cursor()
        for i in range(1, size+1, 1):
            url = self.cf['webservice']['ws_url']
            sql = "INSERT INTO T_WS_ENTRY (WS_ID, URL) VALUES('{}','{}')".format(ws_id_size.format(i),url)
            cursor.execute(sql)
        self.db.commit()
        logging.info('Web Service entry finish...')

    def load_mem(self):
        tws = []
        sql = "SELECT WS_ID, URL FROM T_WS_ENTRY ORDER BY WS_ID ASC"
        cursor = self.db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        i, tmp = 0, []
        for rs in results:
            tmp.append(WsEntry(rs[0], rs[1]))
            tws.append(i)
            i+=1
        y = [tws.pop(random.randrange(len(tws))) for _ in range(len(tws))]
        for inx in y:
            self.ws.append(tmp[inx])
        i, pms, rps = 0, [], []
        for w in self.ws:
            if not rps:
                r = random.randrange(1, 8)
                for _ in range(0, r, 1):
                    t = random.randrange(1, 3)
                    pms.append(Params(self.random_key(), self.random_param_name(), t))
                r = random.randrange(1, 8)
                print("random 0-2:{}".format(r))    
                for _ in range(0, r, 1):
                    t = random.randrange(1, 3)
                    rps.append(Params(self.random_key(), self.random_param_name(), t))
            else:
                for rp in rps:
                    t = random.randrange(1, 3)
                    pms.append(Params(self.random_key(), rp.name, rp.type))
                rps = []
                r = random.randrange(1, 8)
                for _ in range(0, r, 1):
                    t = random.randrange(1, 3)
                    rps.append(Params(self.random_key(), self.random_param_name(), t))
            print("p size:{}".format(len(pms)))        
            w.params = pms
            w.reps = rps
            pms = []
        for w in self.ws:
            print(w)

    def gen_script(self, wb):
        pass
    
    def close_db(self):
        self.db.close()
    
    def random_key(self):
        key_size = int(self.cf['management']['ws_key_size'])
        letters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(letters) for _ in range(key_size))
    
    def random_param_name(self):
        prefix_size = 4
        subfix_size = 8 
        nums = string.digits
        prefix = ''.join(random.choice(nums) for i in range(prefix_size)) 
        letters = string.ascii_uppercase + string.digits
        subfix = ''.join(random.choice(letters) for i in range(subfix_size))
        return prefix + '_' + subfix

def main():
    m = Management()
    m.init_data()
    m.gen_ws(20)
    m.load_mem()
    m.close_db()

if __name__ == "__main__":
    main()
