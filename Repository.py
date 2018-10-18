import pymysql

class Repository:

	def __init__(self, host, user, password, dbname):
		self.db = None
		self.host = host
		self.user = user
		self.password = password
		self.dbname = dbname
	
	def connect(self):
		self.db = MySQL.connect(self.host, self.user, self.password, self.dbname)
	
	def find_slave(self):
		ls = []
		sql = "SELECT IP FROM T_PROCESSOR WHERE IS_MASTER = 'N' AND IS_ACTIVE = 'Y'"
		cursor = self.db.cursor()
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:
			ls.append(row[0])
		return ls
	
	def disconnect(self):
		self.db.close()
	
	def commit(self):
		self.db.commit()
	
	
