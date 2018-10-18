import socket
import time
from threading import Thread

class Pops:

	def __init__(self, s):
		pass

class Slave:

	def __init__(self):
		self.is_terminate = False
		self.serverThread = None
		self.clientThread = None
	
	def server(self):
		print("Start Server")
		# create a socket object
		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		# get local machine name
		host = socket.gethostname()                           
		port = 6681                                           
		# bind to the port
		serversocket.bind((host, port))                                  
		# queue up to 5 requests
		serversocket.listen(5)                                           
		while True:
			# establish a connection
			clientsocket,addr = serversocket.accept()
			rev_msg = clientsocket.recv(1024).decode("utf8")
			print("Got a connection from {}".format(rev_msg))
			msg = "{\"code\":200,\"message\":\"success\"}"+ "\r\n"
			clientsocket.send(msg.encode('ascii'))
			clientsocket.close()
			if rev_msg.startswith("STAR|"):
				self.run_start(rev_msg[4:])
			else:
				self.is_terminate = True
	
	def run_start(self, pops):
		self.is_terminate = False
		self.clientThread = Thread(target=self.run_ga, args=(pops,))
		self.clientThread.start()
	
	def run_ga(self, pops):
		print("POPS{}".format(pops))
		inx = 0
		while not self.is_terminate:
			if inx == 30:
				self.is_terminate = True
				print('Is Terminate')
				self.run_stop()
			print("Loop GA..")
			time.sleep(2)
			inx += 1
		print("Send Stop...")
	
	def run_stop(self):
		message = "STOP|{\"code\":200,\"message\":\"success\"}"
		self.clientThread = Thread(target=self.client, args=(message,))
		self.clientThread.start()
	
	def client(self, cmd):
		print("Start Client....")
		'''master = ('ip':'10.28.104.60', 'port':6680)
		# create a socket object
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		# get local machine name
		port = 6699
		# connection to hostname on the port.
		s.connect((ip, port))                               
		# Receive no more than 1024 bytes
		msg = s.recv(1024)                                     
		s.close()
		print (msg.decode('ascii'))'''
	
	'''def run(self):
		self.serverThread = Thread(target=self.server, args=())
		self.serverThread.start()'''

		
def main():
	slave = Slave()
	slave.server()

if __name__ == "__main__":
	main()
