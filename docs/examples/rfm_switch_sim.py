from time import sleep

from lannerpsp import RFM

rfm = RFM()

print(rfm.get_sim_status())  # It should print 0.

# Power off the mini-PCIe LTE module.
# 01: mPCIe -> off, M.2 -> on
rfm.set_power_status(1)

# Switch to SIM4 slot.
# 10: mPCIe -> second sim (SIM4), M.2 -> first sim (SIM1)
rfm.set_sim_status(2)

# Power on the mini-PCIe LTE module.
# 11: mPCIe -> on,  M.2 -> on
rfm.set_power_status(3)

# It will take about 15 seconds for the SIM card to be switched successfully.
sleep(15)
