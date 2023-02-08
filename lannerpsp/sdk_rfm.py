import logging
from ctypes import byref, c_uint32

from .core import PSP, get_psp_exc_msg
from .exc import (
    PSPError,
    PSPInvalid,
    PSPNotSupport,
)
from .lmbinc import (
    ERR_Invalid,
    ERR_Success,
)
from .sdk_dll import DLL

logger = logging.getLogger(__name__)

SUPPORTED_PLATFORMS = ("LEB-7242",)
UNSUPPORTED_PLATFORMS = ("LEC-7230", "NCA-2510", "V3S", "V6S",)


class RFM:
    """
    Radio Frequency Module.

    :param bool check_platform:
        Set to :data:`True` to check if the platform supports this feature.
        Defaults to :data:`False` for better compatibility.
    :raises PSPNotSupport: This function is not supported
        (when ``check_platform`` is set to :data:`True`).
    :raises NotImplementedError: It has not been verified to run on this platform
        (when ``check_platform`` is set to :data:`True`).
    """

    def __init__(self, check_platform: bool = False) -> None:
        self._version = DLL().get_version()
        if not check_platform:
            return
        if self._version.platform_id in SUPPORTED_PLATFORMS:
            pass
        elif self._version.platform_id in UNSUPPORTED_PLATFORMS:
            raise PSPNotSupport("Not supported on this platform")
        else:
            raise NotImplementedError

    def get_power_status(self) -> int:
        """
        Get module power status.

        bit 0 means M.2 module, bit 1 means mPCIe module

        0: power off, 1: power on

        - 0 (00): mPCIe -> off, M.2 -> off
        - 1 (01): mPCIe -> off, M.2 -> on
        - 2 (10): mPCIe -> on,  M.2 -> off
        - 3 (11): mPCIe -> on,  M.2 -> on

        Example:

        .. code-block:: pycon

            >>> rfm = RFM()
            >>> power_status = rfm.get_power_status()
            3

        :return: module power status
        :rtype: int
        :raises PSPError: General PSP functional error.
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

        bit 0 means M.2 module, bit 1 means mPCIe module

        0: power off, 1: power on

        - 0 (00): mPCIe -> off, M.2 -> off
        - 1 (01): mPCIe -> off, M.2 -> on
        - 2 (10): mPCIe -> on,  M.2 -> off
        - 3 (11): mPCIe -> on,  M.2 -> on

        Example:

        .. code-block:: pycon

            >>> rfm = RFM()
            >>> rfm.set_power_status(1)

        :param int value: module power status 0 ~ 3
        :raises TypeError: The input parameters type error.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPError: General PSP functional error.
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

        bit 0 means M.2 module, bit 1 means mPCIe module

        0: first sim, 1: second sim

        - 0 (00): mPCIe -> first sim (SIM3),  M.2 -> first sim (SIM1)
        - 1 (01): mPCIe -> first sim (SIM3),  M.2 -> second sim (SIM2)
        - 2 (10): mPCIe -> second sim (SIM4), M.2 -> first sim (SIM1)
        - 3 (11): mPCIe -> second sim (SIM4), M.2 -> second sim (SIM2)

        Example:

        .. code-block:: pycon

            >>> rfm = RFM()
            >>> sim_status = rfm.get_sim_status()
            0

        :return: SIM card status
        :rtype: int
        :raises PSPError: General PSP functional error.
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

        bit 0 means M.2 module, bit 1 means mPCIe module

        0: first sim, 1: second sim

        - 0 (00): mPCIe -> first sim (SIM3),  M.2 -> first sim (SIM1)
        - 1 (01): mPCIe -> first sim (SIM3),  M.2 -> second sim (SIM2)
        - 2 (10): mPCIe -> second sim (SIM4), M.2 -> first sim (SIM1)
        - 3 (11): mPCIe -> second sim (SIM4), M.2 -> second sim (SIM2)

        Example:

        .. code-block:: pycon

            >>> rfm = RFM()
            >>> rfm.set_sim_status(2)

        :param int value: SIM card status 0 ~ 3
        :raises TypeError: The input parameters type error.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPError: General PSP functional error.
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
