#!usr/local/bin/env python3.7
import asyncio
import json
import aiohttp
from database import Database
from html_parser import HtmlParser

class PasswordPageParser(object):
	"""Parses page https://www.passwordrandom.com/most-popular-passwords/page/N
	N is the number of page which should be parsed
	"""

	RETRIES = 3

	def __init__(self, n):
		self.URL_format = 'https://www.passwordrandom.com/most-popular-passwords/page/{}'
		self.page_number = n

	def arrange_table_data(self, table_data):
		result = []
		for row in table_data:
			if row:
				arranged_row = row[:-1]
				result.append(arranged_row)
		return result

	async def get_page(self):
		url = self.URL_format.format(self.page_number)
		print('Starting {}'.format(url))
		
		async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
			async with session.get(url) as resp:

				html = await resp.text()
				print('Received {}'.format(url))
		return html, resp.status

	async def parse(self):
		retries = PasswordPageParser.RETRIES
		status = None
		while retries > 0 and status != 200:
			html, status = await self.get_page()
			retries -= 1

		if status == 200:
			table_parser = HtmlParser(html)
			table_data = table_parser.parse('get_table_data')

		if table_data:
			arranged_table_data = self.arrange_table_data(table_data)
			return arranged_table_data


if __name__ == '__main__':
	password_page_parsers = [PasswordPageParser(i) for i in range(1, 101 // 1)]

	ioloop = asyncio.get_event_loop()
	tasks = [ioloop.create_task(p.parse()) for p in password_page_parsers]
	wait_tasks = asyncio.wait(tasks)
	ioloop.run_until_complete(wait_tasks)

	tasks_results = []
	for task in tasks:
		tasks_results += task.result()

	print('Saving data to db.')
	db_saver = Database()
	db_saver.save_rows(tasks_results, 'insert_into_passwords_table')
	print('Saved {} passwords'.format(len(tasks_results)))

	ioloop.close()
