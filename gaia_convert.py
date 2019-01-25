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
from pandas import read_csv, DataFrame
from numpy import uint64, float64, log10, sin, cos
import random

if len(argv) <= 2:
    print("Not enough argments given, expected <input.csv> <output.json>")
    exit()

FILENAME = argv[1]
FILENAME_OUT = argv[2]
print("file open")

# Read csv and drop rows with missing data
GAIA_DATA = read_csv(FILENAME).dropna()

print("calc dist")
# Calculate distance cheap - No more use of tan for better performance
distance = abs(1.0 / GAIA_DATA.parallax * 1000.0)

# Star uuid converted to unsigned int64
ids = [uint64(id.split()[-1]) for id in GAIA_DATA.designation]

def calculate_brightness():
    """ Calculate the absolute magnitude based on the GBand mean magnitude """

    # The abs magnitude is increased with distance
    ABS_MAGNITUDE = GAIA_DATA.phot_g_mean_mag - 5.0 * log10(distance / 10.0)

    # Star uuid converted to unsigned int64
    abs_data = DataFrame({'designation': ids, 'brightness': ABS_MAGNITUDE})
    abs_data.to_json("data/ABS_MAGNITUDE.json", orient="records")
def calculate_position():
    """ Converts Equatorial coords to cartesian coords  """

    # star_position = (ra, dec, distance)
    x = float64(distance * cos(GAIA_DATA.ra) * sin(GAIA_DATA.dec))
    y = float64(distance * cos(GAIA_DATA.dec))
    z = float64(distance * sin(GAIA_DATA.ra) * sin(GAIA_DATA.dec))

    position = DataFrame({'designation': ids, 'x': x, 'y': y, 'z': z})
    position.to_json(FILENAME_OUT, orient="records")
def calculate_velocity():
    """ Calculate velocity """
    pass
# def calculate_colour():
#     """ Calculate colour from dataset """
#     # G = whitelight, GBp = blue, and GRp = red
#     pass

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

COLOR_R = []
COLOR_G = []
COLOR_B = []

def calculate_color(t):
    ''' Calculate an RGB colour from a given temperature '''
    ''' t = Temperature in Kelvin between 1000 and 40000 '''
    ''' returns: RGB Aproximate equivalent '''
    from numpy import log
    # color = [0, 0, 0]

    mCOLOR_R  = 0.0
    mCOLOR_G  = 0.0
    mCOLOR_B  = 0.0
    
    temperature_clamped = float(max(min(t, 40000), 1000))
    # max(min(my_value, max_value), min_value)

    temperature_clamped /= 100
    if temperature_clamped <= 66:
        mCOLOR_R = 255
        mCOLOR_G = float(max(min(float(99.4709025861) * log(temperature_clamped) - float(161.1195681661), 255), 0))
        if temperature_clamped > 19:
            mCOLOR_B = float(max(min(float(138.5177312231) * log(temperature_clamped - 10) - float(305.0447927307), 255), 0))
    else:
        mCOLOR_R = float(max(min(float(329.698727446) * (temperature_clamped - 60) ** float(-0.1332047592), 255), 0))
        mCOLOR_G = float(max(min(float(288.1221695283) * (temperature_clamped - 60) ** float(-0.0755148492), 255), 0))
        mCOLOR_B = 255

    mCOLOR_R /= 255
    mCOLOR_G /= 255
    mCOLOR_B /= 255
    # print("COLOR_R: %s, COLOR_G: %s, COLOR_B: %s" % (COLOR_R, COLOR_G, COLOR_B))
    # print("input: %s" % t)
    # print("COLOR_R: %s, COLOR_G: %s, COLOR_B: %s" % (len(COLOR_R), len(COLOR_G), len(COLOR_B)))
    COLOR_R.append(mCOLOR_R)
    COLOR_G.append(mCOLOR_G)
    COLOR_B.append(mCOLOR_B)
    # return color

ABS_MAGNITUDE = GAIA_DATA.phot_g_mean_mag - 5.0 * log10(distance / 10.0)
absmag_bright = [calculate_temp(bright) for bright in ABS_MAGNITUDE]
print("printcolor")
# for color in absmag_bright[:10]:     calculate_color(color)
# colors = [calculate_color(color) for color in absmag_bright]
# [calculate_color(x) for x in absmag_bright[:10]]
print("start calculate color")
[calculate_color(x) for x in absmag_bright]
print("end calculate color")

def calculate_all():

    print("calc absmag start")
    print("calc absmag end")
    print("calc xyz start")
    x = float64(distance * cos(GAIA_DATA.ra) * sin(GAIA_DATA.dec))
    y = float64(distance * cos(GAIA_DATA.dec))
    z = float64(distance * sin(GAIA_DATA.ra) * sin(GAIA_DATA.dec))
    print("calc xyz end")
    print("final dataframe start")
    # print(ABS_MAGNITUDE)
    # print(absmag_bright)
    # print(colors)
    # print("colors1")
    # print(colors[0])
    # print((estimate_temperature(ABS_MAGNITUDE)[0]))
    # 'temperature': absmag_bright
    # print(posi.count(level="Person"))
    # print(COLOR_R)
    position = DataFrame({'d': ids, 'x': x, 'y': y, 'z': z,
                      'm': ABS_MAGNITUDE, 'r': COLOR_R, 'g': COLOR_G, 'b': COLOR_B})
    # position2 = DataFrame('count': position.count(level="ids")
    # print(position.groupby("d").count())
    print("final dataframe end")
    print("final json start")
    position.to_json(FILENAME_OUT, orient="records")
    print("final dataframe end")
    print("data tag start")
    with open(FILENAME_OUT, 'r') as original: data = original.read()
    with open(FILENAME_OUT, 'w') as modified: modified.write('{"data":' + data + '}')
    print("data tag end")

# calculate_brightness()
# calculate_position()
calculate_all()
