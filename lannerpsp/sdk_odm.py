import logging
from ctypes import byref, c_int8
from typing import Any, Dict, NamedTuple

from .core import PSP, get_psp_exc_msg
from .exc import (
    PSPError,
    PSPInvalid,
    PSPNotSupport,
)
from .lmbinc import (
    ERR_Success,
    URMODE_RS232,
    URMODE_RS422,
    URMODE_RS485,
)
from .sdk_dll import DLL

logger = logging.getLogger(__name__)

MODES = ("Loopback", "RS-232", "RS-485", "RS-422")
TERMS = ("Disabled", "Enabled", "----", "-----")


class COMPortInfoModel(NamedTuple):
    """To store COM port information."""
    num: int
    mode: int
    mode_str: str
    termination: bool
    termination_str: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict."""
        return dict(self._asdict())


class COMPort:
    """
    Communication Port.

    :param int num: COM port number
    :raises TypeError: The input parameters type error.
    :raises PSPInvalid: The input parameter is out of range.
    """

    def __init__(self, num: int) -> None:
        self._version = DLL().get_version()
        self._num = num
        # Check type.
        if not isinstance(num, int):
            raise TypeError("'num' type must be int")
        # Check import.
        if self._version.platform_id == "LEB-7242":
            try:
                from portio import ioperm
            except ImportError:
                raise RuntimeError(
                    "Install lannerpsp with 'lec7242' extra in order to use COM port."
                )
        # Check value.
        if self._version.platform_id in ("LEB-7242",):
            if num != 1:
                raise PSPInvalid("'num' can only be set to (1) on this platform")
        elif self._version.platform_id in ("LEC-7230",):
            if not 1 <= num <= 2:
                raise PSPInvalid("'num' can only be set to (1~2) on this platform")
        else:
            raise NotImplementedError

    def get_info(self) -> COMPortInfoModel:
        """
        Get COM port information.

        Example:

        .. code-block:: python

            >>> com1 = COMPort(1)
            >>> com1_info = com1.get_info()
            >>> com1_info.num
            1
            >>> com1_info.mode
            485
            >>> com1_info.mode_str
            'RS-485'
            >>> com1_info.termination
            True
            >>> com1_info.termination_str
            'Enabled'
            >>> com1_info.to_dict()
            {'num': 1, 'mode': 485, 'mode_str': 'RS-485', 'termination': True, 'termination_str': 'Enabled'}

        :return: COM port information
        :rtype: COMPortInfoModel
        :raises PSPError: General PSP functional error.
        """
        if self._version.platform_id not in ("LEC-7230",):
            raise PSPNotSupport("Not support on this platform")
        b_mode = c_int8()
        b_term = c_int8()
        mode_mapping = {URMODE_RS232: 232, URMODE_RS422: 422, URMODE_RS485: 485}
        termination_mapping = {2: True, 1: False}
        with PSP() as psp:
            i_ret = psp.lib.LMB_ODM_GetUartMode(self._num, byref(b_mode))
            msg = get_psp_exc_msg("LMB_ODM_GetUartMode", i_ret)
            if i_ret != ERR_Success:
                raise PSPError(msg)
            i_ret = psp.lib.LMB_ODM_TermStat(self._num, byref(b_term))
            msg = get_psp_exc_msg("LMB_ODM_TermStat", i_ret)
            if i_ret != ERR_Success:
                raise PSPError(msg)
        return COMPortInfoModel(num=self._num,
                                mode=mode_mapping[b_mode.value],
                                mode_str=MODES[b_mode.value],
                                termination=termination_mapping[b_term.value + 1],
                                termination_str=TERMS[b_term.value])

    def set_mode(self, mode: int) -> None:
        """
        Set COM port mode to RS-232, RS-422 or RS-485.

        Example:

        .. code-block:: python

            >>> com1 = COMPort(1)
            >>> com1.set_mode(232)

        :param int mode: 232/422/485
        :raises PermissionError: if not running as root user
        :raises TypeError: The input parameters type error.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPError: General PSP functional error.
        """
        if self._version.platform_id == "LEB-7242":
            from .gpio_config_tool import GPIOConfigTool
            GPIOConfigTool().set_com1_mode(mode)
        elif self._version.platform_id == "LEC-7230":
            self._set_mode(mode)
        else:
            raise PSPNotSupport("Not support on this platform")

    def set_termination(self, enable: bool) -> None:
        """
        Set RS-422/RS-485 termination.

        Example:

        .. code-block:: python

            >>> com1 = COMPort(1)
            >>> com1.set_termination(False)

        :param bool enable: set :data:`True` to enable, otherwise :data:`False`
        :raises PermissionError: if not running as root user
        :raises TypeError: The input parameters type error.
        :raises PSPError: General PSP functional error.
        """
        if self._version.platform_id == "LEB-7242":
            from .gpio_config_tool import GPIOConfigTool
            GPIOConfigTool().set_com1_termination(enable)
        elif self._version.platform_id == "LEC-7230":
            self._set_termination(enable)
        else:
            raise PSPNotSupport("Not support on this platform")

    def _set_mode(self, mode: int) -> None:
        """
        For LEC-7230.

        :raises TypeError: The input parameters type error.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPError: General PSP functional error.
        """
        # Check type.
        if not isinstance(mode, int):
            raise TypeError("'mode' type must be int")
        # Check value.
        if mode not in (232, 422, 485):
            raise PSPInvalid("'mode' value must be 232 or 422 or 485")
        # Run.
        mode_mapping = {232: URMODE_RS232, 422: URMODE_RS422, 485: URMODE_RS485}
        b_mode = c_int8(mode_mapping[mode])
        with PSP() as psp:
            i_ret = psp.lib.LMB_ODM_SetUartMode(self._num, b_mode)
        msg = get_psp_exc_msg("LMB_ODM_SetUartMode", i_ret)
        if i_ret == ERR_Success:
            logger.debug(f"set com port {self._num:d} mode {MODES[mode_mapping[mode]]}")
        else:
            raise PSPError(msg)

    def _set_termination(self, enable: bool) -> None:
        """
        For LEC-7230.

        :param bool enable: ``True`` = enable, ``False`` = disable
        :raises TypeError: The input parameters type error.
        :raises PSPError: General PSP functional error.
        """
        # Check type.
        if not isinstance(enable, bool):
            raise TypeError("'enable' type must be bool")
        # Run.
        termination_mapping = {True: 2, False: 1}
        b_term = c_int8(termination_mapping[enable])
        with PSP() as psp:
            i_ret = psp.lib.LMB_ODM_Termination(self._num, b_term.value - 1)
        msg = get_psp_exc_msg("LMB_ODM_Termination", i_ret)
        if i_ret == ERR_Success:
            logger.debug(f"set com port {self._num:d} termination {TERMS[termination_mapping[enable] - 1]}")
        else:
            raise PSPError(msg)
