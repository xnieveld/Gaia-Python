#!/usr/bin/python3
''' Script to replace empty values in Gaia JSON dataset with null '''
import os
import sys
import fileinput

FILENAME = sys.argv[1]
FILEPATHNAME = FILENAME.split(".json")[0]
FILENAME_SIMPLE = os.path.basename(FILENAME).split(".json")[0]
TEXT_TO_SEARCH = ',,'
REPLACEMENT_TEXT = ',null,'

def replace():
    ''' Replaces empty value with null '''
    with fileinput.FileInput(FILENAME, inplace=True, backup='-original.json') as file:
        for line in file:
            print(line.replace(TEXT_TO_SEARCH, REPLACEMENT_TEXT), end='')

    #dirty, run again to catch more
    with fileinput.FileInput(FILENAME, inplace=True, backup='-first.json') as file:
        for line in file:
            print(line.replace(TEXT_TO_SEARCH, REPLACEMENT_TEXT), end='')

    #dirty, run again to catch more
    with fileinput.FileInput(FILENAME, inplace=True, backup='-second.json') as file:
        for line in file:
            print(line.replace(',]', ',null]'), end='')

replace()

os.remove("%s.json" % FILEPATHNAME)
os.remove("%s.json-first.json" % FILEPATHNAME)
os.rename("%s.json-second.json" % FILEPATHNAME, "%s-parsed.json" % FILEPATHNAME)
os.rename("%s.json-original.json" % FILEPATHNAME, "%s.json" % FILEPATHNAME)
# gaia.json
# gaia.json-first.json
# gaia.json-second.json
# gaia.json-original.json
