import logging
from time import sleep

from .lmbinc import PSP

logger = logging.getLogger(__name__)


class GPSLED:
    """
    GPS Status LED.

    sdk/src_utils/sdk_sled_gps/sdk_sled_gps.c

    :param lmb_io_path: path of liblmbio.so
    :param lmb_api_path: path of liblmbapi.so
    """

    def __init__(self,
                 lmb_io_path: str = "/opt/lanner/psp/bin/amd64/lib/liblmbio.so",
                 lmb_api_path: str = "/opt/lanner/psp/bin/amd64/lib/liblmbapi.so") -> None:
        self._lmb_io_path = lmb_io_path
        self._lmb_api_path = lmb_api_path

    def off(self) -> None:
        """Set GPS Status LED to off."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_SLED_SetGPSLED(0)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetGPSLED", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.info("set gps led off")

    def on(self) -> None:
        """Set GPS Status LED to on."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_SLED_SetGPSLED(1)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetGPSLED", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.info("set gps led on")

    def blink(self) -> None:
        """Set GPS Status LED to blink."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_SLED_SetGPSLED(2)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetGPSLED", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.info("set gps led blink")

    def test(self, seconds: float = 2.0) -> None:
        """For testing (default 2 seconds delay).

        :param seconds: seconds
        """
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_SLED_SetGPSLED(1)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetGPSLED", i_ret)
                logger.error(error_message)
            else:
                logger.info("set gps led on")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetGPSLED(2)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetGPSLED", i_ret)
                logger.error(error_message)
            else:
                logger.info("set gps led blink")

            sleep(seconds)

            i_ret = psp.LMB_SLED_SetGPSLED(0)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SLED_SetGPSLED", i_ret)
                logger.error(error_message)
            else:
                logger.info("set gps led off")
