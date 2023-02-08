import logging

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

SUPPORTED_PLATFORMS = ("LEB-7242",)
UNSUPPORTED_PLATFORMS = ("LEB-2680", "LEC-2290", "LEC-7230", "NCA-2510", "V3S", "V6S",)


class GPSStatusLED:
    """
    GPS Status LED.

    :param bool check_platform:
        Set to :data:`True` to check if the platform supports this feature.
        Defaults to :data:`False` for better compatibility.
    :raises PSPNotSupport: This function is not supported
        (when ``check_platform`` is set to :data:`True`).
    :raises NotImplementedError: It has not been verified to run on this platform
        (when ``check_platform`` is set to :data:`True`).
    """

    def __init__(self, check_platform: bool = False) -> None:
        self._version = DLL().get_version()
        if not check_platform:
            return
        if self._version.platform_id in SUPPORTED_PLATFORMS:
            pass
        elif self._version.platform_id in UNSUPPORTED_PLATFORMS:
            raise PSPNotSupport("Not supported on this platform")
        else:
            raise NotImplementedError

    def off(self) -> None:
        """
        Set the GPS status LED display mode to off.

        Example:

        .. code-block:: pycon

            >>> gps_status_led = GPSStatusLED()
            >>> gps_status_led.off()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: General PSP functional error.
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

        .. code-block:: pycon

            >>> gps_status_led = GPSStatusLED()
            >>> gps_status_led.on()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: General PSP functional error.
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

        .. code-block:: pycon

            >>> gps_status_led = GPSStatusLED()
            >>> gps_status_led.blink()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: General PSP functional error.
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

        .. code-block:: pycon

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
