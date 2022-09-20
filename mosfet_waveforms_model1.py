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
Ii = Io * D
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


# Time
samples = 10000
periods = 1
t = np.linspace(start=0, stop=T*periods, num=samples*periods, endpoint=False)


# Vi, Ii
sVi = Vi * np.ones(samples * periods)
sIi = Ii * np.ones(samples * periods)
# plt.figure(); plt.plot(t, sVi); plt.plot(t, sIi); plt.show();


# Vgs
waveform_start_delay = int(samples) // 4
ton = D * T
toff = (1 - D) * T
sVgs = np.zeros(samples)
on = waveform_start_delay
off = on + int(D * samples)
sVgs[on:off] = Vdriver
sVgs = np.tile(sVgs, periods)


# Io
sIo = np.zeros(samples)
a = on
b = off
sIo[a:b] = np.linspace(start=Io_min, stop=Io_max, num=b-a, endpoint=False)
s = np.linspace(start=Io_max, stop=Io_min, num=b-a, endpoint=False)
sIo[b:] = s[:a]
sIo[:a] = s[a:]
del s
sIo = np.tile(sIo, periods)


# From diode or in case of synchronous, from body diode:
Qrr = 500e-9
trr = 100e-9
Ifrr_peak = 2 * Qrr / trr


# Id
# sId = np.zeros(samples)
sId = sIo.copy()
a = on
b = a + int(samples * (tr + td_on) / T)
sId[a:b] = np.linspace(start=0, stop=sIo[b], num=b-a, endpoint=False)
sId[:a] = 0
c = b + int(samples * (trr / T) // 2)
d = b + int(samples * (trr / T))
sId[b:c] = np.linspace(start=sIo[b], stop=(sIo[c]+Ifrr_peak), num=c-b, endpoint=False)
sId[c:d] = np.linspace(start=(sIo[c]+Ifrr_peak), stop=sIo[d], num=d-c, endpoint=False)
a = off + int(samples * tr / T)
b = a + int(samples * (tf + td_off) / T)
sId[a:b] = np.linspace(start=sIo[a], stop=0, num=b-a, endpoint=False)
sId[b:] = 0
sId = np.tile(sId, periods)


# Vds
sVds = np.ones(samples) * Rds_on * sId[:samples]
a = on + int(samples * (td_on + tr) / T)
b = a + int(samples * tr / T)
sVds[:a] = Vi
sVds[a:b] = np.linspace(start=Vi, stop=Rds_on * Io, num=b-a, endpoint=False)
a = off
b = a + int(samples * tf / T)
sVds[a:] = Vi
sVds[a:b] = np.linspace(start=Rds_on * Io, stop=Vi, num=b-a, endpoint=False)
sVds = np.tile(sVds, periods)


# Vds turnon Overshoot
Vds_peak = 52
turnon_overshoot_freq = 1e6
turnon_overshoot_time = 1/(turnon_overshoot_freq * 2)
turnon_overshoot = 1 + (Vds_peak/Vi)
sOvrs = np.ones(samples)
a = on + int(samples * tr / T)
b = a + int( samples * (turnon_overshoot_time / T) // 2)
c = a + int( samples * turnon_overshoot_time / T )
sOvrs[a:b] += np.linspace(start=0, stop=turnon_overshoot, num=b-a, endpoint=False)
sOvrs[b:c] += np.linspace(start=turnon_overshoot, stop=0, num=c-b, endpoint=False)


# Vds turnoff Overshoot
turnoff_overshoot_freq = 1e6
turnoff_overshoot_time = 1/(turnoff_overshoot_freq * 2)
turnoff_overshoot = 1 + (Vds_peak/Vi)
a = off
b = a + int( samples * (turnoff_overshoot_time / T) // 2)
c = a + int( samples * turnoff_overshoot_time / T )
sOvrs[a:b] += np.linspace(start=0, stop=turnoff_overshoot, num=b-a, endpoint=False)
sOvrs[b:c] += np.linspace(start=turnoff_overshoot, stop=0, num=c-b, endpoint=False)
sOvrs = np.tile(sOvrs, periods)


# Apply Vds overshoot
sVds = sVds * sOvrs


# Idd (diode current)
sIdd = sIo.copy()
a = on
b = off + int(samples * tr / T)
sIdd[a:b] = 0
a = on
b = a + int(samples * (tr + td_on) / T)
sIdd[a:b] = np.linspace(start=sIo[a], stop=0, num=b-a, endpoint=False)
a = off + int(samples * tr / T)
b = a + int(samples * (tf + td_off) / T)
sIdd[a:b] = np.linspace(start=0, stop=sIo[b], num=b-a, endpoint=False)
sIdd = np.tile(sIdd, periods)
# plt.figure(); plt.plot(t, sIdd); plt.show()


# Vdd (diode voltage)
# sVdd = np.zeros(samples)
# a = on + int(samples * (tr + td_on) / T)
# b = off
# sVdd[a:b] = Vi
# a = on + int(samples * (tr + td_on) / T)
# b = a + int(samples * tr / T)
# sVdd[a:b] = np.linspace(start=0, stop=Vi, num=b-a, endpoint=False)
# a = off
# b = a + int(samples * tf / T)
# sVdd[a:b] = np.linspace(start=Vi, stop=0, num=b-a, endpoint=False)
# sVdd = np.tile(sVdd, periods)
# plt.figure(); plt.plot(t, sVdd); plt.show()

sVdd = sVi - sVds


# Vo
sVo = sVdd.copy()


# Pt (total mosfet losses)
sPt = sId * sVds
Pt_avg = np.average(sPt)
print(f"Total mosfet loss: {Pt_avg} W")

sPi = sVi * sIi
Pi_avg = np.average(sPi)
print(f"Input power: {Pi_avg} W")

sPo = (sVo * sIo)
Po_avg = np.average(sPo)
print(f"Output power: {Po_avg} W")


# Plot
fig, ax = plt.subplots(nrows=6, ncols=1, sharex='col', squeeze=True, figsize=(10,10))
fig.suptitle('Simplified Mosfet Losses')
ax[0].plot(t, sVgs, label='Vgs(t)')
ax[0].legend()

color = 'tab:orange'
ax[1].set_xlabel('time [s]')
ax[1].set_ylabel('[V]', color=color)
ax[1].plot(t, sVds, label='Vds(t)', color=color)
ax[1].tick_params(axis='y', labelcolor=color)
axtwin = ax[1].twinx()
color = 'tab:blue'
axtwin.set_ylabel('[A]', color=color)
axtwin.plot(t, sId, label='Id(t)', color=color)
axtwin.plot(t, sIdd, label='Idd(t)', color='tab:green')
axtwin.tick_params(axis='y', labelcolor=color)
h1, l1 = ax[1].get_legend_handles_labels()
h2, l2 = axtwin.get_legend_handles_labels()
ax[1].legend(h1+h2, l1+l2, loc=2)

color = 'tab:orange'
ax[2].set_xlabel('time [s]')
ax[2].set_ylabel('[V]', color=color)
ax[2].plot(t, sVo, label='Vo(t)', color=color)
ax[2].tick_params(axis='y', labelcolor=color)
axtwin = ax[2].twinx()
color = 'tab:blue'
axtwin.set_ylabel('[A]', color=color)
axtwin.plot(t, sIo, label='Io(t)', color=color)
axtwin.tick_params(axis='y', labelcolor=color)
h1, l1 = ax[2].get_legend_handles_labels()
h2, l2 = axtwin.get_legend_handles_labels()
ax[2].legend(h1+h2, l1+l2, loc=2)

ax[3].plot(t, sPt, label='Pt(t)')
ax[3].plot(t, np.array([Pt_avg] * len(sPt)), label=f'Pt avg: {round(Pt_avg)} [W]')
ax[3].legend()

ax[4].plot(t, sVi, label=f'Vi(t)')
ax[4].plot(t, sVo, label=f'Vo(t)')
ax[4].legend()

ax[5].plot(t, sIo, label=f'Io(t)')
ax[5].plot(t, sIi, label=f'Ii(t)')
ax[5].legend()

plt.tight_layout()
plt.show()

fig.tight_layout()
plt.show()