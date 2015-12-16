import MySQLdb

HOST = 'bgnalm.mysql.pythonanywhere-services.com'
USER = 'bgnalm'
PASSWORD = 'michaelml'
DB = 'bgnalm$akinator_v2'


class DB_Conn(object):

	def _init_connection(self):
		self._db = MySQLdb.connect(HOST, USER, PASSWORD, DB)
		self._cursor = self._db.cursor()

	def __init__(self):
		self._init_connection()	

	def query(self, query):
		try:
			self._cursor.execute(query)
		except:
			self._init_connection()
			self._cursor.execute(query)

	def select(self, query):
		self.query(query)
		return self._cursor.fetchall()

	def get_rows(self):
		return self._cursor.rowcount

	def last_insert_id(self):
		self._cursor.lastrowid

	def close(self):
		self._db.close()