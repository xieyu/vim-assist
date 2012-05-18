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

class FileAcceptor:
	def __init__(self):
		pass

	def accept(self, fileCandidate, options = None):
		if options is None:
			return self.editFile(fileCandidate)

	def editFile(self, fileCandidate):
		vim.command("silent e %s"%fileCandidate.getFilePath())
		#keep it
		return True

class LineAcceptor(FileAcceptor):
	def __init__(self):
		FileAcceptor.__init__(self)
		pass
	def accept(self, lineCandidate, options = None):
		if options is None:
			return self.editFile(lineCandidate)

	def editFile(self, lineCandidate):
		vim.command("silent e %s"%lineCandidate.getFilePath())
		vim.command("%d"%lineCandidate.getLineNum())
		#keep the window
		return True
		


