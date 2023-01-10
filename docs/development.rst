===========
Development
===========

.. currentmodule:: lannerpsp

The main GitHub repository for the project can be found at:

    https://github.com/lanneriotsw/psp-api-python

Development installation
========================

.. code-block:: console

    $ sudo apt install python3-pip python3-venv

.. code-block:: console

    $ cd
    $ git clone git@github.com:lanneriotsw/psp-api-python.git
    $ cd psp-api-python
    $ python3 -m venv venv
    $ source venv/bin/activate
    (venv) $ pip install .[test,doc,dev]

Building the docs
=================

.. code-block:: console

    $ cd ~/psp-api-python
    $ source venv/bin/activate
    (venv) $ make html -C docs

Low Level API usage
===================

Call PSP functions from the C DLL via the :attr:`PSP.lib` property:

.. code-block:: python

    from lannerpsp import PSP, get_psp_exc_msg

    with PSP() as psp:  # Automatically Init() and DeInit().
        # Get the DLL/SO to call C functions by `lib` property.
        # Example to set LTE Status LED to green blink.
        i_ret = psp.lib.LMB_SLED_SetLteStateLED(4)
    msg = get_psp_exc_msg("LMB_SLED_SetLteStateLED", i_ret)
    print(msg)
