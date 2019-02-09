from bs4 import BeautifulSoup

class HtmlParser(object):
	"""Finds elements on html page and parses them to python objects
	"""

	def __init__(self, html):
		self.html = html

	def get_table_data(self):
		rows = []
		soup = BeautifulSoup(self.html)
		for row in soup.select('table tr'):
			row_data = []
			for td in row.select('td'):
				row_data.append(td.text.replace("'", "''"))
			rows.append(row_data)
		return rows

	def parse(self, function_name):
		function = HtmlParser.__dict__.get(function_name, None)
		return function(self)
