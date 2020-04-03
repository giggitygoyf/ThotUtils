# local library
from ThotUtils.Scrapers import cyberdrop, erome, thothub

class ThotUtilsFactory:
	def __init__(self):
		self._builders = {
			'cyberdrop.me': cyberdrop.CyberDropDownloaderBuilder(),
			'erome.com': erome.EromeDownloaderBuilder(),
			'thothub.tv': thothub.ThotHubDownloaderBuilder(),
			'forum.thothub.tv': thothub.ThotHubForumDownloaderBuilder(),
		}

	def register_builder(self, key, builder):
		self._builders[key] = builder

	def create(self, key, **kwargs):
		builder = self._builders.get(key)
		if not builder:
			raise ValueError(key)
		return builder(**kwargs)