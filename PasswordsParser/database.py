import psycopg2

class Database(object):

	"""Saves parsed data to db
	"""

	def __init__(self):
		# should be saved outside the file.
		self.conn_string = "host='db' port=5432 dbname='passwords' "\
					  "user='postgres' password='123'"

		print('Connecting to database \r\n {}'.format(self.conn_string))

		#Creating connection with db
		self.conn = psycopg2.connect(self.conn_string)
		self.conn.autocommit = False
		print("Autocommit enabled={}".format(self.conn.autocommit))

		print('Creating database connection cursor')
		
		self.cursor = self.conn.cursor()

	def insert_into_passwords_table(self, values):
		self.cursor.execute("insert into public.passwords " \
			"(rank, password, md5, length, letters, symbols, numbers, parsed_at) " \
			"VALUES ({},'{}','{}',{},{},{},{}, now())"\
			.format(*values))

	def save_rows(self, rows, function_name):
		function = Database.__dict__.get(function_name, None)
		if function:
			for row in rows:
				if row:
					function(self, row)
			self.conn.commit()
		else:
			print('No function {}.'.format(function_name))
