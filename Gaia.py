# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 10:19:42 2018

@author: Mourad
"""
import pandas as pd
import matplotlib.pyplot as plt

# Deze variabel importeert de CSV bestand van Gaia
gaiadatasets = pd.read_csv("data.csv")

print(gaiadatasets)
# Hier worden de columns van de datasets uitgeplukt
gaia_ra = gaiadatasets.ra
gaia_dec = gaiadatasets.dec
gaia_l = gaiadatasets.l
gaia_b = gaiadatasets.b

# De uitgeplukte columns worden gemerged
lengte_breedte = pd.DataFrame({'l': gaia_l,
                               'b': gaia_b})

# print(lengte_breedte)
merge = pd.DataFrame({'ra': gaia_ra,
                      'dec': gaia_dec})

# print(merge)
plt.plot(lengte_breedte)
plt.show()
