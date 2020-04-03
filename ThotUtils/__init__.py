# local library
from ThotUtils.CyberDrop.cyberdrop import CyberDropDownloaderBuilder
from ThotUtils.Erome.erome import EromeDownloaderBuilder

class ThotUtilsFactory:
	def __init__(self):
		self._builders = {
			'CyberDrop': CyberDropDownloaderBuilder(),
			'Erome': EromeDownloaderBuilder()
		}

	def register_builder(self, key, builder):
		self._builders[key] = builder

	def create(self, key, **kwargs):
		builder = self._builders.get(key)
		if not builder:
			raise ValueError(key)
		return builder(**kwargs)