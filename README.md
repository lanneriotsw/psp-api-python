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
* Python 3.6+

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
from lannerpsp import SLED

# Set System/Status LED to green.
SLED.green()

# Set System/Status LED to red/amber.
SLED.red()

# Set System/Status LED to off.
SLED.off()

# For testing (default 2 seconds delay).
SLED.test(2)
```

GPS Status LED:

```python
from lannerpsp import SLEDGPS

# Set GPS Status LED to on.
SLEDGPS.on()

# Set GPS Status LED to blink.
SLEDGPS.blink()

# Set GPS Status LED to off.
SLEDGPS.off()

# For testing (default 2 seconds delay).
SLEDGPS.test(2)
```

LTE Status LED:

```python
from lannerpsp import SLEDLTE

# Set LTE Status LED to red.
SLEDLTE.red()

# Set LTE Status LED to red blink.
SLEDLTE.red_blink()

# Set LTE Status LED to green.
SLEDLTE.green()

# Set LTE Status LED to green blink.
SLEDLTE.green_blink()

# Set LTE Status LED to yellow.
SLEDLTE.yellow()

# Set LTE Status LED to yellow blink.
SLEDLTE.yellow_blink()

# Set LTE Status LED to off.
SLEDLTE.off()

# For testing (default 2 seconds delay).
SLEDLTE.test(2)
```

LTE Stress LED:

```python
from lannerpsp import SLEDLTEStress

# Set LTE Stress LED to show 87% signal strength.
SLEDLTEStress.set_strength(87)

# Set LTE Stress LED to off.
SLEDLTEStress.off()

# For testing (default 2 seconds delay).
SLEDLTEStress.test(2)
```

Hardware Monitor:

```python
from lannerpsp import HWM

# Get CPU-1 temperature.
cpu1_temp = HWM.get_cpu_temp(1)

# Get CPU-2 temperature.
cpu2_temp = HWM.get_cpu_temp(2)

# Get SYS-1 temperature.
sys1_temp = HWM.get_sys_temp(1)

# Get SYS-2 temperature.
sys2_temp = HWM.get_sys_temp(2)

# Get CPU-1 core voltage.
core1_voltage = HWM.get_vcore(1)

# Get CPU-2 core voltage.
core2_voltage = HWM.get_vcore(2)

# Get 12V voltage.
v12_voltage = HWM.get_12v()

# Get 5V voltage.
v5_voltage = HWM.get_5v()

# Get 3.3V voltage.
v33_voltage = HWM.get_3v3()

# Get 5VSB voltage.
v5sb_voltage = HWM.get_5vsb()

# Get 3.3VSB voltage.
v33sb_voltage = HWM.get_3v3sb()

# Get Vbat voltage.
vbat_voltage = HWM.get_vbat()

# Get PowerSupply 1 AC voltage.
psu1_voltage = HWM.get_power_supply(1)

# Get PowerSupply 2 AC voltage.
psu2_voltage = HWM.get_power_supply(2)

# For hardware monitor testing.
HWM.testhwm()
```

Radio Frequency Module:

```python
from lannerpsp import RFM

# Get LTE Module power state.
# 
# bit 0 represent m.2 module, bit 1 represent mPCIE module
# 1: power on, 0: power off
# 
# 0 (00): mPcie -> off, m.2 -> off
# 1 (01): mPcie -> off, m.2 -> on
# 2 (10): mPcie -> on,  m.2 -> off
# 3 (11): mPcie -> on,  m.2 -> on
rfm_module_status = RFM.get_module()

# Set LTE Module power state to 00.
# mPcie -> off, m.2 -> off.
RFM.set_module(0)

# Set LTE Module power state to 01.
# mPcie -> off, m.2 -> on.
RFM.set_module(1)

# Set LTE Module power state to 10.
# mPcie -> on,  m.2 -> off.
RFM.set_module(2)

# Set LTE Module power state to 11.
# mPcie -> on,  m.2 -> on.
RFM.set_module(3)

# Get SIM card state.
# 
# bit 0 represent m.2 module, bit 1 represent mPCIE module
# 0: first sim, 1: second sim
# 
# 0 (00): mPcie -> first sim (SIM3),  m.2 -> first sim (SIM1)
# 1 (01): mPcie -> first sim (SIM3),  m.2 -> second sim (SIM2)
# 2 (10): mPcie -> second sim (SIM4), m.2 -> first sim (SIM1)
# 3 (11): mPcie -> second sim (SIM4), m.2 -> second sim (SIM2)
rfm_sim_status = RFM.get_sim()

# Set SIM card state to 00.
# mPcie -> first sim (SIM3),  m.2 -> first sim (SIM1).
RFM.set_sim(0)

# Set SIM card state to 01.
# mPcie -> first sim (SIM3),  m.2 -> second sim (SIM2).
RFM.set_sim(1)

# Set SIM card state to 10.
# mPcie -> second sim (SIM4), m.2 -> first sim (SIM1).
RFM.set_sim(2)

# Set SIM card state to 11.
# mPcie -> second sim (SIM4), m.2 -> second sim (SIM2).
RFM.set_sim(3)
```

GPS:

```python
from lannerpsp import GPS

# Search GPS port.
gps_port = GPS.search_port()
```

G-Sensor:

```python
from lannerpsp import GSR

# Get X direction acceleration value.
x_accel = GSR.get_data().f_x_mg

# Get Y direction acceleration value.
y_accel = GSR.get_data().f_y_mg

# Get Z direction acceleration value.
z_accel = GSR.get_data().f_z_mg

# Get X direction offset value.
x_offset = GSR.get_offset().w_x_axis

# Get Y direction offset value.
y_offset = GSR.get_offset().w_y_axis

# Get Z direction offset value.
z_offset = GSR.get_offset().w_z_axis

# For testing.
GSR.test()
```

COM Port:

```python
from lannerpsp import ComPort

# Set COM1 to RS232 mode.
ComPort.set_com1_mode(232)

# Set COM1 to RS422 mode.
ComPort.set_com1_mode(422)

# Set COM1 to RS485 mode.
ComPort.set_com1_mode(485)

# Enable COM1 termination.
ComPort.set_com1_termination(True)

# Disable COM1 termination.
ComPort.set_com1_termination(False)
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
            PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
            return
        # Set LTE Status LED to green blink.
        i_ret = psp.LMB_SLED_SetLteStateLED(4)
        if i_ret != PSP.ERR_Success:
            PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
            return
```

### Debug

You can import `logging` to catch output messages:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```
