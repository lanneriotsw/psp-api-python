import logging
from ctypes import byref, c_uint32
from typing import Optional

from .lmbinc import PSP

logger = logging.getLogger(__name__)


class RFM:
    """
    Radio Frequency Module.

    sdk/src_utils/sdk_rfm/sdk_rfm.c
    """

    _udw_reg = c_uint32(0)

    @classmethod
    def get_module(cls) -> Optional[int]:
        """Get LTE Module power state.

        bit 0 represent m.2 module, bit 1 represent mPCIE module
        1: power on , 0: power off

        0 (00): mPcie -> off, m.2 -> off
        1 (01): mPcie -> off, m.2 -> on
        2 (10): mPcie -> on,  m.2 -> off
        3 (11): mPcie -> on,  m.2 -> on
        """
        with PSP() as psp:
            i_ret = psp.LMB_RFM_GetModule(byref(cls._udw_reg))
            if i_ret == PSP.ERR_Success:
                logger.info(f"get rfm module status {cls._udw_reg.value:x}")
                return cls._udw_reg.value
            else:
                PSP.show_error("LMB_RFM_GetModule", i_ret)

    @classmethod
    def set_module(cls, value: int) -> None:
        """Set LTE Module power state.

        bit 0 represent m.2 module, bit 1 represent mPCIE module
        1: power on, 0: power off

        0 (00): mPcie -> off, m.2 -> off
        1 (01): mPcie -> off, m.2 -> on
        2 (10): mPcie -> on,  m.2 -> off
        3 (11): mPcie -> on,  m.2 -> on
        """
        with PSP() as psp:
            i_ret = psp.LMB_RFM_SetModule(value)
            if i_ret == PSP.ERR_Success:
                logger.info(f"set rfm module status {value}")
            else:
                PSP.show_error("LMB_RFM_SetModule", i_ret)

    @classmethod
    def get_sim(cls) -> Optional[int]:
        """Get SIM card state.

        bit 0 represent m.2 module, bit 1 represent mPCIE module
        0: first sim, 1: second sim

        0 (00): mPcie -> first sim (SIM3),  m.2 -> first sim (SIM1)
        1 (01): mPcie -> first sim (SIM3),  m.2 -> second sim (SIM2)
        2 (10): mPcie -> second sim (SIM4), m.2 -> first sim (SIM1)
        3 (11): mPcie -> second sim (SIM4), m.2 -> second sim (SIM2)
        """
        with PSP() as psp:
            i_ret = psp.LMB_RFM_GetSIM(byref(cls._udw_reg))
            if i_ret == PSP.ERR_Success:
                logger.info(f"get rfm sim status {cls._udw_reg.value:x}")
                return cls._udw_reg.value
            else:
                PSP.show_error("LMB_RFM_GetSIM", i_ret)

    @classmethod
    def set_sim(cls, value: int) -> None:
        """Set SIM card state.

        bit 0 represent m.2 module, bit 1 represent mPCIE module
        0: first sim, 1: second sim

        0 (00): mPcie -> first sim (SIM3),  m.2 -> first sim (SIM1)
        1 (01): mPcie -> first sim (SIM3),  m.2 -> second sim (SIM2)
        2 (10): mPcie -> second sim (SIM4), m.2 -> first sim (SIM1)
        3 (11): mPcie -> second sim (SIM4), m.2 -> second sim (SIM2)
        """
        with PSP() as psp:
            i_ret = psp.LMB_RFM_SetSIM(value)
            if i_ret == PSP.ERR_Success:
                logger.info(f"set rfm sim status {value}")
            else:
                PSP.show_error("LMB_RFM_SetSIM", i_ret)
