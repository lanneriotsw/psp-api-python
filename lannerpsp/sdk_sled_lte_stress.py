import logging
from time import sleep

from .lmbinc import PSP

logger = logging.getLogger(__name__)


class LteStressLED:
    """
    LTE Stress LED.

    sdk/src_utils/sdk_sled_lte_stress/sdk_sled_lte_stress.c

    :param lmb_io_path: path of liblmbio.so
    :param lmb_api_path: path of liblmbapi.so
    """

    def __init__(self,
                 lmb_io_path: str = "/opt/lanner/psp/bin/amd64/lib/liblmbio.so",
                 lmb_api_path: str = "/opt/lanner/psp/bin/amd64/lib/liblmbapi.so") -> None:
        self._lmb_io_path = lmb_io_path
        self._lmb_api_path = lmb_api_path

    def off(self) -> None:
        """Set LTE Stress LED to off."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_SLED_SetLteStressLED(-1)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStressLED", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.info("set lte stress led off")

    def set_strength(self, percent: int) -> None:
        """Set LTE Stress LED signal strength."""
        # Check type.
        if not isinstance(percent, int):
            raise TypeError("'percent' type must be int")
        # Check value.
        if not 0 <= percent <= 100:
            raise ValueError("'percent' value must be between 0 and 100")
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_SLED_SetLteStressLED(percent)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStressLED", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.info(f"set lte stress led {percent}%")

    def test(self, seconds: float = 2.0) -> None:
        """For testing (default 2 seconds delay).

        :param seconds: seconds
        """
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_SLED_SetLteStressLED(90)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStressLED", i_ret)
                logger.error(error_message)
            else:
                logger.info("lte stress led show level 8")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetLteStressLED(78)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStressLED", i_ret)
                logger.error(error_message)
            else:
                logger.info("lte stress led show level 7")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetLteStressLED(66)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStressLED", i_ret)
                logger.error(error_message)
            else:
                logger.info("lte stress led show level 6")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetLteStressLED(54)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStressLED", i_ret)
                logger.error(error_message)
            else:
                logger.info("lte stress led show level 5")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetLteStressLED(42)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStressLED", i_ret)
                logger.error(error_message)
            else:
                logger.info("lte stress led show level 4")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetLteStressLED(30)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStressLED", i_ret)
                logger.error(error_message)
            else:
                logger.info("lte stress led show level 3")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetLteStressLED(18)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStressLED", i_ret)
                logger.error(error_message)
            else:
                logger.info("lte stress led show level 2")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetLteStressLED(6)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStressLED", i_ret)
                logger.error(error_message)
            else:
                logger.info("lte stress led show level 1")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetLteStressLED(-1)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetLteStressLED", i_ret)
                logger.error(error_message)
            else:
                logger.info("set lte stress led off")
