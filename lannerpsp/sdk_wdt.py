import logging

from .lmbinc import PSP

logger = logging.getLogger(__name__)


class WatchdogTimer:
    """
    Watchdog Timer.

    sdk/src_utils/sdk_sled/sdk_wdt.c

    :param lmb_io_path: path of liblmbio.so
    :param lmb_api_path: path of liblmbapi.so
    """

    def __init__(self,
                 lmb_io_path: str = "/opt/lanner/psp/bin/amd64/lib/liblmbio.so",
                 lmb_api_path: str = "/opt/lanner/psp/bin/amd64/lib/liblmbapi.so") -> None:
        self._lmb_io_path = lmb_io_path
        self._lmb_api_path = lmb_api_path

    def enable(self, seconds: int) -> None:
        """Enable watchdog timer for specific seconds.

        :param seconds: seconds
        """
        # Check type.
        if not isinstance(seconds, int):
            raise TypeError("'seconds' type must be int")
        # Check value.
        if seconds <= 0:
            raise ValueError("'seconds' value must be > 0")
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_WDT_Config(seconds, 1)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_WDT_Config", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            i_ret = psp.LMB_WDT_Start()
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_WDT_Start", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.info(f"enable watchdog timer for {seconds:d} seconds")

    def disable(self) -> None:
        """Disable watchdog timer."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_WDT_Stop()
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_WDT_Stop", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.info("disable watchdog timer")

    def reset(self) -> None:
        """Reset watchdog timer."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_WDT_Tick()
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_WDT_Tick", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.info("reset watchdog timer")
