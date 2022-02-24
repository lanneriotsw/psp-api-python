# Python API for Lanner PSP

[![PyPI version](https://badge.fury.io/py/lannerpsp.svg)](https://badge.fury.io/py/lannerpsp)
[![License: MIT](https://img.shields.io/pypi/l/lannerpsp)](https://opensource.org/licenses/MIT)
[![Python version](https://img.shields.io/pypi/pyversions/lannerpsp)](https://www.python.org/)

[Lanner PSP](https://link.lannerinc.com/psp) is an SDK that facilitates communication between you and
your Lanner IPC's IO.

-----

## Requirements

* **ROOT** privileges
* [Core SDKs](https://github.com/lanneriotsw/psp-manager)
* [Python 3.6+](https://www.python.org/)

-----

## Installation

### Method 1: Using `pip`

```shell
pip install lannerpsp
```

### Method 2: From source

```shell
git clone https://github.com/lanneriotsw/psp-api-python.git
cd psp-api-python
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
from lannerpsp import HardwareMonitor

hwm = HardwareMonitor()

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

# Get all exist value to list.
hwm.get_all()
```

Radio Frequency Module:

```python
from lannerpsp import RadioFrequencyModule

rfm = RadioFrequencyModule()

# Get LTE Module power state.
# 
# bit 0 means m.2 module, bit 1 means mPCIE module
# 0: power off, 1: power on
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
# bit 0 means m.2 module, bit 1 means mPCIE module
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
from lannerpsp import GSensor

gsr = GSensor()

# Get X direction acceleration raw data.
accel_raw_x = gsr.get_accel().raw_x

# Get Y direction acceleration raw data.
accel_raw_y = gsr.get_accel().raw_y

# Get Z direction acceleration raw data.
accel_raw_z = gsr.get_accel().raw_z

# Get X direction acceleration mg value.
accel_mg_x = gsr.get_accel().mg_x

# Get Y direction acceleration mg value.
accel_mg_y = gsr.get_accel().mg_y

# Get Z direction acceleration mg value.
accel_mg_z = gsr.get_accel().mg_z

# Get X direction offset raw data.
offset_raw_x = gsr.get_offset().raw_x

# Get Y direction offset raw data.
offset_raw_y = gsr.get_offset().raw_y

# Get Z direction offset raw data.
offset_raw_z = gsr.get_offset().raw_z

# For testing.
gsr.test()
```

Software Reset:

```python
from lannerpsp import SoftwareReset

swr = SoftwareReset()

# Get software reset button status.
swr_status = swr.get_status()

# Use callback function to detect software 
# reset button status (default 10 seconds).
swr.exec_callback()

# For testing (default 5 seconds delay).
swr.test(5)

# Returns `True` if the device is currently active and `False` otherwise.
is_swr_pressed = swr.is_pressed

# Pause the script until the device is activated.
swr.wait_for_press()

# Pause the script until the device is deactivated.
swr.wait_for_release()
```

Watchdog Timer:

```python
from lannerpsp import WatchdogTimer

wdt = WatchdogTimer()

# Enable watchdog timer for 10 seconds.
wdt.enable(10)

# Reset watchdog timer.
wdt.reset()

# Disable watchdog timer.
wdt.disable()
```

Liquid Crystal Display Module:

```python
from lannerpsp import LCM

lcm = LCM()

# Get LCM module type.
lcm.get_module_type()

# Get LCM keys status.
lcm.get_keys_status()

# Set LCM backlight on.
lcm.set_backlight(True)

# Set LCM backlight off.
lcm.set_backlight(False)

# Set LCM cursor to row -> 2, column -> 6.
lcm.set_cursor(2, 6)

# Write string on LCM.
lcm.write("Hello World")

# Clear string on LCM.
lcm.clear()

# Use callback function to detect LCM Keys status.
lcm.exec_callback()
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
    with PSP() as psp:  # Automatically Init() and DeInit().
        # Get BIOS version.
        bios_version = psp.bios_version

        # Get IODRV version.
        iodrv_version = psp.iodrv_version

        # Get PSP/SDK version.
        sdk_version = psp.sdk_version

        # Get the DLL/SO to call C functions by `lib` property.
        # Example to set LTE Status LED to green blink.
        i_ret = psp.lib.LMB_SLED_SetLteStateLED(4)
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
