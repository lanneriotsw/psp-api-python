=============
Basic Recipes
=============

.. currentmodule:: lannerpsp

The following recipes demonstrate some of the capabilities of the "Python API
for Lanner PSP". Please note that all recipes are written assuming Python 3.6+.

Importing Lanner PSP
====================

.. module:: lannerpsp

In Python, libraries and functions used in a script must be imported by name
at the top of the file, with the exception of the functions built into Python
by default.

For example, to use the :class:`HWM` interface from Lanner PSP, it
should be explicitly imported::

    from lannerpsp import HWM

Now :class:`~lannerpsp.HWM` is available directly in your script::

    hwm = HWM()

Alternatively, the whole Lanner PSP library can be imported::

    import lannerpsp

In this case, all references to items within Lanner PSP must be prefixed::

    hwm = lannerpsp.HWM()

Hardware Configuration
======================

The Hardware Configuration Diagram, Block Diagram and Motherboard Layout can
be found in the user manual on Lanner's official website `product page`_.

.. _product page: https://lannerinc.com/products

GPIO
====

Example for `LEC-2290`_:

.. image:: images/LEC-2290_GPIO.*

`LEC-2290`_ has 1x 20 pin terminal block 8 DI (12V) & 8 DO (12V,100mA) Isolation, you can get
or set the :class:`GPIO` status according to your needs:

.. literalinclude:: examples/gpio_full_usage.py

.. _LEC-2290: https://lannerinc.com/products/intelligent-edge-appliances/embedded-platform/lec-2290

GPS
===

Example for `V6S`_:

.. image:: images/V6S_GPS.*

Connect the GPS antenna and place it in an open and unshaded place to ensure
that the GPS can receive satellite signals normally.

Search for the port of the :class:`GPS` on `V6S`_:

.. literalinclude:: examples/gps_search_port.py

.. _V6S: https://lannerinc.com/products/intelligent-edge-appliances/vehicle-rail-computer/v6s

LCD Module
==========

Example for `NCA-2510`_:

.. image:: images/NCA-2510_LCM.*

`NCA-2510`_ has a LCD Module with a keypad, you can write string to the :class:`LCM`
or get the keypad status:

.. literalinclude:: examples/lcm_write.py

.. _NCA-2510: https://lannerinc.com/products/telecom-datacenter-appliances/vcpe-ucpe-platforms/nca-2510

COM Port
========

Example for `LEC-7230M`_:

.. image:: images/LEC-7230M_COMPort.*

`LEC-7230M`_ has 2x DB9 Serial COM ports supporting RS232/422/485, you can set
the :class:`COMPort` mode according to your needs:

.. literalinclude:: examples/com_port_set_mode.py

.. _LEC-7230M: https://lannerinc.com/products/intelligent-edge-appliances/embedded-platform/lec-7230m

PoE
===

Example for `IIoT-I530`_:

.. image:: images/IIoT-I530_PoE.*

`IIoT-I530`_ SKU A has 6x GbE RJ45 for PoE+ (Total PoE budget of 120W), you can set
the :class:`PoE` power status according to your needs:

.. literalinclude:: examples/poe_full_usage.py

.. _IIoT-I530: https://lannerinc.com/products/intelligent-edge-appliances/intelligent-video-platform/iiot-i530

RF Module
=========

Example for `LEC-7242`_:

.. image:: images/LEC-7242_RFM.*

Installation for SIM Card
-------------------------

1. Locate the SIM card slot. Unsecure the screw and remove the cover from the front panel.
2. Insert the SIM card into the slot with the **gold contacts** facing side.

.. image:: images/LEC-7242_install_sim_card_1.*
    :scale: 30%
.. image:: images/LEC-7242_install_sim_card_2.*
    :scale: 30%

SIM1, SIM2 for M.2 LTE module, SIM3, SIM4 for mini-PCIe LTE module:

.. image:: images/LEC-7242_install_sim_card_3.*

.. note::

    **No need to shut down the system while installing/exchanging the SIM card.**
    The Cover-Remove-detect I/O will deliver the GPO signal and cut off the Power
    of m.2 and mini PCIe while uninstalls the cover.

`LEC-7242`_ is pre-installed with a mini-PCIe LTE module. Suppose a SIM card is
installed in each of the SIM3 and SIM4 slots, and SIM3 is enabled. If you want
to switch the SIM card from SIM3 slot to SIM4 slot:

.. literalinclude:: examples/rfm_switch_sim.py

.. _LEC-7242: https://lannerinc.com/products/intelligent-edge-appliances/embedded-platform/lec-7242

System LED
==========

Example for `LEC-7242`_:

.. image:: images/LEC-7242_SystemLED.*

`LEC-7242`_ has a Yellow LED for Alarm, you can set the :class:`SystemLED`
light mode according to your needs:

.. literalinclude:: examples/system_led_set_mode.py

GPS Status LED
==============

Example for `LEC-7242`_:

.. image:: images/LEC-7242_GPSStatusLED.*

`LEC-7242`_ has 1x Blue LED for GPS status, you can set the :class:`GPSStatusLED`
light mode according to your needs:

.. literalinclude:: examples/gps_status_led_set_mode.py

LTE Status LED
==============

Example for `LEC-7242`_:

.. image:: images/LEC-7242_LTEStatusLED.*

`LEC-7242`_ has 1x Yellow/Green/Red LED for LTE status, you can set the :class:`LTEStatusLED`
light mode according to your needs:

.. literalinclude:: examples/lte_status_led_set_mode.py

LTE Stress LED
==============

Example for `LEC-7242`_:

.. image:: images/LEC-7242_LTEStressLED.*

`LEC-7242`_ has 4x Blue LED for LTE signal level status, you can set the :class:`LTEStressLED`
signal strength from 1% to 100%:

.. literalinclude:: examples/lte_stress_led_set_strength.py

Software Reset Button
=====================

Example for `NCR-1510`_:

.. image:: images/NCR-1510_SWR.*

If you want to change reset button mode from hardware reset to software reset, you
must move the **JRESET1** pin jumper on the motherboard from pins 1-2 to pins 2-3.

.. image:: images/NCR-1510_reset_pin_1.*
.. image:: images/NCR-1510_reset_pin_2.*

Check if a :class:`SWR` is pressed:

.. literalinclude:: examples/swr_is_pressed.py

Wait for a button to be pressed before continuing:

.. literalinclude:: examples/swr_wait_for_press.py

.. _NCR-1510: https://lannerinc.com/products/intelligent-edge-appliances/rugged-wireless-gateway/ncr-1510
