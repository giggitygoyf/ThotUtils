# standard library
import argparse
import os

# local library
from ThotUtils import ThotUtilsFactory

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'--host',
	)
	args = parser.parse_args()

	thotutils = ThotUtilsFactory()
	downloader = thotutils.create(args.host)

	if os.path.isfile("URLS.txt") and os.stat("URLS.txt").st_size != 0:
		url_file = open("URLS.txt", "r")
		for line in url_file:
			# skip blank lines
			if line in ['\n', '\r\n']:
				continue

			downloader.parse_page(url=line.rstrip())