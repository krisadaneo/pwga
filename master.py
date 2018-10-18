import socket
from threading import Thread

class Master:

	def __init__(self):
		self.serverThread = None
		self.clientThread = None
	
	def server(self):
		print("Start Server")
		# create a socket object
		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		# get local machine name
		host = socket.gethostname()                           
		port = 6690                                           
		# bind to the port
		serversocket.bind((host, port))                                  
		# queue up to 5 requests
		serversocket.listen(5)                                           
		while True:
			# establish a connection
			clientsocket,addr = serversocket.accept()
			rev_msg = clientsocket.recv(1024).decode("utf8")
			print("Got a connection from %s" % str(addr))
			self.clientThread = Thread(target=self.run_client, args=())
			self.clientThread.start()
			'''msg = 'Thank you for connecting'+ "\r\n"
			s.send("STOP|{\"code\":200,\"message\":\"success\"}".encode("utf8"))
			clientsocket.send(msg.encode('ascii'))'''
			clientsocket.close()
	
	def run_client(self, cmd):
		message = None
		'''if cmd == "start":
			population = repository.gen_population()
			message = self.to_message(population)
		else:
			message = "stop"'''
		self.clientThread = Thread(target=self.client, args=(message,))
		self.clientThread.start()
	
	def client(self):
		print("Start Client")
		'''slaves = repository.find_slave()'''
		'''for ip in slaves:'''
		# create a socket object
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		# get local machine name
		port = 6681
		# connection to hostname on the port.
		s.connect(("10.28.104.60", port))                               
		# Receive no more than 1024 bytes
		s.send("STOP|{\"code\":200,\"message\":\"success\"}".encode("utf8"))
		msg = s.recv(1024)
		s.close()
		print (msg.decode('ascii'))
	
	'''def run(self):
		self.serverThread = Thread(target=self.server, args=())
		self.serverThread.start()'''

		
def main():
	master = Master()
	master.client()

if __name__ == "__main__":
	main()
