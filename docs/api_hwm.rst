======================
API - Hardware Monitor
======================

.. module:: lannerpsp.sdk_hwm

.. currentmodule:: lannerpsp

Regular Classes
===============

The following classes are intended for general use with the devices they
represent. All classes in this section are concrete (not abstract).

HWM
---

.. autoclass:: HWM
    :members: get_cpu_temp, get_sys_temp, get_core_volt,
        get_12v_volt, get_5v_volt, get_3v3_volt, get_5vsb_volt, get_3v3sb_volt,
        get_bat_volt, get_dimm_volt, get_psu_volt,
        get_cpu_fan_speed, get_sys_fan_speed, get_fan_speed, get_fan_speed_ex,
        get_sensor_name, get_sensor_msg, list_supported_sensors

Models
======

The following models are used to store data for data modeling.

HWMSensorModel
--------------

.. autoclass:: HWMSensorModel
    :members: to_dict

Supported Platforms
===================

.. note::

    Almost for all versions of Lanner PSP on all platforms.

The following platforms have been verified and confirmed to be supported:

* `IIoT-I530`_
* `LEC-2290`_
* `LEC-7230M`_
* `LEC-7242`_
* `NCA-2510`_
* `V3S`_
* `V6S`_

.. _IIoT-I530: https://lannerinc.com/products/intelligent-edge-appliances/intelligent-video-platform/iiot-i530
.. _LEC-2290: https://lannerinc.com/products/intelligent-edge-appliances/embedded-platform/lec-2290
.. _LEC-7230M: https://lannerinc.com/products/intelligent-edge-appliances/embedded-platform/lec-7230m
.. _LEC-7242: https://lannerinc.com/products/intelligent-edge-appliances/embedded-platform/lec-7242
.. _NCA-2510: https://lannerinc.com/products/telecom-datacenter-appliances/vcpe-ucpe-platforms/nca-2510
.. _V3S: https://lannerinc.com/products/intelligent-edge-appliances/vehicle-rail-computer/v3s
.. _V6S: https://lannerinc.com/products/intelligent-edge-appliances/vehicle-rail-computer/v6s
