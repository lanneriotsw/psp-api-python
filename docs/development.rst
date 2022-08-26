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
    (venv) $ pip install -r requirements.txt

Building the docs
=================

.. code-block:: console

    $ cd ~/psp-api-python
    $ source venv/bin/activate
    (venv) $ make html -C docs
