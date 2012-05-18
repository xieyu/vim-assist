#finder
finder is a  plugin for vim, which make write extension for immedidate search 
(like vim plugin Ctrlp Or Command-T) easily

*Written in python.
*provide several useful components
*easy to write extension

##Concepts:
There several Class in this packet:
* Candidate is a basic record for search, It's member name will be shown to user, and it's member content used for search
* Finder is used for select suite candidate from Candidates, it must provide query, getSuiteCandidate, getSuiteCandidateNum intereface
* Acceptor will be called when user select some candidate, it must provide intereface : accept

##How to write extension
###basic 
You just need provide candidates that will be searched
*see Finder.vim function findInCurrentBuffer for ref


##Attension:
* just use SharedFactory.getMatchController to get a controller

##current not stable, not ready for use.

