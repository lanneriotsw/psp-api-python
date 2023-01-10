=========
Changelog
=========

.. currentmodule:: lannerpsp

Release 0.0.11 (2023-01-10)
===========================

Bug Fixes
---------

* Fix sphinx docs :exc:`ModuleNotFoundError` when building on `readthedocs`_.

Release 0.0.10 (2023-01-10)
===========================

What's New
----------

* Add :class:`HWM` graphic card support for `LEC-2290`_.
* Add `LEC-2290`_ test scripts for PSP version 2.1.2 and 2.1.3.
* Use `pyproject.toml` to replace `setup.cfg`, `setup.py` and `requirements.txt`.
* Add Lanner logo and Lanner icon to sphinx docs.

Bug Fixes
---------

* Changed optional dependency name `lec7242` to `portio` for generality.
* Remove redundant log message in :class:`HWM`.

.. _LEC-2290: https://lannerinc.com/products/intelligent-edge-appliances/embedded-platform/lec-2290

Release 0.0.9 (2022-09-23)
==========================

What's New
----------

* Add the ``all`` identifier to install all optional dependencies via ``pip install lannerpsp[all]``
  for compatibility with all product types.
* Change :exc:`ValueError` to :exc:`PSPInvalid` in :meth:`GPIOConfigTool.set_com1_mode` for better
  consistency.
* Add the ``check_platform`` parameter to the ``__init__`` method of multiple objects to check if the
  current platform supports it.
* Update the docs.

Bug Fixes
---------

* Fix all display names to start with uppercase for :meth:`HWM.list_supported_sensors`.

Release 0.0.8 (2022-08-30)
==========================

What's New
----------

* Add :file:`recipes` with beautiful pictures.
* Remove LICENSE block shown in PyPi.

Bug Fixes
---------

* Fix :meth:`HWM.list_supported_sensors` docs from °C to C.
* Fix code-block decorator from python to pycon.

Release 0.0.7 (2022-08-30)
==========================

Not exists.

Release 0.0.6 (2022-08-29)
==========================

What's New
----------

* Change ``README.md`` to ``README.rst``.
* Remove usage from ``README.rst`` and make documentation by `sphinx`_ on `readthedocs`_.
* Remove :attr:`sdk_version`, :attr:`iodrv_version`, :attr:`bios_version` from :class:`PSP`.
* Remove :meth:`PSP.get_error_message` from :class:`PSP`.
* Add exception classes.
* Change :class:`ComPort` to :class:`COMPort`.
* Add :class:`DLL`.
* Change :class:`GPSLED` to :class:`GPSStatusLED`.
* Change :class:`GSensor` to :class:`GSR`.
* Change :class:`HardwareMonitor` to :class:`HWM`.
* Change :class:`LteStateLED` to :class:`LTEStatusLED`.
* Change :class:`LteStressLED` to :class:`LTEStressLED`.
* Change :class:`RadioFrequencyModule` to :class:`RFM`.
* Change :class:`SoftwareReset` to :class:`SWR`.
* Change :class:`WatchdogTimer` to :class:`WDT`.
* Add direct access to COM port for `LEC-7242`_ with :class:`GPIOConfigTool`.
* Add :meth:`WDT.config`.
* Add ``time_base`` setting to :meth:`WDT.config` and :meth:`WDT.enable`.
* Add PSP 3.0.0 support for `LEC-7230M`_.
* Update test cases.

Bug Fixes
---------

* Enhanced fool-proof checks for many functions.

.. _sphinx: https://www.sphinx-doc.org/en/master/
.. _readthedocs: https://psp-api-python.readthedocs.io/
.. _LEC-7242: https://lannerinc.com/products/intelligent-edge-appliances/embedded-platform/lec-7242
.. _LEC-7230M: https://lannerinc.com/products/intelligent-edge-appliances/embedded-platform/lec-7230m

Release 0.0.5 (2022-02-24)
==========================

What's New
----------

* Add :class:`LCM`.
* Add :class:`LCM` usage in ``README.md``.

Bug Fixes
---------

* Fix ``seconds`` fool-proof check in :meth:`WatchdogTimer.enable`.

Release 0.0.4 (2021-12-03)
==========================

What's New
----------

* Add :attr:`bios_version` property to :class:`PSP`.
* Add :attr:`iodrv_version` property to :class:`PSP`.
* Add :attr:`sdk_version` property to :class:`PSP`.
* Change :class:`GSR` to :class:`GSensor`.
* Change :class:`HWM` to :class:`HardwareMonitor`.
* Change :class:`RFM` to :class:`RadioFrequencyModule`.
* Change API usage in :class:`GSensor`.
* Change output type from dict to list in :meth:`HardwareMonitor.get_all`.
* Change output method from ``logging`` to :func:`print` in all ``test`` functions.
* Change logging level from ``INFO`` to ``DEBUG``.
* Update usages in ``README.md``.
* Update test cases in ``tests/``.

Bug Fixes
---------

* Fix permission check in :class:`ComPort`.
* Fix :meth:`SoftwareReset.test` stdout error when setting less than 5 seconds.

Release 0.0.3 (2021-11-18)
==========================

What's New
----------

* Add :class:`SoftwareReset` and :class:`WatchdogTimer`.

Release 0.0.2 (2021-10-05)
==========================

Barely usable, but not very useful.

Release 0.0.1 (2021-09-29)
==========================

Just try to release, **do not use** this version...
