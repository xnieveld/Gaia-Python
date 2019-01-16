#!/usr/bin/python3
import sys
import fileinput

filename = sys.argv[1]
text_to_search = ',,'
replacement_text = ',null,'
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