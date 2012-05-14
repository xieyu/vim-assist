import re
import VimUtils
def containCompare(content, pattern):
	return pattern in content

def containIgnoreCaseCompare(content, pattern):
	return pattern.lower() in content.lower()

def regualarCompare(content, pattern, options=None):
	try:
		# FIXME:code is little ugly here
		if options:
			pattern = re.compile(pattern, options)
		else:
			pattern = re.compile(pattern)
		return pattern.match(content)
	except:
		# FIXME:does vim has exit function ?
		VimUtils.error("invalidate regual pattern!")
		return False

	
def fuzzyCompare(content, pattern):
	index = 0
	for ch in pattern:
		index = content.find(ch, index, -1)
		if index == -1:
			return False
	return True

def regualarIgnoreCaseCompare(content, pattern):
	return regualarCompare(content, pattern, re.IGNORECASE)

def fuzzyIgnoreCaseCompare(content, pattern):
	return fuzzyCompare(content.lower(), pattern.lower())
	

