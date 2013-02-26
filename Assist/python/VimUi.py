#intereface for Hot SearchWindow
import vim
import re

class SearchBackend:
    def search(self, word):
        return []

    def getKeyActionMaps(self):
        return [("<cr>","close"),("<2-LeftMouse>","preview"),("<c-o>","preview"), ("<c-p>", "preview")]

    def handle(self, action, iterm):
        return iterm.onAction(action)


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

class SearchWindow:
    def __init__(self, backend):
        self.prompt = Prompt()
        self.backend = backend
        self.searchResultIterms = []

    @staticmethod
    def runApp(backend):
        global vimAssistSearchWindow
        vimAssistSearchWindow = SearchWindow(backend)
        vimAssistSearchWindow.createShowBuffer("vimAssistSearchWindow")


    def showMatchedResult(self):
        pat = self.prompt.getName()
        self.searchResultIterms = self.backend.search(pat)
        buffer = vim.current.buffer
        buffer[:] = None
        for i, iterm in enumerate(self.searchResultIterms):
            if i == 0 and len(buffer) == 1 and buffer[0] == "":
                buffer[0] = iterm.displayText()
            else:
                buffer.append(iterm.displayText())
        win_height = min(len(self.searchResultIterms), 15)
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


    def createShowBuffer(self, varName):
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

        printables = """/!"#$%&'()*+,-.0123456789:<=>?#@"ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_abcdefghijklmnopqrstuvwxyz{}~"""
        mapcmd = "noremap <silent> <buffer>"

        for byte in printables :
            vim.command("%s %s :python %s.onKeyPressed('%s')<CR>" % (mapcmd, byte, varName, byte))

        vim.command("%s  <Tab>    :python %s.onKeyPressed('%s')<cr>" %(mapcmd, varName, "Tab"))
        vim.command("%s  <BS>     :python %s.onKeyPressed('%s')<cr>" %(mapcmd, varName, "BS"))
        vim.command("%s  <Del>    :python %s.onKeyPressed('%s')<cr>" %(mapcmd, varName, "Del"))
        vim.command("%s  <Esc>    :python %s.onKeyPressed('%s')<cr>" %(mapcmd, varName, "ESC"))
        vim.command("%s  <C-j>    :python %s.onCursorMove('down')<cr>" %(mapcmd, varName))
        vim.command("%s  <C-k>    :python %s.onCursorMove('up')<cr>" %(mapcmd, varName))
        vim.command("%s  <C-y>    :python %s.onYankContent()<cr>" %(mapcmd, varName))

        for keyMap in self.backend.getKeyActionMaps():
            vim.command("%s %s :python %s.handleKeyAction('%s')<CR>"%(mapcmd, keyMap[0], varName, keyMap[1]))


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

    def yankContent(self):
        work_buffer=vim.current.buffer
        row,col = vim.current.window.cursor
        content = re.escape( work_buffer[row-1])
        vim.command('let @@="%s"' % content )
        print "line has been yanked."

    def onKeyPressed(self, key):
        if key == "Tab" :
            pass
        elif key == "BS" or key == "Del":
            self.prompt.deleteLast()
            self.prompt.show()
            self.showMatchedResult()
        elif key == "ESC":
            self.clean()
        else :
            self.prompt.append(key)
            self.prompt.show()
            self.showMatchedResult()

    def handleKeyAction(self, key):
        row, col = vim.current.window.cursor
        if len(self.searchResultIterms) < row:
            return
        iterm = self.searchResultIterms[row - 1]
        shouldCloseWindow = self.backend.handle(key, iterm)
        if shouldCloseWindow:
            self.clean()

    def clean(self):
        vim.command("bwipeout")
        vim.command("echo ''")
        self.restoreEnv()
        self.restoreWinsize()
        vim.command("exec '%s wincmd w'" % self.last_winnr)
