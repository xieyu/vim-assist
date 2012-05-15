import os
import Settings
class SettingManager:
	def __init__(self):
		self.keyMaps={}
		pass

	def getScopeKeyMap(self, scope, command):
		try:
			return self.keyMaps[scope][command]
		except:
			return None

	def setScopeKeyMap(self, scope, key, command):
		try:
			self.keyMaps[scope][command] = key
		except:
			self.keyMaps[scope]={}
			self.keyMaps[scope][command] = key

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

	def getDictionIgnorePatterns(self):
		return None

	#private
	def parser(self, filePath):
		f = open(filePath)
		self.reposPaths= [path for path in f.readlines() if os.path.exists(path)]



#use for Manager all kinds of settings
settingManager = SettingManager()

#set keys
for scope, maps in Settings.keyMaps.items():
	for keymap, command in maps:
		settingManager.setScopeKeyMap(scope, keymap, command)
#set repos paths
settingManager.setReposConfigureFilePath(Settings.reposFilePath)
