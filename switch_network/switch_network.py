import numpy as np
import blank as blank

paths = {
            'antenna': [0,0,0],
            'load': [0,1,0],
            'open', [1,0,0],
            'short': [1,0,1]
        }



class SwitchNetwork:

    def __init__(self, gpios, paths=paths):

        '''make a dictionary of the objects and their switch paths.
        set up the software interfacing.
        '''
        self.paths = paths #will just need to write this by hand. 
        self.state = self.powerdown() #state will initially be in the low power mode, defined as the key to the path that is all zeros.
        
    def switch(self, pathname, verbose=False):
        '''set switches at given GPIO pins to the low/high power modes specified at paths.'''
        assert pathname in self.paths.keys() #make sure the path name is in the keys
        path = self.paths[pathname]
        #implement the necessary switch shifts.
        self.state = (pathname, np.sum(path)) #set the active state status
        if verbose: #if the verbose flag is set, then print stuff
            print(pathname, ' is set.')
            for idx, i in enumerate(self.gpios):
                print(f'GPIO{i} set to {path[idx]}.'
    
    def powerdown(self):
        #call switch func on lowest power state.
        states = list(self.paths.keys())
        default = states[np.sum(np.array(list(dic.values())), axis=1) == 0] #get the state that has the lowest power
        self.switch(pathname=default)
        assert self.state[1] == 0 #by the end of this func, the first index of the state attribute should be 0, where the 0th index is the pathname.
        
