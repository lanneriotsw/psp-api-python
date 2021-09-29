import logging
from time import sleep

from .lmbinc import PSP

logger = logging.getLogger(__name__)


class SLEDGPS:
    """
    GPS Status LED.

    sdk/src_utils/sdk_sled_gps/sdk_sled_gps.c
    """

    @classmethod
    def off(cls) -> None:
        """Set GPS Status LED to off."""
        with PSP() as psp:
            i_ret = psp.LMB_SLED_SetGPSLED(0)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetGPSLED", i_ret)
                return
            logger.info("set gps led off")

    @classmethod
    def on(cls) -> None:
        """Set GPS Status LED to on."""
        with PSP() as psp:
            i_ret = psp.LMB_SLED_SetGPSLED(1)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetGPSLED", i_ret)
                return
            logger.info("set gps led on")

    @classmethod
    def blink(cls) -> None:
        """Set GPS Status LED to blink."""
        with PSP() as psp:
            i_ret = psp.LMB_SLED_SetGPSLED(2)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetGPSLED", i_ret)
                return
            logger.info("set gps led blink")

    @classmethod
    def test(cls, seconds: float = 2.0) -> None:
        """For testing (default 2 seconds delay).

        :param seconds: seconds
        """
        with PSP() as psp:
            i_ret = psp.LMB_SLED_SetGPSLED(1)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetGPSLED", i_ret)
            else:
                logger.info("set gps led on")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetGPSLED(2)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetGPSLED", i_ret)
            else:
                logger.info("set gps led blink")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetGPSLED(0)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetGPSLED", i_ret)
            else:
                logger.info("set gps led off")

            sleep(seconds)
