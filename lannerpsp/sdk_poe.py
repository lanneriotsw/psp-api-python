import logging
from ctypes import byref, c_uint32
from math import log2
from typing import Any, Dict, NamedTuple

from .core import PSP, convert_to_bit_array, get_psp_exc_msg
from .exc import (
    PSPError,
    PSPInvalid,
    PSPNotOpened,
    PSPNotSupport,
)
from .lmbinc import (
    DISABLE,
    ENABLE,
    ERR_NotOpened,
    ERR_NotSupport,
    ERR_Success,
)
from .sdk_dll import DLL

logger = logging.getLogger(__name__)

SUPPORTED_PLATFORMS = ("LEB-2680", "LEC-2290", "V3S", "V6S",)
UNSUPPORTED_PLATFORMS = ("LEB-7242", "LEC-7230", "NCA-2510",)


class PoEInfoModel(NamedTuple):
    """To store PoE information."""
    number_of_poe_ports: int
    power_status: Dict[int, bool]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict."""
        return dict(self._asdict())


class PoE:
    """
    Power over Ethernet.

    :param int num: LAN port number
    :raises TypeError: The input parameters type error.
    :raises PSPNotSupport: This function is not supported.
    :raises PSPInvalid: The input parameter is out of range.
    :raises PSPError: General PSP functional error.
    """

    def __init__(self, num: int) -> None:
        self._version = DLL().get_version()
        self._num = num
        # Check type.
        if not isinstance(num, int):
            raise TypeError("'num' type must be int")
        # Check value.
        number_of_poe_ports = self._get_supported_ports_count()
        if not 1 <= num <= number_of_poe_ports:
            raise PSPInvalid(f"'num' can only be set to (1~{number_of_poe_ports}) on this platform")

    @classmethod
    def get_info(cls) -> PoEInfoModel:
        """
        Get the PoE information supported by this platform.

        Example:

        .. code-block:: pycon

            >>> poe_info = PoE.get_info()
            >>> poe_info
            PoEInfoModel(number_of_poe_ports=6, power_status={1: True, 2: False, 3: True, 4: True, 5: True, 6: True})
            >>> poe_info.number_of_poe_ports
            6
            >>> poe_info.power_status
            {1: True, 2: False, 3: True, 4: True, 5: True, 6: True}
            >>> poe_info.to_dict()
            {'number_of_poe_ports': 6, 'power_status': {1: True, 2: True, 3: True, 4: True, 5: True, 6: True}}

        :return: The PoE information.
        :rtype: PoEInfoModel
        :raises PSPNotSupport: This function is not supported.
        :raises PSPNotOpened: Device port is not opened yet.
        :raises PSPError: General PSP functional error.
        """
        number_of_poe_ports = cls._get_supported_ports_count()
        # Get the power status of each port.
        udw_status = c_uint32(0)
        with PSP() as psp:
            i_ret = psp.lib.LMB_IGN_GetPoePower(0xFFFFFFFF, byref(udw_status))
            try:
                # Prevent the UART of the MCU from being occupied.
                psp.lib.LMB_IGN_ClosePort()
            except AttributeError:
                pass
        msg = get_psp_exc_msg("LMB_IGN_GetPoePower", i_ret)
        if i_ret == ERR_Success:
            # Convert integer to bit array.
            power_status_list = convert_to_bit_array(udw_status.value)
            # Fill the space with 0 from the beginning of the list.
            power_status_list[0:0] = [0 for _ in range(number_of_poe_ports - len(power_status_list))]
            # Reverse the list so that the port numbers start at 1.
            power_status_list.reverse()
            power_status = {}
            for i in range(number_of_poe_ports):
                power_status[i + 1] = bool(power_status_list[i])
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        else:
            raise PSPError(msg)
        return PoEInfoModel(
            number_of_poe_ports=number_of_poe_ports,
            power_status=power_status,
        )

    def enable(self) -> None:
        """
        Enable the PoE port power (power on by auto).

        Example:

        .. code-block:: pycon

            >>> poe1 = PoE(1)
            >>> poe1.enable()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPError: General PSP functional error.
        """
        with PSP() as psp:
            i_ret = psp.lib.LMB_POE_SetPortPower(self._num, ENABLE)
            try:
                # Prevent the UART of the MCU from being occupied.
                psp.lib.LMB_IGN_ClosePort()
            except AttributeError:
                pass
        msg = get_psp_exc_msg("LMB_POE_SetPortPower", i_ret)
        if i_ret == ERR_Success:
            logger.debug(f"LAN{self._num} port power on by auto")
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        else:
            raise PSPError(msg)

    def disable(self) -> None:
        """
        Disable the PoE port power (power off).

        Example:

        .. code-block:: pycon

            >>> poe1 = PoE(1)
            >>> poe1.disable()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPError: General PSP functional error.
        """
        with PSP() as psp:
            i_ret = psp.lib.LMB_POE_SetPortPower(self._num, DISABLE)
            try:
                # Prevent the UART of the MCU from being occupied.
                psp.lib.LMB_IGN_ClosePort()
            except AttributeError:
                pass
        msg = get_psp_exc_msg("LMB_POE_SetPortPower", i_ret)
        if i_ret == ERR_Success:
            logger.debug(f"LAN{self._num} port power off")
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        else:
            raise PSPError(msg)

    def get_power_status(self) -> bool:
        """
        Get the PoE port power status.

        Example:

        .. code-block:: pycon

            >>> poe1 = PoE(1)
            >>> poe1.get_power_status()
            True

        :return: PoE LAN port power status. :data:`True` means PoE power is enabled by auto,
            :data:`False` means PoE power is disabled.
        :rtype: bool
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPError: General PSP functional error.
        """
        udw_status = c_uint32(0)
        with PSP() as psp:
            i_ret = psp.lib.LMB_POE_GetPortStatus(self._num, byref(udw_status))
            try:
                # Prevent the UART of the MCU from being occupied.
                psp.lib.LMB_IGN_ClosePort()
            except AttributeError:
                pass
        msg = get_psp_exc_msg("LMB_POE_GetPortStatus", i_ret)
        if i_ret == ERR_Success:
            return bool(udw_status.value)
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        else:
            raise PSPError(msg)

    @classmethod
    def _get_supported_ports_count(cls) -> int:
        """
        Get the number of LAN ports that support PoE.

        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: General PSP functional error.
        """
        udw_ports = c_uint32(0)
        with PSP() as psp:
            try:
                i_ret = psp.lib.LMB_POE_QueryDevices(byref(udw_ports))
            except AttributeError:
                raise PSPNotSupport("Not supported on this platform")
            try:
                # Prevent the UART of the MCU from being occupied.
                psp.lib.LMB_IGN_ClosePort()
            except AttributeError:
                pass
        msg = get_psp_exc_msg("LMB_POE_QueryDevices", i_ret)
        if i_ret == ERR_Success:
            logger.debug(f"PoE ports = 0x{udw_ports.value:08X}")
            return int(log2(udw_ports.value + 1))
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)
