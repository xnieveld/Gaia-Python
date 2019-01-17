# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 10:19:42 2018

@author: Mourad Nasser
"""
#import cartesian as cartesian
import pandas as pd
import matplotlib.pyplot as plt
import math as m
import numpy as np
import json as js
from collections import Counter

# Deze variabel importeert de CSV bestand van Gaia
gaiadatasets = pd.read_csv("data/data.csv")

# print(gaiadatasets)

# print(gaiadatasets[2:])
# Hier worden de columns van de datasets uitgeplukt
gaia_ra = gaiadatasets.ra
gaia_dec = gaiadatasets.dec
gaia_par = gaiadatasets.parallax
gaia_phot_g_mean_mag = gaiadatasets.phot_g_mean_mag
gaia_colour = gaiadatasets.astrometric_pseudo_colour


designation = gaiadatasets.designation



# print(lengte_breedte)
merge = pd.DataFrame({'ra': gaia_ra,
                      'dec': gaia_dec})

# Hoek omrekenen
pi = 3.14159
tan = (gaia_par / 1000 / 60 / 60 / 180)
d = (2 * 1.511 * 10 ** 11) / np.tan(tan * m.pi)
#print(gaia_par)
#print(d)

# distance modulus omrekenen

# reminder t = 10 ** 4


# Absolute Magnitude
Absolute_Magnitude = gaia_phot_g_mean_mag - 5 * np.log10((d / (3.08567758149137 * 10 ** 16) / 10))
# Hier wordt bekeken hoeveel rijen geen data hebben.
absmag_columns = ['designation', 'abs_mag_conv']
#stops = pd.DataFrame(data, columns=absmag_columns)
Abs_emptyValue = pd.DataFrame({'aantal_lege_magnitudes': Absolute_Magnitude})
print(Abs_emptyValue.isnull().sum().sum())

# NaN wordt uit de lijst gehaald.
absolute = Absolute_Magnitude.dropna()
abs_data = pd.DataFrame({'designation': designation, 'sterBright': absolute})
# De helderheid van de sterren worden geformatteerd in een decimaal
abs_data = abs_data.round({'designation': 0, 'sterBright': 1})
absolute_data = abs_data.dropna()
print(absolute_data)

outputfile_absmagnitude = "data/abs_magnitude.json"
Abs_magnitude = absolute_data.to_json(outputfile_absmagnitude, orient="records")
#print(Abs_magnitude)

# X Y Z
polar_x = gaia_ra
polar_y = gaia_dec
polar_z = d

X = np.cos(polar_x) * np.sin(polar_y)
Y = np.cos(polar_y)
Z = np.sin(polar_x) * np.sin(polar_y)

cartesian = (X * polar_z + Y * polar_z + Z * polar_z)
center = 0.0
cart = cartesian + center

cart = cart.dropna()

cartesian = pd.DataFrame({'cartesian': cart})
cartesian = cartesian.round(1)
print(cartesian)

outputfile_carts = "data/Cartesian.json"
carts = cartesian.to_json(outputfile_carts, orient="records")

ra = gaia_ra
ra = gaia_ra.round(1)
dec = gaia_dec
dec = gaia_dec.round(1)
distance = d
distance = distance.round(1)
print(distance)
pmra = gaiadatasets.pmra
pmdec = gaiadatasets.pmdec
Gaia_radial_velocity = gaiadatasets.radial_velocity
radial_velocity = Gaia_radial_velocity.dropna()
star_position = (ra, dec, distance)



ster_positx = np.cos(ra) * np.sin(dec)
ster_posity = np.cos(dec)
ster_positz = np.sin(ra) * np.sin(dec)


ster_positx = ster_positx.round(2)
print(ster_positx)

ster_posity = ster_posity.round(2)
print(ster_posity)


ster_positz = ster_positz.round(2)
print(ster_positz)


sterpositie = pd.DataFrame({'designation' : designation,'sterX' : ster_positx, 'sterY' : ster_posity, 'sterZ' : ster_positz})

print(sterpositie)

outputfile_ster = "data/sterXYZ.json"
sterpositie = sterpositie.to_json(outputfile_ster, orient="records")


ster_positie = (ster_positx * distance + ster_posity * distance + ster_positz * distance)

a = ster_positie
a = ster_positie.round(1)
print(a)

velocity_x = np.cos(pmra + ra) + np.sin(pmdec + dec)
velocity_y = np.cos(pmdec + dec)
velocity_z = np.sin(pmra + ra) * np.sin(pmdec + dec)
velocity = (velocity_x * (distance + radial_velocity) + velocity_y * (distance + radial_velocity) + velocity_z * (distance + radial_velocity))

b = ster_positie + velocity

velocity = (b - a)

# velocity_column = ['Velocity' velocity]
velocity = velocity.dropna()
velocity = pd.DataFrame({'velocity': velocity})
velocity = velocity.astype('double')
print(velocity)

# G = whitelight, GBp = blue, and GRp = red