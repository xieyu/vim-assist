#a simple abstract layer of VIm intereface
#Author: xieyu3 at gmail dot com 
#License: BSD

import vim
import os
import string

class VimWidget:
	def __init__(self, bufferName):
		self.bufferName = bufferName
		self.create(self.bufferName)
		self.minHeight = None
		self.maxHeight = None

	def close(self):
		try:
			bufferId = int(vim.eval("bufnr('%s')"%self.bufferName))
			if bufferId != -1:
				vim.command("bdelete! %d"%bufferId)
		except:
			pass
	
	def create(self, bufferName):
		#close the old one, if it exists
		self.close() 
		vim.command("bo sp %s"%bufferName) #create a new buffer on bottom
		self.bufferId = int(vim.eval("bufnr('%')"))
		self.windowId = int(vim.eval("winnr()"))
		for b in vim.buffers:
			if b.number == self.bufferId:
				self.buffer = b
		for w in vim.windows:
			if w.buffer.number == self.bufferId:
				self.window = w

	def setContent(self, content):
		self.unlock()
		self.buffer[:] = content
		self.lock()
		self.updateWindowHeight()

	def setLocalOptions(self, options):
		for option in options:
			vim.command("setlocal %s"%option)

	def setHeight(self, height):
		self.window.height = height

	def setHeightRange(self, minHeight, maxHeight):
		self.minHeight = minHeight
		self.maxHeight = maxHeight
		self.setHeight(max(self.minHeight, min(self.maxHeight, len(self.buffer))))

	def updateWindowHeight(self):
		if self.minHeight and self.maxHeight:
			self.setHeight(max(self.minHeight, min(self.maxHeight, len(self.buffer))))

	def show(self):
		vim.command("redraw")
	
	def lock(self):
		#TODO:set it only when option nomodifiable is already setted 
		vim.command("setlocal nomodifiable")

	def unlock(self):
		vim.command("setlocal modifiable")

#Window that can register key map
class Window:
	def __init__(self, selfName, title):
		'''selfName is a hack for in vim, so we can call self member function, it should be the same with your var
		   for example: window = Window("window", title), *make sure python can access the name from glaobal scope*
		   and if you set win= window, then please call win.setSelfName("win") before call win.show()
		   it is used in self.doMapMemberFunction function.
		'''
		self.selfName = selfName
		self.title = title
		self.widget = None
		self.keyMaps = []

	def setSelfName(self, selfName):
		self.selfName = selfName

	def getSelfName(self, selfName):
		return self.selfName

	def setContent(self, content):
		self.widget.setContent(content)

	def getContent(self):
		self.widget.getContent()

	def show(self):
		self.widget = VimWidget(self.title)
		self.makeKeysMap()
		self.widget.setLocalOptions(("buftype=nofile", "nobuflisted" ))
		self.widget.setHeightRange(5, 8)
		for (key, function, param) in self.keyMaps:
			self.doMap(key, function, param)
		vim.command("noremap <C-m> :map<CR>")


	def close(self):
		vim.command(":close")

	def setOptions(self, options):
		pass 

	def registerKeyMap(self, key, function, param=None):
		self.keyMaps.append((key, function, param))

	#private functions
	def doMap(self, key, function, param=None):
		if param is None:
			vim.command("noremap <silent> <buffer> %s :py %s()<CR>"%(key, function))
		else: 
			vim.command('''noremap <silent> <buffer> %s :py %s("%s")<CR>'''%(key, function, param))

	def registerMemberFunction(self, key, function, param=None):
		functionName = "%s.%s"%(self.selfName, function)
		self.registerKeyMap(key, functionName, param)

#window that with prompt line
class MatchWindow(Window):
	def __init__(self, selfName, title, listener):
		Window.__init__(self, selfName, title)
		self.prompt = Prompt(listener)
		self.makeKeysMap()

	def makeKeysMap(self):
		#normal keys
		punctuation ='<>`@#~!"$%&/()=+*-_.,;:?\\\'{}[] ' # and space excpet "|"
		for key in string.letters + string.digits + punctuation:
			self.registerMemberFunction("<Char-%d>"%ord(key),'handleNormalKey',key)

		#specail keys,which used to control prompt line edit
		#note: we can not direct pass key to function in vim, so map it with values
		specailKeysMap = [("<ESC>","esc"),("<BS>","bs"), ("<Del>","del"), ("<Left>","left"), 
				("<Right>","right"), ("<C-a>", "home"), ("<C-e>","end"),
				("<C-k>","kill"),("<C-h>","left"),("<C-l>","right"),
				("<C-d>","del")]

		for key, keyValue in specailKeysMap:
			self.registerMemberFunction(key, 'handleSpecailKey', keyValue)

	def close(self):
		print "call me"
		Window.close(self)
		self.prompt.close()

	def handleNormalKey(self, key):
		self.prompt.add(key)

	def handleSpecailKey(self, keyValue):
		handler={"esc":self.close,
				"bs": self.prompt.backspace,
				"del":self.prompt.delete,
				"right":self.prompt.cursorRight,
				"left":self.prompt.cursorLeft,
				"kill" :self.prompt.killToEnd,
				"home" :self.prompt.cursorStart,
				"end" :self.prompt.cursorEnd
				}[keyValue]
		handler()

