#a simple abstract layer of VIm intereface
#Author: xieyu3 at gmail dot com 
#License: BSD

import vim
import os

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

	def setContents(self, contents):
		self.unlock()
		self.buffer[:] = contents
		self.lock()
		self.updateWindowHeight()

	#TODO:use python args list at here
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

def showResults(title, results, fileParser):
	windowId = int(vim.eval("winnr()"))
	widget = VimWidget(title)
	widget.setContents(results)
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
