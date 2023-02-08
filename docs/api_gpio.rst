==========
API - GPIO
==========

.. module:: lannerpsp.sdk_gpio

.. currentmodule:: lannerpsp

Regular Classes
===============

The following classes are intended for general use with the devices they
represent. All classes in this section are concrete (not abstract).

GPIO
----

.. autoclass:: GPIO
    :members: get_info, get_digital_in, get_digital_out, set_digital_out

Models
======

The following models are used to store data for data modeling.

GPIOInfoModel
-------------

.. autoclass:: GPIOInfoModel
    :members: to_dict

Supported Platforms
===================

The following platforms have been verified and confirmed to be supported:

* `IIoT-I530`_
* `LEC-2290`_
* `LEC-7230M`_
* `NCA-2510`_
* `V3S`_
* `V6S`_

.. _IIoT-I530: https://lannerinc.com/products/intelligent-edge-appliances/intelligent-video-platform/iiot-i530
.. _LEC-2290: https://lannerinc.com/products/intelligent-edge-appliances/embedded-platform/lec-2290
.. _LEC-7230M: https://lannerinc.com/products/intelligent-edge-appliances/embedded-platform/lec-7230m
.. _NCA-2510: https://lannerinc.com/products/telecom-datacenter-appliances/vcpe-ucpe-platforms/nca-2510
.. _V3S: https://lannerinc.com/products/intelligent-edge-appliances/vehicle-rail-computer/v3s
.. _V6S: https://lannerinc.com/products/intelligent-edge-appliances/vehicle-rail-computer/v6s
