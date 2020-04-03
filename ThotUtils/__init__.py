# local library
from ThotUtils.Scrapers import cyberdrop, erome, thothub

class ThotUtilsFactory:
	def __init__(self):
		self._builders = {
			'CyberDrop': cyberdrop.CyberDropDownloaderBuilder(),
			'Erome': erome.EromeDownloaderBuilder(),
			'ThotHub': thothub.ThotHubDownloaderBuilder(),
		}

	def register_builder(self, key, builder):
		self._builders[key] = builder

	def create(self, key, **kwargs):
		builder = self._builders.get(key)
		if not builder:
			raise ValueError(key)
		return builder(**kwargs)