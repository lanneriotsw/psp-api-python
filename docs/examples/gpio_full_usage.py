from lannerpsp import GPIO

gpio = GPIO()

# Get GPIO information.
gpio_info = gpio.get_info()

# Get the number of GPI/DI pins on LEC-2290:
print(gpio_info.number_of_di_pins)  # It should print 8.

# Get the number of GPO/DO pins on LEC-2290:
print(gpio_info.number_of_do_pins)  # It should print 8.

# Get GPI/DI status (LSB is DI_0).
print(gpio.get_digital_in())

# Set the values of (DO_7 to DO_0) to (1101 0011) signal,
# you can use your preferred integer representation (LSB is DO_0).
# 1. Use binary integer:
gpio.set_digital_out(0b11010011)
# 2. Use octal integer:
gpio.set_digital_out(0o323)
# 3. Use decimal integer:
gpio.set_digital_out(211)
# 4. Use hexadecimal integer:
gpio.set_digital_out(0xD3)
