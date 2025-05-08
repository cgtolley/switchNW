from switch_network import SwitchNetwork
import numpy as np

#PATHS = {
#            'VNAO'   : '1000000',
#            'VNAS'   : '1100000',
#            'VNAL'   : '0010000',
#            'VNAANT' : '0000010',
#            'VNAN'   : '0000011',
#            'VNARF'  : '0001100',
#            'RFN'    : '0000001',
#            'RFANT'  : '0000000'
#        }

#GPIOS = [2,7,1,6,3,0,4] 

snw = SwitchNetwork(serport='/dev/ttyACM0')
for key, inst in snw.paths.items():
    input(f'press Enter to proceed.')
    snw.switch(key, verbose=True)
