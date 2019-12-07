import sys
import socket
import logging
import configparser
from threading import Thread
from Repository import Repository

class Master:

	def __init__(self):
		logging.basicConfig(filename='master.log', level=logging.INFO)
		logging.info("Master initialize...")
		self.cf = configparser.ConfigParser()
		self.cf.read('config.ini')
		self.is_stop = False
		logging.info("Load database...")
		self.repo = Repository(self.cf['database']['url'], 
			self.cf['database']['user'], self.cf['database']['password'], self.cf['database']['dbname'])
		self.repo.connect()
		ms = self.repo.find_master()
		self.ip = ms.ip
		self.port = ms.port
	
	def service(self):
		logging.info("Master running...")
		try:
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
				s.bind((self.ip, self.port))                                  
				s.listen(8)
				logging.info("wait connection...")
				conn, addr = s.accept()
				while True:                                           
					with conn:
						while True:
							data = conn.recv(1024)
							if not data:
								break
							if data.startswith("TERM|"):
								conn.close()
								self.is_stop = True
								self.repo.disconnect()
								logging.info("Master terminate...")
								return True
							else:
								logging.debug("Got a connection from %s" % str(addr))
								self.run_cmd(data)
		except Exception as ex:
			logging.error("Open socket master error.", ex)
		return False

	def run_cmd(self, data):
		try:
			cmd = data[0:4]
			logging.debug("Pass run_cmd:{}".format(cmd))
			sl = repo.find_slave()
			for sv in sl:
				logging.debug("exec -> run_slave:{},{}".format(sv.ip, sv.port))
				runable = Thread(target=self.run_slave, args=(sv.ip, sv.port, str(data),))
				runable.start()
			logging.info("called any slave..")
		except Exception as ex:
			logging.error("master run_cmd error:", ex)

	def run_slave(self, ip, port, data):
		logging.debug("call run_slave ->{},{},{}".format(ip, port, data))
		try:
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
				s.connect((ip, port))
				s.sendall(data)
				rs = s.recv(4096)
				s.close()
				logging.debug("Slave Response :{}".format(rs))
		except:
			logging.error("Run Slave Error.")

def main():
	master = Master()
	master.service()

if __name__ == "__main__":
	main()
