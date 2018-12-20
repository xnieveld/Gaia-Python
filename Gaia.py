# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 10:19:42 2018

@author: Mourad Nasser
"""
import cartesian as cartesian
import pandas as pd
import matplotlib.pyplot as plt
import math as m
import numpy as np
import json as js
from collections import Counter

# Deze variabel importeert de CSV bestand van Gaia
gaiadatasets = pd.read_csv("data.csv")

# print(gaiadatasets)

# print(gaiadatasets[2:])
# Hier worden de columns van de datasets uitgeplukt
gaia_ra = gaiadatasets.ra
gaia_dec = gaiadatasets.dec
gaia_l = gaiadatasets.l
gaia_b = gaiadatasets.b
gaia_par = gaiadatasets.parallax
Apparant_Magnitude = gaiadatasets.phot_g_mean_mag
gaia_colour = gaiadatasets.astrometric_pseudo_colour

#print(gaia_colour)
# De uitgeplukte columns worden gemerged
lengte_breedte = pd.DataFrame({'l': gaia_l,
                               'b': gaia_b})

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

Absolute_Magnitude = Apparant_Magnitude - 5 * np.log10((d / (3.08567758149137 * 10 ** 16) / 10))
# Hier wordt bekeken hoeveel rijen geen data hebben.
Abs_emptyValue = pd.DataFrame(Absolute_Magnitude)
print("Aantal lege: ")
print(Abs_emptyValue.isnull().sum().sum())

# NaN wordt uit de lijst gehaald.
absolute = Absolute_Magnitude.dropna()
print("Absolute Magnitude zonder legen values: ")
print(absolute)

Abs_magnitude = absolute.to_json(orient="index")
print(Abs_magnitude)

with open('abs_magintude.json', 'w') as outfile:
 js.dumps(Abs_magnitude)

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

print(cart)

carts = cart.to_json(orient="index")
with open('Cartesian.json', 'w') as outfile:
 js.dumps(carts)
# Vx Vy Vz

Vx = gaiadatasets.pmra
Vy = gaiadatasets.pmdec
Vz = gaiadatasets.radial_velocity
print(Vz)


vector_x = np.cos(Vx) * np.sin(Vy)
vector_y = np.cos(Vy)
vector_z = np.sin(Vx) * np.sin(Vy)

V = vector_x * Vz + vector_y * Vz + vector_z * Vz

vect_x = vector_x * Vz
vect_y = vector_y * Vz
vect_z = vector_z * Vz




# Astrometric psuedo colour
#νeff [µm−1] = 2.0 −1.8π/arctan + (0.331 + 0.572C − 0.014C^2 + 0.045C^3)
# C in nanometer omrekenen

C = ~340 - 910

veff = gaia_colour - 1.8/pi * np.arctan(0.331 + 0.572 + C - 0.014 + C ** 2 + 0.045 + C ** 3)

print(veff)