#!/usr/bin/python3
# s4s gaia convert script by MrX
# script requirement: at least 8GB of RAM for the full 1m stars file
import io
import ijson
import sys

filename = sys.argv[1]
#filename = "gaia-3m-NaN.json"
#filename_temp = "gaia-3m-NaN-temp.json"
#filename_out = "gaia-3m-out.json"
filename_out = sys.argv[3]
outputfile_gaia = filename_out

print("starting script")
#def parse_json(json_filename):
#
#    with open(json_filename, 'rb') as input_file:
#        parser = ijson.parse(input_file)
#        
#        for prefix, event, value in data:
#    if event == 'string':
#        print(value)
#        for prefix, type, value in parser:
#            print('prefix={}, type={}, value={}'.format(prefix, type, value))
#            
#parse_json(sys.argv[1])
def parse_float(x):
    try:
        x = float(x)
    except Exception:
        x = 0
    return x

def parse():
#print("derp")
#println(filename)
    data = []
    good_columns = ['designation', 'ref_epoch', 'ra', 'ra_error', 'dec', 'dec_error', 'parallax', 'parallax_error', 'pmra', 'pmra_error', 'pmdec', 'pmdec_error', 'astrometric_pseudo_colour', 'astrometric_pseudo_colour_error', 'phot_g_mean_mag', 'radial_velocity', 'radial_velocity_error', 'l', 'b', 'ecl_lon', 'ecl_lat']
    column_names = good_columns

    # print(f 'moo')# print(good_columns)# print(f 'moo')
    print("file open")
    with open(filename, encoding="UTF-8") as json_file:
#    with open(filename, 'r') as json_file:
#        data = json.load(json_file)
#        for row in data['data']:
        #        for prefix, type, value in parser:
#            print('prefix={}, type={}, value={}'.format(prefix, type, value))
        objects = ijson.items(json_file, 'data.item')
        for row in objects:
            selected_row = []
            for item in good_columns:
                selected_row.append(row[column_names.index(item)])
            data.append(selected_row)
    print("file read done")
#    print(data[0])

    #def combine():
    import pandas as pd
    print("start reading stops")

    stops = pd.DataFrame(data, columns=good_columns)
    print("finish reading stops")

#    stops["designation"].value_counts()
    print(stops["designation"].value_counts())

    import numpy as np

    print("starting float apply to phot_g_mean_mag")
    stops["phot_g_mean_mag"] = stops["phot_g_mean_mag"].apply(parse_float)
    print("finish float apply to phot_g_mean_mag")
    #    output();

#def output():
#    print(stops)
    print("starting to_json")
    output = stops.to_json(outputfile_gaia, orient='records')
    print("done with json output, yay!")
#    print(output)
    
#
#userInput = input("Run:\n\n1 - Parse File\n2 - Combine\n3 - Output into JSON\nInput: ")
#try:
#    val = int(userInput)
#except ValueError:
#  print("That's not an int!")
#if (val == 1): parse();
#if (val == 2): combine();
#if (val == 3): output();
#parse();