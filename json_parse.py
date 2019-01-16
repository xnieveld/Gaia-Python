#!/usr/bin/python3
# s4s gaia convert script by MrX
import io
import ijson
import sys
import pandas as pd
import numpy as np
print("Gaia Python JSON parsing script")
# print("Arguments passed were: ", str(sys.argv))

if(len(sys.argv) <= 2):
    print("Not enough argments given, expected <file input> <outputfile>")
    exit()

#filename = "gaia-dataset.json"
#filename_out = "gaia-dataset-out.json"
filename = sys.argv[1]
filename_out = sys.argv[2]

print("starting script")
def parse_float(x):
    try:
        x = float(x)
    except Exception:
        x = 0
    return x

def parse():
    data = []
    good_columns = ['designation', 'ra', 'dec', 'parallax', 'pmra', 'pmdec', 'astrometric_pseudo_colour', 'phot_g_mean_mag']
    column_names = good_columns
    print("file open")
    with open(filename, encoding="UTF-8") as json_file:
        objects = ijson.items(json_file, 'data.item')
        for row in objects:
            selected_row = []
            for item in good_columns:
                selected_row.append(row[column_names.index(item)])
            data.append(selected_row)
    print("file read done")
#    print(data[0])
    print("start reading stops")

    stops = pd.DataFrame(data, columns=good_columns)
    print("finish reading stops")
    stops["designation"].value_counts()
    # print(stops["designation"].value_counts())

    print("starting float apply to phot_g_mean_mag")
    stops["phot_g_mean_mag"] = stops["phot_g_mean_mag"].apply(parse_float)
    print("finish float apply to phot_g_mean_mag")

    print("starting to_json")
    output = stops.to_json(filename_out, orient='records')
    print("done with json output, yay!")
parse();