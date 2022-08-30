from lannerpsp import SWR

button = SWR()

while True:
    if button.is_pressed:
        print("Button is pressed")
    else:
        print("Button is not pressed")
