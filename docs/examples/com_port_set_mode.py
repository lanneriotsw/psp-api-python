from lannerpsp import COMPort

com1 = COMPort(1)

# Set COM port mode to RS-485.
com1.set_mode(485)

# Get COM port information.
com1_info = com1.get_info()

print(com1_info.mode)  # It should print 485.
print(com1_info.mode_str)  # It should print 'RS-485'.
