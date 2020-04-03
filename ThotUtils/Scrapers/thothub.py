# standard library
import getpass
import json
import os

# external libraries
import cloudscraper
from bs4 import BeautifulSoup

# internal libraries
from ThotUtils.thot_utils import ThotUtils


class ThotHubDownloader(ThotUtils):
	def __init__(self):
		super().__init__()

	def identify_set(self, soup):
		setname = str(soup.find("h1").string)
		if setname is not None:
			print(f"Set name: {setname}")

			# set the path to a directory based on the setname
			setpath = self.path + f'/{setname}'
			if not os.path.exists(setpath):
				os.mkdir(setpath)
			os.chdir(setpath)
			self.logger.info(f'Path to set: {setpath}')
		else:
			raise ValueError

	def find_image_links(self, url, soup):
		urls = set()

		gallery = soup.find("figure", attrs={"data-g1-gallery": True})

		if gallery is None:
			return None
		else:
			gallery_json = json.loads(gallery['data-g1-gallery'])
			for i in gallery_json:
				href = i['full']
				try:
					href = super().validate_href(url, href)
					urls.add(href)
				except ValueError:
					continue

		self.logger.info(f'Videos found: {len(urls)}')
		return urls

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

	def parse_page(self, url):
		# self.logger.info(f'Parsing started for: {url}')
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


class ThotHubDownloaderBuilder:
	def __init__(self):
		self._instance = None

	def __call__(self, **_ignored):
		if not self._instance:
			self._instance = ThotHubDownloader()
		return self._instance


class ThotHubForumDownloader(ThotUtils):
	def __init__(self):
		super().__init__()
		self.login_url = 'https://forum.thothub.tv/index.php?login/login'
		self.credentials = []

	def login(self):
		self.credentials['login'] = getpass.getuser('ThotHub Forum Username: ')
		self.credentials['password'] = getpass.getpass('ThotHub Forum Password: ')

	def identify_set(self, soup):
		setname = str(soup.find("h1").string)
		if setname is not None:
			print(f"Set name: {setname}")

			# set the path to a directory based on the setname
			setpath = self.path + f'/{setname}'
			if not os.path.exists(setpath):
				os.mkdir(setpath)
			os.chdir(setpath)
			self.logger.info(f'Path to set: {setpath}')
		else:
			raise ValueError

	def parse_page(self, url):\
		# self.logger.info(f'Parsing started for: {url}')
		print(f'Parsing started for: {url}')

		# login and start the session
		scraper = cloudscraper.CloudScraper()
		self.login()
		scraper.post(url=self.login_url, data=self.credentials)
		
		# create the BeautifulSoup object
		soup = BeautifulSoup(scraper.get(url=url, headers=self.headers).content, 'html5lib')

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


class ThotHubForumDownloaderBuilder:
	def __init__(self):
		self._instance = None

	def __call__(self, **_ignored):
		if not self._instance:
			self._instance = ThotHubForumDownloader()
		return self._instance