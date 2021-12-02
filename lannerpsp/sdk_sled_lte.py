import logging

from .lmbinc import PSP
from .utils import show_delay

logger = logging.getLogger(__name__)


class LteStateLED:
    """
    LTE Status LED.

    sdk/src_utils/sdk_sled_lte/sdk_sled_lte.c

    :param lmb_io_path: path of liblmbio.so
    :param lmb_api_path: path of liblmbapi.so
    """

    def __init__(self,
                 lmb_io_path: str = "/opt/lanner/psp/bin/amd64/lib/liblmbio.so",
                 lmb_api_path: str = "/opt/lanner/psp/bin/amd64/lib/liblmbapi.so") -> None:
        self._lmb_io_path = lmb_io_path
        self._lmb_api_path = lmb_api_path

    def off(self) -> None:
        """Set LTE Status LED to off."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_SLED_SetLteStateLED(0)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStateLED", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.debug("set lte led off")

    def red(self) -> None:
        """Set LTE Status LED to red."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_SLED_SetLteStateLED(0)  # Clear color.
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStateLED", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            i_ret = psp.lib.LMB_SLED_SetLteStateLED(1)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStateLED", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.debug("set lte led red on")

    def red_blink(self) -> None:
        """Set LTE Status LED to red blink."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_SLED_SetLteStateLED(0)  # Clear color.
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStateLED", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            i_ret = psp.lib.LMB_SLED_SetLteStateLED(2)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStateLED", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.debug("set lte led red blink")

    def green(self) -> None:
        """Set LTE Status LED to green."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_SLED_SetLteStateLED(0)  # Clear color.
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStateLED", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            i_ret = psp.lib.LMB_SLED_SetLteStateLED(3)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStateLED", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.debug("set lte led green on")

    def green_blink(self) -> None:
        """Set LTE Status LED to green blink."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_SLED_SetLteStateLED(0)  # Clear color.
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStateLED", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            i_ret = psp.lib.LMB_SLED_SetLteStateLED(4)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStateLED", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.debug("set lte led green blink")

    def yellow(self) -> None:
        """Set LTE Status LED to yellow."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_SLED_SetLteStateLED(0)  # Clear color.
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStateLED", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            i_ret = psp.lib.LMB_SLED_SetLteStateLED(5)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStateLED", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.debug("set lte led yellow on")

    def yellow_blink(self) -> None:
        """Set LTE Status LED to yellow blink."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_SLED_SetLteStateLED(0)  # Clear color.
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStateLED", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            i_ret = psp.lib.LMB_SLED_SetLteStateLED(6)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStateLED", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.debug("set lte led yellow blink")

    def test(self, seconds: int = 2) -> None:
        """For testing (default 2 seconds delay).

        :param seconds: seconds
        """
        # Check type.
        if not isinstance(seconds, int):
            raise TypeError("'seconds' type must be int")
        # Check value.
        if seconds <= 0:
            raise ValueError("'seconds' value must be >= 0")
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_SLED_SetLteStateLED(1)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStateLED", i_ret)
                print(f"\033[1;31m{error_message}\033[0m")
            else:
                print("set lte led red on")

            show_delay(seconds)

            i_ret = psp.lib.LMB_SLED_SetLteStateLED(2)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStateLED", i_ret)
                print(f"\033[1;31m{error_message}\033[0m")
            else:
                print("set lte led red blink")

            show_delay(seconds)

            i_ret = psp.lib.LMB_SLED_SetLteStateLED(0)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStateLED", i_ret)
                print(f"\033[1;31m{error_message}\033[0m")
            else:
                print("set lte led off")

            show_delay(seconds)

            i_ret = psp.lib.LMB_SLED_SetLteStateLED(3)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStateLED", i_ret)
                print(f"\033[1;31m{error_message}\033[0m")
            else:
                print("set lte led green on")

            show_delay(seconds)

            i_ret = psp.lib.LMB_SLED_SetLteStateLED(4)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStateLED", i_ret)
                print(f"\033[1;31m{error_message}\033[0m")
            else:
                print("set lte led green blink")

            show_delay(seconds)

            i_ret = psp.lib.LMB_SLED_SetLteStateLED(0)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStateLED", i_ret)
                print(f"\033[1;31m{error_message}\033[0m")
            else:
                print("set lte led off")

            show_delay(seconds)

            i_ret = psp.lib.LMB_SLED_SetLteStateLED(5)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStateLED", i_ret)
                print(f"\033[1;31m{error_message}\033[0m")
            else:
                print("set lte led yellow on")

            show_delay(seconds)

            i_ret = psp.lib.LMB_SLED_SetLteStateLED(6)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStateLED", i_ret)
                print(f"\033[1;31m{error_message}\033[0m")
            else:
                print("set lte led yellow blink")

            show_delay(seconds)

            i_ret = psp.lib.LMB_SLED_SetLteStateLED(0)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStateLED", i_ret)
                print(f"\033[1;31m{error_message}\033[0m")
            else:
                print("set lte led off")
