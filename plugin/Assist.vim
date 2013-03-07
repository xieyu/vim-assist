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

function! GetCusorWordIfEmpty(pattern)
	let l:word=a:pattern
	if l:word == ""
		let l:word = expand("<cword>")
	endif
	return l:word
endfunction


function! SearchHistory(pattern)
	python vimAssistSearchWindow = SearchWindow(FileSearchBackend(HistoryAssist.getHistoryIterms(vim.eval("a:pattern"))))
	python vimAssistSearchWindow.show("vimAssistSearchWindow")
endfunction

function! GtagsSymbolDefine(pattern)
	let l:word = GetCusorWordIfEmpty(a:pattern)
	python displayWindow = SearchWindow(TagSearchBackend(GtagsAssist.searchSymbolDefine(vim.eval("l:word"))))
	python displayWindow.show("displayWindow")
endfunction


function! GtagsSymbolRef(pattern)
	let l:word= GetCusorWordIfEmpty(a:pattern)
	python displayWindow = SearchWindow(TagSearchBackend(GtagsAssist.searchSymbolRef(vim.eval("l:word"))))
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
	let l:word= GetCusorWordIfEmpty(a:pattern)
	python displayWindow = SearchWindow(TagSearchBackend(AgAssist.search(vim.eval("l:word"))))
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
command! -nargs=? Gs                 call GtagsSymbolDefine(<q-args>)
command! -nargs=? Gr                 call GtagsSymbolRef(<q-args>)
command! -nargs=? Gf                 call GtagsFile(<q-args>)
command! -nargs=1 Gtagdir               py   GtagsAssist.setWorkdir(<q-args>)

"The sliver searcher
command! -nargs=? Ag                   call AgSearch(<q-args>)
command! -nargs=1 -complete=dir Agdir                py AgAssist.setWorkdir(<q-args>)
command! AgClearWorkdir                py AgAssist.clearWorkdir()

"File path search
command! -nargs=? Fn                   call FileNvSearch(<q-args>)
command! -nargs=1 -complete=dir Fndir  py FileNvAssist.setWorkdir(<q-args>)
command!  Fncleardir                   py FileNvAssist.clearWorkdir()


"book marks commands
command! AddBookmark                   py BookMarkAssist.addCurrentCursorToBookmark()
command! SearchBookMark                call SearchBookMark()
command! EditBookMark                  py BookMarkAssist.edit()
"command! EditBookmark                  py BookMarkAssist.edit()

"Recent files
command! -nargs=? SeachHistory                            call SearchHistory(<q-args>)
command! EditHistory                   py HistoryAssist.edit()
au BufRead,BufNewFile * 			   py HistoryAssist.add()


"Gik
command! Gkblame                    py GitAssist.gitkCurrentLine()
command! Gklog                      py GitAssist.gitkLogCurrentBuffer()
command! -nargs=* Gitk              py GitAssist.gitkCmd(<q-args>)

"Ctags
command! CtagsCurrentFile     call CtagsSearchCurrentFile()
