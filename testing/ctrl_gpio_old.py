import machine
import sys
import time
#setup the switch pin
switch=machine.Pin(2, machine.Pin.OUT)

def set_pin_state(state):
    '''sets the python state based on the command received thru serial.'''
    if state == '1':
        switch.value(1)
    elif state=='0':
        switch.value(0)
    else:
        print('invalid command')

while True:
    command = sys.stdin.read(1).strip()
    if command:
        print(f'read {command}.')
        set_pin_state(command)
    time.sleep(0.1)
