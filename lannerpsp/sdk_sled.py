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

SUPPORTED_PLATFORMS = ("LEB-7242", "NCA-2510",)
UNSUPPORTED_PLATFORMS = ("LEB-2680", "LEC-2290", "LEC-7230", "V3S", "V6S",)


class SystemLED:
    """
    System LED.

    The LED colors is dependent on the platform hardware configuration.

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

    def get_status(self) -> int:
        """
        Get the system LED display mode status.

        Example:

        .. code-block:: pycon

            >>> system_led = SystemLED()
            >>> system_led.get_status()
            2

        :return: system LED status
        :rtype: int
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: General PSP functional error.
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

        .. code-block:: pycon

            >>> system_led = SystemLED()
            >>> system_led.off()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: General PSP functional error.
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

        .. code-block:: pycon

            >>> system_led = SystemLED()
            >>> system_led.green()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: General PSP functional error.
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

        .. code-block:: pycon

            >>> system_led = SystemLED()
            >>> system_led.red()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: General PSP functional error.
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

        .. code-block:: pycon

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
