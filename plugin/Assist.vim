if !has("python")
    echo "need python support!"
    finish
endif

"SETUP PATH
let s:pluginPath= escape(expand('<sfile>:p:h'), '\')
let g:assistHome= s:pluginPath."/../Assist/"

function! RunPyFile(filename)
	exec "pyfile ".g:assistHome."python/".a:filename
endfunction

call RunPyFile("Common.py")
"load python files
call RunPyFile("VimUi.py")
call RunPyFile("GitAssist.py")
call RunPyFile("SearchBackend.py")
call RunPyFile("HistoryAssist.py")
call RunPyFile("BookMarkAssist.py")
call RunPyFile("GtagsAssist.py")
call RunPyFile("AgAssist.py")
call RunPyFile("CtagsAssist.py")
call RunPyFile("FileNvAssist.py")

function! SearchHistory()
	python vimAssistSearchWindow = SearchWindow(FileSearchBackend(HistoryAssist.getHistoryIterms()))
	python vimAssistSearchWindow.show("vimAssistSearchWindow")
endfunction

function! GtagsSymbolDefine(pattern)
	python displayWindow = SearchWindow(TagSearchBackend(GtagsAssist.searchSymbolDefine(vim.eval("a:pattern"))))
	python displayWindow.show("displayWindow")
endfunction


function! GtagsSymbolRef(pattern)
	python displayWindow = SearchWindow(TagSearchBackend(GtagsAssist.searchSymbolRef(vim.eval("a:pattern"))))
	python displayWindow.show("displayWindow")
endfunction

function! GtagsFile(pattern)
	python displayWindow = SearchWindow(FileSearchBackend(GtagsAssist.searchFile(vim.eval("a:pattern"))))
	python displayWindow.show("displayWindow")
endfunction

function! SearchBookMark()
	python displayWindow = SearchWindow(TagSearchBackend(BookMarkAssist.getBookMarkIterms()))
	python displayWindow.show("displayWindow")
endfunction

function! AgSearch(pattern)
	python displayWindow = SearchWindow(TagSearchBackend(AgAssist.search(vim.eval("a:pattern"))))
	python displayWindow.show("displayWindow")
endfunction

function! CtagsSearchCurrentFile()
	python displayWindow = SearchWindow(CtagSearchBackend(CtagsAssist.getCurrentFileTags()))
	python displayWindow.show("displayWindow")
endfunction

function! FileNvSearch(pattern)
	python displayWindow= SearchWindow(FileSearchBackend(FileNvAssist.getFileIterms(vim.eval("a:pattern"))))
	python displayWindow.show("displayWindow")
endfunction



"Commands:"
"Gtags command
command! -nargs=1 GtagsSymbolDefine     call GtagsSymbolDefine(<q-args>)
command! -nargs=1 GtagsSymbolRef        call GtagsSymbolRef(<q-args>)
command! -nargs=1 GtagsFile             call GtagsFile(<q-args>)
command! -nargs=1 GtagsWorkDir          py   GtagsAssist.setWorkdir(<q-args>)

"The sliver searcher
command! -nargs=1 Ag                   call AgSearch(<q-args>)
command! -nargs=1 -complete=dir Agdir                py AgAssist.setWorkdir(<q-args>)
command! AgClearWorkdir                py AgAssist.clearWorkdir()

"File path search
command! -nargs=? Fg                   call FileNvSearch(<q-args>)
command! -nargs=1 -complete=dir Fgdir  py FileNvAssist.setWorkdir(<q-args>)


"book marks commands
command! AddBookmark                   py BookMarkAssist.addCurrentCursorToBookmark()
command! SearchBookMark                call SearchBookMark()
command! EditBookMark                  py BookMarkAssist.edit()
"command! EditBookmark                  py BookMarkAssist.edit()

"Recent files
command! SearchHistory                 call SearchHistory()
command! EditHistory                   py HistoryAssist.edit()
au BufRead,BufNewFile * 			   py HistoryAssist.add()


"Gik
command! Gkblame                    py GitAssist.gitkCurrentLine()
command! Gklog                      py GitAssist.gitkLogCurrentBuffer()
command! -nargs=* Gitk              py GitAssist.gitkCmd(<q-args>)

"Ctags
command! CtagsSearchCurrentFile     call CtagsSearchCurrentFile()


"Maps:
nmap <leader>r :SearchHistory<CR>
nmap <leader>b :SearchBookMark<CR>
nmap <leader>c :CtagsSearchCurrentFile<CR>
nmap <leader>ab :AddBookmark<CR>

"use ag search
nmap <leader>ag :Ag  <C-R>=expand("<cword>")<CR><CR>

nmap <leader>gs :GtagsSymbolRef <C-R>=expand("<cword>")<CR><CR>
nmap <leader>gd :GtagsSymbolDefine <C-R>=expand("<cword>")<CR><CR>
nmap <leader>gf :GtagsFile 

"nmap <leader>ga :ChangeBetweenHeaderAndCFile<CR>

nmap<leader>gp :Gklog<CR>
nmap<leader>gl :Gkblame<CR>

