==============
API - ODM
==============

.. module:: lannerpsp.sdk_odm

.. currentmodule:: lannerpsp

Regular Classes
===============

The following classes are intended for general use with the devices they
represent. All classes in this section are concrete (not abstract).

COMPort
-------

.. note::

    For `LEC-7230M`_, `LEC-7242`_.

.. autoclass:: COMPort
    :members: get_info, set_mode, set_termination

Models
======

The following models are used to store data for data modeling.

COMPortInfoModel
----------------

.. autoclass:: COMPortInfoModel
    :members: to_dict

.. _LEC-7230M: https://lannerinc.com/products/intelligent-edge-appliances/embedded-platform/lec-7230m
.. _LEC-7242: https://lannerinc.com/products/intelligent-edge-appliances/embedded-platform/lec-7242
