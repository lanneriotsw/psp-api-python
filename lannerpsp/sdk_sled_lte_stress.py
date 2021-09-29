import logging
from time import sleep

from .lmbinc import PSP

logger = logging.getLogger(__name__)


class SLEDLTEStress:
    """
    LTE Stress LED.

    sdk/src_utils/sdk_sled_lte_stress/sdk_sled_lte_stress.c
    """

    @classmethod
    def off(cls) -> None:
        """Set LTE Stress LED to off."""
        with PSP() as psp:
            i_ret = psp.LMB_SLED_SetLteStressLED(-1)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStressLED", i_ret)
                return
            logger.info("set lte stress led off")

    @classmethod
    def set_strength(cls, percent: int):
        """Set LTE Stress LED signal strength."""
        with PSP() as psp:
            i_ret = psp.LMB_SLED_SetLteStressLED(percent)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStressLED", i_ret)
            logger.info(f"set lte stress led {percent}%")

    @classmethod
    def test(cls, seconds: float = 2.0) -> None:
        """For testing (default 2 seconds delay).

        :param seconds: seconds
        """
        with PSP() as psp:
            i_ret = psp.LMB_SLED_SetLteStressLED(90)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStressLED", i_ret)
            else:
                logger.info("lte stress led show level 8")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetLteStressLED(78)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStressLED", i_ret)
            else:
                logger.info("lte stress led show level 7")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetLteStressLED(66)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStressLED", i_ret)
            else:
                logger.info("lte stress led show level 6")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetLteStressLED(54)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStressLED", i_ret)
            else:
                logger.info("lte stress led show level 5")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetLteStressLED(42)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStressLED", i_ret)
            else:
                logger.info("lte stress led show level 4")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetLteStressLED(30)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStressLED", i_ret)
            else:
                logger.info("lte stress led show level 3")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetLteStressLED(18)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStressLED", i_ret)
            else:
                logger.info("lte stress led show level 2")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetLteStressLED(6)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStressLED", i_ret)
            else:
                logger.info("lte stress led show level 1")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetLteStressLED(-1)
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_SLED_SetLteStressLED", i_ret)
            else:
                logger.info("set lte stress led off")

            sleep(seconds)
