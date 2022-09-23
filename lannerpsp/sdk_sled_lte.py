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
UNSUPPORTED_PLATFORMS = ("LEC-7230", "NCA-2510", "V3S", "V6S",)


class LTEStatusLED:
    """
    LTE Status LED.

    :param bool check_platform:
        Set to :data:`True` to check if the platform supports this feature.
        Defaults to :data:`False` for better compatibility.
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
        Set the LTE status LED display mode to off.

        Example:

        .. code-block:: pycon

            >>> lte_status_led = LTEStatusLED()
            >>> lte_status_led.off()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: General PSP functional error.
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

        .. code-block:: pycon

            >>> lte_status_led = LTEStatusLED()
            >>> lte_status_led.red()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: General PSP functional error.
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

        .. code-block:: pycon

            >>> lte_status_led = LTEStatusLED()
            >>> lte_status_led.red_blink()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: General PSP functional error.
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

        .. code-block:: pycon

            >>> lte_status_led = LTEStatusLED()
            >>> lte_status_led.green()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: General PSP functional error.
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

        .. code-block:: pycon

            >>> lte_status_led = LTEStatusLED()
            >>> lte_status_led.green_blink()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: General PSP functional error.
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

        .. code-block:: pycon

            >>> lte_status_led = LTEStatusLED()
            >>> lte_status_led.yellow()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: General PSP functional error.
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

        .. code-block:: pycon

            >>> lte_status_led = LTEStatusLED()
            >>> lte_status_led.yellow_blink()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: General PSP functional error.
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

        .. code-block:: pycon

            >>> lte_status_led = LTEStatusLED()
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
