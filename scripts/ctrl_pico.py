import machine
import sys
import time

#set up the gpio switches
PINS = [2,7,1,6,3,0,4]
SETPINS = {f'idx{pindex}' : machine.Pin(PINS[pindex], machine.Pin.OUT) for pindex in range(len(PINS))}

def set_switch_states(statestr, pins=SETPINS):
    '''takes a string of 0s and 1s from the controlling computer. for each of these elements and toggles the 0/1 state indicated for the GPIO pin at the correct index.'''
    states = [int(i) for i in statestr] #processes the command

    try: #mus have same number of states as pins
        assert len(states) == len(pins)
    except AssertionError:
        print('not enough states for num of pins.') 
        return

    for pindex in range(len(states)):
        state = states[pindex]
        try: #if state is not 0 or 1, it can't get through
            assert (state == 1) or (state==0)
        except AssertionError:
            print(f'invalid state value: {state}.')
            break

        pins[f'idx{pindex}'].value(state) #set the value of the pin at idx{pindex}

while True:
    command = sys.stdin.readline(len(PINS)) #get the correct number of characters
    if command:
        print(f'read {command}')
        set_switch_states(statestr=command, pins=SETPINS)
    time.sleep(0.1)


