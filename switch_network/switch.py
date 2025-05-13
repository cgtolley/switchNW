import numpy as np
import warnings
import time
import serial

'''The SwitchNetwork class sends commands to the pico connected to the serport. 

Hard-coded variables: 
PATHS dictionary. The keys start with where the path starts: either RF (port connected to LNA) or VNA (port connected to the VNA), and end with the end of the path - ANT (antenna), O, S, L (OSL standards), or N (noise source).
GPIOS list. gpio pin numbers - the index of the pin should correspond to the index of the state it should be in for each path in PATHS.
''' 
PATHS = {
            'VNAO'   : '1000000',
            'VNAS'   : '1100000',
            'VNAL'   : '0010000',
            'VNAANT' : '0000010',
            'VNAN'   : '0000011',
            'VNARF'  : '0001100',
            'RFN'    : '0000001',
            'RFANT'  : '0000000'
        }

GPIOS = [2,7,1,6,3,0,4]

class SwitchNetwork:

    def __init__(self, gpios=GPIOS, paths=PATHS, serport= '/dev/ttyACM0'):

        '''make a dictionary of the objects and their switch paths.
        set up the software interfacing.
        '''
        self.paths = paths #will just need to write this by hand. 
        self.state = None #state will initially be in the low power mode, defined as the key to the path that is all zeros.
        self.ser = serial.Serial(serport, 115200)
        self.gpios = gpios
        self.powerdown()
 
    def switch(self, pathname, verbose=False):
        '''set switches at given GPIO pins to the low/high power modes specified at paths.
            
            IN
            pathname : the key for the path you want to switch to.
            verbose : if True, then the function prints the states of the GPIO pins for verification.

            OUT 
            writes the pathname and the sum of the logic commands to the self.state property as a tuple.
                ex: self.state = ('VNAANT', 0)
            '''
        assert pathname in self.paths.keys() #make sure the path name is in the keys
        path = self.paths[pathname]
        self.ser.write(path.encode()) #encode the path and write to the thing 
        time.sleep(0.02) #20ms activation time
        pathsum = sum([int(i) for i in list(path)])
        self.state = (pathname, pathsum) 
        
        if verbose: #if the verbose flag is set, then print stuff
            print(pathname, ' is set.')
            for idx, i in enumerate(self.gpios):
                print(f'GPIO{i} set to {path[idx]}.')
    
    def powerdown(self):
        '''
            Finds and switches to the lowest power mode in self.paths. If none of the paths are set such that all switches are in the 0 state, it throws a warning that there is a still power being drawn. 

        '''
        #call switch func on lowest power state.
        states = np.array(list(self.paths.keys()))
        pathstr = np.array(list(self.paths.values()))
        
        pathsums = np.array([sum([int(i) for i in path]) for path in pathstr])
        lowpower = states[pathsums == min(pathsums)][0]
        self.switch(pathname=lowpower)
        
        try:
            assert self.state[1] == 0 #by the end of this func, the first index of the state attribute should be 0, where the 0th index is the pathname.
        except AssertionError:
            warnings.warn('WARNING: lowest power mode has one or more switches in the high power state.')
        finally:
            time.sleep(0.1)
