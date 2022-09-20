"""
This script is reproducing the an608a from Vishay:
https://www.vishay.com/docs/73217/an608a.pdf
"""

from math import log


# Mosfet parameters (max)
Vds_D = 16.5
Ids_D = 11
Rds_on_D = 2.15e-3
Vgs_th = 2.22
Vgs_p = 2.8
Ciss = 4320e-12  # at Vds_D
Qgd_D = 5e-9
Rgi = 2.5


# Circuit conditions (max)
Vds = 13.5
Vgs = 5.5
Ids = 16
Rg_ext = 360


# Calculations
Rg = Rgi + Rg_ext

# Equation 11:
t1 = Rg * Ciss * log(1 / (1 - (Vgs_th / Vgs)))

# Equation 17:
tir = Rg * Ciss * log( (Vgs - Vgs_th) / (Vgs - Vgs_p) )

# Equation 18:
tvf = Rg * (Qgd_D / Vds_D) * (Vds / (Vgs - Vgs_p))

# Equation 19:
tvr = Rg * (Qgd_D / Vds_D) * (Vds / Vgs_p)

# Equation 20:
tif = Rg * Ciss * log(Vgs_p / Vgs_th)

# Equation 21:
td_on = tir + t1

# Equation 22:
tr = tvf

# Equation 14 and 23:
td_off = Rg * Ciss * log(Vgs / Vgs_p)

# Equation 24:
tf = tvr

print(f'tir = {round(tir*1e9, 2)} ns, expected:', 755)
print(f'tvf = {round(tvf*1e9, 2)} ns, expected:', 549)
print(f'tvr = {round(tvr*1e9, 2)} ns, expected:', 530)
print(f'tif = {round(tif*1e9, 2)} ns, expected:', 1222)
print(f'td_on = {round(td_on*1e9, 2)} ns, expected:', 1555)
print(f'tr = {round(tr*1e9, 2)} ns, expected:', 549)
print(f'td_off = {round(td_off*1e9, 2)} ns, expected:', 1175)
print(f'tf = {round(tf*1e9, 2)} ns, expected:', 530)
print()

"""
Result: We fail to reproduce the results stated in the reference.
"""