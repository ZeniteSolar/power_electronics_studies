"""
Switching Regulator IC Series - Calculation of Power Loss (Synchronous):

https://d1d2qsbl8m0m72.cloudfront.net/en/products/databook/applinote/ic/power/switching_regulator/power_loss_appli-e.pdf

"""


# Parameters
Vin = 12
Vo = 5
Io = 3
Ron_H = 100e-3
Ron_L = 70e-3
fsw = 2E6
tr = 4e-9
tf = 6e-9
Vd = 0.5
tdr = 30e-9
tdf = 30e-9
Qg_H = 1e-9
Qg_L = 1e-9
Cg_H = 200e-12
Cg_L = 200e-12
Vgs = 5
Icc = 1e-3


# Equation 1
Pon_H = (Io**2) * Ron_H * (Vo / Vin)
Pon_L = (Io**2) * Ron_L * (1 -Vo / Vin)

Psw_H = 0.5 * Vin * Io * (tr + tf) * fsw

Pd = Vd * Io * (tdr + tdf) * fsw

Pg = (Qg_H + Qg_L) * Vgs * fsw
Pg_alt = (Cg_H + Cg_L) * Vgs**2 * fsw

Pic = Vin * Icc

Pt = Pon_H = Pon_L + Psw_H + Pd + Pg + Pic

print(f'Pon_H : {round(Pon_H*1e3, 2)} mW, expected:', 375)
print(f'Pon_L : {round(Pon_L*1e3, 2)} mW, expected:', 367.5)
print(f'Psw_H : {round(Psw_H*1e3, 2)} mW, expected:', 360)
print(f'Pd : {round(Pd*1e3, 2)} mW, expected:', 180)
print(f'Pg : {round(Pg*1e3, 2)} mW, expected:', 20)
print(f'Pg_alt : {round(Pg_alt*1e3, 2)} mW, expected:', 20)
print(f'Pic : {round(Pic*1e3, 2)} mW, expected:', 12)
print(f'Pt : {round(Pt, 2)} W, expected:', 1.31)