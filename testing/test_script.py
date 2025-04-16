import time
import machine

#commands used:
#mpremote cp test_script.py :test_script.py
#mpremote run test_script.py

led = machine.Pin(25, machine.Pin.OUT)

t0=time.time()
while time.time() - t0 < 5: #blink for 5 seconds
    led.toggle()
    time.sleep(0.5)

#turn off the led
led.value(0)
print('Finished blinking!')

