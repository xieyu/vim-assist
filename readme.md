#Assist for vim#
As a programmer, there always annoy things to do, such as find file to edit or search the sybmol where it is referenced and where is it defined. 
so I integrate some useful tools into vim, to make it more comfortable to use vim.

###Require###
Require python and vim compled with python feature. and install [code search](http://code.google.com/p/codesearch/)


##Common intereface##
all tools in vim-assit  such as locatefile or code search, will open a window to show the search result, In this window you can use following keymaps

* `<esc>`   close the search window
* `<enter>` open file under cursor and close the search window
* `<c-o>``  open file under cursor without close the search window, and jump to the window that open the file
* `<c-p>`   open file under cursor withtout close the search window, without jump to window that open the file
* `<c-j>`   select next one
* `<c-k>`   select pre one

##Locate File##
Locate file is used for quick file search, just like ctrlp and command-t

###L###
use command L, it will search the all the file under vim current dir or the path you set by command Lcd

	:L part-of-filename

it will show an buffer, that contain the file which match the <code>part-of-filename</code>, then continue input the
part of filename, it will continue on match the file with your input.

###Lcd###
set the search dir, the default one is vim current dir.

	:Lcd ~/codes/demo

if the path is not exist, for example <code>:Lcd demo</code>, then it will open a window and show all the history path(which you Lcd before..) which match 'demo'.

###Lswitch###

switch between [.h|.hpp] with [.cpp|.m|.c|.cc] in vim current dir or the dir set by Lcd
	
	:Lswitch

###Lbuffer###
use command Lbuffer, it will list all the file that you opened in vim now. then you can quick search and jump to that file

	:Lbuffer

##Ctags Search##

this tool is used to quick locate to the function or class defined in current file. current provide one command:

	:Ctagcurfile

require install <code>exuberant-ctags</code>, for ubuntu user:

	sudo apt-get install exuberant-ctags


<code>Ctagcurfile</code> command will list all the symbols(function, marco, class) define in the search window, then you can input some pattern to quick search.

suggest make a map for it in your <code>.vimrc</code>

	nmap <leader>c  :Ctagcurfile<CR>

##Code Search##

First you should install [google code search tool](http://code.google.com/p/codesearch/), 

then set it to $PATH, and setup these tow tool's path in your <code>.vimrc</code>,  like this:

	let g:assist_csearch="~/Apps/codesearch-0.01/csearch"
	let g:assist_cindex="~/Apps/codesearch-0.01/cindex"

###Cindex###
make index for code-dir

	:Cindex code-dir

###Cs###
before search, you should make index by command <code>:Cindex</code>

It will show line that match this pattern, if pattern is empty(that you just input command Cs), then word under the cursor will be used.

	:Cs pattern

after the result is shown in the buffer, you can continue search by input filename@content, which will compare the search result with filename and content. for example
bar@foo, it will search in the candidate which file name contain 'bar' and foo cotained in content

pattern, use * to represent any number of any char, and $ represent end. ^ represent start, for example

	^dox*bar*.cpp$@^class*Message$

it will search the tag  which file name is start with "dox" and end with ".cpp", and content is start with "class", end with "Message"

and the dir that you want to search can be set by command Cscd.

###Cscd##
only search code under dir-path, if not set, it will search all files that you have cindexed. 

	Cscd dir-path

##Buffer Search##
###Bs###
Bs means buffer search, it will show the line in current buffer which contain pattern, if pattern is empty, 
the word under the cursor will be used.

	:Bs pattern

after the result is shown in the buffer, you can continue search by input filename@content, which will compare the search result with filename and content.

###Bsa###
same with command Bs but search all buffer

	:Bsa pattern

##Gitk##
need install gitk first

	sudo apt-get install gitk

###Gkblame###
Gkblame will call gitk to show the commit which change current line.	

	:Gkblame

###Gklog###
command <code>Gklog</code>, this will call gitk to show the log of current file.

	:Gklog

###Gitk###
same useage as command gitk

	:Gitk args

##TODO##
* better search pattern, and rank, hightlight search result.
* locate to symobl quick in the project instead of just cur file.
* make index of LocateFile, so can hold large code project like webkit.
* bookmark, history search, open file with sys default app.
* google, stackoverflow, wiki search etc.
