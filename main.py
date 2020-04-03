# standard library
import os

# local library
from ThotUtils.utils import CommonUtils
from ThotUtils import ThotUtilsFactory

if __name__ == '__main__':
	# get starting path
	path = str(os.getcwd()) + '\downloads'
	if not os.path.exists(path):
		os.mkdir(path)

	# define the object factory
	thotutils = ThotUtilsFactory()

	# initialize the urls to process
	urls = {}

	# process URLS.txt and break up into groups by host
	if os.path.isfile("URLS.txt") and os.stat("URLS.txt").st_size != 0:
		url_list = [line.rstrip('\n\r\n') for line in open("URLS.txt", "r")]
		url_dict = [{CommonUtils.netloc(u):u} for u in url_list]
		for u in url_dict:
			for key, value in u.items():
				urls.setdefault(key, []).append(value)

	# for each host, create a downloader object and process
	for h, u in urls.items():
		# reset path location for each host
		os.chdir(path)
		downloader = thotutils.create(h)
		for url in u:
			downloader.parse_page(url=url)