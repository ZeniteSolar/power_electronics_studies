import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, exp


def Io_min(Vi, D, fsw, L, R, E):
    e1 = (1 - exp( D / (fsw * L / R) ))
    e2 = (1 - exp( 1 / (fsw * L / R) ))

    Io_min = ((Vi / R) * (e1 / e2)) - (E / R)
    return Io_min


def Io_max(Vi, D, fsw, L, R, E):
    e1 = (1 - exp( - D / (fsw * L / R) ))
    e2 = (1 - exp( - 1 / (fsw * L / R) ))

    Io_max = ((Vi / R) * (e1 / e2)) - (E / R)
    return Io_max



# Converter
fsw = 12.55e3
T = 1/12.55e3
D = 0.5
Vi = 22.1
Io = 98
Vo = D * Vi
Ii = Io / D
Po = Vo * Io
Pi = Vi * Ii

Vdriver = 15


# Motor no teste
# Ea = kv * wa
Ra = 35e-3
La = 23e-6
Ea = Vo - (Io * Ra)
kv = 0.0107  # RPM / V
wa = Ea / kv


Io_min = Io_min(Vi, D, fsw, La, Ra, Ea)
Io_max = Io_max(Vi, D, fsw, La, Ra, Ea)


# Mosfet
tr = 355e-9
tf = 350e-9
td_on = 500e-9
td_off = 360e-9
Rds_on = 2.3e-3 * 1.6 * 2.35
Vgs_th = 4.5


# Time
samples = 10000
periods = 1
t = np.linspace(start=0, stop=T*periods, num=samples*periods, endpoint=False)

ton = D * T
toff = (1 - D) * T


def generate_Vgs(t):

    # initial time 
    t0 = int(samples) // 4

    dVds_dt = (0.9 - 0.1) * Vds / tvr
    dVid_dt = (0.9 - 0.1) * Id / tir

    # time at Vgs_th (threshold)
    t1 = t0 + 0

    # time at Vgs_p (plateau)
    # time of end of charge Qgs
    t2 = t0 + 0

    # time of end of charge Qgd
    t3 = t0 + 0

    # time at full Vgs
    t4 = t0 + 0



    sVgs = np.zeros(samples)
    on = waveform_start_delay
    off = on + int(D * samples)
    sVgs[on:off] = Vdriver

    a = on
    b = a + int( samples * td_on / T )
    sVgs[a:b] = np.linspace(start=0, stop=Vdriver, num=b-a, endpoint=False)

    sVgs = np.tile(sVgs, periods)
    return sVgs


def generate_Vds(t):
    return t


sVgs = generate_Vgs(t)
sVds = generate_Vds(t)


plt.figure()
plt.plot(t, sVgs)
plt.plot(t, sVds)
plt.show()
