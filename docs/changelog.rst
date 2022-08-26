=========
Changelog
=========

.. currentmodule:: lannerpsp

Release 0.0.6 (2022-08-??)
==========================

What's New
----------

* ??

Bug Fixes
----------

* ??

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
