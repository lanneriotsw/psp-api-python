==============
API - COM Port
==============

.. module:: lannerpsp.sdk_odm_com_port

.. currentmodule:: lannerpsp

Regular Classes
===============

The following classes are intended for general use with the devices they
represent. All classes in this section are concrete (not abstract).

COMPort
-------

.. autoclass:: COMPort
    :members: get_info, set_mode, set_termination

Models
======

The following models are used to store data for data modeling.

COMPortInfoModel
----------------

.. autoclass:: COMPortInfoModel
    :members: to_dict

Supported Platforms
===================

.. note::

    The `LEC-7242`_ requires some additional dependencies to be installed via ``pip install lannerpsp[lec7242]``
    to use the COM port.

The following platforms have been verified and confirmed to be supported:

* `LEC-7230M`_
* `LEC-7242`_

.. _LEC-7230M: https://lannerinc.com/products/intelligent-edge-appliances/embedded-platform/lec-7230m
.. _LEC-7242: https://lannerinc.com/products/intelligent-edge-appliances/embedded-platform/lec-7242
