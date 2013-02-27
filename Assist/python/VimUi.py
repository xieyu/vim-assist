#intereface for Hot SearchWindow
import vim
import re

class SearchBackend:
    def search(self, word):
        return []

    def getKeyActionMaps(self):
        return [("<cr>","close"),("<2-LeftMouse>","preview"),("<c-o>","preview"), ("<c-p>", "preview"), ("<c-y>", "yank")]

    def handle(self, action, iterm):
        return iterm.onAction(action)

    def getInitDisplayIterms(self):
        return []

class DisplayBackend:
    def getDisplayIterms(self):
        return []

    def getKeyActionMaps(self):
        return [("<cr>","close"),("<2-LeftMouse>","preview"),("<c-o>","preview"), ("<c-p>", "preview"), ("<c-y>", "yank")]

    def handle(self, action, iterm):
        return iterm.onAction(action)

class ItermsDisplayer(DisplayBackend):
    def __init__(self, iterms):
        self.iterms = iterms

    def getDisplayIterms(self):
        return self.iterms

class ItermsFilter(SearchBackend):
    def __init__(self, iterms):
        self.iterms = iterms

    def getInitDisplayIterms(self):
        return self.iterms

    def search(self, word):
        return [iterm for iterm in self.iterms if self.itermPassCheck(word, iterm)]

    def itermPassCheck(self, world, iterm):
        return True


class DisplayWindow(object):
    def __init__(self, backend):
        self.backend = backend
        self.iterms = []

    def showIterms(self, iterms):
        buffer = vim.current.buffer
        buffer[:] = None
        for i, iterm in enumerate(iterms):
            if i == 0 and len(buffer) == 1 and buffer[0] == "":
                buffer[0] = iterm.displayText()
            else:
                buffer.append(iterm.displayText())
        win_height = max(min(len(iterms), 25), 4)
        vim.command("resize %s" % str(win_height) )

    def saveEnv(self):
        self.timeoutlen = vim.eval("&timeoutlen")
        self.insertmode = vim.eval("&insertmode")
        self.showcmd = vim.eval("&showcmd")
        self.report = vim.eval("&report")
        self.sidescroll = vim.eval("&sidescroll")
        self.sidescrolloff = vim.eval("&sidescrolloff")
        self.guicursor = vim.eval("&guicursor")
        self.cursor_bg = vim.eval("""synIDattr(synIDtrans(hlID("Cursor")), "bg")""")
        self.last_winnr = vim.eval("winnr()")
        if self.cursor_bg == None :
            self.cursor_bg = "white"

        #save each window height
        winnr = vim.eval("winnr('$')")
        self.winheights = []
        for i in range(1,int(winnr)):
            self.winheights.append(vim.eval("winheight('%s')" % str(i)))

    def restoreEnv(self):
        vim.command("set timeoutlen=%s" % self.timeoutlen)

        if self.insertmode == "0" :
            vim.command("set noinsertmode")
        else :
            vim.command("set insertmode")

        if self.showcmd == "0":
            vim.command("set noshowcmd")
        else :
            vim.command("set showcmd")

        vim.command("set report=%s" % self.report )
        vim.command("set sidescroll=%s" % self.sidescroll)
        vim.command("set sidescrolloff=%s" % self.sidescrolloff)

        vim.command("set guicursor=%s" % self.guicursor)
        vim.command("highlight Cursor guifg=black guibg=%s" % (self.cursor_bg))

    def restoreWinsize(self):
        for i in range(0,len(self.winheights)):
            vim.command("exec '%s wincmd w'" % str(i+1) )
            vim.command("resize %s" % self.winheights[i])

    def createShowBuffer(self):
        self.saveEnv()
        vim.command("silent! keepalt botright 1split explorer_buffer")
        vim.command("setlocal bufhidden=delete")
        vim.command("setlocal buftype=nofile")
        vim.command("setlocal noswapfile")
        vim.command("setlocal nowrap")
        vim.command("setlocal nonumber")
        vim.command("setlocal foldcolumn=0")
        vim.command("setlocal nocursorline")
        vim.command("setlocal nospell")
        vim.command("setlocal nobuflisted")
        vim.command("setlocal textwidth=0")
        vim.command("setlocal noreadonly")
        vim.command("setlocal cursorline")

        vim.command("set timeoutlen=0")
        vim.command("set noinsertmode")
        vim.command("set noshowcmd")
        vim.command("set nolist")
        vim.command("set report=9999")
        vim.command("set sidescroll=0")
        vim.command("set sidescrolloff=0")

        vim.command("set guicursor+=a:blinkon0")
        bg = vim.eval("""synIDattr(synIDtrans(hlID("Normal")), "bg")""")
        if bg :
            vim.command("highlight Cursor guifg=black guibg=%s" % (bg))

    def doMapKeys(self, selfName):
        mapcmd = "noremap <silent> <buffer>"
        vim.command("%s  <Tab>    :python %s.onKeyPressed('%s')<cr>" %(mapcmd, selfName, "Tab"))
        vim.command("%s  <BS>     :python %s.onKeyPressed('%s')<cr>" %(mapcmd, selfName, "BS"))
        vim.command("%s  <Del>    :python %s.onKeyPressed('%s')<cr>" %(mapcmd, selfName, "Del"))
        vim.command("%s  <Esc>    :python %s.onKeyPressed('%s')<cr>" %(mapcmd, selfName, "ESC"))
        vim.command("%s  <C-j>    :python %s.onCursorMove('down')<cr>" %(mapcmd, selfName))
        vim.command("%s  <C-k>    :python %s.onCursorMove('up')<cr>" %(mapcmd, selfName))

        for keyMap in self.backend.getKeyActionMaps():
            vim.command("%s %s :python %s.handleKeyAction('%s')<CR>"%(mapcmd, keyMap[0], selfName, keyMap[1]))

    def show(self, selfName):
        self.createShowBuffer()
        self.doMapKeys(selfName)
        self.iterms = self.backend.getDisplayIterms()
        self.showIterms(self.iterms)

    def onKeyPressed(self, key):
        if key == "ESC":
            self.clean()

    def onPastContent(self):
        content = vim.eval("getreg('+')")
        content = content.replace("\n","").strip()
        self.prompt.append(content)
        self.prompt.show()
        self.showMatchedResult()

    def onCursorMove(self, direction):
        work_buffer = vim.current.buffer
        win = vim.current.window
        row,col = win.cursor
        if direction == "up" :
            if row > 1 : win.cursor = ( row-1 , col)
        else :
            if row < len(work_buffer) : win.cursor = ( row+1 , col)

    def handleKeyAction(self, action):
        row, col = vim.current.window.cursor
        if len(self.iterms) < row:
            return
        iterm = self.iterms[row - 1]
        shouldCloseWindow = self.backend.handle(action, iterm)
        if shouldCloseWindow:
            self.clean()

    def clean(self):
        vim.command("bwipeout")
        vim.command("echo ''")
        self.restoreEnv()
        self.restoreWinsize()

