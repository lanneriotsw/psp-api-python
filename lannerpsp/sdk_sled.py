import logging
from ctypes import byref, c_uint8

from .core import PSP, get_psp_exc_msg
from .exc import (
    PSPError,
    PSPInvalid,
    PSPNotOpened,
    PSPNotSupport,
)
from .lmbinc import (
    ERR_Invalid,
    ERR_NotOpened,
    ERR_NotSupport,
    ERR_Success,
)
from .sdk_dll import DLL
from .utils import show_delay

logger = logging.getLogger(__name__)


class SystemLED:
    """
    System LED.

    The LED colors is dependent on the platform hardware configuration.
    """

    def __init__(self) -> None:
        self._version = DLL().get_version()

    def get_status(self) -> int:
        """
        Get the system LED display mode status.

        Example:

        .. code-block:: python

            >>> system_led = SystemLED()
            >>> system_led.get_status()

        :return: system LED status
        :rtype: int
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: This function failed.
        """
        ub_read = c_uint8(0xFF)
        with PSP() as psp:
            i_ret = psp.lib.LMB_SLED_GetSystemLED(byref(ub_read))
        msg = get_psp_exc_msg("LMB_SLED_GetSystemLED", i_ret)
        if i_ret == ERR_Success:
            return ub_read.value
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def off(self) -> None:
        """
        Set the system LED display mode to off.

        Example:

        .. code-block:: python

            >>> system_led = SystemLED()
            >>> system_led.off()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: This function failed.
        """
        with PSP() as psp:
            i_ret = psp.lib.LMB_SLED_SetSystemLED(0)
        msg = get_psp_exc_msg("LMB_SLED_SetSystemLED", i_ret)
        if i_ret == ERR_Success:
            pass
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)
        # Check setting.
        if self.get_status() == 0:
            logger.debug("set status led off")
        else:
            logger.warning("set status led failure")

    def green(self) -> None:
        """
        Set the system LED display mode to green.

        Example:

        .. code-block:: python

            >>> system_led = SystemLED()
            >>> system_led.green()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: This function failed.
        """
        with PSP() as psp:
            i_ret = psp.lib.LMB_SLED_SetSystemLED(1)
        msg = get_psp_exc_msg("LMB_SLED_SetSystemLED", i_ret)
        if i_ret == ERR_Success:
            pass
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)
        # Check setting.
        if self.get_status() == 1:
            logger.debug("set status led green")
        else:
            logger.warning("set status led failure")

    def red(self) -> None:
        """
        Set the system LED display mode to red/amber.

        Example:

        .. code-block:: python

            >>> system_led = SystemLED()
            >>> system_led.red()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: This function failed.
        """
        with PSP() as psp:
            i_ret = psp.lib.LMB_SLED_SetSystemLED(2)
        msg = get_psp_exc_msg("LMB_SLED_SetSystemLED", i_ret)
        if i_ret == ERR_Success:
            pass
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)
        # Check setting.
        if self.get_status() == 2:
            logger.debug("set status led red/amber")
        else:
            logger.warning("set status led failure")

    def test(self, secs: int = 2) -> None:
        """
        For testing (default 2 seconds delay).

        Example:

        .. code-block:: python

            >>> system_led = SystemLED()
            >>> system_led.test()
            LMB_SLED_SetSystemLED: 0xffffffff: function failure
            2. 1. 0.
            set status led red/amber
            2. 1. 0.
            set status led off

        :param int secs: seconds for test
        :raises TypeError: The input parameters type error.
        :raises ValueError: The input parameters value error.
        """
        # Check type.
        if not isinstance(secs, int):
            raise TypeError("'secs' type must be int")
        # Check value.
        if secs <= 0:
            raise ValueError("'secs' value must be >= 0")
        # Run.
        with PSP() as psp:
            i_ret = psp.lib.LMB_SLED_SetSystemLED(1)
            if i_ret != ERR_Success:
                msg = get_psp_exc_msg("LMB_SLED_SetSystemLED", i_ret)
                print(f"\033[1;31m{msg}\033[0m")
            else:
                print("set status led green")

            show_delay(secs)

            i_ret = psp.lib.LMB_SLED_SetSystemLED(2)
            if i_ret != ERR_Success:
                msg = get_psp_exc_msg("LMB_SLED_SetSystemLED", i_ret)
                print(f"\033[1;31m{msg}\033[0m")
            else:
                print("set status led red/amber")

            show_delay(secs)

            i_ret = psp.lib.LMB_SLED_SetSystemLED(0)
            if i_ret != ERR_Success:
                msg = get_psp_exc_msg("LMB_SLED_SetSystemLED", i_ret)
                print(f"\033[1;31m{msg}\033[0m")
            else:
                print("set status led off")


