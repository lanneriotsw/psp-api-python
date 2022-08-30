from time import sleep

from lannerpsp import LTEStatusLED

led = LTEStatusLED()

led.red()
sleep(2)
led.red_blink()
sleep(2)
led.green()
sleep(2)
led.green_blink()
sleep(2)
led.yellow()
sleep(2)
led.yellow_blink()
sleep(2)
led.off()
