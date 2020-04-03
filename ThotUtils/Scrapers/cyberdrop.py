# standard library
import os
import re

# external libraries
import cloudscraper
from bs4 import BeautifulSoup

# internal libraries
from ThotUtils.thot_utils import ThotUtils


class CyberDropDownloader(ThotUtils):
	def __init__(self):
		super().__init__()

	def identify_set(self, soup):
		# format the setname
		setname = str(soup.find('title').string)
		setname = setname[7:setname.rfind(" – ", 1)]
		#self.logger.info(f'Set name: {setname}')
		print(f'Set name: {setname}')

		# set the path to a directory based on the setname
		setpath = self.path + f'/{setname}'
		if not os.path.exists(setpath):
			os.mkdir(setpath)
		os.chdir(setpath)
		self.logger.info(f'Path to set: {setpath}')

	def find_image_links(self, url, soup):
		urls = set()

		for a in soup.findAll(href=re.compile("\.(jpg|png)$")):
			href = a.attrs.get("href")

			try:
				href = super().validate_href(url, href)
			except ValueError:
				continue

			# remove favicons
			if not re.search(r'favicon\.', href.split('/')[-1]):
				urls.add(href)

		self.logger.info(f'Images found: {len(urls)}')
		return urls

	def parse_page(self, url):
		#self.logger.info(f'Parsing started for: {url}')
		print(f'Parsing started for: {url}')

		# create the BeautifulSoup object
		scraper = cloudscraper.create_scraper()
		soup = BeautifulSoup(scraper.get(url=url, headers=self.headers).content, 'html5lib')

		# identify the set and change to directory for it
		self.identify_set(soup)

		# find all the images linked to on the page
		urls = self.find_image_links(url, soup)

		if urls is not None:
			# download the images
			super().download_files_parallel(urls)
		else:
			print("no images found")

		#self.logger.info(f'Parsing complete for: {url}')
		print(f'Parsing complete for: {url}')


class CyberDropDownloaderBuilder:
	def __init__(self):
		self._instance = None

	def __call__(self, **_ignored):
		if not self._instance:
			self._instance = CyberDropDownloader()
		return self._instance
