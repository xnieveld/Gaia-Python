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

# Hoek omrekenen
TAN = (GAIA_PAR / 1000 / 60 / 60 / 180)
RAW_D = (2 * 1.511 * 10 ** 11) / np.tan(TAN * math.pi)

# print(lengte_breedte)
# merge = pd.DataFrame({'ra': GAIA_RA, 'dec': GAIA_DEC})

def brightness():
    ''' Berekent helderheid ster '''

    # print(gaia_par)
    # print(RAW_D)
    # distance modulus omrekenen
    # reminder t = 10 ** 4

    # Absolute Magnitude
    absolute_magnitude = GAIA_PHOT_G_MEAN_MAG - 5 * \
    np.log10((RAW_D / (3.08567758149137 * 10 ** 16) / 10))
    # Hier wordt bekeken hoeveel rijen geen data hebben.
    # absmag_columns = ['designation', 'abs_mag_conv']
    #stops = pd.DataFrame(data, columns=absmag_columns)
    abs_empty_value = pd.DataFrame({'aantal_lege_magnitudes': absolute_magnitude})
    print(abs_empty_value.isnull().sum().sum())

    # NaN wordt uit de lijst gehaald.
    absolute = absolute_magnitude.dropna()
    abs_data = pd.DataFrame({'designation': DESIGNATION, 'sterBright': absolute})
    # De helderheid van de sterren worden geformatteerd in een decimaal
    absolute_data = (abs_data.round({'designation': 0, 'sterBright': 1})).dropna()
    print(absolute_data)

    # en file wegschrijven naar JSON
    absolute_data.to_json("data/abs_magnitude.json", orient="records")

def convert_xyz():
    ''' Converts Gaia data to XYZ values '''
    polar_x = GAIA_RA
    polar_y = GAIA_DEC
    polar_z = RAW_D

    gaia_x = np.cos(polar_x) * np.sin(polar_y)
    gaia_y = np.cos(polar_y)
    gaia_z = np.sin(polar_x) * np.sin(polar_y)

    cartesian = (gaia_x * polar_z + gaia_y * polar_z + gaia_z * polar_z)
    # center = 0.0
    cart_nan = (cartesian + 0.0).dropna()

    cartesian = pd.DataFrame({'cartesian': cart_nan}).round(1)
    print(cartesian)

    cartesian.to_json("data/Cartesian.json", orient="records")

    var_ra = GAIA_RA.round(1)
    dec = GAIA_DEC.round(1)
    distance = RAW_D

    distance = distance.round(1)
    print(distance)

    # star_position = (ra, dec, distance)

    ster_pos_x = np.cos(var_ra) * np.sin(dec)
    ster_pos_y = np.cos(dec)
    ster_pos_z = np.sin(var_ra) * np.sin(dec)

    ster_pos_x = ster_pos_x.round(2)
    print(ster_pos_x)

    ster_pos_y = ster_pos_y.round(2)
    print(ster_pos_y)

    ster_pos_z = ster_pos_z.round(2)
    print(ster_pos_z)

    sterpositie = pd.DataFrame({'designation': DESIGNATION, 'sterX': ster_pos_x,
                                'sterY': ster_pos_y, 'sterZ': ster_pos_z})
    print(sterpositie)

    sterpositie.to_json("data/sterXYZ.json", orient="records")

    ster_positie = (ster_pos_x * distance + ster_pos_y *
                    distance + ster_pos_z * distance)

    gaia_ster_a = ster_positie.round(1)
    print(gaia_ster_a)

    velocity_x = np.cos(GAIA_PMRA + var_ra) + np.sin(GAIA_PMDEC + dec)
    velocity_y = np.cos(GAIA_PMDEC + dec)
    velocity_z = np.sin(GAIA_PMRA + var_ra) * np.sin(GAIA_PMDEC + dec)
    velocity = (velocity_x * (distance + GAIA_RADIAL_VELOCITY) + velocity_y *
                (distance + GAIA_RADIAL_VELOCITY) + velocity_z * (distance + GAIA_RADIAL_VELOCITY))

    gaia_ster_b = ster_positie + velocity

    velocity = (gaia_ster_b - gaia_ster_a)

    # velocity_column = ['Velocity': velocity]
    velocity = velocity.dropna()
    velocity = pd.DataFrame({'velocity': velocity})
    velocity = velocity.astype('double')
    print(velocity)
    # end xyz
    # G = whitelight, GBp = blue, and GRp = red

brightness()
convert_xyz()