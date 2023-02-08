import logging
from ctypes import byref, c_int32, c_uint8, c_uint32
from math import log2
from typing import Any, Dict, NamedTuple

from .core import PSP, get_psp_exc_msg
from .exc import (
    PSPError,
    PSPNotOpened,
    PSPNotSupport,
)
from .lmbinc import (
    ERR_NotOpened,
    ERR_NotSupport,
    ERR_Success,
)
from .sdk_dll import DLL

logger = logging.getLogger(__name__)

SUPPORTED_PLATFORMS = ("LEB-2680", "LEC-2290", "LEC-7230", "NCA-2510", "V3S", "V6S",)
UNSUPPORTED_PLATFORMS = ("LEB-7242",)


class GPIOInfoModel(NamedTuple):
    """To store GPIO information."""
    number_of_di_pins: int
    number_of_do_pins: int

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict."""
        return dict(self._asdict())


class GPIO:
    """
    General Purpose Input/Output.

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

    def get_info(self) -> GPIOInfoModel:
        """
        Get the GPIO information supported by this platform.

        Example:

        .. code-block:: pycon

            >>> gpio = GPIO()
            >>> gpio_info = gpio.get_info()
            >>> gpio_info
            GPIOInfoModel(number_of_di_pins=8, number_of_do_pins=4)
            >>> gpio_info.number_of_di_pins
            8
            >>> gpio_info.number_of_do_pins
            4
            >>> gpio_info.to_dict()
            {'number_of_di_pins': 8, 'number_of_do_pins': 4}

        :return: The GPIO information.
        :rtype: GPIOInfoModel
        :raises PSPNotSupport: This function is not supported.
        :raises PSPNotOpened: Device port is not opened yet.
        :raises PSPError: General PSP functional error.
        """
        if self._version.platform_id in ("LEB-2680",):
            # Use ignition MCU.
            udw_in_pins = c_uint32(0)
            udw_out_pins = c_uint32(0)
            with PSP() as psp:
                i_ret = psp.lib.LMB_IGN_GetDigitalPins(byref(udw_out_pins), byref(udw_in_pins))
                psp.lib.LMB_IGN_ClosePort()  # Prevent the UART of the MCU from being occupied.
            msg = get_psp_exc_msg("LMB_IGN_GetDigitalPins", i_ret)
            if i_ret == ERR_Success:
                return GPIOInfoModel(
                    number_of_di_pins=int(log2(udw_in_pins.value + 1)),
                    number_of_do_pins=int(log2(udw_out_pins.value + 1)),
                )
            elif i_ret == ERR_NotSupport:
                raise PSPNotSupport(msg)
            elif i_ret == ERR_NotOpened:
                raise PSPNotOpened(msg)
            else:
                raise PSPError(msg)
        else:
            ub_in_pins = c_uint8(0)
            ub_out_pins = c_uint8(0)
            with PSP() as psp:
                i_ret = psp.lib.LMB_GPIO_GetInfo(0, byref(ub_in_pins), byref(ub_out_pins))
                try:
                    # Prevent the UART of the MCU from being occupied.
                    psp.lib.LMB_IGN_ClosePort()
                except AttributeError:
                    pass
            msg = get_psp_exc_msg("LMB_GPIO_GetInfo", i_ret)
            if i_ret == ERR_Success:
                return GPIOInfoModel(
                    number_of_di_pins=ub_in_pins.value,
                    number_of_do_pins=ub_out_pins.value,
                )
            elif i_ret == ERR_NotSupport:
                raise PSPNotSupport(msg)
            elif i_ret == ERR_NotOpened:
                raise PSPNotOpened(msg)
            else:
                raise PSPError(msg)

    def get_digital_in(self) -> int:
        """
        Get the GPI/DI status.

        Example:

        .. code-block:: pycon

            >>> gpio = GPIO()
            >>> gpio.get_digital_in()
            12

        :return: GPI/DI status in decimal. When converted to binary, the LSB represents DI_0.
        :rtype: int
        :raises PSPNotSupport: This function is not supported.
        :raises PSPNotOpened: Device port is not opened yet.
        :raises PSPError: General PSP functional error.
        """
        gpio_info = self.get_info()
        udw_dio_stat = c_int32(0)
        if self._version.platform_id in ("LEB-2680",):
            # Use ignition MCU.
            with PSP() as psp:
                i_ret = psp.lib.LMB_IGN_GetDigitalIn(2 ** gpio_info.number_of_di_pins - 1, byref(udw_dio_stat))
                psp.lib.LMB_IGN_ClosePort()  # Prevent the UART of the MCU from being occupied.
            msg = get_psp_exc_msg("LMB_IGN_GetDigitalIn", i_ret)
        else:
            with PSP() as psp:
                i_ret = psp.lib.LMB_GPIO_GpiRead(0, byref(udw_dio_stat))
                try:
                    # Prevent the UART of the MCU from being occupied.
                    psp.lib.LMB_IGN_ClosePort()
                except AttributeError:
                    pass
            msg = get_psp_exc_msg("LMB_GPIO_GpiRead", i_ret)
        if i_ret == ERR_Success:
            logger.debug(f"read DI status: 0x{udw_dio_stat.value:02X}")
            return udw_dio_stat.value
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        else:
            raise PSPError(msg)

    def get_digital_out(self) -> int:
        """
        Get the GPO/DO status.

        Example:

        .. code-block:: pycon

            >>> gpio = GPIO()
            >>> gpio.get_digital_out()
            3

        :return: GPO/DO status in decimal. When converted to binary, the LSB represents DO_0.
        :rtype: int
        :raises PSPNotSupport: This function is not supported.
        :raises PSPNotOpened: Device port is not opened yet.
        :raises PSPError: General PSP functional error.
        """
        gpio_info = self.get_info()
        udw_dio_stat = c_int32(0)
        if self._version.platform_id in ("LEB-2680",):
            # Use ignition MCU.
            with PSP() as psp:
                i_ret = psp.lib.LMB_IGN_GetDigitalOut(2 ** gpio_info.number_of_do_pins - 1, byref(udw_dio_stat))
                psp.lib.LMB_IGN_ClosePort()  # Prevent the UART of the MCU from being occupied.
            msg = get_psp_exc_msg("LMB_IGN_GetDigitalOut", i_ret)
        else:
            with PSP() as psp:
                i_ret = psp.lib.LMB_GPIO_GpoRead(0, byref(udw_dio_stat))
                try:
                    # Prevent the UART of the MCU from being occupied.
                    psp.lib.LMB_IGN_ClosePort()
                except AttributeError:
                    pass
            msg = get_psp_exc_msg("LMB_GPIO_GpoRead", i_ret)
        if i_ret == ERR_Success:
            logger.debug(f"read DO status: 0x{udw_dio_stat.value:02X}")
            return udw_dio_stat.value
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        else:
            raise PSPError(msg)

    def set_digital_out(self, status: int) -> None:
        """
        Set the GPO/DO status.

        Example:

        .. code-block:: pycon

            >>> gpio = GPIO()
            >>> gpio.set_digital_out(0x0A)

        :param int status: GPO/DO status.
            This value can be binary, octal, decimal or hexadecimal with type :class:`int`.
            For example, to write the ``[high, low, high, low]`` signal from **DO_3** to **DO_0**,
            just set this parameter to ``0b1010``, ``0o12``, ``0x0A`` or ``10``.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPNotOpened: Device port is not opened yet.
        :raises PSPError: General PSP functional error.
        """
        if not isinstance(status, int):
            raise TypeError("'status' type must be int")
        gpio_info = self.get_info()
        if self._version.platform_id in ("LEB-2680",):
            # Use ignition MCU.
            with PSP() as psp:
                i_ret = psp.lib.LMB_IGN_SetDigitalOut(2 ** gpio_info.number_of_do_pins - 1, status)
                psp.lib.LMB_IGN_ClosePort()  # Prevent the UART of the MCU from being occupied.
            msg = get_psp_exc_msg("LMB_IGN_SetDigitalOut", i_ret)
        else:
            with PSP() as psp:
                i_ret = psp.lib.LMB_GPIO_GpoWrite(0, status)
                try:
                    # Prevent the UART of the MCU from being occupied.
                    psp.lib.LMB_IGN_ClosePort()
                except AttributeError:
                    pass
            msg = get_psp_exc_msg("LMB_GPIO_GpoWrite", i_ret)
        if i_ret == ERR_Success:
            logger.debug(f"write DI status: {status:d}")
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        else:
            raise PSPError(msg)
