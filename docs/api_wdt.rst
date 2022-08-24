=========
API - WDT
=========

.. module:: lannerpsp.sdk_wdt

.. currentmodule:: lannerpsp

Regular Classes
===============

The following classes are intended for general use with the devices they
represent. All classes in this section are concrete (not abstract).

WDT
---

.. note::

    Almost for all versions of Lanner PSP on all platforms.

.. autoclass:: WDT
    :members: get_info, config, enable, disable, reset

Models
======

The following models are used to store data for data modeling.

WDTInfoModel
------------

.. autoclass:: WDTInfoModel
    :members: to_dict
