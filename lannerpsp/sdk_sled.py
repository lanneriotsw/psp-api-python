import logging
from ctypes import byref, c_uint8
from time import sleep

from .lmbinc import PSP

logger = logging.getLogger(__name__)


class SLED:
    """
    System/Status LED.

    sdk/src_utils/sdk_sled/sdk_sled.c
    """

    _ub_read = c_uint8(0xFF)

    @classmethod
    def off(cls) -> None:
        """Set System/Status LED to off."""
        with PSP() as psp:
            i_ret = psp.LMB_SLED_SetSystemLED(0)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetSystemLED", i_ret)
                return
            i_ret = psp.LMB_SLED_GetSystemLED(byref(cls._ub_read))
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_GetSystemLED", i_ret)
                return
            if cls._ub_read.value == 0:
                logger.info("set status led off")
            else:
                logger.warning("set status led failure")

    @classmethod
    def green(cls) -> None:
        """Set System/Status LED to green."""
        with PSP() as psp:
            i_ret = psp.LMB_SLED_SetSystemLED(1)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetSystemLED", i_ret)
                return
            i_ret = psp.LMB_SLED_GetSystemLED(byref(cls._ub_read))
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_GetSystemLED", i_ret)
                return
            if cls._ub_read.value == 1:
                logger.info("set status led green")
            else:
                logger.warning("set status led failure")

    @classmethod
    def red(cls) -> None:
        """Set System/Status LED to red/amber."""
        with PSP() as psp:
            i_ret = psp.LMB_SLED_SetSystemLED(2)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetSystemLED", i_ret)
                return
            i_ret = psp.LMB_SLED_GetSystemLED(byref(cls._ub_read))
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_GetSystemLED", i_ret)
                return
            if cls._ub_read.value == 2:
                logger.info("set status led red/amber")
            else:
                logger.warning("set status led failure")

    @classmethod
    def test(cls, seconds: float = 2.0) -> None:
        """For testing (default 2 seconds delay).

        :param seconds: seconds
        """
        with PSP() as psp:
            i_ret = psp.LMB_SLED_SetSystemLED(1)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetSystemLED", i_ret)
            else:
                logger.info("set status led green")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetSystemLED(2)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetSystemLED", i_ret)
            else:
                logger.info("set status led red/amber")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetSystemLED(0)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetSystemLED", i_ret)
            else:
                logger.info("set status led off")