class Prompt(object) :
    def __init__(self):
        self.key_strokes = []

    def getName(self):
        return "".join(self.key_strokes)

    def append(self,char):
        self.key_strokes.append(char)

    def deleteLast(self):
        self.key_strokes = self.key_strokes[0:-1]

    def show(self):
        vim.command("echo '%s%s'" % (">> ", self.getName() ))

class SearchWindow(DisplayWindow):
    def __init__(self, backend):
        self.prompt = Prompt()
        self.backend = backend

    def show(self, selfName):
        self.createShowBuffer()
        self.doMapKeys(selfName)
        self.iterms = self.backend.getInitDisplayIterms()
        self.showIterms(self.iterms)

    def showMatchedIterms(self):
        pat = self.prompt.getName()
        self.iterms = self.backend.search(pat)
        self.showIterms(self.iterms)

    def doMapKeys(self, selfName):
        super(SearchWindow, self).doMapKeys(selfName)
        printables = """/!"#$%&'()*+,-.0123456789:<=>?#@"ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_abcdefghijklmnopqrstuvwxyz{}~"""
        mapcmd = "noremap <silent> <buffer>"
        for byte in printables :
            vim.command("%s %s :python %s.onKeyPressed('%s')<CR>" % (mapcmd, byte, selfName, byte))

    def onKeyPressed(self, key):
        if key == "Tab" :
            pass
        elif key == "BS" or key == "Del":
            self.prompt.deleteLast()
            self.prompt.show()
            self.showMatchedIterms()
        elif key == "ESC":
            self.clean()
        else :
            self.prompt.append(key)
            self.prompt.show()
            self.showMatchedIterms()
