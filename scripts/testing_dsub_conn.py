from switch_network import SwitchNetwork
import numpy as np

PATHS = {
            'one' : '100',
            'two' : '010',
            'three' : '001',
            'all' : '111',
            'none' : '000'
        }

GPIOS = [3,2,4]

snw = SwitchNetwork(serport='/dev/ttyACM0', gpios=GPIOS, paths=PATHS)
input(snw.state)
for key, inst in PATHS.items():
    input(f'switching to {key}. press Enter to proceed.')
    snw.switch(key, verbose=True)
