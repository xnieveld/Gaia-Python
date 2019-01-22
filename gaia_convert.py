# -*- coding: utf-8 -*-
"""
@author: Mourad Nasser
"""
#import cartesian as cartesian
import math
import pandas as pd
import numpy as np

# Deze variabel importeert de CSV bestand van Gaia
GAIADATASETS = pd.read_csv("data/data.csv")
GAIADATASETS = GAIADATASETS.dropna()

# print(gaiadatasets[2:])
''' Hier worden de columns van de datasets uitgeplukt '''
GAIA_RA = GAIADATASETS.ra
GAIA_DEC = GAIADATASETS.dec
GAIA_PAR = GAIADATASETS.parallax
GAIA_PHOT_G_MEAN_MAG = GAIADATASETS.phot_g_mean_mag
GAIA_COLOUR = GAIADATASETS.astrometric_pseudo_colour
DESIGNATION = GAIADATASETS.designation
GAIA_PMRA = GAIADATASETS.pmra
GAIA_PMDEC = GAIADATASETS.pmdec
GAIA_RADIAL_VELOCITY = GAIADATASETS.radial_velocity

# Calculate distance cheap - No more use of tan for better performance
DISTANCE = (1.0 / GAIA_PAR * 1000.0)

# Star uuid converted to unsigned int64
STAR_IDS = [np.uint64(id.split()[-1]) for id in DESIGNATION]


def brightness():
    """ Berekent helderheid ster """

    # Absolute Magnitude
    absolute_magnitude = np.float(GAIA_PHOT_G_MEAN_MAG - 5 *
                                  np.log10((abs(DISTANCE) / (3.08567758149137 * 10 ** 16) / 10)))

    # Star uuid converted to unsigned int64
    abs_data = pd.DataFrame(
        {'designation': STAR_IDS, 'brightness': absolute_magnitude})

    # en file wegschrijven naar JSON
    abs_data.to_json("data/abs_magnitude.json", orient="records")


def convert_xyz():
    ''' Converts Gaia data to XYZ values '''

    # star_position = (ra, dec, distance)
    star_pos_x = np.float64(DISTANCE * np.cos(GAIA_RA) * np.sin(GAIA_DEC))
    star_pos_y = np.float64(DISTANCE * np.cos(GAIA_DEC))
    star_pos_z = np.float64(DISTANCE * np.sin(GAIA_RA) * np.sin(GAIA_DEC))

    star_pos = pd.DataFrame({'designation': STAR_IDS, 'x': star_pos_x,
                             'y': star_pos_y, 'z': star_pos_z})

    star_pos.to_json("data/starXYZ.json", orient="records")


def calculate_velocity():
    """ Calculate velocity """
    pass


def calculate_colour():
    """ Calculate colour from dataset """
    # G = whitelight, GBp = blue, and GRp = red
    pass

brightness()
convert_xyz()
