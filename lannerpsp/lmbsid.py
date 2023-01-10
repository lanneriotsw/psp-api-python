from enum import auto, Enum, unique

HWM_DISPLAY_NAME_MAPPING = {
    # Temperature area
    "HWMID_TEMP_CPU1": "CPU 1 temperature",
    "HWMID_TEMP_CPU2": "CPU 2 temperature",
    "HWMID_TEMP_CPU3": "CPU 3 temperature",
    "HWMID_TEMP_CPU4": "CPU 4 temperature",
    "HWMID_TEMP_SYS1": "SYS 1 temperature",
    "HWMID_TEMP_SYS2": "SYS 2 temperature",
    "HWMID_TEMP_SYS3": "SYS 3 temperature",
    "HWMID_TEMP_SYS4": "SYS 4 temperature",
    "HWMID_TEMP_PCH": "PCH temperature",
    # CPU1 DIMM Temperature
    "HWMID_TEMP_DIMMP1A0": "CPU 1 DIMM A0 temperature",
    "HWMID_TEMP_DIMMP1A1": "CPU 1 DIMM A1 temperature",
    "HWMID_TEMP_DIMMP1B0": "CPU 1 DIMM B0 temperature",
    "HWMID_TEMP_DIMMP1B1": "CPU 1 DIMM B1 temperature",
    "HWMID_TEMP_DIMMP1C0": "CPU 1 DIMM C0 temperature",
    "HWMID_TEMP_DIMMP1C1": "CPU 1 DIMM C1 temperature",
    "HWMID_TEMP_DIMMP1D0": "CPU 1 DIMM D0 temperature",
    "HWMID_TEMP_DIMMP1D1": "CPU 1 DIMM D1 temperature",
    "HWMID_TEMP_DIMMP1E0": "CPU 1 DIMM E0 temperature",
    "HWMID_TEMP_DIMMP1E1": "CPU 1 DIMM E1 temperature",
    "HWMID_TEMP_DIMMP1F0": "CPU 1 DIMM F0 temperature",
    "HWMID_TEMP_DIMMP1F1": "CPU 1 DIMM F1 temperature",
    "HWMID_TEMP_DIMMP1G0": "CPU 1 DIMM G0 temperature",
    "HWMID_TEMP_DIMMP1G1": "CPU 1 DIMM G1 temperature",
    "HWMID_TEMP_DIMMP1H0": "CPU 1 DIMM H0 temperature",
    "HWMID_TEMP_DIMMP1H1": "CPU 1 DIMM H1 temperature",
    # CPU2 DIMM Temperature
    "HWMID_TEMP_DIMMP2A0": "CPU 2 DIMM A0 temperature",
    "HWMID_TEMP_DIMMP2A1": "CPU 2 DIMM A1 temperature",
    "HWMID_TEMP_DIMMP2B0": "CPU 2 DIMM B0 temperature",
    "HWMID_TEMP_DIMMP2B1": "CPU 2 DIMM B1 temperature",
    "HWMID_TEMP_DIMMP2C0": "CPU 2 DIMM C0 temperature",
    "HWMID_TEMP_DIMMP2C1": "CPU 2 DIMM C1 temperature",
    "HWMID_TEMP_DIMMP2D0": "CPU 2 DIMM D0 temperature",
    "HWMID_TEMP_DIMMP2D1": "CPU 2 DIMM D1 temperature",
    "HWMID_TEMP_DIMMP2E0": "CPU 2 DIMM E0 temperature",
    "HWMID_TEMP_DIMMP2E1": "CPU 2 DIMM E1 temperature",
    "HWMID_TEMP_DIMMP2F0": "CPU 2 DIMM F0 temperature",
    "HWMID_TEMP_DIMMP2F1": "CPU 2 DIMM F1 temperature",
    "HWMID_TEMP_DIMMP2G0": "CPU 2 DIMM G0 temperature",
    "HWMID_TEMP_DIMMP2G1": "CPU 2 DIMM G1 temperature",
    "HWMID_TEMP_DIMMP2H0": "CPU 2 DIMM H0 temperature",
    "HWMID_TEMP_DIMMP2H1": "CPU 2 DIMM H1 temperature",
    # Voltage area
    "HWMID_VCORE_CPU1": "CPU 1 Vcore",
    "HWMID_VCORE_CPU2": "CPU 2 Vcore",
    "HWMID_VCORE_CPU3": "CPU 3 Vcore",
    "HWMID_VCORE_CPU4": "CPU 4 Vcore",
    "HWMID_VOLT_P12V": "12V",
    "HWMID_VOLT_P5V": "5V",
    "HWMID_VOLT_P3V3": "3.3V",
    "HWMID_VOLT_P5VSB": "Standby 5V",
    "HWMID_VOLT_P3V3SB": "Standby 3.3V",
    "HWMID_VOLT_VBAT": "Battery",
    "HWMID_VOLT_DDRCH1": "DDR channel 1",
    "HWMID_VOLT_DDRCH2": "DDR channel 2",
    "HWMID_VOLT_DDRCH3": "DDR channel 3",
    "HWMID_VOLT_DDRCH4": "DDR channel 4",
    "HWMID_VOLT_DDRCH5": "DDR channel 5",
    "HWMID_VOLT_DDRCH6": "DDR channel 6",
    "HWMID_VOLT_DDRCH7": "DDR channel 7",
    "HWMID_VOLT_DDRCH8": "DDR channel 8",
    "HWMID_VOLT_PVNN": "VNN",
    "HWMID_VOLT_P1V05": "1.05V",
    "HWMID_VOLT_P1V8": "1.8V",
    "HWMID_VOLT_PVCCIO_CPU1": "CPU 1 VCCIO",
    "HWMID_VOLT_PVCCIO_CPU2": "CPU 2 VCCIO",
    "HWMID_VOLT_PVCCIO_CPU3": "CPU 3 VCCIO",
    "HWMID_VOLT_PVCCIO_CPU4": "CPU 4 VCCIO",
    "HWMID_VOLT_PVCCSA_CPU1": "CPU 1 VCCSA",
    "HWMID_VOLT_PVCCSA_CPU2": "CPU 2 VCCSA",
    "HWMID_VOLT_PVCCSA_CPU3": "CPU 3 VCCSA",
    "HWMID_VOLT_PVCCSA_CPU4": "CPU 4 VCCSA",
    # Fan area
    "HWMID_RPM_FanCpu1": "CPU 1 fan speed",
    "HWMID_RPM_FanCpu2": "CPU 2 fan speed",
    "HWMID_RPM_FanSys1": "SYS 1 fan speed",
    "HWMID_RPM_FanSys2": "SYS 2 fan speed",
    "HWMID_RPM_Fan1A": "Fan 1A speed",
    "HWMID_RPM_Fan1B": "Fan 1B speed",
    "HWMID_RPM_Fan2A": "Fan 2A speed",
    "HWMID_RPM_Fan2B": "Fan 2B speed",
    "HWMID_RPM_Fan3A": "Fan 3A speed",
    "HWMID_RPM_Fan3B": "Fan 3B speed",
    "HWMID_RPM_Fan4A": "Fan 4A speed",
    "HWMID_RPM_Fan4B": "Fan 4B speed",
    "HWMID_RPM_Fan5A": "Fan 5A speed",
    "HWMID_RPM_Fan5B": "Fan 5B speed",
    "HWMID_RPM_Fan6A": "Fan 6A speed",
    "HWMID_RPM_Fan6B": "Fan 6B speed",
    "HWMID_RPM_Fan7A": "Fan 7A speed",
    "HWMID_RPM_Fan7B": "Fan 7B speed",
    "HWMID_RPM_Fan8A": "Fan 8A speed",
    "HWMID_RPM_Fan8B": "Fan 8B speed",
    "HWMID_RPM_Fan9A": "Fan 9A speed",
    "HWMID_RPM_Fan9B": "Fan 9B speed",
    "HWMID_RPM_Fan10A": "Fan 10A speed",
    "HWMID_RPM_Fan10B": "Fan 10B speed",
    # Power supply area
    "HWMID_PSU1_STATUS": "PSU 1 status",
    "HWMID_PSU1_VOLTIN": "PSU 1 Vin",
    "HWMID_PSU1_VOLTOUT": "PSU 1 Vout",
    "HWMID_PSU1_CURRENTIN": "PSU 1 Iin",
    "HWMID_PSU1_CURRENTOUT": "PSU 1 Iout",
    "HWMID_PSU1_POWERIN": "PSU 1 Pin",
    "HWMID_PSU1_POWEROUT": "PSU 1 Pout",
    "HWMID_PSU1_FAN1": "PSU 1 fan 1 speed",
    "HWMID_PSU1_FAN2": "PSU 1 fan 2 speed",
    "HWMID_PSU1_TEMP1": "PSU 1 temperature 1",
    "HWMID_PSU1_TEMP2": "PSU 1 temperature 2",
    "HWMID_PSU2_STATUS": "PSU 2 status",
    "HWMID_PSU2_VOLTIN": "PSU 2 Vin",
    "HWMID_PSU2_VOLTOUT": "PSU 2 Vout",
    "HWMID_PSU2_CURRENTIN": "PSU 2 Iin",
    "HWMID_PSU2_CURRENTOUT": "PSU 2 Iout",
    "HWMID_PSU2_POWERIN": "PSU 2 Pin",
    "HWMID_PSU2_POWEROUT": "PSU 2 Pout",
    "HWMID_PSU2_FAN1": "PSU 2 fan 1 speed",
    "HWMID_PSU2_FAN2": "PSU 2 fan 2 speed",
    "HWMID_PSU2_TEMP1": "PSU 2 temperature 1",
    "HWMID_PSU2_TEMP2": "PSU 2 temperature 2",
    # add here for new items
    #
    "HWMID_VOLT_VCCGT": "VCC GT",
}


