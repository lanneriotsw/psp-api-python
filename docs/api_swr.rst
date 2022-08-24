=========
API - SWR
=========

.. module:: lannerpsp.sdk_swr

.. currentmodule:: lannerpsp

Regular Classes
===============

The following classes are intended for general use with the devices they
represent. All classes in this section are concrete (not abstract).

SWR
---

.. note::

    For `LEC-7242`_, `NCA-2510`_.

.. autoclass:: SWR
    :members: get_status, exec_callback, test, is_pressed, wait_for_press, wait_for_release

.. _LEC-7242: https://lannerinc.com/products/intelligent-edge-appliances/embedded-platform/lec-7242
.. _NCA-2510: https://lannerinc.com/products/telecom-datacenter-appliances/vcpe-ucpe-platforms/nca-2510
