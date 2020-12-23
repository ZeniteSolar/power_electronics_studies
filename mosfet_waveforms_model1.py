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
tr = 291e-9
tf = 595e-9
Rds_on = 2.3e-3 * 1.6 * 2.35
# Vf_av = 0.6
# If_av = Io


# Time
samples = 10000
periods = 3
t = np.linspace(start=0, stop=T*periods, num=samples*periods, endpoint=False)


# Vgs
ton = D * T
toff = (1 - D) * T
sVgs = np.zeros(len(t) // periods)
son = int(len(t) // periods)//4
soff = son + int(D * len(t) // periods)
sVgs[son:soff] = Vdriver
sVgs = np.tile(sVgs, periods)


# Io
sIo = np.zeros(len(t) // periods)
sIo[son:soff] = np.linspace(start=Io_min, stop=Io_max, num=soff-son, endpoint=False)
s = np.linspace(start=Io_max, stop=Io_min, num=soff-son, endpoint=False)
sIo[soff:] = s[:son]
sIo[:son] = s[son:]
del s
sIo = np.tile(sIo, periods)


# Id
sId = np.zeros(len(t) // periods)
sId[son:soff] = sIo[son:soff]
a = son
b = a + int(tr * fsw)
sId[a:b] = np.linspace(start=0, stop=Io, num=b-a, endpoint=False)
a = soff
b = a + int(tf * fsw)
sId[a:b] = np.linspace(start=Io, stop=0, num=b-a, endpoint=False)
sId = np.tile(sId, periods)


# Vds
sVds = np.ones(len(t) // periods) * Rds_on * sId[:len(t) // periods]
sVds[soff:] = Vi
sVds[:son] = Vi
a = son
b = a + int(tr * fsw)
sVds[a:b] = np.linspace(start=Vi, stop=Rds_on * Io, num=b-a, endpoint=False)
a = soff
b = a + int(tf * fsw)
sVds[a:b] = np.linspace(start=Rds_on * Io, stop=Vi, num=b-a, endpoint=False)
sVds = np.tile(sVds, periods)


# Pt
sPt = sId * sVds
Pt_avg = np.average(sPt)
print(f"Total mosfet loss: {Pt_avg} W")


# Plot
fig, ax = plt.subplots(nrows=4, ncols=1, sharex='col', squeeze=True, figsize=(10,5))
fig.suptitle('Simplified Mosfet Losses')
ax[0].plot(t, sVgs, label='Vgs(t)')
ax[0].legend()
ax[1].plot(t, sVds, label='Vds(t)')
ax[1].legend()
ax[2].plot(t, sId, label='Id(t)')
ax[2].plot(t, sIo, label='Io(t)')
ax[2].legend()
ax[3].plot(t, sPt, label='Pt(t)')
ax[3].plot(t, np.array([Pt_avg] * len(sPt)), label=f'Pt avg: {round(Pt_avg)} [W]')
ax[3].legend()
plt.tight_layout()
plt.show()

