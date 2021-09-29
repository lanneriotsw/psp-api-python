import logging
from time import sleep

from .lmbinc import PSP

logger = logging.getLogger(__name__)


class SLEDLTE:
    """
    LTE Status LED.

    sdk/src_utils/sdk_sled_lte/sdk_sled_lte.c
    """

    @classmethod
    def off(cls) -> None:
        """Set LTE Status LED to off."""
        with PSP() as psp:
            i_ret = psp.LMB_SLED_SetLteStateLED(0)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
                return
            logger.info("set lte led off")

    @classmethod
    def red(cls) -> None:
        """Set LTE Status LED to red."""
        with PSP() as psp:
            i_ret = psp.LMB_SLED_SetLteStateLED(0)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
                return
            i_ret = psp.LMB_SLED_SetLteStateLED(1)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
                return
            logger.info("set lte led red on")

    @classmethod
    def red_blink(cls) -> None:
        """Set LTE Status LED to red blink."""
        with PSP() as psp:
            i_ret = psp.LMB_SLED_SetLteStateLED(0)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
                return
            i_ret = psp.LMB_SLED_SetLteStateLED(2)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
                return
            logger.info("set lte led red blink")

    @classmethod
    def green(cls) -> None:
        """Set LTE Status LED to green."""
        with PSP() as psp:
            i_ret = psp.LMB_SLED_SetLteStateLED(0)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
                return
            i_ret = psp.LMB_SLED_SetLteStateLED(3)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
                return
            logger.info("set lte led green on")

    @classmethod
    def green_blink(cls) -> None:
        """Set LTE Status LED to green blink."""
        with PSP() as psp:
            i_ret = psp.LMB_SLED_SetLteStateLED(0)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
                return
            i_ret = psp.LMB_SLED_SetLteStateLED(4)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
                return
            logger.info("set lte led green blink")

    @classmethod
    def yellow(cls) -> None:
        """Set LTE Status LED to yellow."""
        with PSP() as psp:
            i_ret = psp.LMB_SLED_SetLteStateLED(0)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
                return
            i_ret = psp.LMB_SLED_SetLteStateLED(5)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
                return
            logger.info("set lte led yellow on")

    @classmethod
    def yellow_blink(cls) -> None:
        """Set LTE Status LED to yellow blink."""
        with PSP() as psp:
            i_ret = psp.LMB_SLED_SetLteStateLED(0)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
                return
            i_ret = psp.LMB_SLED_SetLteStateLED(6)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
                return
            logger.info("set lte led yellow blink")

    @classmethod
    def test(cls, seconds: float = 2.0) -> None:
        """For testing (default 2 seconds delay).

        :param seconds: seconds
        """
        with PSP() as psp:
            i_ret = psp.LMB_SLED_SetLteStateLED(1)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
            else:
                logger.info("set lte led red on")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetLteStateLED(2)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
            else:
                logger.info("set lte led red blink")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetLteStateLED(0)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
            else:
                logger.info("set lte led off")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetLteStateLED(3)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
            else:
                logger.info("set lte led green on")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetLteStateLED(4)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
            else:
                logger.info("set lte led green blink")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetLteStateLED(0)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
            else:
                logger.info("set lte led off")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetLteStateLED(5)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
            else:
                logger.info("set lte led yellow on")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetLteStateLED(6)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
            else:
                logger.info("set lte led yellow blink")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetLteStateLED(0)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
            else:
                logger.info("set lte led off")

            sleep(seconds)
