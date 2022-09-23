====================================
Installing Python API for Lanner PSP
====================================

.. Note::

    "Python API for Lanner PSP" uses Python to call the shared object file generated after PSP
    compilation to execute PSP functions, and encapsulates many C functions in PSP into Python
    interfaces, so please make sure to install `Core SDK`_ before use.

Method 1: From PyPI
===================

.. code-block:: shell

    pip install lannerpsp

Method 2: From source
=====================

.. code-block:: shell

    git clone https://github.com/lanneriotsw/psp-api-python.git
    cd psp-api-python
    python setup.py install

.. _Core SDK: https://github.com/lanneriotsw/psp-manager
