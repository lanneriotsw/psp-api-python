from lannerpsp import LCM

lcm = LCM()

# Clear LCM display.
lcm.clear()

# Move the cursor to the initial position.
lcm.set_cursor(1, 1)

# Write string to LCD module.
lcm.write("Hello World")
