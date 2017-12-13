import yaml
import hashlib
from file_cache import FileCache
from datetime import timedelta

cache = FileCache(timedelta(minutes=10))

def loadNotes(lang, filename):
	result = None
	try:
		f = cache.fetch("assets/notes/" + lang + "/" + filename, "r")
	except Exception as ex:
		print("WARNING: Unable to load notes for " + lang + "/" + filename)
	if (result == None and lang != "en"):
		return loadNotes("en", filename)
	elif (result != None):
		return result
	else:
		return None

def inflateItems(items, lang):
	for key, category in items.items():
		for item in category:
			if (item.get("notes") != None):
				item["notes"] = loadNotes(lang, item["notes"])
				if (item["notes"] == None): item.pop("notes", None)
			if (item.get("app") != None):
				item["identifier"] = hashlib.sha256(str(item["app"]).encode()).hexdigest()
			if (item.get("osu") != None):
				item["identifier"] = hashlib.sha256((str(item["osu"]) + str(item["final"])).encode()).hexdigest()
	return items

def inflateConfig(config, params):
	config["firmwares"] = inflateItems(config["firmwares"], params.get("lang", "en"))
	config["applications"] = inflateItems(config["applications"], params.get("lang", "en"))
	return config

lastConfig = None
def getConfig(provider, params):
	config = None
	filename = "config"
	if (len(provider) != 0):
		filename += "_" + provider
	filename += ".yml"
	config = yaml.load(cache.fetch(filename))
	if (config == None and lastConfig != None):
		print("WARNING: An error happened during config loading.")
		return lastConfig
	elif (config != None):
		lastConfig = inflateConfig(config, params)
		return config
	else:
		raise Exception("Unable to load config file")

lastDevices = None
def getDevices(provider, params):
	devices = None
	filename = "devices"
	if (len(provider) != 0):
		filename += "_" + provider
	filename += ".yml"
	devices = yaml.load(cache.fetch(filename))
	if (devices == None and lastDevices != None):
		print("WARNING: An error happened during config loading.")
		return lastDevices
	elif (devices != None):
		lastDevices = devices
		return devices
	else:
		raise Exception("Unable to load devices file")

class LedgerUpdateAPI:

	def getLastFirmware(self, handler, path, params):
		return (500, {"not": "implemented"})

	def getFirmwares(self, handler, path, params):
		try:
			return (200, getConfig(params.get("provider", [""])[0], params)["firmwares"])
		except:
			return (404, {"error": "Provider not found"})

	def getApplications(self, handler, path, params):
		try:
			return (200, getConfig(params.get("provider", [""])[0], params)["applications"])
		except Exception as ex:
			return (404, {"error": "Provider not found"})

	def getDevices(self, handler, path, params):
		try:
			return (200, getDevices(params.get("provider", [""])[0], params))
		except Exception as ex:
			return (404, {"error": "Provider not found"})

	def notFound(self, handler, path, params):
		return (404, {"error": "Call not found"})
