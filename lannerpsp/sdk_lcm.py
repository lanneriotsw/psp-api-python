import logging
from ctypes import byref, c_char_p, c_uint8, CFUNCTYPE

from .lmbinc import LCMInfo, LCMKeyMsg, PSP

logger = logging.getLogger(__name__)


class LCM:
    """
    Liquid Crystal Display Module.

    sdk/src_utils/sdk_lcm/sdk_lcm.c

    :param lmb_io_path: path of liblmbio.so
    :param lmb_api_path: path of liblmbapi.so
    """

    DEFAULT_LCM_PORT = "/dev/ttyS1"
    DEFAULT_BAUD_RATE = 19200

    def __init__(self,
                 lmb_io_path: str = "/opt/lanner/psp/bin/amd64/lib/liblmbio.so",
                 lmb_api_path: str = "/opt/lanner/psp/bin/amd64/lib/liblmbapi.so") -> None:
        self._lmb_io_path = lmb_io_path
        self._lmb_api_path = lmb_api_path
        self._ub_keys = c_uint8(0)
        self._lcm_info = LCMInfo()
        self._str_lcm_port = c_char_p(self.DEFAULT_LCM_PORT.encode())
        self._dw_speed = self.DEFAULT_BAUD_RATE

    def get_module_type(self) -> str:
        """Get LCM module type."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_LCM_OpenPort(self._str_lcm_port, self._dw_speed)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_LCM_OpenPort", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            i_ret = psp.lib.LMB_LCM_DeviceInfo(byref(self._lcm_info))
            if i_ret == PSP.ERR_Success:
                module_type = "UART"
            else:
                module_type = "LPT"
            logger.debug(f"LCM module type is {module_type}")
            psp.lib.LMB_LCM_DeviceClose()
            return module_type

    def get_keys_status(self) -> int:
        """Get LCM keys status.

        bit 0 means Key 1, bit 1 means Key2, bit 2 means Key 3, bit 3 means Key4
        1: pressed , 0: released

        0 (0000): key1 -> off, key2 -> off, key3 -> off, key4 -> off
        1 (0001): key1 -> on, key2 -> off, key3 -> off, key4 -> off
        2 (0010): key1 -> off, key2 -> on, key3 -> off, key4 -> off
        4 (0100): key1 -> off, key2 -> off, key3 -> on, key4 -> off
        8 (1000): key1 -> off, key2 -> off, key3 -> off, key4 -> on
        """
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_LCM_OpenPort(self._str_lcm_port, self._dw_speed)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_LCM_OpenPort", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            i_ret = psp.lib.LMB_LCM_KeysStatus(byref(self._ub_keys))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_LCM_KeysStatus", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.debug(f"LCM keys status is {self._ub_keys.value:02x}")
            psp.lib.LMB_LCM_DeviceClose()
            return self._ub_keys.value

    def set_backlight(self, enable: bool) -> None:
        """Set LCM backlight."""
        # Check type.
        if not isinstance(enable, bool):
            raise TypeError("'enable' type must be bool")
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_LCM_OpenPort(self._str_lcm_port, self._dw_speed)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_LCM_OpenPort", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            i_ret = psp.lib.LMB_LCM_LightCtrl(c_uint8(enable & 0xFF).value)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_LCM_LightCtrl", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.debug(f"set LCM backlight to {enable}")
            psp.lib.LMB_LCM_DeviceClose()

    def set_cursor(self, row: int, column: int = 1) -> None:
        """Set LCM cursor."""
        # Check type.
        if not isinstance(row, int):
            raise TypeError("'row' type must be int")
        if not isinstance(column, int):
            raise TypeError("'column' type must be int")
        # Check value has been done by the PSP.
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_LCM_OpenPort(self._str_lcm_port, self._dw_speed)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_LCM_OpenPort", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            i_ret = psp.lib.LMB_LCM_SetCursor(column, row)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_LCM_SetCursor", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.debug(f"set LCM cursor to row {row} column {column}")
            psp.lib.LMB_LCM_DeviceClose()

    def write(self, msg: str) -> None:
        """Write string on LCM."""
        # Check type.
        if not isinstance(msg, str):
            raise TypeError("'msg' type must be str")
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_LCM_OpenPort(self._str_lcm_port, self._dw_speed)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_LCM_OpenPort", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            i_ret = psp.lib.LMB_LCM_WriteString(c_char_p(msg.encode()))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_LCM_WriteString", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.debug(f"write '{msg}' on LCM")
            psp.lib.LMB_LCM_DeviceClose()

    def clear(self) -> None:
        """Clear string on LCM."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_LCM_OpenPort(self._str_lcm_port, self._dw_speed)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_LCM_OpenPort", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            i_ret = psp.lib.LMB_LCM_DisplayClear()
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_LCM_DisplayClear", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.debug(f"clear string on LCM")
            psp.lib.LMB_LCM_DeviceClose()

    @classmethod
    def _callback(cls, stu_lcm_msg: LCMKeyMsg) -> None:
        """Callback function for exec_callback()."""
        print(f"<Callback> LCM Item = 0x{stu_lcm_msg.ub_keys:02X}, "
              f"Status = 0x{stu_lcm_msg.ub_status:02X}, "
              f"time is {stu_lcm_msg.stu_time.uw_year:04d}/"
              f"{stu_lcm_msg.stu_time.ub_month:02d}/"
              f"{stu_lcm_msg.stu_time.ub_day:02d} "
              f"{stu_lcm_msg.stu_time.ub_hour:02d}:"
              f"{stu_lcm_msg.stu_time.ub_minute:02d}:"
              f"{stu_lcm_msg.stu_time.ub_second:02d}")

    def exec_callback(self) -> None:
        """Use callback function to detect LCM Keys status."""
        c_callback = CFUNCTYPE(None, LCMKeyMsg)
        p_callback = c_callback(self._callback)
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_LCM_OpenPort(self._str_lcm_port, self._dw_speed)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_LCM_OpenPort", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            i_ret = psp.lib.LMB_LCM_KeysCallback(p_callback, 150)
            if i_ret != PSP.ERR_Success:
                print("-----> hook LCM Keys callback failure <-------")
                return
            print("----> hook LCM Keys Callback OK <----")
            print("===> pause !!! hit <enter> to end <===")
            input()
            i_ret = psp.lib.LMB_LCM_KeysCallback(None, 150)
            if i_ret == PSP.ERR_Success:
                print("----> hook LCM Keys Callback Disable OK <----")
            psp.lib.LMB_LCM_DeviceClose()
