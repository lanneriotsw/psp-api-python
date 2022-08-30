=========
Changelog
=========

.. currentmodule:: lannerpsp

Release 0.0.8 (2022-08-30)
==========================

What's New
----------

* Add :file:`recipes` with beautiful pictures.
* Remove LICENSE block shown in PyPi.

Bug Fixes
----------

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
* Add :meth:`WDT.enable`.
* Add ``time_base`` setting to :meth:`WDT.config` and :meth:`WDT.enable`.
* Add PSP 3.0.0 support for `LEC-7230M`_.
* Update test cases.

Bug Fixes
----------

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
----------

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
----------

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
