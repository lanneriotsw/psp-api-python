# Python API for Lanner-PSP

[![PyPI version](https://badge.fury.io/py/lannerpsp.svg)](https://badge.fury.io/py/lannerpsp)
[![License: MIT](https://img.shields.io/pypi/l/lannerpsp)](https://opensource.org/licenses/MIT)
[![Python version](https://img.shields.io/pypi/pyversions/lannerpsp)](https://www.python.org/)

[Lanner PSP](https://iot.lannerinc.com/psp/PSP_Summary.htm) is an SDK that facilitates communication between you and
your Lanner IPC's IO.

-----

## Requirements

* **ROOT** privileges
* [Core SDKs](https://github.com/jrchen982/lannerpsp)
* [Python 3.6+](https://www.python.org/)

-----

## Installation

### Method 1: Using `pip`

```shell
pip install lannerpsp
```

### Method 2: From source

```shell
git clone https://github.com/jrchen982/lannerpsp-python
cd lannerpsp-python
python setup.py install
```

-----

## Usage

### High Level API usage

System/Status LED:

```python
from lannerpsp import SystemLED

system_led = SystemLED()

# Set System/Status LED to green.
system_led.green()

# Set System/Status LED to red/amber.
system_led.red()

# Set System/Status LED to off.
system_led.off()

# For testing (default 2 seconds delay).
system_led.test(2)
```

GPS Status LED:

```python
from lannerpsp import GPSLED

gps_led = GPSLED()

# Set GPS Status LED to on.
gps_led.on()

# Set GPS Status LED to blink.
gps_led.blink()

# Set GPS Status LED to off.
gps_led.off()

# For testing (default 2 seconds delay).
gps_led.test(2)
```

LTE Status LED:

```python
from lannerpsp import LteStateLED

lte_state_led = LteStateLED()

# Set LTE Status LED to red.
lte_state_led.red()

# Set LTE Status LED to red blink.
lte_state_led.red_blink()

# Set LTE Status LED to green.
lte_state_led.green()

# Set LTE Status LED to green blink.
lte_state_led.green_blink()

# Set LTE Status LED to yellow.
lte_state_led.yellow()

# Set LTE Status LED to yellow blink.
lte_state_led.yellow_blink()

# Set LTE Status LED to off.
lte_state_led.off()

# For testing (default 2 seconds delay).
lte_state_led.test(2)
```

LTE Stress LED:

```python
from lannerpsp import LteStressLED

lte_stress_led = LteStressLED()

# Set LTE Stress LED to show 87% signal strength.
lte_stress_led.set_strength(87)

# Set LTE Stress LED to off.
lte_stress_led.off()

# For testing (default 2 seconds delay).
lte_stress_led.test(2)
```

Hardware Monitor:

```python
from lannerpsp import HWM

hwm = HWM()

# Get CPU-1 temperature.
cpu1_temp = hwm.get_cpu_temp(1)

# Get CPU-2 temperature.
cpu2_temp = hwm.get_cpu_temp(2)

# Get SYS-1 temperature.
sys1_temp = hwm.get_sys_temp(1)

# Get SYS-2 temperature.
sys2_temp = hwm.get_sys_temp(2)

# Get CPU-1 core voltage.
core1_voltage = hwm.get_vcore(1)

# Get CPU-2 core voltage.
core2_voltage = hwm.get_vcore(2)

# Get 12V voltage.
v12_voltage = hwm.get_12v()

# Get 5V voltage.
v5_voltage = hwm.get_5v()

# Get 3.3V voltage.
v33_voltage = hwm.get_3v3()

# Get 5VSB voltage.
v5sb_voltage = hwm.get_5vsb()

# Get 3.3VSB voltage.
v33sb_voltage = hwm.get_3v3sb()

# Get Vbat voltage.
vbat_voltage = hwm.get_vbat()

# Get PowerSupply 1 AC voltage.
psu1_voltage = hwm.get_power_supply(1)

# Get PowerSupply 2 AC voltage.
psu2_voltage = hwm.get_power_supply(2)

# For hardware monitor testing.
hwm.testhwm()

# Get all exist value to dict.
hwm.get_all()
```

Radio Frequency Module:

```python
from lannerpsp import RFM

rfm = RFM()

# Get LTE Module power state.
# 
# bit 0 represent m.2 module, bit 1 represent mPCIE module
# 1: power on, 0: power off
# 
# 0 (00): mPcie -> off, m.2 -> off
# 1 (01): mPcie -> off, m.2 -> on
# 2 (10): mPcie -> on,  m.2 -> off
# 3 (11): mPcie -> on,  m.2 -> on
rfm_module_status = rfm.get_module()

# Set LTE Module power state to 00.
# mPcie -> off, m.2 -> off.
rfm.set_module(0)

# Set LTE Module power state to 01.
# mPcie -> off, m.2 -> on.
rfm.set_module(1)

# Set LTE Module power state to 10.
# mPcie -> on,  m.2 -> off.
rfm.set_module(2)

# Set LTE Module power state to 11.
# mPcie -> on,  m.2 -> on.
rfm.set_module(3)

# Get SIM card state.
# 
# bit 0 represent m.2 module, bit 1 represent mPCIE module
# 0: first sim, 1: second sim
# 
# 0 (00): mPcie -> first sim (SIM3),  m.2 -> first sim (SIM1)
# 1 (01): mPcie -> first sim (SIM3),  m.2 -> second sim (SIM2)
# 2 (10): mPcie -> second sim (SIM4), m.2 -> first sim (SIM1)
# 3 (11): mPcie -> second sim (SIM4), m.2 -> second sim (SIM2)
rfm_sim_status = rfm.get_sim()

# Set SIM card state to 00.
# mPcie -> first sim (SIM3),  m.2 -> first sim (SIM1).
rfm.set_sim(0)

# Set SIM card state to 01.
# mPcie -> first sim (SIM3),  m.2 -> second sim (SIM2).
rfm.set_sim(1)

# Set SIM card state to 10.
# mPcie -> second sim (SIM4), m.2 -> first sim (SIM1).
rfm.set_sim(2)

# Set SIM card state to 11.
# mPcie -> second sim (SIM4), m.2 -> second sim (SIM2).
rfm.set_sim(3)
```

GPS:

```python
from lannerpsp import GPS

gps = GPS()

# Search GPS port.
gps_port = gps.search_port()
```

G-Sensor:

```python
from lannerpsp import GSR

gsr = GSR()

# Get X direction acceleration value.
x_accel = gsr.get_axis_data().f_x_mg

# Get Y direction acceleration value.
y_accel = gsr.get_axis_data().f_y_mg

# Get Z direction acceleration value.
z_accel = gsr.get_axis_data().f_z_mg

# Get X direction offset value.
x_offset = gsr.get_axis_offset().w_x_axis

# Get Y direction offset value.
y_offset = gsr.get_axis_offset().w_y_axis

# Get Z direction offset value.
z_offset = gsr.get_axis_offset().w_z_axis

# For testing.
gsr.test()
```

COM Port:

```python
from lannerpsp import ComPort

com_port = ComPort()

# Set COM1 to RS232 mode.
com_port.set_com1_mode(232)

# Set COM1 to RS422 mode.
com_port.set_com1_mode(422)

# Set COM1 to RS485 mode.
com_port.set_com1_mode(485)

# Enable COM1 termination.
com_port.set_com1_termination(True)

# Disable COM1 termination.
com_port.set_com1_termination(False)
```

### Low Level API usage

Call the DLL by the `PSP()` instance:

```python
from lannerpsp import PSP


def main() -> None:
    with PSP() as psp:  # Automatically initialize the DLL.
        # Set LTE Status LED to off (clear color).
        i_ret = psp.LMB_SLED_SetLteStateLED(0)
        if i_ret != PSP.ERR_Success:
            error_message = PSP.get_error_message("LMB_SLED_SetLteStateLED", i_ret)
            raise PSP.PSPError(error_message)
        # Set LTE Status LED to green blink.
        i_ret = psp.LMB_SLED_SetLteStateLED(4)
        if i_ret != PSP.ERR_Success:
            error_message = PSP.get_error_message("LMB_SLED_SetLteStateLED", i_ret)
            raise PSP.PSPError(error_message)
```

### Debug

You can import `logging` to catch output messages:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```