class GPSStatusLED:
    """
    GPS Status LED.
    """

    def __init__(self) -> None:
        self._version = DLL().get_version()

    def off(self) -> None:
        """
        Set the GPS status LED display mode to off.

        Example:

        .. code-block:: python

            >>> gps_status_led = GPSStatusLED()
            >>> gps_status_led.off()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: This function failed.
        """
        with PSP() as psp:
            i_ret = psp.lib.LMB_SLED_SetGPSLED(0)
        msg = get_psp_exc_msg("LMB_SLED_SetGPSLED", i_ret)
        if i_ret == ERR_Success:
            logger.debug("set gps led off")
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def on(self) -> None:
        """
        Set the GPS status LED display mode to on.

        Example:

        .. code-block:: python

            >>> gps_status_led = GPSStatusLED()
            >>> gps_status_led.on()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: This function failed.
        """
        with PSP() as psp:
            i_ret = psp.lib.LMB_SLED_SetGPSLED(1)
        msg = get_psp_exc_msg("LMB_SLED_SetGPSLED", i_ret)
        if i_ret == ERR_Success:
            logger.debug("set gps led on")
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def blink(self) -> None:
        """
        Set the GPS status LED display mode to blink.

        Example:

        .. code-block:: python

            >>> gps_status_led = GPSStatusLED()
            >>> gps_status_led.blink()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: This function failed.
        """
        with PSP() as psp:
            i_ret = psp.lib.LMB_SLED_SetGPSLED(2)
        msg = get_psp_exc_msg("LMB_SLED_SetGPSLED", i_ret)
        if i_ret == ERR_Success:
            logger.debug("set gps led blink")
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def test(self, secs: int = 2) -> None:
        """
        For testing (default 2 seconds delay).

        Example:

        .. code-block:: python

            >>> gps_status_led = GPSStatusLED()
            >>> gps_status_led.test()
            set gps led on
            2. 1. 0.
            set gps led blink
            2. 1. 0.
            set gps led off

        :param int secs: seconds for test
        :raises TypeError: The input parameters type error.
        :raises ValueError: The input parameters value error.
        """
        # Check type.
        if not isinstance(secs, int):
            raise TypeError("'secs' type must be int")
        # Check value.
        if secs <= 0:
            raise ValueError("'secs' value must be >= 0")
        # Run.
        with PSP() as psp:
            i_ret = psp.lib.LMB_SLED_SetGPSLED(1)
            if i_ret != ERR_Success:
                msg = get_psp_exc_msg("LMB_SLED_SetGPSLED", i_ret)
                print(f"\033[1;31m{msg}\033[0m")
            else:
                print("set gps led on")

            show_delay(secs)

            i_ret = psp.lib.LMB_SLED_SetGPSLED(2)
            if i_ret != ERR_Success:
                msg = get_psp_exc_msg("LMB_SLED_SetGPSLED", i_ret)
                print(f"\033[1;31m{msg}\033[0m")
            else:
                print("set gps led blink")

            show_delay(secs)

            i_ret = psp.lib.LMB_SLED_SetGPSLED(0)
            if i_ret != ERR_Success:
                msg = get_psp_exc_msg("LMB_SLED_SetGPSLED", i_ret)
                print(f"\033[1;31m{msg}\033[0m")
            else:
                print("set gps led off")


