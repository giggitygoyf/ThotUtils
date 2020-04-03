from urllib.parse import urlparse, urljoin

class CommonUtils:
	@staticmethod
	def netloc(url):
		if urlparse(url).netloc.split('.')[0] == 'www':
			return '.'.join(urlparse(url).netloc.split('.')[1:])
		else:
			return urlparse(url).netloc