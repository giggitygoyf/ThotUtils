# standard library
import concurrent.futures
import logging
import os
import shutil
from tqdm import tqdm
from urllib.parse import urlparse, urljoin

# external library
import cloudscraper


class ThotUtils:
	def __init__(self):
		self.headers = {
			'headers': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'
		}
		self.path = str(os.getcwd())
		self.retries = 5

		# create logging handlers
		s_handler = logging.StreamHandler()
		s_handler.setLevel(logging.INFO)
		s_handler.setFormatter(logging.Formatter('%(name)s - %(message)s'))

		# create loggers
		self.logger = logging.getLogger(__name__)
		self.logger.addHandler(s_handler)

	@staticmethod
	def validate_href(url, href):
		if href == "" or href is None:
			raise ValueError

		# join the URL if it's relative (not absolute link)
		href = urljoin(url, href)
		parsed_href = urlparse(href)

		# remove URL GET parameters, URL fragments, etc.
		href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

		return href

	def download_file(self, url):
		scraper = cloudscraper.create_scraper()
		local_filename = url.split('/')[-1]
		with scraper.get(url, headers=self.headers, stream=True) as r:
			with open(local_filename, 'wb') as f:
				shutil.copyfileobj(r.raw, f)

		return local_filename

	def download_files_serial(self, urls):
		for url in urls:
			self.download_file(urls)

	def download_files_parallel(self, urls):
		with concurrent.futures.ThreadPoolExecutor() as executor:
			_ = list(tqdm(executor.map(self.download_file, urls), total=len(urls)))
