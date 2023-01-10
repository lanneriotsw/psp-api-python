=====================
API - Watch Dog Timer
=====================

.. module:: lannerpsp.sdk_wdt

.. currentmodule:: lannerpsp

Regular Classes
===============

The following classes are intended for general use with the devices they
represent. All classes in this section are concrete (not abstract).

WDT
---

.. autoclass:: WDT
    :members: get_info, config, enable, disable, reset

Models
======

The following models are used to store data for data modeling.

WDTInfoModel
------------

.. autoclass:: WDTInfoModel
    :members: to_dict

Supported Platforms
===================

.. note::

    Almost for all versions of Lanner PSP on all platforms.

The following platforms have been verified and confirmed to be supported:

* `LEC-2290`_
* `LEC-7230M`_
* `LEC-7242`_
* `NCA-2510`_
* `V3S`_
* `V6S`_

.. _LEC-2290: https://lannerinc.com/products/intelligent-edge-appliances/embedded-platform/lec-2290
.. _LEC-7230M: https://lannerinc.com/products/intelligent-edge-appliances/embedded-platform/lec-7230m
.. _LEC-7242: https://lannerinc.com/products/intelligent-edge-appliances/embedded-platform/lec-7242
.. _NCA-2510: https://lannerinc.com/products/telecom-datacenter-appliances/vcpe-ucpe-platforms/nca-2510
.. _V3S: https://lannerinc.com/products/intelligent-edge-appliances/vehicle-rail-computer/v3s
.. _V6S: https://lannerinc.com/products/intelligent-edge-appliances/vehicle-rail-computer/v6s
