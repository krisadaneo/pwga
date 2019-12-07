import MySQLdb
'''
Repository of Parallel Genetic Algorithms
'''
class Processor:

	def __init__(self, ip, port):
		self.ip = ip
		self.port = port

class Repository:

	def __init__(self, host, user, password, dbname):
		self.db = None
		self.host = host
		self.user = user
		self.password = password
		self.dbname = dbname
	
	def connect(self):
		try:
			self.db = MySQLdb.connect(self.host, self.user, self.password, self.dbname)
			return True
		except:
			return False

	def find_master(self):
		try:
			sql = "SELECT IP, PORT FROM T_PROCESSOR WHERE IS_MASTER = 'Y' AND IS_ACTIVE = 'Y'"
			cursor = self.db.cursor()
			cursor.execute(sql)
			results = cursor.fetchall()
			for row in results:
				return Processor(row[0], row[1])
		except:
			return None 

	def find_slave(self):
		ls = []
		try:
			sql = "SELECT IP, PORT FROM T_PROCESSOR WHERE IS_MASTER = 'N' AND IS_ACTIVE = 'Y'"
			cursor = self.db.cursor()
			cursor.execute(sql)
			results = cursor.fetchall()
			for row in results:
				ls.append(Processor(row[0], row[1]))
			return ls
		except:
			return ls
	
	def slave_size(self):
		try:
			sql = "SELECT COUNT(*) FROM T_PROCESSOR WHERE IS_MASTER = 'N' AND IS_ACTIVE = 'Y'"
			cursor = self.db.cursor()
			cursor.execute(sql)
			results = cursor.fetchall()
			for row in results:
				ls.append(Processor(row[0], row[1]))
			return ls
		except:
			return ls

	def find_slave_entry(self):
		try:
			sql = "SELECT IP, PORT FROM T_PROCESSOR WHERE IS_MASTER = 'N' AND IS_ACTIVE = 'Y' AND IS_EMPTY = 'Y'"
			cursor = self.db.cursor()
			cursor.execute(sql)
			results = cursor.fetchall()
			for row in results:
				return Processor(row[0], row[1])
		except:
			return None
	
	def reserve_slave(self, ip, port):
		try:
			sql = "UPDATE T_PROCESSOR SET IS_EMPTY = 'N' WHERE IS_MASTER = 'N' AND IP = '{}' AND PORT = {}".format(ip, port)
			cursor = self.db.cursor()
			cursor.execute(sql)
			return True
		except:
			return False
	
	def reserve_master(self, ip, port):
		try:
			sql = "UPDATE T_PROCESSOR SET IS_EMPTY = 'N' WHERE IS_MASTER = 'Y'"
			cursor = self.db.cursor()
			cursor.execute(sql)
			return True
		except:
			return False
	
	def release_slave(self, ip, port):
		try:
			sql = "UPDATE T_PROCESSOR SET IS_EMPTY = 'Y' WHERE IS_MASTER = 'N' AND IP = '{}' AND PORT = {}".format(ip, port)
			cursor = self.db.cursor()
			cursor.execute(sql)
			return True
		except:
			return False
	
	def init_master(self, ip, port):
		try:
			sql = "UPDATE T_PROCESSOR SET IP = '{}', PORT = {}, IS_EMPTY = 'Y' WHERE IS_MASTER = 'Y' ".format(ip, port)
			cursor = self.db.cursor()
			cursor.execute(sql)
			return True
		except:
			return False
	
	def disconnect(self):
		self.db.close()
	
	def commit(self):
		self.db.commit()
	

	
def main():
	res = Repository("mysqldb-server", "dopa_user", "P@ss4321", "pwsga")
	res.connect()
	s = res.find_master()
	print("{},{}".format(s.ip, s.port))
	res.disconnect()
	
if __name__ == "__main__":
		main()

