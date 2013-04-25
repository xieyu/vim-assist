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

call RunPyFile("Init.py")
call RunPyFile("Common.py")
call RunPyFile("VimUi.py")
call RunPyFile("GitAssist.py")
call RunPyFile("SearchBackend.py")
call RunPyFile("HistoryManager.py")
call RunPyFile("Locate.py")
call RunPyFile("BookMarkAssist.py")
call RunPyFile("GtagsAssist.py")
call RunPyFile("AgAssist.py")
call RunPyFile("CtagsAssist.py")
call RunPyFile("CodeSearchAssist.py")


"Commands:"
"Gtags command
"command! -nargs=? Gs                 call GtagsSymbolDefine(<q-args>)
"command! -nargs=? Gr                 call GtagsSymbolRef(<q-args>)
"command! -nargs=? Gf                 call GtagsFile(<q-args>)
"command! -nargs=1 Gtagdir            py   GtagsAssist.setWorkdir(<q-args>)
"
""The sliver searcher
"command! -nargs=? Ag                   call AgSearch(<q-args>)
"command! -nargs=1 -complete=dir Agdir                py AgAssist.setWorkdir(<q-args>)
"command! AgClearWorkdir                py AgAssist.clearWorkdir()
"
""The codesearch
"command! -nargs=? Cs                   call CodeSearch(<q-args>)
"command! -nargs=1 -complete=dir Csdir    py CodeSearchAssist.setSearchDir(<q-args>)
"command! -nargs=1 -complete=dir CsMakeIndex   py CodeSearchAssist.makeIndex(<q-args>)
"
""File path search
"command! -nargs=? LocateFile            call LocateFile(<q-args>)
"command! -nargs=1 -complete=dir Lcd		py Locate.setWorkdir(<q-args>)
"
"
""book marks commands
"command! AddBookmark                   py BookMarkAssist.addCurrentCursorToBookmark()
"command! SearchBookMark                call SearchBookMark()
"command! EditBookMark                  py BookMarkAssist.edit()
""command! EditBookmark                  py BookMarkAssist.edit()

"Recent files
command! SeachHistory         py LocateFile.startSearch("")
command! EditHistory                   py HistoryManager.edit()
au BufRead,BufNewFile * 			   py HistoryManager.add()


"Gitk
command! Gkblame                    py GitAssist.gitkCurrentLine()
command! Gklog                      py GitAssist.gitkLogCurrentBuffer()
command! -nargs=* Gitk              py GitAssist.gitkCmd(<q-args>)

"Ctags
command! CtagsCurrentFile           call CtagsSearchCurrentFile()

"Opengl document
"command! -nargs=* Openglman         call OpenGLMan(<q-args>)
"command! -nargs=* GoogleSearch      call GoogleSearch(<q-args>)
"command! -nargs=1 Bts               py OperaBts.browserBug(<q-args>)
"command! -nargs=* StackOverFlow     call StackOverFlow(<q-args>)
