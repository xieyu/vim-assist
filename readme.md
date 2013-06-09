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

##Code Search##

First you should install [google code search tool](http://code.google.com/p/codesearch/), and set it to $PATH, and setup these tow program's path, maybe like this:

	let g:assist_csearch="~/Apps/codesearch-0.01/csearch"
	let g:assist_cindex="~/Apps/codesearch-0.01/cindex"

###Cs###
It will show line that match this pattern, if pattern is empty(that you just input command Cs), then word under the cursor will be used.

	:Cs pattern

after the result is shown in the buffer, you can continue search by input filename@content, which will compare the search result with filename and content. for example
bar@foo, it will search in the candidate which file name contain 'bar' and foo cotained in content

pattern, use * to represent any number of any char, and $ represent end. ^ represent start, for example

	^dox*bar*.cpp$

and the dir that you want to search can be set by command Cscd.

###Cscd##
only search code under dir-path

	Cscd dir-path

###Cindex###
make index for code-dir

	:Cindex code-dir


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
