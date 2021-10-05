import logging
from ctypes import byref, c_uint8
from time import sleep

from .lmbinc import PSP

logger = logging.getLogger(__name__)


class SystemLED:
    """
    System/Status LED.

    sdk/src_utils/sdk_sled/sdk_sled.c

    :param lmb_io_path: path of liblmbio.so
    :param lmb_api_path: path of liblmbapi.so
    """

    def __init__(self,
                 lmb_io_path: str = "/opt/lanner/psp/bin/amd64/lib/liblmbio.so",
                 lmb_api_path: str = "/opt/lanner/psp/bin/amd64/lib/liblmbapi.so") -> None:
        self._lmb_io_path = lmb_io_path
        self._lmb_api_path = lmb_api_path
        self._ub_read = c_uint8(0xFF)

    def off(self) -> None:
        """Set System/Status LED to off."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_SLED_SetSystemLED(0)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetSystemLED", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            i_ret = psp.LMB_SLED_GetSystemLED(byref(self._ub_read))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_GetSystemLED", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            if self._ub_read.value == 0:
                logger.info("set status led off")
            else:
                logger.warning("set status led failure")

    def green(self) -> None:
        """Set System/Status LED to green."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_SLED_SetSystemLED(1)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetSystemLED", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            i_ret = psp.LMB_SLED_GetSystemLED(byref(self._ub_read))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_GetSystemLED", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            if self._ub_read.value == 1:
                logger.info("set status led green")
            else:
                logger.warning("set status led failure")

    def red(self) -> None:
        """Set System/Status LED to red/amber."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_SLED_SetSystemLED(2)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetSystemLED", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            i_ret = psp.LMB_SLED_GetSystemLED(byref(self._ub_read))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_GetSystemLED", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            if self._ub_read.value == 2:
                logger.info("set status led red/amber")
            else:
                logger.warning("set status led failure")

    def test(self, seconds: float = 2.0) -> None:
        """For testing (default 2 seconds delay).

        :param seconds: seconds
        """
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_SLED_SetSystemLED(1)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetSystemLED", i_ret)
                logger.error(error_message)
            else:
                logger.info("set status led green")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetSystemLED(2)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetSystemLED", i_ret)
                logger.error(error_message)
            else:
                logger.info("set status led red/amber")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetSystemLED(0)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetSystemLED", i_ret)
                logger.error(error_message)
            else:
                logger.info("set status led off")
