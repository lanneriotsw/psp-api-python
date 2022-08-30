from time import sleep

from lannerpsp import SystemLED

led = SystemLED()

while True:
    led.red()
    sleep(1)
    led.off()
    sleep(1)
