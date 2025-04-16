from cmt_vna import VNA
import matplotlib.pyplot as plt
import numpy as np
from switch_network import SwitchNetwork

vna = VNA()

snw = SwitchNetwork()

#just doing it manually, no for loops
freqs = vna.setup(npoints=100)

snw.switch('open')
open_std = vna.measure_S11()

snw.switch('short')
short_std = vna.measure_S11()

snw.switch('load')
load = vna.measure_S11()

snw.switch('antenna')
antenna = vna.measure_S11()

plt.ion()
fig, ax = plt.subplots(2,1, figsize=(8,8), sharex = True)

ax[0].plot(freqs, 20*np.log10(np.abs(short_std)), label='short')
ax[0].plot(freqs, 20*np.log10(np.abs(open_std)), label='open')
ax[0].plot(freqs, 20*np.log10(np.abs(load)), label='load')
ax[0].legend()

ax[1].plot(freqs, 20*np.log10(np.abs(antenna)))
ax[1].set_xlabel('Frequency [Hz]')

plt.show(block=True)
