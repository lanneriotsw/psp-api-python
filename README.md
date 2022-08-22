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

### Debug

You can import `logging` to catch output messages:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```