class LteStatusLED:
    """
    LTE Status LED.
    """

    def __init__(self) -> None:
        self._version = DLL().get_version()

    def off(self) -> None:
        """
        Set the LTE status LED display mode to off.

        Example:

        .. code-block:: python

            >>> lte_status_led = LteStatusLED()
            >>> lte_status_led.off()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: This function failed.
        """
        with PSP() as psp:
            i_ret = psp.lib.LMB_SLED_SetLteStateLED(0)
        msg = get_psp_exc_msg("LMB_SLED_SetLteStateLED", i_ret)
        if i_ret == ERR_Success:
            logger.debug("set lte led off")
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def red(self) -> None:
        """
        Set the LTE status LED display mode to red.

        Example:

        .. code-block:: python

            >>> lte_status_led = LteStatusLED()
            >>> lte_status_led.red()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: This function failed.
        """
        self.off()  # Clear color.
        with PSP() as psp:
            i_ret = psp.lib.LMB_SLED_SetLteStateLED(1)
        msg = get_psp_exc_msg("LMB_SLED_SetLteStateLED", i_ret)
        if i_ret == ERR_Success:
            logger.debug("set lte led red on")
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def red_blink(self) -> None:
        """
        Set the LTE status LED display mode to red blink.

        Example:

        .. code-block:: python

            >>> lte_status_led = LteStatusLED()
            >>> lte_status_led.red_blink()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: This function failed.
        """
        self.off()  # Clear color.
        with PSP() as psp:
            i_ret = psp.lib.LMB_SLED_SetLteStateLED(2)
        msg = get_psp_exc_msg("LMB_SLED_SetLteStateLED", i_ret)
        if i_ret == ERR_Success:
            logger.debug("set lte led red blink")
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def green(self) -> None:
        """
        Set the LTE status LED display mode to green.

        Example:

        .. code-block:: python

            >>> lte_status_led = LteStatusLED()
            >>> lte_status_led.green()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: This function failed.
        """
        self.off()  # Clear color.
        with PSP() as psp:
            i_ret = psp.lib.LMB_SLED_SetLteStateLED(3)
        msg = get_psp_exc_msg("LMB_SLED_SetLteStateLED", i_ret)
        if i_ret == ERR_Success:
            logger.debug("set lte led green on")
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def green_blink(self) -> None:
        """
        Set the LTE status LED display mode to green blink.

        Example:

        .. code-block:: python

            >>> lte_status_led = LteStatusLED()
            >>> lte_status_led.green_blink()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: This function failed.
        """
        self.off()  # Clear color.
        with PSP() as psp:
            i_ret = psp.lib.LMB_SLED_SetLteStateLED(4)
        msg = get_psp_exc_msg("LMB_SLED_SetLteStateLED", i_ret)
        if i_ret == ERR_Success:
            logger.debug("set lte led green blink")
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def yellow(self) -> None:
        """
        Set the LTE status LED display mode to yellow.

        Example:

        .. code-block:: python

            >>> lte_status_led = LteStatusLED()
            >>> lte_status_led.yellow()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: This function failed.
        """
        self.off()  # Clear color.
        with PSP() as psp:
            i_ret = psp.lib.LMB_SLED_SetLteStateLED(5)
        msg = get_psp_exc_msg("LMB_SLED_SetLteStateLED", i_ret)
        if i_ret == ERR_Success:
            logger.debug("set lte led yellow on")
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def yellow_blink(self) -> None:
        """
        Set the LTE status LED display mode to yellow blink.

        Example:

        .. code-block:: python

            >>> lte_status_led = LteStatusLED()
            >>> lte_status_led.yellow_blink()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: This function failed.
        """
        self.off()  # Clear color.
        with PSP() as psp:
            i_ret = psp.lib.LMB_SLED_SetLteStateLED(6)
        msg = get_psp_exc_msg("LMB_SLED_SetLteStateLED", i_ret)
        if i_ret == ERR_Success:
            logger.debug("set lte led yellow blink")
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def test(self, secs: int = 2) -> None:
        """
        For testing (default 2 seconds delay).

        Example:

        .. code-block:: python

            >>> lte_status_led = LteStatusLED()
            >>> lte_status_led.test()
            set lte led red on
            2. 1. 0.
            set lte led red blink
            2. 1. 0.
            set lte led off
            2. 1. 0.
            set lte led green on
            2. 1. 0.
            set lte led green blink
            2. 1. 0.
            set lte led off
            2. 1. 0.
            set lte led yellow on
            2. 1. 0.
            set lte led yellow blink
            2. 1. 0.
            set lte led off

        :param int secs: seconds for test
        :raises TypeError: The input parameters type error.
        :raises ValueError: The input parameters value error.
        """
        # Check type.
        if not isinstance(secs, int):
            raise TypeError("'secs' type must be int")
        # Check value.
        if secs <= 0:
            raise ValueError("'secs' value must be >= 0")
        # Run.
        with PSP() as psp:
            i_ret = psp.lib.LMB_SLED_SetLteStateLED(1)
            if i_ret != ERR_Success:
                msg = get_psp_exc_msg("LMB_SLED_SetLteStateLED", i_ret)
                print(f"\033[1;31m{msg}\033[0m")
            else:
                print("set lte led red on")

            show_delay(secs)

            i_ret = psp.lib.LMB_SLED_SetLteStateLED(2)
            if i_ret != ERR_Success:
                msg = get_psp_exc_msg("LMB_SLED_SetLteStateLED", i_ret)
                print(f"\033[1;31m{msg}\033[0m")
            else:
                print("set lte led red blink")

            show_delay(secs)

            i_ret = psp.lib.LMB_SLED_SetLteStateLED(0)
            if i_ret != ERR_Success:
                msg = get_psp_exc_msg("LMB_SLED_SetLteStateLED", i_ret)
                print(f"\033[1;31m{msg}\033[0m")
            else:
                print("set lte led off")

            show_delay(secs)

            i_ret = psp.lib.LMB_SLED_SetLteStateLED(3)
            if i_ret != ERR_Success:
                msg = get_psp_exc_msg("LMB_SLED_SetLteStateLED", i_ret)
                print(f"\033[1;31m{msg}\033[0m")
            else:
                print("set lte led green on")

            show_delay(secs)

            i_ret = psp.lib.LMB_SLED_SetLteStateLED(4)
            if i_ret != ERR_Success:
                msg = get_psp_exc_msg("LMB_SLED_SetLteStateLED", i_ret)
                print(f"\033[1;31m{msg}\033[0m")
            else:
                print("set lte led green blink")

            show_delay(secs)

            i_ret = psp.lib.LMB_SLED_SetLteStateLED(0)
            if i_ret != ERR_Success:
                msg = get_psp_exc_msg("LMB_SLED_SetLteStateLED", i_ret)
                print(f"\033[1;31m{msg}\033[0m")
            else:
                print("set lte led off")

            show_delay(secs)

            i_ret = psp.lib.LMB_SLED_SetLteStateLED(5)
            if i_ret != ERR_Success:
                msg = get_psp_exc_msg("LMB_SLED_SetLteStateLED", i_ret)
                print(f"\033[1;31m{msg}\033[0m")
            else:
                print("set lte led yellow on")

            show_delay(secs)

            i_ret = psp.lib.LMB_SLED_SetLteStateLED(6)
            if i_ret != ERR_Success:
                msg = get_psp_exc_msg("LMB_SLED_SetLteStateLED", i_ret)
                print(f"\033[1;31m{msg}\033[0m")
            else:
                print("set lte led yellow blink")

            show_delay(secs)

            i_ret = psp.lib.LMB_SLED_SetLteStateLED(0)
            if i_ret != ERR_Success:
                msg = get_psp_exc_msg("LMB_SLED_SetLteStateLED", i_ret)
                print(f"\033[1;31m{msg}\033[0m")
            else:
                print("set lte led off")


