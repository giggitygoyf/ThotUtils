# standard library
import concurrent.futures
import os
import re
from tqdm import tqdm
from urllib.parse import urlparse, urljoin

# external libraries
import requests
from bs4 import BeautifulSoup

# internal libraries
from ThotUtils.thot_utils import ThotUtils


class EromeDownloader(ThotUtils):
	def __init__(self):
		super().__init__()

	def identify_set(self, soup):
		setname = str(soup.find("h1").string)
		print(f"Set name: {setname}")

		# set the path to a directory based on the setname
		setpath = self.path + f'/{setname}'
		if not os.path.exists(setpath):
			os.mkdir(setpath)
		os.chdir(setpath)
		self.logger.info(f'Path to set: {setpath}')

	def find_image_links(self, url, soup):
		return None

	def find_video_links(self, url, soup):
		urls = set()

		for v in soup.findAll("source"):
			href = v.attrs.get("src")

			try:
				href = super().validate_href(url, href)
				urls.add(href)
			except ValueError:
				continue

		self.logger.info(f'Videos found: {len(urls)}')
		return urls

	def download_video(self, href):
		filename = href.split('/')[-1]
		self.logger.debug(f'Downloading {href} as {filename}')

	def parse_page(self, url):
		# self.logger.info(f'Parsing started for: {url}')
		print(f'Parsing started for: {url}')

		# create the BeautifulSoup object
		soup = BeautifulSoup(requests.get(url=url, headers=self.headers).content, 'html.parser')

		# identify the set and change to directory for it
		self.identify_set(soup)

		# find all the images linked to on the page
		urls = self.find_image_links(url, soup)

		if urls is not None:
			# download the images
			self.download_files_parallel(urls)
		else:
			print("no images found")

		# find all the videos linked to on the page
		urls = self.find_video_links(url, soup)

		if urls is not None:
			# download the videos
			super().download_files_parallel(urls)
		else:
			print("no videos found")

		# self.logger.info(f'Parsing complete for: {url}')
		print(f'Parsing complete for: {url}')


class EromeDownloaderBuilder:
	def __init__(self):
		self._instance = None

	def __call__(self, **_ignored):
		if not self._instance:
			self._instance = EromeDownloader()
		return self._instance


if __name__ == '__main__':
	erome = EromeDownloader()

	if os.path.isfile("URLS.txt") and os.stat("URLS.txt").st_size != 0:
		url_file = open("URLS.txt", "r")
		for line in url_file:
			# skip blank lines
			if line in ['\n', '\r\n']:
				continue

			erome.parse_page(url=line.rstrip())