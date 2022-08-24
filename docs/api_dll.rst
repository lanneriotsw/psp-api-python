=========
API - DLL
=========

.. module:: lannerpsp.sdk_dll

.. currentmodule:: lannerpsp

Regular Classes
===============

The following classes are intended for general use with the devices they
represent. All classes in this section are concrete (not abstract).

DLL
---

.. note::

    For all versions of Lanner PSP on all platforms.

.. autoclass:: DLL
    :members: get_version, get_bios_id

Models
======

The following models are used to store data for data modeling.

DLLVersionModel
---------------

.. autoclass:: DLLVersionModel
    :members: to_dict
