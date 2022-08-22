import logging
from ctypes import byref, c_uint32

from .core import PSP, get_psp_exc_msg
from .exc import (
    PSPError,
    PSPInvalid,
)
from .lmbinc import (
    ERR_Invalid,
    ERR_Success,
)
from .sdk_dll import DLL

logger = logging.getLogger(__name__)


class RFM:
    """
    Radio Frequency Module.
    """

    def __init__(self) -> None:
        self._version = DLL().get_version()

    def get_power_status(self) -> int:
        """
        Get module power status.

        bit 0 means m.2 module, bit 1 means mPCIE module

        0: power off, 1: power on

        - 0 (00): mPcie -> off, m.2 -> off
        - 1 (01): mPcie -> off, m.2 -> on
        - 2 (10): mPcie -> on,  m.2 -> off
        - 3 (11): mPcie -> on,  m.2 -> on

        Example:

        .. code-block:: python

            >>> rfm = RFM()
            >>> power_status = rfm.get_power_status()
            3

        :return: module power status
        :rtype: int
        :raises PSPError: General function error.
        """
        udw_reg = c_uint32(0)
        with PSP() as psp:
            i_ret = psp.lib.LMB_RFM_GetModule(byref(udw_reg))
        msg = get_psp_exc_msg("LMB_RFM_GetModule", i_ret)
        if i_ret == ERR_Success:
            logger.debug(f"get module power status {udw_reg.value:x}")
            return udw_reg.value
        else:
            raise PSPError(msg)

    def set_power_status(self, value: int) -> None:
        """
        Set module power status.

        bit 0 means m.2 module, bit 1 means mPCIE module

        0: power off, 1: power on

        - 0 (00): mPcie -> off, m.2 -> off
        - 1 (01): mPcie -> off, m.2 -> on
        - 2 (10): mPcie -> on,  m.2 -> off
        - 3 (11): mPcie -> on,  m.2 -> on

        Example:

        .. code-block:: python

            >>> rfm = RFM()
            >>> rfm.set_power_status(1)

        :param int value: module power status 0 ~ 3
        :raises TypeError: The input parameters type error.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPError: General function error.
        """
        # Check type.
        if not isinstance(value, int):
            raise TypeError("'value' type must be int")
        # Check value has been done by the PSP.
        # Run.
        with PSP() as psp:
            i_ret = psp.lib.LMB_RFM_SetModule(value)
        msg = get_psp_exc_msg("LMB_RFM_SetModule", i_ret)
        if i_ret == ERR_Success:
            logger.debug(f"set module power status {value:d}")
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        else:
            raise PSPError(msg)

    def get_sim_status(self) -> int:
        """
        Get SIM card status.

        bit 0 means m.2 module, bit 1 means mPCIE module

        0: first sim, 1: second sim

        - 0 (00): mPcie -> first sim (SIM3),  m.2 -> first sim (SIM1)
        - 1 (01): mPcie -> first sim (SIM3),  m.2 -> second sim (SIM2)
        - 2 (10): mPcie -> second sim (SIM4), m.2 -> first sim (SIM1)
        - 3 (11): mPcie -> second sim (SIM4), m.2 -> second sim (SIM2)

        Example:

        .. code-block:: python

            >>> rfm = RFM()
            >>> sim_status = rfm.get_sim_status()
            0

        :return: SIM card status
        :rtype: int
        :raises PSPError: General function error.
        """
        udw_reg = c_uint32(0)
        with PSP() as psp:
            i_ret = psp.lib.LMB_RFM_GetSIM(byref(udw_reg))
        msg = get_psp_exc_msg("LMB_RFM_GetSIM", i_ret)
        if i_ret == ERR_Success:
            logger.debug(f"get sim card status {udw_reg.value:x}")
            return udw_reg.value
        else:
            raise PSPError(msg)

    def set_sim_status(self, value: int) -> None:
        """
        Set SIM card status.

        bit 0 means m.2 module, bit 1 means mPCIE module
        0: first sim, 1: second sim

        0 (00): mPcie -> first sim (SIM3),  m.2 -> first sim (SIM1)
        1 (01): mPcie -> first sim (SIM3),  m.2 -> second sim (SIM2)
        2 (10): mPcie -> second sim (SIM4), m.2 -> first sim (SIM1)
        3 (11): mPcie -> second sim (SIM4), m.2 -> second sim (SIM2)

        Example:

        .. code-block:: python

            >>> rfm = RFM()
            >>> rfm.set_sim_status(2)

        :param int value: SIM card status 0 ~ 3
        :raises TypeError: The input parameters type error.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPError: General function error.
        """
        # Check type.
        if not isinstance(value, int):
            raise TypeError("'value' type must be int")
        # Check value has been done by the PSP.
        # Run.
        with PSP() as psp:
            i_ret = psp.lib.LMB_RFM_SetSIM(value)
        msg = get_psp_exc_msg("LMB_RFM_SetSIM", i_ret)
        if i_ret == ERR_Success:
            logger.debug(f"set sim card status {value:d}")
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        else:
            raise PSPError(msg)
