from lannerpsp import PoE

# Get PoE information.
poe_info = PoE.get_info()

# Get the number of PoE ports on IIoT-I530:
print(poe_info.number_of_poe_ports)  # It should print 6.

# Get the power status of all PoE ports on IIoT-I530:
print(poe_info.power_status)

# Use PoE port-1:
poe1 = PoE(1)

# Enable the PoE port-1 power (power on by auto):
poe1.enable()

# Get the PoE port-1 power status:
print(poe1.get_power_status())  # It should print True.

# Disable the PoE port-1 power (power off):
poe1.disable()

# Get the PoE port-1 power status:
print(poe1.get_power_status())  # It should print False.
