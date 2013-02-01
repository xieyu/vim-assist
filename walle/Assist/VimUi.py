#intereface for Hot SearchWindow
import vim

class HotSearchWindowBackEnd:
    def search(self, word):
        return []

    def getKeyActionMaps(self):
        return [("<cr>","close"),("<2-LeftMouse>","preview"),("<c-o>","preview"), ("<c-p>", "preview")]

    def handle(self, action, iterm):
        return iterm.onAction(action)


class HotSearchWindow:
    backend = None
    searchText = None
    searchResult = []
    preMode = None
    title = None
    @staticmethod
    def setbackend(backend):
        HotSearchWindow.backend = backend
        pass

    @staticmethod
    def setPromt(prompt):
        HotSearchWindow.prompt=prompt

    @staticmethod
    def show(title=""):
        HotSearchWindow.title = "hotsearch"
        if title!= "":
            HotSearchWindow.title = "hotsearch-%s"%title
        vim.command("bo sp hotsearch-%s" % HotSearchWindow.title)
        vim.command("autocmd BufEnter <buffer> python HotSearchWindow.onBufEnter()")
        vim.command("autocmd BufLeave <buffer> python HotSearchWindow.onBufLeave()")
        vim.command("autocmd CursorMovedI <buffer>  python HotSearchWindow.onCursorMoveI()")
        vim.command("setlocal nowrap");
        vim.command("setlocal textwidth=0");
        vim.command("setlocal buftype=nofile")
        vim.command("setlocal completefunc=''")
        vim.command("startinsert")
        vim.command('''inoremap <expr> <buffer> <Enter> '<C-O>:python HotSearchWindow.handleKey("Enter")<CR>' ''')
        keyMaps = HotSearchWindow.backend.getKeyActionMaps()
        for keyMap in keyMaps:
            vim.command("nnoremap <silent> <buffer> %s :python HotSearchWindow.handleKey('%s')<CR>"%keyMap)

    @staticmethod
    def onCursorMoveI():
        (row, col) = vim.current.window.cursor
        buffer = vim.current.buffer
        if row > 1:
            vim.command("setlocal cul")
            vim.command("setlocal completefunc=''")
            return
        vim.command('setlocal nocul')
        vim.command("setlocal completefunc=''")
        text = buffer[0]
        if not HotSearchWindow.searchText is text:
            HotSearchWindow.searchResult = HotSearchWindow.backend.search(text)
            buffer[1:] = [iterm.displayText() for iterm in HotSearchWindow.searchResult]

    @staticmethod
    def handleKey(key):
        (row, col) = vim.current.window.cursor
        if row == 1:
            iterm = HotSearchWindow.searchResult[0]
        else:
            iterm = HotSearchWindow.searchResult[row - 2]

        shouldCloseWindow = HotSearchWindow.backend.handle(key, iterm)
        if shouldCloseWindow:
            bufNumber = vim.eval("bufnr('%s')" % HotSearchWindow.title)
            vim.command(":%s bd!" % bufNumber)

    @staticmethod
    def onBufEnter():
        (row, col) = vim.current.window.cursor
        buffer = vim.current.buffer
        if row == 1:
            vim.command("startinsert")

    @staticmethod
    def onBufLeave():
        if HotSearchWindow.preMode != 'i':
            vim.command("stopinsert")