@unique
class HWMSensorItemV23(Enum):
    # Temperature area
    HWMID_TEMP_CPU1 = 0
    HWMID_TEMP_CPU2 = auto()
    HWMID_TEMP_CPU3 = auto()
    HWMID_TEMP_CPU4 = auto()
    HWMID_TEMP_SYS1 = auto()
    HWMID_TEMP_SYS2 = auto()
    HWMID_TEMP_SYS3 = auto()
    HWMID_TEMP_SYS4 = auto()
    HWMID_TEMP_PCH = auto()
    # CPU1 DIMM Temperature
    HWMID_TEMP_DIMMP1A0 = auto()
    HWMID_TEMP_DIMMP1A1 = auto()
    HWMID_TEMP_DIMMP1B0 = auto()
    HWMID_TEMP_DIMMP1B1 = auto()
    HWMID_TEMP_DIMMP1C0 = auto()
    HWMID_TEMP_DIMMP1C1 = auto()
    HWMID_TEMP_DIMMP1D0 = auto()
    HWMID_TEMP_DIMMP1D1 = auto()
    HWMID_TEMP_DIMMP1E0 = auto()
    HWMID_TEMP_DIMMP1E1 = auto()
    HWMID_TEMP_DIMMP1F0 = auto()
    HWMID_TEMP_DIMMP1F1 = auto()
    HWMID_TEMP_DIMMP1G0 = auto()
    HWMID_TEMP_DIMMP1G1 = auto()
    HWMID_TEMP_DIMMP1H0 = auto()
    HWMID_TEMP_DIMMP1H1 = auto()
    # CPU2 DIMM Temperature
    HWMID_TEMP_DIMMP2A0 = auto()
    HWMID_TEMP_DIMMP2A1 = auto()
    HWMID_TEMP_DIMMP2B0 = auto()
    HWMID_TEMP_DIMMP2B1 = auto()
    HWMID_TEMP_DIMMP2C0 = auto()
    HWMID_TEMP_DIMMP2C1 = auto()
    HWMID_TEMP_DIMMP2D0 = auto()
    HWMID_TEMP_DIMMP2D1 = auto()
    HWMID_TEMP_DIMMP2E0 = auto()
    HWMID_TEMP_DIMMP2E1 = auto()
    HWMID_TEMP_DIMMP2F0 = auto()
    HWMID_TEMP_DIMMP2F1 = auto()
    HWMID_TEMP_DIMMP2G0 = auto()
    HWMID_TEMP_DIMMP2G1 = auto()
    HWMID_TEMP_DIMMP2H0 = auto()
    HWMID_TEMP_DIMMP2H1 = auto()
    # Voltage area
    HWMID_VCORE_CPU1 = auto()
    HWMID_VCORE_CPU2 = auto()
    HWMID_VCORE_CPU3 = auto()
    HWMID_VCORE_CPU4 = auto()
    HWMID_VOLT_P12V = auto()
    HWMID_VOLT_P5V = auto()
    HWMID_VOLT_P3V3 = auto()
    HWMID_VOLT_P5VSB = auto()
    HWMID_VOLT_P3V3SB = auto()
    HWMID_VOLT_VBAT = auto()
    HWMID_VOLT_DDRCH1 = auto()
    HWMID_VOLT_DDRCH2 = auto()
    HWMID_VOLT_DDRCH3 = auto()
    HWMID_VOLT_DDRCH4 = auto()
    HWMID_VOLT_DDRCH5 = auto()
    HWMID_VOLT_DDRCH6 = auto()
    HWMID_VOLT_DDRCH7 = auto()
    HWMID_VOLT_DDRCH8 = auto()
    HWMID_VOLT_PVNN = auto()
    HWMID_VOLT_P1V05 = auto()
    HWMID_VOLT_PVCCIO_CPU1 = auto()
    HWMID_VOLT_PVCCIO_CPU2 = auto()
    HWMID_VOLT_PVCCIO_CPU3 = auto()
    HWMID_VOLT_PVCCIO_CPU4 = auto()
    HWMID_VOLT_PVCCSA_CPU1 = auto()
    HWMID_VOLT_PVCCSA_CPU2 = auto()
    HWMID_VOLT_PVCCSA_CPU3 = auto()
    HWMID_VOLT_PVCCSA_CPU4 = auto()
    # Fan area
    HWMID_RPM_FanCpu1 = auto()
    HWMID_RPM_FanCpu2 = auto()
    HWMID_RPM_FanSys1 = auto()
    HWMID_RPM_FanSys2 = auto()
    HWMID_RPM_Fan1A = auto()
    HWMID_RPM_Fan1B = auto()
    HWMID_RPM_Fan2A = auto()
    HWMID_RPM_Fan2B = auto()
    HWMID_RPM_Fan3A = auto()
    HWMID_RPM_Fan3B = auto()
    HWMID_RPM_Fan4A = auto()
    HWMID_RPM_Fan4B = auto()
    HWMID_RPM_Fan5A = auto()
    HWMID_RPM_Fan5B = auto()
    HWMID_RPM_Fan6A = auto()
    HWMID_RPM_Fan6B = auto()
    HWMID_RPM_Fan7A = auto()
    HWMID_RPM_Fan7B = auto()
    HWMID_RPM_Fan8A = auto()
    HWMID_RPM_Fan8B = auto()
    HWMID_RPM_Fan9A = auto()
    HWMID_RPM_Fan9B = auto()
    HWMID_RPM_Fan10A = auto()
    HWMID_RPM_Fan10B = auto()
    # Power supply area
    HWMID_PSU1_STATUS = auto()
    HWMID_PSU1_VOLTIN = auto()
    HWMID_PSU1_VOLTOUT = auto()
    HWMID_PSU1_CURRENTIN = auto()
    HWMID_PSU1_CURRENTOUT = auto()
    HWMID_PSU1_POWERIN = auto()
    HWMID_PSU1_POWEROUT = auto()
    HWMID_PSU1_FAN1 = auto()
    HWMID_PSU1_FAN2 = auto()
    HWMID_PSU1_TEMP1 = auto()
    HWMID_PSU1_TEMP2 = auto()
    HWMID_PSU2_STATUS = auto()
    HWMID_PSU2_VOLTIN = auto()
    HWMID_PSU2_VOLTOUT = auto()
    HWMID_PSU2_CURRENTIN = auto()
    HWMID_PSU2_CURRENTOUT = auto()
    HWMID_PSU2_POWERIN = auto()
    HWMID_PSU2_POWEROUT = auto()
    HWMID_PSU2_FAN1 = auto()
    HWMID_PSU2_FAN2 = auto()
    HWMID_PSU2_TEMP1 = auto()
    HWMID_PSU2_TEMP2 = auto()
    # add here for new items
    #
    HWMID_TOTAL = auto()


