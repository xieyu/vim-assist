import vim

"""
Acceptor is used for handle user's accept selection, It is used in MatchController, and should 
define follow intereface

"@interface
class Acceptor():
	def __init__(self):
		pass
	def accept(self, candidate, options = None):
		#if you want keep the MatchController window open:
		return True
"
you can register key map with option:
MatchController.addKeyMapForCommand("acceptSelect", keys, option):

@Attention: keys should be a list, and option should be a string.

in matchController the default key map that will triger accept is <cr>, and default option is None, 
"""
class Acceptor:
	def __init__(self):
		pass
	def getKeysMap():
		"should return a dic {'key':'param',} or None"
		return None
	def accept(self, candidate, param):
		pass

class FileAcceptor(Acceptor):
	def __init__(self):
		pass

	def accept(self, fileCandidate, options = None):
		if options is None:
			return self.editFile(fileCandidate)

	def selectWindow(self):
		vim.command("wincmd w") #try next window

	def editFile(self, fileCandidate):
		self.selectWindow()
		vim.command("silent e %s"%fileCandidate.getFilePath())
		#close the window
		return False

class LineAcceptor(Acceptor):
	def __init__(self):
		pass

	def accept(self, lineCandidate, options = None):
		if options is None:
			return self.editFile(lineCandidate)

	def selectWindow(self):
		vim.command("wincmd w") #try next window

	def editFile(self, lineCandidate):
		self.selectWindow()
		vim.command("silent e %s"%lineCandidate.getFilePath())
		vim.command("%d"%lineCandidate.getLineNum())
		#close the query the window
		return False

class WorldAcceptor(Acceptor):
	def __init__(self):
		pass
	def accept(self, lineCandidate, options = None):
		pass
	def editFile(self, WordCandidate):
		pass

		


