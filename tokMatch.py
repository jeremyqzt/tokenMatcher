import os
import re
import optparse

#Dataclasses may not be available in earlier version of python...
class functionItem:
	def __init__(self, functionName, fileOrigin, functionDeclaration, lineNumber, regexMatched = False):
		self.functionName = functionName
		self.fileOrigin = fileOrigin
		self.functionDeclaration = functionDeclaration
		self.lineNumber = lineNumber
		self.regexMatched = regexMatched
	def __str__(self):
		return (("Function: %s, Line #: %d, file: %s") %(self.functionName, self.lineNumber, self.fileOrigin))

def generateCtags(path, debug = False):
	if (0 != os.system("ctags -x --c-types=f $(find " + path + " -name '*.c') > ctags.txt")):
		print("Failed to generate ctags file")
	filepath = 'ctags.txt'
	totalFuncs = 1
	functionsTable = {}

	with open(filepath) as fp:
		lines = fp.readlines()

		for line in lines:
			toHash = line.split()
			newEntry = functionItem(toHash[0], toHash[3], toHash[4], int(toHash[2]), False)
			functionsTable[toHash[0]] = newEntry
			line = fp.readline()
			totalFuncs += 1

	if debug:
		for index in functionsTable:
			print(functionsTable[index])
		print(("Parsed A Total of %d functions" % (totalFuncs)))

	return functionsTable

def walkDirectoryAndFiles(source, fileType):
	fs = []
	for root, dirnames, filenames in os.walk(source):
		for filename in filenames:
			if filename.endswith(fileType):
				fs.append(os.path.join(root, filename))
	return fs

def parseCode(functionsHashTable, tok, directory, fileType=".c", postSplit=1, debug = False,):
	allFilesToRead = walkDirectoryAndFiles(directory, fileType)
	if debug:
		print(allFilesToRead)

	matchedButUnrecognized = []
	for filepath in allFilesToRead:
		with open(filepath) as fp:
			lines = fp.readlines()
			for line in lines:
				if tok in line:
					splitLine = line.split()
					token = splitLine[postSplit].strip()
					if token in functionsHashTable:
						t = functionsHashTable[token]
						t.regexMatched = True
					else:
						matchedButUnrecognized.append(line)
	if debug:
		for i in matchedButUnrecognized:
			print ("Line %s found but did not find any matching function declaration" % (i))

def summarize(functionsHashTable):
	count = 0
	for function in functionsHashTable:
		obj = functionsHashTable[function]
		if (not obj.regexMatched):
			count += 1
			print("Did not find matching Token for %s" % (str(obj)))

	print("Total Missing: %d" % (count))

if __name__ == "__main__":
	parser = optparse.OptionParser(usage="%prog [options] path")
	parser.add_option("-r", "--token", dest="token",
		help="Token to match [default: %default]", default="*")
	parser.add_option("-p", "--pos", dest="pos",
		help="Position of important var [default: %default]", default=1)
	parser.add_option("-f", "--ftype", dest="type",
		help="Type of file to read [default: %default]", default=".c")

	opt, args = parser.parse_args()
	if len(args) != 1:
		parser.error("No path given")
		exit(-1)
	else:
		path = args[0]

	functionTable = generateCtags(path)
	parseCode(functionTable, opt.token, path, opt.type, opt.pos, False)
	summarize(functionTable)
