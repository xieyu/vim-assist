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
"call RunPyFile("GitAssist.py")
call RunPyFile("SearchBackend.py")
call RunPyFile("HistoryAssist.py")
call RunPyFile("BookMarkAssist.py")
call RunPyFile("GtagsAssist.py")
call RunPyFile("AgAssist.py")
"call RunPyFile("GtagsAssist.py")
"call RunPyFile("BufferListAssist.py")
function! SearchHistory()
	call RunPyFile("HistoryAssist.py")
	python vimAssistSearchWindow = SearchWindow(FileSearchBackend(HistoryAssist.getHistoryIterms()))
	python vimAssistSearchWindow.show("vimAssistSearchWindow")
endfunction

function! SearchGtagsSymbolDefine(pattern)
	python displayWindow = SearchWindow(TagSearchBackend(GtagsAssist.searchSymbolDefine(vim.eval("a:pattern"))))
	python displayWindow.show("displayWindow")
endfunction


function! SearchGtagsSymbolRef(pattern)
	python displayWindow = SearchWindow(TagSearchBackend(GtagsAssist.searchSymbolRef(vim.eval("a:pattern"))))
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

"Commands:"
"gtags command
command! -nargs=1 SearchSymbolDefine   call SearchGtagsSymbolDefine(<q-args>)
command! -nargs=1 SearchSymbolRef      call SearchGtagsSymbolRef(<q-args>)

command! -nargs=1 Ag                   call AgSearch(<q-args>)
command! -nargs=1 AgWorkdir         py AgAssist.setWorkdir(<q-args>)
command! AgClearWorkdir                py AgAssist.clearWorkdir()


"book marks commands
command! AddBookmark                   py BookMarkAssist.addCurrentCursorToBookmark()
command! EditBookmark                  py BookMarkAssist.edit()

"recent files
command! EditHistory                   py HistoryAssist.edit()
au BufRead,BufNewFile * 			   py HistoryAssist.add()

"search quick in bufferlist
command! SearchBufferListHot		   py BufferListAssist.searchHot()
command! Test                          py HotSearchTest()

"Gik
command! Gkblame                    py GitAssist.gitkCurrentLine()
command! Gklog                      py GitAssist.gitkLogCurrentBuffer()
command! -nargs=* Gitk              py GitAssist.gitkCmd(<q-args>)

"command! MakeFilePathTags              py WalleTagsManager.makeFilePathTags()

"command! ChangeBetweenHeaderAndCFile py SearchAssist.changeBetweenHeaderAndcFile(<q-args>)
"Maps:

nmap <leader>r :call SearchHistory()<CR>
nmap <leader>l :SearchGtagsHistory<CR>
nmap <leader>b :call SearchBookMark()<CR>
nmap <leader>ab :AddBookmark<CR>

"use ag search
nmap <leader>ga :Ag  <C-R>=expand("<cword>")<CR><CR>

nmap <leader>gs :SearchSymbolRef <C-R>=expand("<cword>")<CR><CR>
nmap <leader>gd :SearchSymbolDefine <C-R>=expand("<cword>")<CR><CR>
nmap <leader>gf :SearchFile <C-R>=expand("<cword>")<CR><CR>
"nmap <leader>ga :ChangeBetweenHeaderAndCFile<CR>

nmap<leader>gp :Gklog<CR>
nmap<leader>gl :Gkblame<CR>

