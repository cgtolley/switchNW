from cmt_vna import VNA
import matplotlib.pyplot as plt
import numpy as np
from switch_network import SwitchNetwork
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

parser = ArgumentParser(description = "demo switching and vna measurements.", formatter_class = ArgumentDefaultsHelpFormatter)
parser.add_argument('--sernum', '-s', default='/dev/ttyACM0', help='port path')

args = parser.parse_args()

vna = VNA()

snw = SwitchNetwork(serport = args.serport)

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
