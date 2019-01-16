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
Abs_emptyValue = pd.DataFrame(Absolute_Magnitude)
print("Aantal lege: ")
print(Abs_emptyValue.isnull().sum().sum())

# NaN wordt uit de lijst gehaald.
absolute = Absolute_Magnitude.dropna()
print("Absolute Magnitude zonder legen values: ")
print(absolute)

abs_data = pd.DataFrame({'designation': designation, 'sterBright': absolute})

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

cartesian = X * polar_z + Y * polar_z + Z * polar_z
center = 0.0
cart = cartesian + center

cart = cart.dropna()
print(cart)

outputfile_carts = "data/Cartesian.json"
carts = cart.to_json(outputfile_carts, orient="records")

ra = gaia_ra
dec = gaia_dec
distance = d
pmra = gaiadatasets.pmra
pmdec = gaiadatasets.pmdec
Gaia_radial_velocity = gaiadatasets.radial_velocity
radial_velocity = Gaia_radial_velocity.dropna()
star_position = (ra, dec, distance)
a = star_position


ster_posx = np.cos(ra) * np.sin(dec)
ster_posy = np.cos(dec)
ster_posz = np.sin(ra) * np.sin(dec)

ster_positie = ster_posx * distance + ster_posy * distance + ster_posz * distance

a = ster_positie

velocity_x = np.cos(pmra + ra) + np.sin(pmdec + dec)
velocity_y = np.cos(pmdec + dec)
velocity_z = np.sin(pmra + ra) * np.sin(pmdec + dec)
velocity = (velocity_x * (distance + radial_velocity ) + velocity_y * (distance + radial_velocity) + velocity_z * (distance + radial_velocity ))

b = ster_positie + velocity

Velocity = (b - a)

# velocity_column = ['Velocity' velocity]

velocity = Velocity.dropna()
print(velocity)

# Vx Vy Vz
Vx = gaiadatasets.pmra
Vy = gaiadatasets.pmdec
Vz = gaiadatasets.radial_velocity

vector_x = np.cos(Vx) * np.sin(Vy)
vector_y = np.cos(Vy)
vector_z = np.sin(Vx) * np.sin(Vy)

v = vector_x * Vz + vector_y * Vz + vector_z * Vz

#Vector NaN eruit gehaald
V = v.dropna()
print(V)

# Astrometric psuedo colour
#νeff [µm−1] = 2.0 −1.8π/arctan + (0.331 + 0.572C − 0.014C^2 + 0.045C^3)
# C in nanometer omrekenen

veff = gaia_colour - 1.8/pi * np.arctan(0.331 + 0.572 - 0.014 ** 2 + 0.045 ** 3)

print(veff)