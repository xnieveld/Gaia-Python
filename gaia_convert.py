''' Gaia dataset conversion script '''
# [
#   {
#     "designation": starname,
#     "x": x coordinate,
#     "y": y coordinate,
#     "z": z coordinate,
#     "brightness": brightness,
#     "r":  red (rgb) value,
#     "g":  green (rgb) value,
#     "b":  blue (rgb) value
#   }
# ]

from sys import argv
import random
from pandas import read_csv, DataFrame
from numpy import uint64, float64, log, log10, sin, cos

if len(argv) <= 2:
    print("Not enough argments given, expected <input.csv> <output.json>")
    exit()

FILENAME = argv[1]
FILENAME_OUT = argv[2]
print("Opening file…")

# Read csv and drop rows with missing data
GAIA_DATA = read_csv(FILENAME).dropna()

print("Calculating distance…")
# Calculate distance cheap - No more use of tan for better performance
DISTANCE = abs(1.0 / GAIA_DATA.parallax * 1000.0)

# Star uuid converted to unsigned int64
STAR_DESIGNATION = [uint64(id.split()[-1]) for id in GAIA_DATA.designation]


def calculate_brightness():
    ''' Calculate the absolute magnitude based on the GBand mean magnitude '''

    # The abs magnitude is increased with distance.
    # Star uuid converted to unsigned int64
    abs_data = DataFrame({'designation': STAR_DESIGNATION, 'brightness': (
        GAIA_DATA.phot_g_mean_mag - 5.0 * log10(DISTANCE / 10.0))})
    abs_data.to_json("data/ABS_MAGNITUDE.json", orient="records")


def calculate_position():
    ''' Converts Equatorial coords to cartesian coords  '''

    # star_position = (ra, dec, distance)
    star_x = float64(DISTANCE * cos(GAIA_DATA.ra) * sin(GAIA_DATA.dec))
    star_y = float64(DISTANCE * cos(GAIA_DATA.dec))
    star_z = float64(DISTANCE * sin(GAIA_DATA.ra) * sin(GAIA_DATA.dec))

    position = DataFrame({'designation': STAR_DESIGNATION,
                          'x': star_x, 'y': star_y, 'z': star_z})
    position.to_json(FILENAME_OUT, orient="records")


def calculate_velocity():
    ''' Calculate velocity '''
    print("//TODO: not built yet")


def calculate_temp(absolute_mag):
    ''' Estimates temperature from absolute magnitude '''
    # absolute_mag = float
    temp = float(0)
    # print(absolute_mag)
    if absolute_mag > 15:
        temp = 2000
    elif absolute_mag > 10:
        temp = random.uniform(2000, 4000)
    elif absolute_mag > 6:
        temp = random.uniform(3000, 5000)
    elif absolute_mag > 4:
        temp = random.uniform(4500, 6500)
        if random.uniform(0, 1) < 0.1:
            temp = 3000
    elif absolute_mag > 2:
        temp = random.uniform(6000, 10000)
        if random.uniform(0, 1) < 0.1:
            temp = random.uniform(3000, 6000)

    elif absolute_mag > -1:
        temp = random.uniform(10000, 20000)
        if random.uniform(0, 1) < 0.5:
            temp = random.uniform(3500, 6500)
    else:
        temp = random.uniform(20000, 40000)
        if random.uniform(0, 1) < 0.3:
            temp = random.uniform(6000, 12000)
    return temp

COLOUR_R = []
COLOUR_G = []
COLOUR_B = []


def calculate_colour(star_temperature):
    ''' Calculate an RGB colour from a given temperature
        t = Temperature in Kelvin between 1000 and 40000
        returns: RGB Aproximate equivalent
        Currently estimated, Gaia has actual color data '''

    calc_colour_r = 0.0
    calc_colour_g = 0.0
    calc_colour_b = 0.0

    # restrict temperature to 1000 - 40000
    temperature_clamped = float(max(min(star_temperature, 40000), 1000))

    # check individual colour intensity
    temperature_clamped /= 100
    if temperature_clamped <= 66:
        calc_colour_r = 255
        calc_colour_g = float(max(min(float(
            99.4709025861) * log(temperature_clamped) - float(161.1195681661), 255), 0))
        if temperature_clamped > 19:
            calc_colour_b = float(max(min(float(
                138.5177312231) * log(temperature_clamped - 10) - float(305.0447927307), 255), 0))
    else:
        calc_colour_r = float(max(min(float(
            329.698727446) * (temperature_clamped - 60) ** float(-0.1332047592), 255), 0))
        calc_colour_g = float(max(min(float(
            288.1221695283) * (temperature_clamped - 60) ** float(-0.0755148492), 255), 0))
        calc_colour_b = 255

    # divide by 255 for rgb
    calc_colour_r /= 255
    calc_colour_g /= 255
    calc_colour_b /= 255
    # print("COLOUR_R: %s, COLOUR_G: %s, COLOUR_B: %s" % (COLOUR_R, COLOUR_G, COLOUR_B))
    # print("input: %s" % t)
    # print("COLOUR_R: %s, COLOUR_G: %s, COLOUR_B: %s" % (len(COLOUR_R), len(COLOUR_G), len(COLOUR_B)))

    # append individual r/g/b colours to R/G/B array
    COLOUR_R.append(calc_colour_r)
    COLOUR_G.append(calc_colour_g)
    COLOUR_B.append(calc_colour_b)
    # return colour

ABS_MAGNITUDE = GAIA_DATA.phot_g_mean_mag - 5.0 * log10(DISTANCE / 10.0)
ABSMAG_BRIGHT = [calculate_temp(bright) for bright in ABS_MAGNITUDE]
# [calculate_colour(x) for x in absmag_bright[:10]]
print("Calculating colour…")
for x in ABSMAG_BRIGHT:
    calculate_colour(x)


def calculate_all():
    ''' Run all scripts, including the previous position and brightness '''

    print("Calculating XYZ…")
    star_x = float64(DISTANCE * cos(GAIA_DATA.ra) * sin(GAIA_DATA.dec))
    star_y = float64(DISTANCE * cos(GAIA_DATA.dec))
    star_z = float64(DISTANCE * sin(GAIA_DATA.ra) * sin(GAIA_DATA.dec))

    print("Outputting to DataFrame…")
    position = DataFrame({'d': STAR_DESIGNATION, 'x': star_x, 'y': star_y, 'z': star_z,
                          'm': ABS_MAGNITUDE, 'r': COLOUR_R, 'g': COLOUR_G, 'b': COLOUR_B})
    # position2 = DataFrame('count': position.count(level="STAR_DESIGNATION")
    # print(position.groupby("STAR_DESIGNATION").count())
    print("Writing output JSON to file…")
    position.to_json(FILENAME_OUT, orient="records")
    print("Prepending and appending JSON to make to make it compatible with Unity…")
    # Unity likes a named JSON block
    with open(FILENAME_OUT, 'r') as original:
        data = original.read()
    with open(FILENAME_OUT, 'w') as modified:
        modified.write('{"data":' + data + '}')
    print("Done.")

# calculate_brightness()
# calculate_position()
calculate_all()
