=========
API - HWM
=========

.. module:: lannerpsp.sdk_hwm

.. currentmodule:: lannerpsp

Regular Classes
===============

The following classes are intended for general use with the devices they
represent. All classes in this section are concrete (not abstract).

HWM
---

.. note::

    Almost for all versions of Lanner PSP on all platforms.

.. autoclass:: HWM
    :members: get_cpu_temp, get_sys_temp, get_core_volt,
        get_12v_volt, get_5v_volt, get_3v3_volt, get_5vsb_volt, get_3v3sb_volt,
        get_bat_volt, get_dimm_volt, get_psu_volt,
        get_cpu_fan_speed, get_sys_fan_speed, get_fan_speed, get_fan_speed_ex,
        get_sensor_name, get_sensor_msg, list_supported_sensors, testhwm

Models
======

The following models are used to store data for data modeling.

HWMSensorModel
--------------

.. autoclass:: HWMSensorModel
    :members: to_dict
