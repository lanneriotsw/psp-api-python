=========
API - LED
=========

.. module:: lannerpsp.sdk_sled

.. currentmodule:: lannerpsp

Regular Classes
===============

The following classes are intended for general use with the devices they
represent. All classes in this section are concrete (not abstract).

SystemLED
---------

.. note::

    For `LEC-7242`_, `NCA-2510`_.

.. autoclass:: SystemLED
    :members: get_status, off, green, red, test

GPSStatusLED
------------

.. note::

    For `LEC-7242`_.

.. autoclass:: GPSStatusLED
    :members: off, on, blink, test

LTEStatusLED
------------

.. note::

    For `LEC-7242`_.

.. autoclass:: LTEStatusLED
    :members: off, red, red_blink, green, green_blink, yellow, yellow_blink, test

LTEStressLED
------------

.. note::

    For `LEC-7242`_.

.. autoclass:: LTEStressLED
    :members: off, set_strength, test

.. _LEC-7242: https://lannerinc.com/products/intelligent-edge-appliances/embedded-platform/lec-7242
.. _NCA-2510: https://lannerinc.com/products/telecom-datacenter-appliances/vcpe-ucpe-platforms/nca-2510
