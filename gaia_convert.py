# -*- coding: utf-8 -*-
"""
@author: Mourad Nasser
"""

from pandas import read_csv, DataFrame
from numpy import uint64, float64, log10, sin, cos

# Read csv and drop rows with missing data
gaia_data = read_csv("data/data.csv").dropna()

# Calculate distance cheap - No more use of tan for better performance
distance = abs(1.0 / gaia_data.parallax * 1000.0)

# Star uuid converted to unsigned int64
ids = [uint64(id.split()[-1]) for id in gaia_data.designation]


def calculate_brightness():
    """ Calculate the absolute magnitude based on the GBand mean magnitude """

    # The abs magnitude is increased with distance
    abs_magnitude = gaia_data.phot_g_mean_mag - 5.0 * log10(distance / 10.0)

    # Star uuid converted to unsigned int64
    abs_data = DataFrame({'designation': ids, 'brightness': abs_magnitude})
    abs_data.to_json("data/abs_magnitude.json", orient="records")


def calculate_position():
    """ Converts Equatorial coords to cartesian coords  """

    # star_position = (ra, dec, distance)
    x = float64(distance * cos(gaia_data.ra) * sin(gaia_data.dec))
    y = float64(distance * cos(gaia_data.dec))
    z = float64(distance * sin(gaia_data.ra) * sin(gaia_data.dec))

    position = DataFrame({'designation': ids, 'x': x, 'y': y, 'z': z})
    position.to_json("data/starXYZ.json", orient="records")


def calculate_velocity():
    """ Calculate velocity """
    pass


def calculate_colour():
    """ Calculate colour from dataset """
    # G = whitelight, GBp = blue, and GRp = red
    pass

calculate_brightness()
calculate_position()
