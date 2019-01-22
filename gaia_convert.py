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

# print(gaiadatasets)

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
GAIA_RADIAL_VELOCITY = GAIADATASETS.radial_velocity.dropna()

DISTANCE = 1.0 / GAIA_PAR * 1000

# print(lengte_breedte)
# merge = pd.DataFrame({'ra': GAIA_RA, 'dec': GAIA_DEC})
print(DESIGNATION)


def brightness():
    ''' Berekent helderheid ster '''

    # print(gaia_par)
    # print(DISTANCE)
    # distance modulus omrekenen
    # reminder t = 10 ** 4

    # Absolute Magnitude
    absolute_magnitude = GAIA_PHOT_G_MEAN_MAG - 5 * \
        np.log10((DISTANCE / (3.08567758149137 * 10 ** 16) / 10))
    # Hier wordt bekeken hoeveel rijen geen data hebben.
    # absmag_columns = ['designation', 'abs_mag_conv']
    #stops = pd.DataFrame(data, columns=absmag_columns)
    abs_empty_value = pd.DataFrame(
        {'aantal_lege_magnitudes': absolute_magnitude})
    print(abs_empty_value.isnull().sum().sum())

    # NaN wordt uit de lijst gehaald.
    absolute = absolute_magnitude.dropna()

    # Star uuid converted to unsigned int64
    # STAR_ID = np.uint64(DESIGNATION.split()[-1])
    # abs_data = pd.DataFrame(
    #     {'designation': STAR_ID, 'sterBright': absolute})
    # # De helderheid van de sterren worden geformatteerd in een decimaal
    # absolute_data = abs_data.dropna()
    # print(absolute_data)

    # en file wegschrijven naar JSON
    absolute_data.to_json("data/abs_magnitude.json", orient="records")


def convert_xyz():
    ''' Converts Gaia data to XYZ values '''

    # star_position = (ra, dec, distance)
    star_pos_x = np.float64(DISTANCE * np.cos(GAIA_RA) * np.sin(GAIA_DEC))
    star_pos_y = np.float64(DISTANCE * np.cos(GAIA_DEC))
    star_pos_z = np.float64(DISTANCE * np.sin(GAIA_RA) * np.sin(GAIA_DEC))

    # Star uuid converted to unsigned int64
    STAR_ID = np.uint64(DESIGNATION.split()[-1])
    print(STAR_ID)

    star_pos = pd.DataFrame({'designation': STAR_ID, 'starX': star_pos_x,
                             'starY': star_pos_y, 'starZ': star_pos_z})

    star_pos.to_json("data/sterXYZ.json", orient="records")

    # end xyz
    # G = whitelight, GBp = blue, and GRp = red


def calculate_velocity():
    """ Calculate velocity """
    pass


brightness()
convert_xyz()
