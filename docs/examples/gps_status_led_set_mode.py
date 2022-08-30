from time import sleep

from lannerpsp import GPSStatusLED

led = GPSStatusLED()

while True:
    led.on()
    sleep(2)
    led.blink()
    sleep(2)
    led.off()
    sleep(2)
