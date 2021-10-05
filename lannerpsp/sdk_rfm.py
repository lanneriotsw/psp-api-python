import logging
from ctypes import byref, c_uint32

from .lmbinc import PSP

logger = logging.getLogger(__name__)


class RFM:
    """
    Radio Frequency Module.

    sdk/src_utils/sdk_rfm/sdk_rfm.c

    :param lmb_io_path: path of liblmbio.so
    :param lmb_api_path: path of liblmbapi.so
    """

    def __init__(self,
                 lmb_io_path: str = "/opt/lanner/psp/bin/amd64/lib/liblmbio.so",
                 lmb_api_path: str = "/opt/lanner/psp/bin/amd64/lib/liblmbapi.so") -> None:
        self._lmb_io_path = lmb_io_path
        self._lmb_api_path = lmb_api_path
        self._udw_reg = c_uint32(0)

    def get_module(self) -> int:
        """Get LTE Module power state.

        bit 0 represent m.2 module, bit 1 represent mPCIE module
        1: power on , 0: power off

        0 (00): mPcie -> off, m.2 -> off
        1 (01): mPcie -> off, m.2 -> on
        2 (10): mPcie -> on,  m.2 -> off
        3 (11): mPcie -> on,  m.2 -> on
        """
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_RFM_GetModule(byref(self._udw_reg))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_RFM_GetModule", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.info(f"get rfm module status {self._udw_reg.value:x}")
            return self._udw_reg.value

    def set_module(self, value: int) -> None:
        """Set LTE Module power state.

        bit 0 represent m.2 module, bit 1 represent mPCIE module
        1: power on, 0: power off

        0 (00): mPcie -> off, m.2 -> off
        1 (01): mPcie -> off, m.2 -> on
        2 (10): mPcie -> on,  m.2 -> off
        3 (11): mPcie -> on,  m.2 -> on
        """
        # Check type.
        if not isinstance(value, int):
            raise TypeError("'value' type must be int")
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_RFM_SetModule(value)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_RFM_SetModule", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.info(f"set rfm module status {value}")

    def get_sim(self) -> int:
        """Get SIM card state.

        bit 0 represent m.2 module, bit 1 represent mPCIE module
        0: first sim, 1: second sim

        0 (00): mPcie -> first sim (SIM3),  m.2 -> first sim (SIM1)
        1 (01): mPcie -> first sim (SIM3),  m.2 -> second sim (SIM2)
        2 (10): mPcie -> second sim (SIM4), m.2 -> first sim (SIM1)
        3 (11): mPcie -> second sim (SIM4), m.2 -> second sim (SIM2)
        """
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_RFM_GetSIM(byref(self._udw_reg))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_RFM_GetSIM", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.info(f"get rfm sim status {self._udw_reg.value:x}")
            return self._udw_reg.value

    def set_sim(self, value: int) -> None:
        """Set SIM card state.

        bit 0 represent m.2 module, bit 1 represent mPCIE module
        0: first sim, 1: second sim

        0 (00): mPcie -> first sim (SIM3),  m.2 -> first sim (SIM1)
        1 (01): mPcie -> first sim (SIM3),  m.2 -> second sim (SIM2)
        2 (10): mPcie -> second sim (SIM4), m.2 -> first sim (SIM1)
        3 (11): mPcie -> second sim (SIM4), m.2 -> second sim (SIM2)
        """
        # Check type.
        if not isinstance(value, int):
            raise TypeError("'value' type must be int")
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_RFM_SetSIM(value)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_RFM_SetSIM", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.info(f"set rfm sim status {value}")