class LteStressLED:
    """
    LTE Stress LED.
    """

    def __init__(self) -> None:
        self._version = DLL().get_version()

    def off(self) -> None:
        """
        Set the LTE stress LED display mode to off.

        Example:

        .. code-block:: python

            >>> lte_stress_led = LteStressLED()
            >>> lte_stress_led.off()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: This function failed.
        """
        with PSP() as psp:
            i_ret = psp.lib.LMB_SLED_SetLteStressLED(-1)
        msg = get_psp_exc_msg("LMB_SLED_SetLteStressLED", i_ret)
        if i_ret == ERR_Success:
            logger.debug("set lte stress led off")
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def set_strength(self, percent: int) -> None:
        """
        Set the LTE stress LED signal strength.

        Example:

        .. code-block:: python

            >>> lte_stress_led = LteStressLED()
            >>> lte_stress_led.set_strength(87)

        :param int percent: 0 ~ 100 percent of signal strength
        :raises TypeError: The input parameters type error.
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: This function failed.
        """
        # Check type.
        if not isinstance(percent, int):
            raise TypeError("'percent' type must be int")
        # Check value.
        if not 0 <= percent <= 100:
            raise PSPInvalid("'percent' value must be between 0 and 100")
        # Run.
        with PSP() as psp:
            i_ret = psp.lib.LMB_SLED_SetLteStressLED(percent)
        msg = get_psp_exc_msg("LMB_SLED_SetLteStressLED", i_ret)
        if i_ret == ERR_Success:
            logger.debug(f"set lte stress led {percent:d}%")
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def test(self, secs: int = 2) -> None:
        """
        For testing (default 2 seconds delay).

        Example:

        .. code-block:: python

            >>> lte_stress_led = LteStressLED()
            >>> lte_stress_led.test(2)
            lte stress led show level 8
            2. 1. 0.
            lte stress led show level 7
            2. 1. 0.
            lte stress led show level 6
            2. 1. 0.
            lte stress led show level 5
            2. 1. 0.
            lte stress led show level 4
            2. 1. 0.
            lte stress led show level 3
            2. 1. 0.
            lte stress led show level 2
            2. 1. 0.
            lte stress led show level 1
            2. 1. 0.
            set lte stress led off

        :param int secs: seconds for test
        :raises TypeError: The input parameters type error.
        :raises ValueError: The input parameters value error.
        """
        # Check type.
        if not isinstance(secs, int):
            raise TypeError("'secs' type must be int")
        # Check value.
        if secs <= 0:
            raise ValueError("'secs' value must be >= 0")
        # Run.
        with PSP() as psp:
            i_ret = psp.lib.LMB_SLED_SetLteStressLED(90)
            if i_ret != ERR_Success:
                msg = get_psp_exc_msg("LMB_SLED_SetLteStressLED", i_ret)
                print(f"\033[1;31m{msg}\033[0m")
            else:
                print("lte stress led show level 8")

            show_delay(secs)

            i_ret = psp.lib.LMB_SLED_SetLteStressLED(78)
            if i_ret != ERR_Success:
                msg = get_psp_exc_msg("LMB_SLED_SetLteStressLED", i_ret)
                print(f"\033[1;31m{msg}\033[0m")
            else:
                print("lte stress led show level 7")

            show_delay(secs)

            i_ret = psp.lib.LMB_SLED_SetLteStressLED(66)
            if i_ret != ERR_Success:
                msg = get_psp_exc_msg("LMB_SLED_SetLteStressLED", i_ret)
                print(f"\033[1;31m{msg}\033[0m")
            else:
                print("lte stress led show level 6")

            show_delay(secs)

            i_ret = psp.lib.LMB_SLED_SetLteStressLED(54)
            if i_ret != ERR_Success:
                msg = get_psp_exc_msg("LMB_SLED_SetLteStressLED", i_ret)
                print(f"\033[1;31m{msg}\033[0m")
            else:
                print("lte stress led show level 5")

            show_delay(secs)

            i_ret = psp.lib.LMB_SLED_SetLteStressLED(42)
            if i_ret != ERR_Success:
                msg = get_psp_exc_msg("LMB_SLED_SetLteStressLED", i_ret)
                print(f"\033[1;31m{msg}\033[0m")
            else:
                print("lte stress led show level 4")

            show_delay(secs)

            i_ret = psp.lib.LMB_SLED_SetLteStressLED(30)
            if i_ret != ERR_Success:
                msg = get_psp_exc_msg("LMB_SLED_SetLteStressLED", i_ret)
                print(f"\033[1;31m{msg}\033[0m")
            else:
                print("lte stress led show level 3")

            show_delay(secs)

            i_ret = psp.lib.LMB_SLED_SetLteStressLED(18)
            if i_ret != ERR_Success:
                msg = get_psp_exc_msg("LMB_SLED_SetLteStressLED", i_ret)
                print(f"\033[1;31m{msg}\033[0m")
            else:
                print("lte stress led show level 2")

            show_delay(secs)

            i_ret = psp.lib.LMB_SLED_SetLteStressLED(6)
            if i_ret != ERR_Success:
                msg = get_psp_exc_msg("LMB_SLED_SetLteStressLED", i_ret)
                print(f"\033[1;31m{msg}\033[0m")
            else:
                print("lte stress led show level 1")

            show_delay(secs)

            i_ret = psp.lib.LMB_SLED_SetLteStressLED(-1)
            if i_ret != ERR_Success:
                msg = get_psp_exc_msg("LMB_SLED_SetLteStressLED", i_ret)
                print(f"\033[1;31m{msg}\033[0m")
            else:
                print("set lte stress led off")
