#finder
finder is a  plugin for vim, which make write extension for immedidate search 
(like vim plugin Ctrlp Or Command-T) easily

* Written in python.
* provide several useful components
* easy to write extension

##useage
###install
* use pathgon to install it see <a href="https://github.com/tpope/vim-pathogen">pathgon</a> for details

###commands:
* use command EditFinderRepos to add dirs that you want to search
* use command RefreshFinderRepos to refresh index, if there are some changed under these dirs
* command FinderFile will begin search

###keymaps:
* currently I map Ctrl + f with FinderFile, you can remap it with your faverator one.

###Select and move cursor
* after search, use Ctrl + j to select next, Ctrl + k select pre, press Enter to start edit
* when you input something to search, you can use Ctrl + a (move to begine), Ctrl + h (move left), Ctrl + l (move right), Ctrl + e (move to edit)
to move cursor, and Ctrl+w to del word. Just try and enjoy it!
	


##Write extension
well, There're lots of things to be find, tags, functions, symbols and so on. you can easylly write an extension for it like filefinder,
###Concepts:
There several Class in this packet:
* Candidate is a basic record for search, It's member name will be shown to user, and it's member content used for search
* Finder is used for select suite candidate from Candidates, it must provide query, getSuiteCandidate, getSuiteCandidateNum intereface
* Acceptor will be called when user select some candidate, it must provide intereface : accept
* Controller is used to compbine these components..	

###Attension:
pay attension, you must import SharedFactory in this way in your *.vim, It's was caused by a hack for make vim keys to instances member function.

from Factory import SharedFactory