class Prompt:
	def __init__(self, listener):
		self.content=[]
		self.listener = listener
		self.col = 0

	def add(self, key):
		self.content.append(key)
		self.moveCursor(1)
		self.redraw()
		self.notify()

	def clear(self):
		self.content=[]
		self.col = 0
		self.redraw()

	def backspace(self):
		if self.col > 0:
			self.content.pop(self.col-1)
			self.moveCursor(-1)
			self.redraw()
			self.notify()

	def delete(self):
		if self.col >=0 and self.col < len(self.content):
			self.content.pop(self.col)
			self.moveCursor(-1)
			self.redraw()
			self.notify()

	def cursorRight(self):
		self.moveCursor(1)
		self.redraw()

	def cursorStart(self):
		self.col=0
		self.redraw()

	def cursorEnd(self):
		self.col=len(self.content)
		self.redraw()

	def cursorLeft(self):
		self.moveCursor(-1)
		self.redraw()

	def killToEnd(self):
		self.content = self.content[0:self.col]
		self.redraw()
		self.notify()

	#private
	def redraw(self):
		prompt = ">>"
		prompt_highlight = "Comment"
		cursor_highlight = "Cursor"
		normal_heiglight = "Normal"
		left, cursor, right = self.segContent()
		drawMaps=[(prompt, prompt_highlight), (left, normal_heiglight), (cursor, cursor_highlight),(right,normal_heiglight)]
		vim.command("redraw")
		for text, highlight in drawMaps:
			if text is not "":
				#note: echohl don't need escape with quote
				vim.command("echohl %s"%highlight)
				vim.command("echon '%s'"%text)
		vim.command("echohl None")

	def close(self):
		self.clear()
		vim.command("redraw")
		vim.command("echo")

	def notify(self):
		self.listener(self.getContent())

	def getContent(self):
		#return "".join(self.content)
		return "cusor is %d"%self.col+"".join(self.content)

	def moveCursor(self, step):
		self.col += step
		if self.col < 0:
			self.col = 0
		if self.col > len(self.content):
			self.col = len(self.content)
		self.notify()

	def segContent(self):
		empty=""
		whiteSpace=' '
		#cousor should be a whitespace char at end
		left, cursor, right = (empty, whiteSpace, empty)
		if self.content is []:
			return (left, cursor, right)

		left=empty.join(self.content[0:self.col])
		if self.col < len(self.content):
			cursor = str(self.content[self.col])
			right = "".join(self.content[self.col + 1: len(self.content)])
		return (left, cursor, right)


def showResults(title, results, fileParser):
	windowId = int(vim.eval("winnr()"))
	widget = VimWidget(title)
	widget.setContent(results)
	widget.setLocalOptions(("buftype=nofile", "nomodifiable", "nobuflisted" ))
	widget.setHeightRange(5, 8)
	widget.show()
	vim.command("map <buffer> <Space> :py %s(windowId=%d, fileParser=%s, hideSelfAfterOpen=False)<CR>"%("VimUi.openInWindow", windowId, fileParser))
	vim.command("map <buffer> <Enter> :py %s(windowId=%d, fileParser=%s, hideSelfAfterOpen=True)<CR>"%("VimUi.openInWindow", windowId, fileParser))
	vim.command("map <buffer> o :py %s(fileParser=%s, hideSelfAfterOpen=True)<CR>"%("VimUi.systemOpen", fileParser))
	vim.command("map <buffer> <silent> <ESC> :hide<CR>")

#open file in window with windowId
def openInWindow(windowId, fileParser, hideSelfAfterOpen):
	(filePath, lineNum) = fileParser(vim.current.line)

	#TODO:set lineNum more correctly. maybe half of option lines
	if lineNum is None:
		lineNum = 20

	if(os.path.exists(filePath)):
		if hideSelfAfterOpen:
			vim.command("hide") #hide current window
		vim.command("%d wincmd w"%windowId) #move focus to windowId
		#TODO:handle when buffer is already loaded
		vim.command("e %s"%filePath)
		vim.command("%d"%lineNum) #jump to that line

def systemOpen(fileParser, hideSelfAfterOpen):
	(filePath, lineNum) = fileParser(vim.current.line)
	os.system("open %s"%filePath)
