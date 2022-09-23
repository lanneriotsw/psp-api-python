==============
API - G-Sensor
==============

.. module:: lannerpsp.sdk_gsr

.. currentmodule:: lannerpsp

Regular Classes
===============

The following classes are intended for general use with the devices they
represent. All classes in this section are concrete (not abstract).

GSR
---

.. autoclass:: GSR
    :members: get_data, get_offset, test

Models
======

The following models are used to store data for data modeling.

GSRDataModel
------------

.. autoclass:: GSRDataModel
    :members: to_dict

GSROffsetModel
--------------

.. autoclass:: GSROffsetModel
    :members: to_dict

Supported Platforms
===================

.. note::

    GSR is commonly used on V-Series or R-Series platforms.
    See `Vehicle/Rail Computer`_ for more information.

The following platforms have been verified and confirmed to be supported:

* `V3S`_
* `V6S`_

.. _Vehicle/Rail Computer: https://lannerinc.com/products/intelligent-edge-appliances/vehicle-rail-computer
.. _V3S: https://lannerinc.com/products/intelligent-edge-appliances/vehicle-rail-computer/v3s
.. _V6S: https://lannerinc.com/products/intelligent-edge-appliances/vehicle-rail-computer/v6s
