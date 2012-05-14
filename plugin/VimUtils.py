import vim

def getCurBufferContent():
	return vim.current.buffer[:]

def getCurBufferName():
	return vim.current.buffer.name

def getCurWinId():
	return int(vim.eval("winnr()"))

def getCurLineNum():
	(row, col) = vim.current.window.cursor
	return row

def error(msg):
	# FIXME:does vim has exit function ?
	vim.command('''echo "%s"'''%msg)
	vim.command("redraw")

def closeCurWin():
	vim.command("close")

def hideCurWin():
	vim.command("hide")

def openFile(filePath, postion):
	vim.command("silent e %s"%filePath)
	if postion:
		(lin, col) = postion
		#FIXME:how to move to col ?
		if lin:
			vim.command("%d"%lin)

def jumpToLine(lineNum):
	vim.command("%d"%lineNum)

def makeWinFocusOn(winId):
	vim.command("%d wincmd w"%winId)

