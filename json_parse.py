#!/usr/bin/python3
'''S4S Gaia JSON re-formatter script by MrX'''
import sys
import pandas as pd
import ijson
print("Gaia Python JSON parsing script")
# print("Arguments passed were: ", str(sys.argv))

if len(sys.argv) <= 2:
    print("Not enough argments given, expected <file input> <outputfile>")
    exit()

#FILENAME = "gaia-dataset.json"
#FILENAME_OUT = "gaia-dataset-out.json"
FILENAME = sys.argv[1]
FILENAME_OUT = sys.argv[2]

print("starting script")

def parse_float(possible_float):
    ''' Tries to parse floats from other values '''
    try:
        float(possible_float)
    except ValueError:
        print("Parsing of a possible float failed, not a float")

def parse():
    ''' Runs the parsing script'''
    data = []
    good_columns = ['designation', 'ra', 'dec', 'parallax', 'pmra',
                    'pmdec', 'astrometric_pseudo_colour', 'phot_g_mean_mag']
    column_names = good_columns
    print("file open")
    with open(FILENAME, encoding="UTF-8") as json_file:
        objects = ijson.items(json_file, 'data.item')
        for row in objects:
            selected_row = []
            for item in good_columns:
                selected_row.append(row[column_names.index(item)])
            data.append(selected_row)
    print("file read done")
    print("start reading stops")

    stops = pd.DataFrame(data, columns=good_columns)
    print("finish reading stops")
    stops["designation"].value_counts()
    # print(stops["designation"].value_counts())

    print("starting float apply to phot_g_mean_mag")
    stops["phot_g_mean_mag"] = stops["phot_g_mean_mag"].apply(parse_float)
    print("finish float apply to phot_g_mean_mag")

    print("starting to_json")
    stops.to_json(FILENAME_OUT, orient='records')
    print("done with json output, yay!")
parse()
