=========================
Python API for Lanner PSP
=========================

.. image:: https://badge.fury.io/py/lannerpsp.svg
    :target: https://badge.fury.io/py/lannerpsp
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/l/lannerpsp
    :target: https://opensource.org/licenses/MIT
    :alt: License: MIT

.. image:: https://static.pepy.tech/badge/lannerpsp
    :target: https://pepy.tech/project/lannerpsp
    :alt: Total downloads

.. image:: https://img.shields.io/pypi/pyversions/lannerpsp
    :target: https://www.python.org/
    :alt: Python version

A Python interface to access `Lanner PSP`_.

About
=====

`Lanner PSP`_ aims to simplify and enhance the efficiency of customer’s application implementation.
When developers intend to write an application that involves hardware access, they were required
to fully understand the specifications to utilize the drivers. This is often being considered a time-
consuming job which requires lots of related knowledge and time. In order to achieve better full
access hardware functionality, `Lanner`_ invests great effort to ease customer’s development journey
with the release of a suite of reliable Software APIs.

"Python API for Lanner PSP" uses Python to call the shared object file generated after PSP compilation
to execute PSP functions, and encapsulates many C functions in PSP into Python interfaces, so please
make sure to install `Core SDK`_ before use.

If your `Core SDK`_ was installed via the `One-Step Automated Install`_ method, you can use it out of
the box, otherwise you should set the ``liblmbio.so`` and ``liblmbapi.so`` paths before instantiating
other objects. For example:

.. code:: python

    from lannerpsp import PSP, HWM

    PSP.lmb_io_path = "/path/to/liblmbio.so"
    PSP.lmb_api_path = "/path/to/liblmbapi.so"

    hwm = HWM()

    hwm.get_cpu_temp(1)
    ...

Assuming you want to obtain the sensors data for the hardware monitor:

.. code:: python

    from lannerpsp import HWM

    hwm = HWM()

    sensors = hwm.list_supported_sensors()
    for s in sensors:
        print(f"{s.display_name} = {s.value} {s.unit}")

Then run it with **ROOT** privileges, the output will be like:

.. code:: console

    CPU 1 temperature = 41 C
    SYS 1 temperature = 42 C
    CPU 1 Vcore = 0.856 V
    5V = 5.087 V
    3.3V = 3.35 V
    Battery = 3.184 V
    DDR channel 1 = 1.104 V

For complete usage, please refer to the `documentation`_.

Concurrency and Parallelism
===========================

`Lanner PSP`_ invokes many underlying hardware interfaces for communication, such as IPMI, SMBus,
Super I/O, or some MCUs. Some PSP functions may occupy the same communication channel, such as UART
or I2C, etc. Please **avoid** using multi-process or multi-threading unless you can ensure they will
not cause errors due to simultaneous access to the same channel.

Installation
============

To use the "Python API for Lanner PSP", you must have **ROOT** privileges and the `Core SDK`_ must be
installed first. To install "Python API for Lanner PSP", see the `Installation`_ chapter.

Documentation
=============

Comprehensive documentation is available at https://psp-api-python.readthedocs.io/.

Issues and questions
====================

If you have a feature request or bug report, please open an `issue on GitHub`_.
If you have a question or need help, this may be better suited to `Lanner`_'s official online customer service.

Python support
==============

.. warning::

    "Python API for Lanner PSP" only supports Python 3.6 and above.

.. _Lanner PSP: https://link.lannerinc.com/psp
.. _Lanner: https://lannerinc.com/
.. _Core SDK: https://github.com/lanneriotsw/psp-manager
.. _One-Step Automated Install: https://github.com/lanneriotsw/psp-manager#method-1-one-step-automated-install
.. _documentation: https://psp-api-python.readthedocs.io/
.. _Installation: https://psp-api-python.readthedocs.io/en/stable/installing.html
.. _issue on GitHub: https://github.com/lanneriotsw/psp-api-python/issues/new