@unique
class HWMSensorItemV30(Enum):
    # Temperature area
    HWMID_TEMP_CPU1 = 0
    HWMID_TEMP_CPU2 = auto()
    HWMID_TEMP_CPU3 = auto()
    HWMID_TEMP_CPU4 = auto()
    HWMID_TEMP_SYS1 = auto()
    HWMID_TEMP_SYS2 = auto()
    HWMID_TEMP_SYS3 = auto()
    HWMID_TEMP_SYS4 = auto()
    HWMID_TEMP_PCH = auto()
    # CPU1 DIMM Temperature
    HWMID_TEMP_DIMMP1A0 = auto()
    HWMID_TEMP_DIMMP1A1 = auto()
    HWMID_TEMP_DIMMP1B0 = auto()
    HWMID_TEMP_DIMMP1B1 = auto()
    HWMID_TEMP_DIMMP1C0 = auto()
    HWMID_TEMP_DIMMP1C1 = auto()
    HWMID_TEMP_DIMMP1D0 = auto()
    HWMID_TEMP_DIMMP1D1 = auto()
    HWMID_TEMP_DIMMP1E0 = auto()
    HWMID_TEMP_DIMMP1E1 = auto()
    HWMID_TEMP_DIMMP1F0 = auto()
    HWMID_TEMP_DIMMP1F1 = auto()
    HWMID_TEMP_DIMMP1G0 = auto()
    HWMID_TEMP_DIMMP1G1 = auto()
    HWMID_TEMP_DIMMP1H0 = auto()
    HWMID_TEMP_DIMMP1H1 = auto()
    # CPU2 DIMM Temperature
    HWMID_TEMP_DIMMP2A0 = auto()
    HWMID_TEMP_DIMMP2A1 = auto()
    HWMID_TEMP_DIMMP2B0 = auto()
    HWMID_TEMP_DIMMP2B1 = auto()
    HWMID_TEMP_DIMMP2C0 = auto()
    HWMID_TEMP_DIMMP2C1 = auto()
    HWMID_TEMP_DIMMP2D0 = auto()
    HWMID_TEMP_DIMMP2D1 = auto()
    HWMID_TEMP_DIMMP2E0 = auto()
    HWMID_TEMP_DIMMP2E1 = auto()
    HWMID_TEMP_DIMMP2F0 = auto()
    HWMID_TEMP_DIMMP2F1 = auto()
    HWMID_TEMP_DIMMP2G0 = auto()
    HWMID_TEMP_DIMMP2G1 = auto()
    HWMID_TEMP_DIMMP2H0 = auto()
    HWMID_TEMP_DIMMP2H1 = auto()
    # Voltage area
    HWMID_VCORE_CPU1 = auto()
    HWMID_VCORE_CPU2 = auto()
    HWMID_VCORE_CPU3 = auto()
    HWMID_VCORE_CPU4 = auto()
    HWMID_VOLT_P12V = auto()
    HWMID_VOLT_P5V = auto()
    HWMID_VOLT_P3V3 = auto()
    HWMID_VOLT_P5VSB = auto()
    HWMID_VOLT_P3V3SB = auto()
    HWMID_VOLT_VBAT = auto()
    HWMID_VOLT_DDRCH1 = auto()
    HWMID_VOLT_DDRCH2 = auto()
    HWMID_VOLT_DDRCH3 = auto()
    HWMID_VOLT_DDRCH4 = auto()
    HWMID_VOLT_DDRCH5 = auto()
    HWMID_VOLT_DDRCH6 = auto()
    HWMID_VOLT_DDRCH7 = auto()
    HWMID_VOLT_DDRCH8 = auto()
    HWMID_VOLT_PVNN = auto()
    HWMID_VOLT_P1V05 = auto()
    HWMID_VOLT_P1V8 = auto()
    HWMID_VOLT_PVCCIO_CPU1 = auto()
    HWMID_VOLT_PVCCIO_CPU2 = auto()
    HWMID_VOLT_PVCCIO_CPU3 = auto()
    HWMID_VOLT_PVCCIO_CPU4 = auto()
    HWMID_VOLT_PVCCSA_CPU1 = auto()
    HWMID_VOLT_PVCCSA_CPU2 = auto()
    HWMID_VOLT_PVCCSA_CPU3 = auto()
    HWMID_VOLT_PVCCSA_CPU4 = auto()
    # Fan area
    HWMID_RPM_FanCpu1 = auto()
    HWMID_RPM_FanCpu2 = auto()
    HWMID_RPM_FanSys1 = auto()
    HWMID_RPM_FanSys2 = auto()
    HWMID_RPM_Fan1A = auto()
    HWMID_RPM_Fan1B = auto()
    HWMID_RPM_Fan2A = auto()
    HWMID_RPM_Fan2B = auto()
    HWMID_RPM_Fan3A = auto()
    HWMID_RPM_Fan3B = auto()
    HWMID_RPM_Fan4A = auto()
    HWMID_RPM_Fan4B = auto()
    HWMID_RPM_Fan5A = auto()
    HWMID_RPM_Fan5B = auto()
    HWMID_RPM_Fan6A = auto()
    HWMID_RPM_Fan6B = auto()
    HWMID_RPM_Fan7A = auto()
    HWMID_RPM_Fan7B = auto()
    HWMID_RPM_Fan8A = auto()
    HWMID_RPM_Fan8B = auto()
    HWMID_RPM_Fan9A = auto()
    HWMID_RPM_Fan9B = auto()
    HWMID_RPM_Fan10A = auto()
    HWMID_RPM_Fan10B = auto()
    # Power supply area
    HWMID_PSU1_STATUS = auto()
    HWMID_PSU1_VOLTIN = auto()
    HWMID_PSU1_VOLTOUT = auto()
    HWMID_PSU1_CURRENTIN = auto()
    HWMID_PSU1_CURRENTOUT = auto()
    HWMID_PSU1_POWERIN = auto()
    HWMID_PSU1_POWEROUT = auto()
    HWMID_PSU1_FAN1 = auto()
    HWMID_PSU1_FAN2 = auto()
    HWMID_PSU1_TEMP1 = auto()
    HWMID_PSU1_TEMP2 = auto()
    HWMID_PSU2_STATUS = auto()
    HWMID_PSU2_VOLTIN = auto()
    HWMID_PSU2_VOLTOUT = auto()
    HWMID_PSU2_CURRENTIN = auto()
    HWMID_PSU2_CURRENTOUT = auto()
    HWMID_PSU2_POWERIN = auto()
    HWMID_PSU2_POWEROUT = auto()
    HWMID_PSU2_FAN1 = auto()
    HWMID_PSU2_FAN2 = auto()
    HWMID_PSU2_TEMP1 = auto()
    HWMID_PSU2_TEMP2 = auto()
    # add here for new items
    #
    HWMID_TOTAL = auto()
