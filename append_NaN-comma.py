#!/usr/bin/python3
import os
import sys
import fileinput

filename = sys.argv[1]
filepathname = filename.split(".json")[0]
filename_simple = os.path.basename(filename).split(".json")[0]
text_to_search = ',,'
replacement_text = ',null,'

def replace():
	with fileinput.FileInput(filename, inplace=True, backup='-original.json') as file:
		for line in file:
			print(line.replace(text_to_search, replacement_text), end='')

	#dirty, run again to catch more
	with fileinput.FileInput(filename, inplace=True, backup='-first.json') as file:
		for line in file:
			print(line.replace(text_to_search, replacement_text), end='')

	#dirty, run again to catch more
	with fileinput.FileInput(filename, inplace=True, backup='-second.json') as file:
		for line in file:
			print(line.replace(',]', ',null]'), end='')

replace();

os.remove("%s.json" % filepathname)
os.remove("%s.json-first.json" % filepathname)
os.rename("%s.json-second.json" % filepathname, "%s-parsed.json" % filepathname)
os.rename("%s.json-original.json" % filepathname, "%s.json" % filepathname)
# gaia.json
# gaia.json-first.json
# gaia.json-second.json
# gaia.json-original.json