# Python API for Lanner PSP

[![PyPI version](https://badge.fury.io/py/lannerpsp.svg)](https://badge.fury.io/py/lannerpsp)
[![License: MIT](https://img.shields.io/pypi/l/lannerpsp)](https://opensource.org/licenses/MIT)
[![Python version](https://img.shields.io/pypi/pyversions/lannerpsp)](https://www.python.org/)

[Lanner PSP](https://link.lannerinc.com/psp) aims to simplify and enhance the efficiency of customer’s application implementation. 
When developers intend to write an application that involves hardware access, 
they were required to fully understand the specifications to utilize the drivers. 
This is often being considered a time-consuming job which requires lots of related knowledge and time. 
In order to achieve better full access hardware functionality, 
Lanner invests great effort to ease customer’s development journey with the release of a suite of reliable Software APIs.

-----

## Requirements

* **ROOT** privileges
* [Core SDKs](https://github.com/lanneriotsw/psp-manager)
* [Python 3.6+](https://www.python.org/)

-----

## Installation

### Method 1: From PyPI

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

Python executes the functions of PSP by calling the `.so` file which generated after PSP compilation.
If your [Core SDK](https://github.com/lanneriotsw/psp-manager) was installed via the
[One-Step Automated Install](https://github.com/lanneriotsw/psp-manager#method-1-one-step-automated-install)
method, you can use it out of the box, otherwise you should set the `liblmbio.so` and `liblmbapi.so` paths
before instantiating other objects. For example:

```python
from lannerpsp import PSP, HWM

PSP.lmb_io_path = "/path/to/liblmbio.so"
PSP.lmb_api_path = "/path/to/liblmbapi.so"

hwm = HWM()
hwm.get_cpu_temp(1)
...
```

Assuming you want to obtain the sensors data for the hardware monitor, let's create a `test.py` file:

```python
from lannerpsp import HWM

hwm = HWM()
supported_sensors = hwm.list_supported_sensors()
for sensor in supported_sensors:
    print(f"{sensor.display_name} = {sensor.value} {sensor.unit}")
```

Then run it with **ROOT** privileges, the output will be like:

```console
root@lec7242:/home/lanner# python test.py 
CPU 1 temperature = 41 C
SYS 1 temperature = 42 C
CPU 1 Vcore = 0.856 V
5V = 5.087 V
3.3V = 3.35 V
battery = 3.184 V
DDR channel 1 = 1.104 V 
```

For complete usage, please refer to the [documents](https://lannerpsp.readthedocs.io/).
