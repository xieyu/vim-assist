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

#mappings
keyMaps={
		"MatchController":[
		("<C-j>", "selectPre"),
		("<C-p>", "selectPre"), #Don't know why C-p not work
		("<C-n>","selectNext"), 
		("<Up>", "selectPre"),
		("<Down>", "selectNext"),
		("<CR>", "openInOldWinThenHideSelf"),
		("<C-o>","openInOldWin"),
		("<C-t>","openInNewTab"),
		],

		"PromptWindow":[
		("<ESC>","cancel"),
		("<Left>","left"),
		("<Right>","right"),
		("<C-a>", "home"), 
		("<C-e>","end"),
		("<C-h>","left"),
		("<C-l>","right"),
		("<BS>","bs"), 
		("<Del>","del"), 
		("<C-d>","del"),
		("<C-k>","kill"),#like emacs way, del from cursor to end
		]
}
#use for Manager all kinds of settings
settingManager = SettingManager()

for scope, maps in keyMaps.items():
	for keymap, command in maps:
		settingManager.setScopeKeyMap(scope, keymap, command)

