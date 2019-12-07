import time
import sys
import socket
import logging
import configparser
from random import randrange
from threading import Thread
from Repository import Repository

class Pops:

	def __init__(self, s):
		pass

class Slave:

	def __init__(self):
		self.cf = configparser.ConfigParser()
		self.cf.read('config.ini')
		self.repo = Repository(self.cf['database']['url'], 
			self.cf['database']['user'], self.cf['database']['password'], self.cf['database']['dbname'])
		self.repo.connect()
		self.is_terminate = False
		self.is_found = False
		self.runnable = None
		self.is_run_ga = False
		self.ip = None
		self.port = None
		'''self.slave = Thread(target=self.service, args=())
		self.slave.start()'''
			
	def service(self):
		sv = self.repo.find_slave_entry()
		if sv == None:
			return
		self.ip = sv.ip
		self.port = sv.port
		logging.basicConfig(filename="slave-{}.log".format(self.port), level=logging.INFO)
		print("Slave initialize...")		
		print("Start slave ip:{}, port:{}".format(self.ip, self.port))
		# create a ssocket object
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			print("pass1") 
			s.bind((sv.ip, sv.port))
			print("pass2")
			s.listen(5)
			print("pass3")
			while True:                                           
				conn, addr = s.accept()
				print("Wait receive...")
				with conn:
					print("Connected by", addr)
					while True:
						print("Receive...")
						rev = conn.recv(4096)
						'''if self.is_run_ga:
							print("This slave is busy!")
							continue'''
						if not rev:
							break
						rcmd = rev.decode('utf8','strict')
						print("Got a connection from {}".format(rcmd))
						msg = "{\"code\":200,\"message\":\"success\"}"+ "\r\n"
						conn.send(msg.encode('ascii'))
						'''conn.close()'''
						if rcmd.startswith("STAR|"):
							self.run_start(rcmd[4:])
						elif rcmd.startswith("STOP|"):
							self.is_terminate = True
						else:
							self.is_terminate = True
							self.repo.disconnect()
							conn.close()
	
	def run_start(self, pops):
		self.is_terminate = False
		self.runnable = Thread(target=self.run_ga, args=(pops,))
		self.runnable.start()
	
	def run_ga(self, pops):
		self.is_run_ga = True
		len = randrange(10, 20)
		print("POPS{}".format(pops))
		inx = 0
		while not self.is_terminate:
			if inx == len:
				self.is_found = True
				print('Is Found')
				break
			print("Loop GA..")
			time.sleep(2)
			inx += 1
		if self.is_terminate:
			msg = "STOP|{\"code\":200,\"message\":\"is terminate.\"}"
		else:
			msg = "STOP|{\"code\":200,\"message\":\"success.\"}"
		ms = self.repo.find_master()
		self.send_master(ms.ip, ms.port, msg)
		self.is_run_ga = False
		self.is_terminate = False	
		print("Send Stop...")

	def send_master(self, ip, port, msg):
		logging.debug("call send master ->{},{},{}".format(ip, port, msg))
		try:
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
				s.connect((ip, port))
				s.sendall(b"{}".format(msg))
				rs = s.recv(1024)
				s.close()
				logging.debug("Master Response :{}".format(rs))
		except:
			logging.error("Send Master Error.")
		
def main():
	s = Slave()
	s.service()

if __name__ == "__main__":
	main()
