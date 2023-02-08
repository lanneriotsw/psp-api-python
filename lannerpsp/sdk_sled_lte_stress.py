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


class LTEStressLED:
    """
    LTE Stress LED.

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
        Set the LTE stress LED display mode to off.

        Example:

        .. code-block:: pycon

            >>> lte_stress_led = LTEStressLED()
            >>> lte_stress_led.off()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: General PSP functional error.
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

        .. code-block:: pycon

            >>> lte_stress_led = LTEStressLED()
            >>> lte_stress_led.set_strength(87)

        :param int percent: 0 ~ 100 percent of signal strength
        :raises TypeError: The input parameters type error.
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: General PSP functional error.
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

        .. code-block:: pycon

            >>> lte_stress_led = LTEStressLED()
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
