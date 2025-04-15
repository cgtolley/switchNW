import machine
import sys  
import time
while True:
    command = sys.stdin.readline()
    if command:
        print(f'Command  received: {command}.')
        time.sleep(0.1)
