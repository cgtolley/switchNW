import sys
from cmt_vna import VNA
import matplotlib.pyplot as plt
import numpy as np
from switch_network import SwitchNetwork
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from cmt_vna import calkit as cal
import time 

FSTART, FSTOP = 250E6, 1.8E9
#FSTART, FSTOP = 50E6, 250e6 

PATHS = {
            'load' : '010',
            'open' : '101',
            'antenna' : '000',
            'short': '100'
        }

GPIOS = [3,2,7]

SERPORT = '/dev/ttyACM0'

assert len(sys.argv) == 2
filename = sys.argv[-1]

vna = VNA()
snw = SwitchNetwork(serport = SERPORT, gpios = GPIOS, paths=PATHS)

#just doing it manually, no for loops
freqs = vna.setup(npoints=1000, fstart=FSTART, fstop=FSTOP)

snw.switch('short')
short_std = vna.measure_S11()

snw.switch('open')
open_std = vna.measure_S11()

snw.switch('load')
load = vna.measure_S11()

snw.switch('antenna')
antenna = vna.measure_S11()

kit = cal.S911T(freq_Hz = freqs)
vna_stds = np.vstack([open_std, short_std, load])
sparams = {'vna': kit.sparams(stds_meas = vna_stds)}
antenna_cal = cal.calibrate(gammas=np.array([antenna]), sprms_dict=sparams)
np.savez(filename, freqs=freqs, antenna=antenna_cal)

plt.ion()
fig, ax = plt.subplots(2,1, figsize=(8,8), sharex = True)

ax[0].plot(freqs/1e6, 20*np.log10(np.abs(short_std)), label='short')
ax[0].plot(freqs/1e6, 20*np.log10(np.abs(open_std)), label='open')
ax[0].plot(freqs/1e6, 20*np.log10(np.abs(load)), label='load')
ax[0].legend()

ax[1].plot(freqs/1e6, 20*np.log10(np.abs(antenna_cal[0])))
ax[1].set_xlabel('Frequency [MHz]')

plt.show(block=True)
