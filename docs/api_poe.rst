=========
API - PoE
=========

.. module:: lannerpsp.sdk_poe

.. currentmodule:: lannerpsp

Regular Classes
===============

The following classes are intended for general use with the devices they
represent. All classes in this section are concrete (not abstract).

PoE
---

.. autoclass:: PoE
    :members: get_info, enable, disable, get_power_status

Models
======

The following models are used to store data for data modeling.

PoEInfoModel
------------

.. autoclass:: PoEInfoModel
    :members: to_dict

Supported Platforms
===================

The following platforms have been verified and confirmed to be supported:

* `IIoT-I530`_
* `LEC-2290`_
* `V3S`_
* `V6S`_

.. _IIoT-I530: https://lannerinc.com/products/intelligent-edge-appliances/intelligent-video-platform/iiot-i530
.. _LEC-2290: https://lannerinc.com/products/intelligent-edge-appliances/embedded-platform/lec-2290
.. _V3S: https://lannerinc.com/products/intelligent-edge-appliances/vehicle-rail-computer/v3s
.. _V6S: https://lannerinc.com/products/intelligent-edge-appliances/vehicle-rail-computer/v6s
