import numpy as np
import time
import serial

paths = {
            'antenna':'000', 
            'load': '010',
            'open': '100',
            'short':'101'
        }
gpios = [0,1,2]

class SwitchNetwork:

    def __init__(self, gpios=gpios, paths=paths, serport= '/dev/ttyACM0'):

        '''make a dictionary of the objects and their switch paths.
        set up the software interfacing.
        '''
        self.paths = paths #will just need to write this by hand. 
        self.state = None #state will initially be in the low power mode, defined as the key to the path that is all zeros.
        self.ser = serial.Serial(serport, 115200)
        self.gpios = gpios
        self.powerdown()
 
    def switch(self, pathname, verbose=False):
        '''set switches at given GPIO pins to the low/high power modes specified at paths.'''
        assert pathname in self.paths.keys() #make sure the path name is in the keys
        path = self.paths[pathname]
        self.ser.write(path.encode()) #encode the path and write to the thing 
        time.sleep(0.02) #20ms activation time
        pathsum = sum([int(i) for i in list(path)])
        self.state = (pathname, pathsum) #set the active state status
        
        if verbose: #if the verbose flag is set, then print stuff
            print(pathname, ' is set.')
            for idx, i in enumerate(self.gpios):
                print(f'GPIO{i} set to {path[idx]}.')
    
    def powerdown(self):
        #call switch func on lowest power state.
        states = np.array(list(self.paths.keys()))
        pathstr = np.array(list(self.paths.values()))
        allzeros = [all(i=='0' for i in path) for path in pathstr]
        default = states[allzeros][0]
        self.switch(pathname=default)
        try:
            assert self.state[1] == 0 #by the end of this func, the first index of the state attribute should be 0, where the 0th index is the pathname.
        except AssertionError:
            print(f'state is {self.state}')
        finally:
            time.sleep(0.1)
