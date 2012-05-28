import os
import Settings
class SettingManager:
	def __init__(self):
		self.keyMaps={}
		pass

	def getScopeCommandKeys(self, scope, command):
		try:
			return self.keyMaps[scope][command]
		except:
			return []

	def setScopeKeyMap(self, scope, command, keys):
		try:
			self.keyMaps[scope][command] = keys
		except:
			self.keyMaps[scope]={}
			self.keyMaps[scope][command] = keys

	def setReposConfigureFilePath(self, path):
		self.reposConfigureFilePath= path

	def getReposConfigureFilePath(self):
		try:
			return self.reposConfigureFilePath
		except:
			return None

class ReposManager:
	def __init__(self, configfilePath):
		self.parser(configfilePath)

	def getReposPaths(self):
		try:
			return self.reposPaths
		except:
			return None

	def getFileIgnorePatterns(self):
		return None

	def getDirIgnorePatterns(self):
		return None

	#private
	def parser(self, filePath):
		f = open(filePath)
		self.reposPaths= [path for path in f.readlines() if os.path.exists(path)]



#use for Manager all kinds of settings
settingManager = SettingManager()

def setUpKeysMap():
	for scope, maps in Settings.keyMaps.items():
		for command, keys in maps:
			settingManager.setScopeKeyMap(scope, command, keys)

#set repos paths
#settingManager.setReposConfigureFilePath(Settings.reposFilePath)

#setUpKeysMap()
