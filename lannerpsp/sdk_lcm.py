import logging
from ctypes import byref, c_char_p, c_int32, c_uint8, CFUNCTYPE, sizeof

from .core import PSP, get_psp_exc_msg
from .exc import (
    PSPError,
    PSPNotExist,
    PSPInvalid,
    PSPNotOpened,
    PSPNotSupport,
)
from .lmbinc import (
    ERR_Invalid,
    ERR_NotExist,
    ERR_NotOpened,
    ERR_NotSupport,
    ERR_Success,
    LCMInfo,
    LCMKeyMsg,
)
from .sdk_dll import DLL

logger = logging.getLogger(__name__)

DEFAULT_LCM_PORT = "/dev/ttyS1"
DEFAULT_BAUD_RATE = 19200

LCM_UART_TYPE = 1
LCM_LPT_TYPE = 2


class LCM:
    """
    LCD Module.
    """

    def __init__(self) -> None:
        self._version = DLL().get_version()
        self._str_lcm_port = c_char_p(DEFAULT_LCM_PORT.encode())
        self._dw_speed = DEFAULT_BAUD_RATE

    def search_port(self) -> str:
        """
        Get the LCM current connected port and speed.

        .. Note::
            The string maximum length depends on LCD module, normally 40 characters.

        :return: current connected port and speed
        :rtype: str
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPNotExist: This function is not enabled or does not exist.
        :raises PSPError: This function failed.
        """
        dw_speed = c_int32(self._dw_speed)
        with PSP() as psp:
            if self._version.dll_major == 2 and self._version.dll_minor in (1, 2, 3):
                i_ret = psp.lib.LMB_LCM_SearchPort(self._str_lcm_port, byref(dw_speed))
            elif self._version.dll_major == 3 and self._version.dll_minor in (0,):
                i_ret = psp.lib.LMB_LCM_SearchPort(self._str_lcm_port, byref(dw_speed), sizeof(self._str_lcm_port))
            else:
                raise NotImplementedError
        msg = get_psp_exc_msg("LMB_LCM_SearchPort", i_ret)
        if i_ret == ERR_Success:
            return f"port={self._str_lcm_port}, speed={dw_speed.value:d}"
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        elif i_ret == ERR_NotExist:
            raise PSPNotExist(msg)
        else:
            raise PSPError(msg)

    def _open_port(self, psp: PSP) -> None:
        """
        Open the LCM device with path and assigned speed.

        .. Note::
            The string maximum length depends on LCD module, normally 40 characters.

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPNotExist: This function is not enabled or does not exist.
        :raises PSPError: This function failed.
        """
        i_ret = psp.lib.LMB_LCM_OpenPort(self._str_lcm_port, self._dw_speed)
        msg = get_psp_exc_msg("LMB_LCM_OpenPort", i_ret)
        if i_ret == ERR_Success:
            pass
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        elif i_ret == ERR_NotExist:
            raise PSPNotExist(msg)
        else:
            raise PSPError(msg)

    def _open_device(self, psp: PSP) -> None:
        """
        Open and connect LCD module.
        """
        i_ret = psp.lib.LMB_LCM_DeviceOpen()
        msg = get_psp_exc_msg("LMB_LCM_DeviceOpen", i_ret)
        if i_ret == ERR_Success:
            pass
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        elif i_ret == ERR_NotExist:
            raise PSPNotExist(msg)
        else:
            raise PSPError(msg)

    def _close_device(self, psp: PSP) -> None:
        """
        Close and disconnect LCD module.

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: This function failed.
        """
        i_ret = psp.lib.LMB_LCM_DeviceClose()
        msg = get_psp_exc_msg("LMB_LCM_DeviceClose", i_ret)
        if i_ret == ERR_Success:
            pass
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def _get_device_info(self, psp: PSP) -> int:
        """
        Get platform LCM device information.

        :return: LCM module type (UART = 1, LPT = 2)
        :rtype: int
        """
        stu_lcm_info = LCMInfo()
        i_ret = psp.lib.LMB_LCM_DeviceInfo(byref(stu_lcm_info))
        msg = get_psp_exc_msg("LMB_LCM_DeviceInfo", i_ret)
        if i_ret == ERR_Success:
            logger.debug(f"LCM Mode No. is {stu_lcm_info.uw_mode_no:04X}\n"
                         f"LCM Firmware Ver. is {stu_lcm_info.uw_version:04X}\n"
                         f"LCM Speed ={stu_lcm_info.udw_baud_rate:d}")
            return LCM_UART_TYPE
        else:
            # ERR_NotOpened or ERR_NotSupport.
            logger.debug(msg)
            return LCM_LPT_TYPE

    def reset(self) -> None:
        """
        Reset the LCD module.

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: This function failed.
        """
        with PSP() as psp:
            self._open_port(psp)
            if self._get_device_info(psp) == LCM_LPT_TYPE:
                raise PSPNotSupport("LPT type not support reset")
            i_ret = psp.lib.LMB_LCM_Reset()
            msg = get_psp_exc_msg("LMB_LCM_Reset", i_ret)
            if i_ret == ERR_Success:
                pass
            elif i_ret == ERR_NotOpened:
                raise PSPNotOpened(msg)
            elif i_ret == ERR_NotSupport:
                raise PSPNotSupport(msg)
            else:
                raise PSPError(msg)
            self._close_device(psp)

    def get_keys_status(self) -> int:
        """
        Get LCM keys status.

        bit 0 means Key 1, bit 1 means Key2, bit 2 means Key 3, bit 3 means Key4

        1: pressed , 0: released

        - 0 (0000): key1 -> off, key2 -> off, key3 -> off, key4 -> off
        - 1 (0001): key1 -> on, key2 -> off, key3 -> off, key4 -> off
        - 2 (0010): key1 -> off, key2 -> on, key3 -> off, key4 -> off
        - 4 (0100): key1 -> off, key2 -> off, key3 -> on, key4 -> off
        - 8 (1000): key1 -> off, key2 -> off, key3 -> off, key4 -> on

        Example:

        .. code-block:: python

            >>> lcm = LCM()
            >>> lcm.get_keys_status()
            2

        :return: LCM keys status
        :rtype: int
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: No key is pressed.
        """
        ub_keys = c_uint8()
        with PSP() as psp:
            self._open_device(psp)
            i_ret = psp.lib.LMB_LCM_KeysStatus(byref(ub_keys))
            msg = get_psp_exc_msg("LMB_LCM_KeysStatus", i_ret)
            if i_ret == ERR_Success:
                logger.debug(f"LCM keys status is {ub_keys.value:02x}")
            elif i_ret == ERR_NotOpened:
                raise PSPNotOpened(msg)
            elif i_ret == ERR_NotSupport:
                raise PSPNotSupport(msg)
            else:
                raise PSPError(msg)
            self._close_device(psp)
            return ub_keys.value

    def set_backlight(self, enable: bool) -> None:
        """
        Set LCD module light on/off status.

        Example:

        .. code-block:: python

            >>> lcm = LCM()
            >>> lcm.set_backlight(True)

        :param bool enable: ``True`` to enable backlight, otherwise ``False``
        :raises TypeError: The input parameters type error.
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: This function failed.
        """
        # Check type.
        if not isinstance(enable, bool):
            raise TypeError("'enable' type must be bool")
        # Run.
        with PSP() as psp:
            self._open_device(psp)
            i_ret = psp.lib.LMB_LCM_LightCtrl(c_uint8(enable & 0xFF).value)
            msg = get_psp_exc_msg("LMB_LCM_LightCtrl", i_ret)
            if i_ret == ERR_Success:
                logger.debug(f"set LCM backlight to {enable}")
            elif i_ret == ERR_NotOpened:
                raise PSPNotOpened(msg)
            elif i_ret == ERR_NotSupport:
                raise PSPNotSupport(msg)
            else:
                raise PSPError(msg)
            self._close_device(psp)

    def set_cursor(self, row: int, column: int = 1) -> None:
        """
        Set LCM cursor.

        Example:

        .. code-block:: python

            >>> lcm = LCM()
            >>> lcm.set_cursor(2, 6)

        :param int row: assigns row value of LCM display cursor
        :param int column: assigns column value of LCM display cursor
        :raises TypeError: The input parameters type error.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: This function failed.
        """
        # Check type.
        if not isinstance(row, int):
            raise TypeError("'row' type must be int")
        if not isinstance(column, int):
            raise TypeError("'column' type must be int")
        # Check value has been done by the PSP.
        # Run.
        with PSP() as psp:
            self._open_device(psp)
            i_ret = psp.lib.LMB_LCM_SetCursor(column, row)
            msg = get_psp_exc_msg("LMB_LCM_SetCursor", i_ret)
            if i_ret == ERR_Success:
                logger.debug(f"set LCM cursor to row {row} column {column}")
            elif i_ret == ERR_Invalid:
                raise PSPInvalid(msg)
            elif i_ret == ERR_NotOpened:
                raise PSPNotOpened(msg)
            elif i_ret == ERR_NotSupport:
                raise PSPNotSupport(msg)
            else:
                raise PSPError(msg)
            self._close_device(psp)

    def write(self, msg: str) -> None:
        """
        Write string to LCD module.

        Example:

        .. code-block:: python

            >>> lcm = LCM()
            >>> lcm.write("Hello World")

        :param str msg: message string to LCM display
        :raises TypeError: The input parameters type error.
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: This function failed.
        """
        # Check type.
        if not isinstance(msg, str):
            raise TypeError("'msg' type must be str")
        # Run.
        with PSP() as psp:
            self._open_device(psp)
            i_ret = psp.lib.LMB_LCM_WriteString(c_char_p(msg.encode()))
            msg = get_psp_exc_msg("LMB_LCM_WriteString", i_ret)
            if i_ret == ERR_Success:
                logger.debug(f"write '{msg}' on LCM")
            elif i_ret == ERR_NotOpened:
                raise PSPNotOpened(msg)
            elif i_ret == ERR_NotSupport:
                raise PSPNotSupport(msg)
            else:
                raise PSPError(msg)
            self._close_device(psp)

    def clear(self) -> None:
        """
        Clear LCM display.

        Example:

        .. code-block:: python

            >>> lcm = LCM()
            >>> lcm.clear()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: This function failed.
        """
        with PSP() as psp:
            self._open_device(psp)
            i_ret = psp.lib.LMB_LCM_DisplayClear()
            msg = get_psp_exc_msg("LMB_LCM_DisplayClear", i_ret)
            if i_ret == ERR_Success:
                logger.debug(f"clear string on LCM")
            elif i_ret == ERR_NotOpened:
                raise PSPNotOpened(msg)
            elif i_ret == ERR_NotSupport:
                raise PSPNotSupport(msg)
            else:
                raise PSPError(msg)
            self._close_device(psp)

    @classmethod
    def _callback(cls, stu_lcm_msg: LCMKeyMsg) -> None:
        """Callback function for :func:`exec_callback`."""
        print(f"<Callback> LCM Item = 0x{stu_lcm_msg.ub_keys:02X}, "
              f"Status = 0x{stu_lcm_msg.ub_status:02X}, "
              f"time is {stu_lcm_msg.stu_time.uw_year:04d}/"
              f"{stu_lcm_msg.stu_time.ub_month:02d}/"
              f"{stu_lcm_msg.stu_time.ub_day:02d} "
              f"{stu_lcm_msg.stu_time.ub_hour:02d}:"
              f"{stu_lcm_msg.stu_time.ub_minute:02d}:"
              f"{stu_lcm_msg.stu_time.ub_second:02d}")

    def exec_callback(self) -> None:
        """
        Use callback function to detect LCM Keys status.

        Example:

        .. code-block:: python

            >>> lcm = LCM()
            >>> lcm.exec_callback()
            ----> hook LCM Keys Callback OK <----
            ===> pause !!! hit <enter> to end <===
            <Callback> LCM Item = 0x08, Status = 0x08, time is 2022/08/02 16:48:28
            <Callback> LCM Item = 0x08, Status = 0x00, time is 2022/08/02 16:48:28
            <Callback> LCM Item = 0x04, Status = 0x04, time is 2022/08/02 16:48:29
            <Callback> LCM Item = 0x04, Status = 0x00, time is 2022/08/02 16:48:29
            <Callback> LCM Item = 0x08, Status = 0x08, time is 2022/08/02 16:48:30
            <Callback> LCM Item = 0x08, Status = 0x00, time is 2022/08/02 16:48:30
            <Callback> LCM Item = 0x02, Status = 0x02, time is 2022/08/02 16:48:31
            <Callback> LCM Item = 0x02, Status = 0x00, time is 2022/08/02 16:48:31
            <Callback> LCM Item = 0x01, Status = 0x01, time is 2022/08/02 16:48:31
            <Callback> LCM Item = 0x01, Status = 0x00, time is 2022/08/02 16:48:31
            <Callback> LCM Item = 0x08, Status = 0x08, time is 2022/08/02 16:48:32
            <Callback> LCM Item = 0x08, Status = 0x00, time is 2022/08/02 16:48:32

            ----> hook LCM Keys Callback Disable OK <----
        """
        c_callback = CFUNCTYPE(None, LCMKeyMsg)
        p_callback = c_callback(self._callback)
        with PSP() as psp:
            self._open_device(psp)
            i_ret = psp.lib.LMB_LCM_KeysCallback(p_callback, 150)
            if i_ret != ERR_Success:
                print("-----> hook LCM Keys callback failure <-------")
                return
            print("----> hook LCM Keys Callback OK <----")
            print("===> pause !!! hit <enter> to end <===")
            input()
            i_ret = psp.lib.LMB_LCM_KeysCallback(None, 150)
            if i_ret == ERR_Success:
                print("----> hook LCM Keys Callback Disable OK <----")
            self._close_device(psp)
