import logging
import os.path
from configparser import ConfigParser
from ctypes import byref, c_float, c_int32, c_uint16, c_uint32, create_string_buffer, memset, sizeof
from os import PathLike
from re import match
from string import ascii_uppercase
from typing import Any, Dict, Iterable, List, NamedTuple, Union

from .core import PSP, get_psp_exc_msg
from .exc import (
    PSPError,
    PSPInvalid,
    PSPNotOpened,
    PSPNotSupport,
)
from .lmbinc import (
    ERR_Invalid,
    ERR_NotOpened,
    ERR_NotSupport,
    ERR_Success,
)
from .lmbipmi import (
    HWM_TYPE_NONE,
    HWM_TYPE_SIO,
    HWM_TYPE_IPMI,
    HWM_TYPE_SMBUS,
    HWM_TYPE_AST1400,
    IPMISensorInfo,
)
from .lmbsid import HWM_DISPLAY_NAME_MAPPING, HWMSensorItemV23, HWMSensorItemV30
from .sdk_dll import DLL

logger = logging.getLogger(__name__)

ALARM = "\033[1;31mALARM\033[m"
DEFAULT_HWM_CONF = "/etc/lanner/hwm.conf"


class HWMSensorModel(NamedTuple):
    """To store Hardware Monitor sensor information."""
    sid: int
    name: str
    display_name: str
    value: Any
    unit: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict."""
        return dict(self._asdict())


class HWM:
    """
    Hardware Monitor.
    """

    def __init__(self) -> None:
        self._version = DLL().get_version()
        self._dw_sensor_type = c_int32(0)

    def get_cpu_temp(self, num: int) -> int:
        """
        Read temperature of the CPU processor (°C).

        Example:

        .. code-block:: python

            >>> hwm = HWM()
            >>> hwm.get_cpu_temp(1)
            40

        :param int num: selects CPU number
        :return: the current temperature value of the CPU
        :rtype: int
        :raises TypeError: The input parameters type error.
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPError: General PSP functional error.
        """
        # Check type.
        if not isinstance(num, int):
            raise TypeError("'num' type must be int")
        f_temp = c_float()
        with PSP() as psp:
            i_ret = psp.lib.LMB_HWM_GetCpuTemp(num, byref(f_temp))
        msg = get_psp_exc_msg("LMB_HWM_GetCpuTemp", i_ret)
        if i_ret == ERR_Success:
            hwm_id = f"HWMID_TEMP_CPU{num:d}"
            logger.debug(f"{HWM_DISPLAY_NAME_MAPPING[hwm_id]} = {int(f_temp.value):d}")
            return int(f_temp.value)
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def get_sys_temp(self, num: int) -> int:
        """
        Read temperature of the system (°C).

        Example:

        .. code-block:: python

            >>> hwm = HWM()
            >>> hwm.get_sys_temp(1)
            41

        :param int num: selects System sensor
        :return: the current temperature value of the system
        :rtype: int
        :raises TypeError: The input parameters type error.
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPError: General PSP functional error.
        """
        # Check type.
        if not isinstance(num, int):
            raise TypeError("'num' type must be int")
        f_temp = c_float()
        with PSP() as psp:
            i_ret = psp.lib.LMB_HWM_GetSysTemp(num, byref(f_temp))
        msg = get_psp_exc_msg("LMB_HWM_GetSysTemp", i_ret)
        if i_ret == ERR_Success:
            hwm_id = f"HWMID_TEMP_SYS{num:d}"
            logger.debug(f"{HWM_DISPLAY_NAME_MAPPING[hwm_id]} = {int(f_temp.value):d}")
            return int(f_temp.value)
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def get_core_volt(self, num: int) -> float:
        """
        Read the CPU Vcore voltage (V).

        Example:

        .. code-block:: python

            >>> hwm = HWM()
            >>> hwm.get_core_volt(1)
            0.856

        :param int num: selects CPU number
        :return: the current voltage of CPU Vcore
        :rtype: float
        :raises TypeError: The input parameters type error.
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPError: General PSP functional error.
        """
        # Check type.
        if not isinstance(num, int):
            raise TypeError("'num' type must be int")
        f_temp = c_float()
        with PSP() as psp:
            i_ret = psp.lib.LMB_HWM_GetVcore(num, byref(f_temp))
        msg = get_psp_exc_msg("LMB_HWM_GetVcore", i_ret)
        if i_ret == ERR_Success:
            hwm_id = f"HWMID_VCORE_CPU{num:d}"
            logger.debug(f"{HWM_DISPLAY_NAME_MAPPING[hwm_id]} = {f_temp.value:2.3f}")
            return float(f"{f_temp.value:2.3f}")
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def get_12v_volt(self) -> float:
        """
        Read the positive 12V voltage (V).

        Example:

        .. code-block:: python

            >>> hwm = HWM()
            >>> hwm.get_12v_volt()
            12.232

        :return: the current voltage of positive 12V
        :rtype: float
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPError: General PSP functional error.
        """
        f_temp = c_float()
        with PSP() as psp:
            i_ret = psp.lib.LMB_HWM_Get12V(byref(f_temp))
        msg = get_psp_exc_msg("LMB_HWM_Get12V", i_ret)
        if i_ret == ERR_Success:
            hwm_id = "HWMID_VOLT_P12V"
            logger.debug(f"{HWM_DISPLAY_NAME_MAPPING[hwm_id]} = {f_temp.value:2.3f}")
            return float(f"{f_temp.value:2.3f}")
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def get_5v_volt(self) -> float:
        """
        Read the positive 5V voltage (V).

        Example:

        .. code-block:: python

            >>> hwm = HWM()
            >>> hwm.get_5v_volt()
            5.087

        :return: the current voltage of positive 5V
        :rtype: float
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPError: General PSP functional error.
        """
        f_temp = c_float()
        with PSP() as psp:
            i_ret = psp.lib.LMB_HWM_Get5V(byref(f_temp))
        msg = get_psp_exc_msg("LMB_HWM_Get5V", i_ret)
        if i_ret == ERR_Success:
            hwm_id = "HWMID_VOLT_P5V"
            logger.debug(f"{HWM_DISPLAY_NAME_MAPPING[hwm_id]} = {f_temp.value:2.3f}")
            return float(f"{f_temp.value:2.3f}")
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def get_3v3_volt(self) -> float:
        """
        Read the positive 3.3V voltage (V).

        Example:

        .. code-block:: python

            >>> hwm = HWM()
            >>> hwm.get_3v3_volt()
            3.328

        :return: the current voltage of positive 3.3V
        :rtype: float
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPError: General PSP functional error.
        """
        f_temp = c_float()
        with PSP() as psp:
            i_ret = psp.lib.LMB_HWM_Get3V3(byref(f_temp))
        msg = get_psp_exc_msg("LMB_HWM_Get3V3", i_ret)
        if i_ret == ERR_Success:
            hwm_id = "HWMID_VOLT_P3V3"
            logger.debug(f"{HWM_DISPLAY_NAME_MAPPING[hwm_id]} = {f_temp.value:2.3f}")
            return float(f"{f_temp.value:2.3f}")
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def get_5vsb_volt(self) -> float:
        """
        Read the positive 5V standby power (V).

        Example:

        .. code-block:: python

            >>> hwm = HWM()
            >>> hwm.get_5vsb_volt()
            5.003

        :return: the current voltage of positive 5V standby power
        :rtype: float
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPError: General PSP functional error.
        """
        f_temp = c_float()
        with PSP() as psp:
            i_ret = psp.lib.LMB_HWM_Get5Vsb(byref(f_temp))
        msg = get_psp_exc_msg("LMB_HWM_Get5Vsb", i_ret)
        if i_ret == ERR_Success:
            hwm_id = "HWMID_VOLT_P5VSB"
            logger.debug(f"{HWM_DISPLAY_NAME_MAPPING[hwm_id]} = {f_temp.value:2.3f}")
            return float(f"{f_temp.value:2.3f}")
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def get_3v3sb_volt(self) -> float:
        """
        Read the positive 3V/3.3V standby power (V).

        Example:

        .. code-block:: python

            >>> hwm = HWM()
            >>> hwm.get_3v3sb_volt()
            3.344

        :return: the current voltage of positive 3.3V standby power
        :rtype: float
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPError: General PSP functional error.
        """
        f_temp = c_float()
        with PSP() as psp:
            i_ret = psp.lib.LMB_HWM_Get3V3sb(byref(f_temp))
        msg = get_psp_exc_msg("LMB_HWM_Get3V3sb", i_ret)
        if i_ret == ERR_Success:
            hwm_id = "HWMID_VOLT_P3V3SB"
            logger.debug(f"{HWM_DISPLAY_NAME_MAPPING[hwm_id]} = {f_temp.value:2.3f}")
            return float(f"{f_temp.value:2.3f}")
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def get_bat_volt(self) -> float:
        """
        Read the battery voltage (V).

        Example:

        .. code-block:: python

            >>> hwm = HWM()
            >>> hwm.get_bat_volt()
            3.168

        :return: the current voltage of the battery
        :rtype: float
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPError: General PSP functional error.
        """
        f_temp = c_float()
        with PSP() as psp:
            i_ret = psp.lib.LMB_HWM_GetVbat(byref(f_temp))
        msg = get_psp_exc_msg("LMB_HWM_GetVbat", i_ret)
        if i_ret == ERR_Success:
            hwm_id = "HWMID_VOLT_VBAT"
            logger.debug(f"{HWM_DISPLAY_NAME_MAPPING[hwm_id]} = {f_temp.value:2.3f}")
            return float(f"{f_temp.value:2.3f}")
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def get_dimm_volt(self, ch: int) -> float:
        """
        Read the DRAM voltage (V).

        Example:

        .. code-block:: python

            >>> hwm = HWM()
            >>> hwm.get_dimm_volt()
            1.096

        :param int ch: assign DDR channel
        :return: the current voltage of the DDR channel
        :rtype: float
        :raises TypeError: The input parameters type error.
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPError: General PSP functional error.
        """
        # Check type.
        if not isinstance(ch, int):
            raise TypeError("'num' type must be int")
        f_temp = c_float()
        with PSP() as psp:
            i_ret = psp.lib.LMB_HWM_GetVDDR(ch, byref(f_temp))
        msg = get_psp_exc_msg("LMB_HWM_GetVDDR", i_ret)
        if i_ret == ERR_Success:
            hwm_id = f"HWMID_VOLT_DDRCH{ch:d}"
            logger.debug(f"{HWM_DISPLAY_NAME_MAPPING[hwm_id]} = {f_temp.value:2.3f}")
            return float(f"{f_temp.value:2.3f}")
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def get_psu_volt(self, num: int) -> int:
        """
        Read the power supply AC input (V).

        :param int num: assigns the AC power supply number which is described in user manual
        :return: the AC power voltage
        :rtype: int
        :raises TypeError: The input parameters type error.
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPError: General PSP functional error.
        """
        # TODO: Example
        # Check type.
        if not isinstance(num, int):
            raise TypeError("'num' type must be int")
        w_data = c_uint16()
        with PSP() as psp:
            i_ret = psp.lib.LMB_HWM_GetPowerSupply(num, byref(w_data))
        msg = get_psp_exc_msg("LMB_HWM_GetPowerSupply", i_ret)
        if i_ret == ERR_Success:
            hwm_id = f"HWMID_PSU{num:d}_VOLTIN"
            logger.debug(f"{HWM_DISPLAY_NAME_MAPPING[hwm_id]} = {w_data.value:d}")
            return w_data.value
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def get_cpu_fan_speed(self, num: int) -> int:
        """
        Get CPU fan speed (RPM).

        :param int num: the number of fan
        :return: the fan speed
        :rtype: int
        :raises TypeError: The input parameters type error.
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPError: General PSP functional error.
        """
        # TODO: Example
        # Check type.
        if not isinstance(num, int):
            raise TypeError("'num' type must be int")
        w_rpm = c_uint16()
        with PSP() as psp:
            i_ret = psp.lib.LMB_HWM_GetCpuFan(num, byref(w_rpm))
        msg = get_psp_exc_msg("LMB_HWM_GetCpuFan", i_ret)
        if i_ret == ERR_Success:
            hwm_id = f"HWMID_RPM_FanCpu{num:d}"
            logger.debug(f"{HWM_DISPLAY_NAME_MAPPING[hwm_id]} = {int(w_rpm.value):d}")
            return int(w_rpm.value)
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def get_sys_fan_speed(self, num: int) -> int:
        """
        Get SYS fan speed (RPM).

        :param int num: the number of fan
        :return: the fan speed
        :rtype: int
        :raises TypeError: The input parameters type error.
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPError: General PSP functional error.
        """
        # TODO: Example
        # Check type.
        if not isinstance(num, int):
            raise TypeError("'num' type must be int")
        w_rpm = c_uint16()
        with PSP() as psp:
            i_ret = psp.lib.LMB_HWM_GetSysFan(num, byref(w_rpm))
        msg = get_psp_exc_msg("LMB_HWM_GetSysFan", i_ret)
        if i_ret == ERR_Success:
            hwm_id = f"HWMID_RPM_FanSys{num:d}"
            logger.debug(f"{HWM_DISPLAY_NAME_MAPPING[hwm_id]} = {int(w_rpm.value):d}")
            return int(w_rpm.value)
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def get_fan_speed(self, num: int) -> int:
        """
        Read the fan speed which was assigned (RPM).

        Example:

        .. code-block:: python

            >>> hwm = HWM()
            >>> hwm.get_fan_speed(1)
            7297

        :param int num: assigns the fan index number which is described in user manual
        :return: the fan speed
        :rtype: int
        :raises TypeError: The input parameters type error.
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPError: General PSP functional error.
        """
        # Check type.
        if not isinstance(num, int):
            raise TypeError("'num' type must be int")
        w_rpm = c_uint16()
        with PSP() as psp:
            i_ret = psp.lib.LMB_HWM_GetFanSpeed(num, byref(w_rpm))
        msg = get_psp_exc_msg("LMB_HWM_GetFanSpeed", i_ret)
        if i_ret == ERR_Success:
            hwm_id = f"HWMID_RPM_Fan{num:d}A"
            logger.debug(f"{HWM_DISPLAY_NAME_MAPPING[hwm_id]} = {int(w_rpm.value):d}")
            return int(w_rpm.value)
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def get_fan_speed_ex(self, num: int, ex_num: int) -> int:
        """
        Read the fan speed which was assigned (RPM).

        Example:

        .. code-block:: python

            >>> hwm = HWM()
            >>> hwm.get_fan_speed_ex(1, 1)
            7258

        :param int num: assigns the fan index number which is described in user manual
        :param int ex_num: assigns the fan sub-index number which is described in user manual (A=1, B=2, and so on)
        :return: the fan speed
        :rtype: int
        :raises TypeError: The input parameters type error.
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPError: General PSP functional error.
        """
        # Check type.
        if not isinstance(num, int):
            raise TypeError("'num' type must be int")
        if not isinstance(ex_num, int):
            raise TypeError("'ex_num' type must be int")
        w_rpm = c_uint16()
        with PSP() as psp:
            i_ret = psp.lib.LMB_HWM_GetFanSpeedEx(num, byref(w_rpm), ex_num)
        msg = get_psp_exc_msg("LMB_HWM_GetFanSpeedEx", i_ret)
        if i_ret == ERR_Success:
            hwm_id = f"HWMID_RPM_Fan{num:d}{ascii_uppercase[ex_num - 1]}"
            logger.debug(f"{HWM_DISPLAY_NAME_MAPPING[hwm_id]} = {int(w_rpm.value):d}")
            return int(w_rpm.value)
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def get_sensor_name(self, sid: int) -> str:
        """
        Get the sensor ID name by PSP define.

        Example:

        .. code-block:: python

            >>> hwm = HWM()
            >>> hwm.get_sensor_name(0)
            'HWMID_TEMP_CPU1'

        :param int sid: designates sensor index number
        :return: the sensor name of the designated
        :rtype: str
        :raises TypeError: The input parameters type error.
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPError: General PSP functional error.
        """
        # Check type.
        if not isinstance(sid, int):
            raise TypeError("'sid' type must be int")
        # Check value.
        if self._version.dll_major == 2 and self._version.dll_minor == 1:
            pass  # Can not check.
        elif self._version.dll_major == 2 and self._version.dll_minor == 3:
            if sid not in range(HWMSensorItemV23.HWMID_TOTAL.value):
                raise PSPInvalid(f"'sid' value must be in range({HWMSensorItemV23.HWMID_TOTAL.value})")
        elif self._version.dll_major == 3 and self._version.dll_minor == 0:
            if sid not in range(HWMSensorItemV30.HWMID_TOTAL.value):
                raise PSPInvalid(f"'sid' value must be in range({HWMSensorItemV30.HWMID_TOTAL.value})")
        else:
            raise NotImplementedError
        str_id_name = create_string_buffer(50)
        memset(str_id_name, 0, 30)
        with PSP() as psp:
            if self._version.dll_major == 2 and self._version.dll_minor in (1, 2, 3):
                i_ret = psp.lib.LMB_HWM_GetSensorName(sid, str_id_name)
            elif self._version.dll_major == 3 and self._version.dll_minor == 0:
                i_ret = psp.lib.LMB_HWM_GetSensorName(sid, str_id_name, sizeof(str_id_name))
        msg = get_psp_exc_msg("LMB_HWM_GetSensorName", i_ret)
        if i_ret == ERR_Success:
            name: str = str_id_name.value.decode(errors="ignore")
            logger.debug(f"Sensor ID={sid:d}, name is \"{name}\"")
            return name
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def get_sensor_msg(self, sid: int) -> str:
        """
        Read the sensor report message.

        Example:

        .. code-block:: python

            >>> hwm = HWM()
            >>> hwm.get_sensor_msg(0)
            '41000 mCelsius'

        :param int sid: designates sensor index number
        :return: the message of the designated
        :rtype: str
        :raises TypeError: The input parameters type error.
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPError: General PSP functional error.
        """
        # Check type.
        if not isinstance(sid, int):
            raise TypeError("'sid' type must be int")
        # Check value.
        if self._version.dll_major == 2 and self._version.dll_minor == 1:
            pass
        elif self._version.dll_major == 2 and self._version.dll_minor == 3:
            if sid not in range(HWMSensorItemV23.HWMID_TOTAL.value):
                raise PSPInvalid(f"'sid' value must be in range({HWMSensorItemV23.HWMID_TOTAL.value})")
        elif self._version.dll_major == 3 and self._version.dll_minor == 0:
            if sid not in range(HWMSensorItemV30.HWMID_TOTAL.value):
                raise PSPInvalid(f"'sid' value must be in range({HWMSensorItemV30.HWMID_TOTAL.value})")
        else:
            raise NotImplementedError
        str_msg = create_string_buffer(50)
        memset(str_msg, 0, 30)
        with PSP() as psp:
            if self._version.dll_major == 2 and self._version.dll_minor in (1, 2, 3):
                i_ret = psp.lib.LMB_HWM_GetSensorReport(sid, str_msg)
            elif self._version.dll_major == 3 and self._version.dll_minor == 0:
                i_ret = psp.lib.LMB_HWM_GetSensorReport(sid, str_msg, sizeof(str_msg))
        msg = get_psp_exc_msg("LMB_HWM_GetSensorReport", i_ret)
        if i_ret == ERR_Success:
            message: str = str_msg.value.decode(errors="ignore")
            logger.debug(f"Sensor ID={sid:d}, message is \"{message}\"")
            return message
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def list_supported_sensors(self) -> List[HWMSensorModel]:
        """
        List all supported sensors.

        Example:

        .. code-block:: python

            >>> hwm = HWM()
            >>> sensors = hwm.list_supported_sensors()
            >>> for s in sensors:
            ...     s.to_dict()
            {'sid': 0, 'name': 'HWMID_TEMP_CPU1', 'display_name': 'CPU-1 temperature', 'value': 40, 'unit': '°C'}
            {'sid': 2, 'name': 'HWMID_TEMP_SYS1', 'display_name': 'SYS-1 temperature', 'value': 42, 'unit': '°C'}
            .
            .
            .
            {'sid': 12, 'name': 'HWMID_VOLT_DDRCH1', 'display_name': 'VDIMM-1', 'value': 1.096, 'unit': 'V'}
            >>> for s in sensors:
            ...     print(f"{s.display_name} = {s.value} {s.unit}")
            ...
            CPU-1 temperature = 40 °C
            SYS-1 temperature = 42 °C
            .
            .
            .
            VDIMM-1 = 1.096 V

        :return: list of supported sensor model
        :rtype: List[HWMSensorModel]
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPInvalid: The input parameter is out of range.
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPError: General PSP functional error.
        """
        if self._version.dll_major == 2 and self._version.dll_minor == 1:
            total = 100
        elif self._version.dll_major == 2 and self._version.dll_minor in (2, 3):
            total = HWMSensorItemV23.HWMID_TOTAL.value
        elif self._version.dll_major == 3 and self._version.dll_minor == 0:
            total = HWMSensorItemV30.HWMID_TOTAL.value
        else:
            raise NotImplementedError
        supported_sensors = []
        for i in range(total):
            try:
                message = self.get_sensor_msg(i)
            except PSPError:
                continue
            name = self.get_sensor_name(i)
            display_name = HWM_DISPLAY_NAME_MAPPING[name]
            [value_str, unit] = message.strip().split()  # type: str
            if unit in ("mCelsius",):
                value = int(value_str) // 1000
                unit = "C"
            elif unit in ("mVolts",):
                value = int(value_str) / 1000
                unit = "V"
            elif unit in ("mAmps",):
                value = int(value_str) / 1000
                unit = "A"
            elif unit in ("mWatts",):
                value = int(value_str) / 1000
                unit = "W"
            elif unit in ("Volts",):
                value = int(value_str)
                unit = "V"
            elif unit in ("RPM",):
                value = int(value_str)
                unit = "RPM"
            elif unit in ("Status",):
                value = value_str
                unit = "Status"
            else:
                value = None
                # NotImplementedError
            supported_sensors.append(HWMSensorModel(sid=i,
                                                    name=name,
                                                    display_name=display_name,
                                                    value=value,
                                                    unit=unit))
        return supported_sensors

    def testhwm(
            self,
            conf_path: Union[
                str, bytes, "PathLike[str]", "PathLike[bytes]",
                Iterable[Union[str, bytes, "PathLike[str]", "PathLike[bytes]"]],
            ] = "/opt/lanner/psp/bin/amd64/utils/hwm.conf",
    ) -> None:
        """
        For hardware monitor testing.

        Example:

        .. code-block:: python

            >>> hwm = HWM()
            >>> hwm.testhwm()
            CPU-1 temperature =  40 C       (min =  30 C, max =  85 C)
            SYS-1 temperature =  41 C       (min =  25 C, max =  65 C)
            CPU-1 Vcore =   0.856 V         (min =   0.600 V, max =   2.000 V)
            5V =   5.087 V                  (min =   4.500 V, max =   5.500 V)
            3.3V =   3.350 V                (min =   2.970 V, max =   3.630 V)
            Vbat =   3.168 V                (min =   3.000 V, max =   3.300 V)
            VDDR =   1.104 V                (min =   1.080 V, max =   1.320 V)

        or

        .. code-block:: python

            >>> hwm = HWM()
            >>> hwm.testhwm()
            ===> Hardware Monitor Type is SuperIO <===
            Sensor Name        Value          LowCritical      UpperCritical   Result
            -------------------------------------------------------------------------
            SYS1 Temp        =      40 C    (min =      -5 C, max =      70 C)
            SYS2 Temp        =      39 C    (min =      -5 C, max =      70 C)
            Vcore            =   0.784 V    (min =   0.450 V, max =   1.350 V)
            VGFX             =   0.824 V    (min =   0.450 V, max =   1.350 V)
            12V              =  12.232 V    (min =  11.400 V, max =  12.600 V)
            5V               =   5.003 V    (min =   4.750 V, max =   5.250 V)
            VCC3V            =   3.344 V    (min =   3.130 V, max =   3.460 V)
            VSB3V            =   3.344 V    (min =   3.130 V, max =   3.460 V)
            VBAT             =   3.280 V    (min =   2.000 V, max =   3.470 V)

        :type conf_path:
            str or bytes or PathLike[str] or PathLike[bytes]
            or Iterable[str or bytes or PathLike[str] or PathLike[bytes]]
        :param conf_path:
            path of the `hwm.conf`
        """
        if self._version.dll_major == 2 and self._version.dll_minor == 1:
            self._hwm_tst_v21(conf_path)
        elif self._version.dll_major == 2 and self._version.dll_minor == 3:
            self._hwm_tst_v23(conf_path)
        elif self._version.dll_major == 3 and self._version.dll_minor == 0:
            self._hwm_tst_v30(conf_path)
        else:
            raise NotImplementedError

    def _hwm_tst_v21(
            self,
            conf_path: Union[
                str, bytes, "PathLike[str]", "PathLike[bytes]",
                Iterable[Union[str, bytes, "PathLike[str]", "PathLike[bytes]"]],
            ],
    ) -> None:
        """
        For PSP version == '2.1.X'.
        """
        f_temp = c_float()
        w_data = c_uint16()
        w_rpm = c_uint16()
        cp = ConfigParser()
        cp.read(conf_path)
        with PSP() as psp:
            # Temperature area
            if psp.lib.LMB_HWM_GetCpuTemp(1, byref(f_temp)) == ERR_Success:
                min_ = self._str_replace(cp.get("HWM_CPU1_Temp", "min", fallback="0"))
                max_ = self._str_replace(cp.get("HWM_CPU1_Temp", "max", fallback="0"))
                msg = f"CPU-1 temperature = {int(f_temp.value):3d} C\t" \
                      f"(min = {min_:3.0f} C, max = {max_:3.0f} C)"
                if f_temp.value < min_ or f_temp.value > max_:
                    msg += f" {ALARM}"
                print(msg)
            if psp.lib.LMB_HWM_GetCpuTemp(2, byref(f_temp)) == ERR_Success:
                min_ = self._str_replace(cp.get("HWM_CPU2_Temp", "min", fallback="0"))
                max_ = self._str_replace(cp.get("HWM_CPU2_Temp", "max", fallback="0"))
                msg = f"CPU-2 temperature = {int(f_temp.value):3d} C\t" \
                      f"(min = {min_:3.0f} C, max = {max_:3.0f} C)"
                if f_temp.value < min_ or f_temp.value > max_:
                    msg += f" {ALARM}"
                print(msg)
            if psp.lib.LMB_HWM_GetSysTemp(1, byref(f_temp)) == ERR_Success:
                min_ = self._str_replace(cp.get("HWM_SYS1_Temp", "min", fallback="0"))
                max_ = self._str_replace(cp.get("HWM_SYS1_Temp", "max", fallback="0"))
                msg = f"SYS-1 temperature = {int(f_temp.value):3d} C\t" \
                      f"(min = {min_:3.0f} C, max = {max_:3.0f} C)"
                if f_temp.value < min_ or f_temp.value > max_:
                    msg += f" {ALARM}"
                print(msg)
            if psp.lib.LMB_HWM_GetSysTemp(2, byref(f_temp)) == ERR_Success:
                min_ = self._str_replace(cp.get("HWM_SYS2_Temp", "min", fallback="0"))
                max_ = self._str_replace(cp.get("HWM_SYS2_Temp", "max", fallback="0"))
                msg = f"SYS-2 temperature = {int(f_temp.value):3d} C\t" \
                      f"(min = {min_:3.0f} C, max = {max_:3.0f} C)"
                if f_temp.value < min_ or f_temp.value > max_:
                    msg += f" {ALARM}"
                print(msg)
            # Voltage area
            if psp.lib.LMB_HWM_GetVcore(1, byref(f_temp)) == ERR_Success:
                min_ = self._str_replace(cp.get("HWM_Core1_volt", "min", fallback="0"))
                max_ = self._str_replace(cp.get("HWM_Core1_volt", "max", fallback="0"))
                msg = f"CPU-1 Vcore = {f_temp.value:7.3f} V\t\t" \
                      f"(min = {min_:7.3f} V, max = {max_:7.3f} V)"
                round_up_buffer = int(f_temp.value * 1000)
                if round_up_buffer < int(min_ * 1000) or round_up_buffer > int(max_ * 1000):
                    msg += f" {ALARM}"
                print(msg)
            if psp.lib.LMB_HWM_GetVcore(2, byref(f_temp)) == ERR_Success:
                min_ = self._str_replace(cp.get("HWM_Core2_volt", "min", fallback="0"))
                max_ = self._str_replace(cp.get("HWM_Core2_volt", "max", fallback="0"))
                msg = f"CPU-2 Vcore = {f_temp.value:7.3f} V\t\t" \
                      f"(min = {min_:7.3f} V, max = {max_:7.3f} V)"
                round_up_buffer = int(f_temp.value * 1000)
                if round_up_buffer < int(min_ * 1000) or round_up_buffer > int(max_ * 1000):
                    msg += f" {ALARM}"
                print(msg)
            if psp.lib.LMB_HWM_Get12V(byref(f_temp)) == ERR_Success:
                min_ = self._str_replace(cp.get("HWM_12v_volt", "min", fallback="0"))
                max_ = self._str_replace(cp.get("HWM_12v_volt", "max", fallback="0"))
                msg = f"12V = {f_temp.value:7.3f} V\t\t\t" \
                      f"(min = {min_:7.3f} V, max = {max_:7.3f} V)"
                round_up_buffer = int(f_temp.value * 1000)
                if round_up_buffer < int(min_ * 1000) or round_up_buffer > int(max_ * 1000):
                    msg += f" {ALARM}"
                print(msg)
            if psp.lib.LMB_HWM_Get5V(byref(f_temp)) == ERR_Success:
                min_ = self._str_replace(cp.get("HWM_5v_volt", "min", fallback="0"))
                max_ = self._str_replace(cp.get("HWM_5v_volt", "max", fallback="0"))
                msg = f"5V = {f_temp.value:7.3f} V\t\t\t" \
                      f"(min = {min_:7.3f} V, max = {max_:7.3f} V)"
                round_up_buffer = int(f_temp.value * 1000)
                if round_up_buffer < int(min_ * 1000) or round_up_buffer > int(max_ * 1000):
                    msg += f" {ALARM}"
                print(msg)
            if psp.lib.LMB_HWM_Get3V3(byref(f_temp)) == ERR_Success:
                min_ = self._str_replace(cp.get("HWM_3v3_volt", "min", fallback="0"))
                max_ = self._str_replace(cp.get("HWM_3v3_volt", "max", fallback="0"))
                msg = f"3.3V = {f_temp.value:7.3f} V\t\t" \
                      f"(min = {min_:7.3f} V, max = {max_:7.3f} V)"
                round_up_buffer = int(f_temp.value * 1000)
                if round_up_buffer < int(min_ * 1000) or round_up_buffer > int(max_ * 1000):
                    msg += f" {ALARM}"
                print(msg)
            if psp.lib.LMB_HWM_Get5Vsb(byref(f_temp)) == ERR_Success:
                min_ = self._str_replace(cp.get("HWM_5vsb_volt", "min", fallback="0"))
                max_ = self._str_replace(cp.get("HWM_5vsb_volt", "max", fallback="0"))
                msg = f"5VSB = {f_temp.value:7.3f} V\t\t" \
                      f"(min = {min_:7.3f} V, max = {max_:7.3f} V)"
                round_up_buffer = int(f_temp.value * 1000)
                if round_up_buffer < int(min_ * 1000) or round_up_buffer > int(max_ * 1000):
                    msg += f" {ALARM}"
                print(msg)
            if psp.lib.LMB_HWM_Get3V3sb(byref(f_temp)) == ERR_Success:
                min_ = self._str_replace(cp.get("HWM_3v3sb_volt", "min", fallback="0"))
                max_ = self._str_replace(cp.get("HWM_3v3sb_volt", "max", fallback="0"))
                msg = f"3.3VSB = {f_temp.value:7.3f} V\t\t" \
                      f"(min = {min_:7.3f} V, max = {max_:7.3f} V)"
                round_up_buffer = int(f_temp.value * 1000)
                if round_up_buffer < int(min_ * 1000) or round_up_buffer > int(max_ * 1000):
                    msg += f" {ALARM}"
                print(msg)
            if psp.lib.LMB_HWM_GetVbat(byref(f_temp)) == ERR_Success:
                min_ = self._str_replace(cp.get("HWM_vBat_volt", "min", fallback="0"))
                max_ = self._str_replace(cp.get("HWM_vBat_volt", "max", fallback="0"))
                msg = f"Vbat = {f_temp.value:7.3f} V\t\t" \
                      f"(min = {min_:7.3f} V, max = {max_:7.3f} V)"
                round_up_buffer = int(f_temp.value * 1000)
                if round_up_buffer < int(min_ * 1000) or round_up_buffer > int(max_ * 1000):
                    msg += f" {ALARM}"
                print(msg)
            if psp.lib.LMB_HWM_GetVDDR(1, byref(f_temp)) == ERR_Success:
                min_ = self._str_replace(cp.get("HWM_vddr_volt", "min", fallback="0"))
                max_ = self._str_replace(cp.get("HWM_vddr_volt", "max", fallback="0"))
                msg = f"VDDR = {f_temp.value:7.3f} V\t\t" \
                      f"(min = {min_:7.3f} V, max = {max_:7.3f} V)"
                round_up_buffer = int(f_temp.value * 1000)
                if round_up_buffer < int(min_ * 1000) or round_up_buffer > int(max_ * 1000):
                    msg += f" {ALARM}"
                print(msg)
            if psp.lib.LMB_HWM_GetPowerSupply(1, byref(w_data)) == ERR_Success:
                min_ = self._str_replace(cp.get("HWM_PSU1_volt", "min", fallback="0"))
                max_ = self._str_replace(cp.get("HWM_PSU1_volt", "max", fallback="0"))
                msg = f"PowerSupply 1 AC voltage = {w_data.value:3d} V\t" \
                      f"(min = {min_:3.0f} V, max = {max_:3.0f} V)"
                if w_data.value < min_ or w_data.value > max_:
                    msg += f" {ALARM}"
                print(msg)
            if psp.lib.LMB_HWM_GetPowerSupply(2, byref(w_data)) == ERR_Success:
                min_ = self._str_replace(cp.get("HWM_PSU2_volt", "min", fallback="0"))
                max_ = self._str_replace(cp.get("HWM_PSU2_volt", "max", fallback="0"))
                msg = f"PowerSupply 2 AC voltage = {w_data.value:3d} V\t" \
                      f"(min = {min_:3.0f} V, max = {max_:3.0f} V)"
                if w_data.value < min_ or w_data.value > max_:
                    msg += f" {ALARM}"
                print(msg)
            # Fan area
            if psp.lib.LMB_HWM_GetCpuFan(1, byref(w_rpm)) == ERR_Success:
                min_ = self._str_replace(cp.get("HWM_CPU1_RPM", "min", fallback="0"))
                max_ = self._str_replace(cp.get("HWM_CPU1_RPM", "max", fallback="0"))
                msg = f"CPU FAN 1 speed = {w_rpm.value:5d} rpm\t" \
                      f"(min = {min_:5.0f} rpm, max = {max_:5.0f} rpm)"
                if w_rpm.value < min_ or w_rpm.value > max_:
                    msg += f" {ALARM}"
                print(msg)
            if psp.lib.LMB_HWM_GetCpuFan(2, byref(w_rpm)) == ERR_Success:
                min_ = self._str_replace(cp.get("HWM_CPU2_RPM", "min", fallback="0"))
                max_ = self._str_replace(cp.get("HWM_CPU2_RPM", "max", fallback="0"))
                msg = f"CPU FAN 2 speed = {w_rpm.value:5d} rpm\t" \
                      f"(min = {min_:5.0f} rpm, max = {max_:5.0f} rpm)"
                if w_rpm.value < min_ or w_rpm.value > max_:
                    msg += f" {ALARM}"
                print(msg)
            if psp.lib.LMB_HWM_GetSysFan(1, byref(w_rpm)) == ERR_Success:
                min_ = self._str_replace(cp.get("HWM_SYS1_RPM", "min", fallback="0"))
                max_ = self._str_replace(cp.get("HWM_SYS1_RPM", "max", fallback="0"))
                msg = f"SYS FAN 1 speed = {w_rpm.value:5d} rpm\t" \
                      f"(min = {min_:5.0f} rpm, max = {max_:5.0f} rpm)"
                if w_rpm.value < min_ or w_rpm.value > max_:
                    msg += f" {ALARM}"
                print(msg)
            if psp.lib.LMB_HWM_GetSysFan(2, byref(w_rpm)) == ERR_Success:
                min_ = self._str_replace(cp.get("HWM_SYS2_RPM", "min", fallback="0"))
                max_ = self._str_replace(cp.get("HWM_SYS2_RPM", "max", fallback="0"))
                msg = f"SYS FAN 2 speed = {w_rpm.value:5d} rpm\t" \
                      f"(min = {min_:5.0f} rpm, max = {max_:5.0f} rpm)"
                if w_rpm.value < min_ or w_rpm.value > max_:
                    msg += f" {ALARM}"
                print(msg)

    def _hwm_tst_v23(
            self,
            conf_path: Union[
                str, bytes, "PathLike[str]", "PathLike[bytes]",
                Iterable[Union[str, bytes, "PathLike[str]", "PathLike[bytes]"]],
            ],
    ) -> None:
        """
        For PSP version == '2.3.X'.
        """
        show_ipmi_only = False
        if os.path.isfile(conf_path):
            print(f"\033[1;31m<Note> found {conf_path} file, critical value will change !!!\033[m")
        else:
            conf_path = DEFAULT_HWM_CONF
            if os.path.isfile(conf_path):
                print(f"\033[1;31m<Note> found {conf_path} file, critical value will change !!!\033[m")
        cp = ConfigParser()
        cp.read(conf_path)

        with PSP() as psp:
            psp.lib.LMB_HWM_GetSensorType(byref(self._dw_sensor_type))

        if self._dw_sensor_type.value == HWM_TYPE_NONE:
            print("\033[1;31m<Warning> Hardware Monitor Type is Unknown !!!\033[m")
            return
        elif self._dw_sensor_type.value == HWM_TYPE_IPMI:
            show_ipmi_only = True
            print("\033[1;34m===> Hardware Monitor Type is IPMI <===\033[m")
        elif self._dw_sensor_type.value == HWM_TYPE_AST1400:
            print("\033[1;34m===> Hardware Monitor Type is AST-1400 <===\033[m")
        elif self._dw_sensor_type.value == HWM_TYPE_SMBUS:
            print("\033[1;34m===> Hardware Monitor Type is SMBus <===\033[m")
        elif self._dw_sensor_type.value == HWM_TYPE_SIO:
            print("\033[1;34m===> Hardware Monitor Type is SuperIO <===\033[m")
        else:
            print("\033[1;31m<Warning> Hardware Monitor Type is Unknown !!!\033[m")
            return

        print("Sensor Name        Value          LowCritical      UpperCritical   Result")
        print("-------------------------------------------------------------------------")

        # CPU Temperature
        sid = HWMSensorItemV23.HWMID_TEMP_CPU1.value
        for i in range(sid, sid + 4):
            self._show_temperature_v23(i, cp)
        # SYS Temperature
        sid = HWMSensorItemV23.HWMID_TEMP_SYS1.value
        for i in range(sid, sid + 4):
            self._show_temperature_v23(i, cp)

        # PCH Temperature
        sid = HWMSensorItemV23.HWMID_TEMP_PCH.value
        self._show_temperature_v23(sid, cp)

        # CPU DIMM Temperature
        sid = HWMSensorItemV23.HWMID_TEMP_DIMMP1A0.value
        for i in range(sid, sid + 32):
            self._show_temperature_v23(i, cp)

        # CPU Vcore
        sid = HWMSensorItemV23.HWMID_VCORE_CPU1.value
        for i in range(sid, sid + 4):
            self._show_voltage_v23(i, cp)
        # P12V
        sid = HWMSensorItemV23.HWMID_VOLT_P12V.value
        self._show_voltage_v23(sid, cp)
        # P5V
        sid = HWMSensorItemV23.HWMID_VOLT_P5V.value
        self._show_voltage_v23(sid, cp)
        # P3.3V
        sid = HWMSensorItemV23.HWMID_VOLT_P3V3.value
        self._show_voltage_v23(sid, cp)
        # P5VSB
        sid = HWMSensorItemV23.HWMID_VOLT_P5VSB.value
        self._show_voltage_v23(sid, cp)
        # P3.3VSB
        sid = HWMSensorItemV23.HWMID_VOLT_P3V3SB.value
        self._show_voltage_v23(sid, cp)
        # VBAT
        sid = HWMSensorItemV23.HWMID_VOLT_VBAT.value
        self._show_voltage_v23(sid, cp)
        # 1.05V
        sid = HWMSensorItemV23.HWMID_VOLT_P1V05.value
        self._show_voltage_v23(sid, cp)
        # VCCIO
        sid = HWMSensorItemV23.HWMID_VOLT_PVCCIO_CPU1.value
        for i in range(sid, sid + 4):
            self._show_voltage_v23(i, cp)

        # VCCSA
        sid = HWMSensorItemV23.HWMID_VOLT_PVCCSA_CPU1.value
        for i in range(sid, sid + 4):
            self._show_voltage_v23(i, cp)
        # VNN
        sid = HWMSensorItemV23.HWMID_VOLT_PVNN.value
        self._show_voltage_v23(sid, cp)

        # DDR Voltage
        sid = HWMSensorItemV23.HWMID_VOLT_DDRCH1.value
        for i in range(sid, sid + 8):
            self._show_voltage_v23(i, cp)
        # extern sensors
        sid = HWMSensorItemV23.HWMID_PSU2_TEMP2.value + 1
        for i in range(sid, HWMSensorItemV23.HWMID_TOTAL.value):
            self._show_voltage_v23(i, cp)

        sid = HWMSensorItemV23.HWMID_RPM_Fan1A.value
        for i in range(10):
            self._show_rpm_v23(i * 2 + sid, cp)
            self._show_rpm_v23(i * 2 + sid + 1, cp)

        # IPMI PSU
        for i in range(2):
            if show_ipmi_only:
                print("\033[2;31m================ For PSU when BMC exist ==========================\033[m")
                show_ipmi_only = False

            # PSU VIn
            sid = HWMSensorItemV23.HWMID_PSU1_VOLTIN.value + 11 * i
            self._show_voltage_v23(sid, cp)
            # PSU Vout
            sid = HWMSensorItemV23.HWMID_PSU1_VOLTOUT.value + 11 * i
            self._show_voltage_v23(sid, cp)
            # PSU Current In
            sid = HWMSensorItemV23.HWMID_PSU1_CURRENTIN.value + 11 * i
            self._show_current_v23(sid, cp)
            # PSU Current Out
            sid = HWMSensorItemV23.HWMID_PSU1_CURRENTOUT.value + 11 * i
            self._show_current_v23(sid, cp)
            # PSU Power In
            sid = HWMSensorItemV23.HWMID_PSU1_POWERIN.value + 11 * i
            self._show_watts_v23(sid, cp)
            # PSU Power Out
            sid = HWMSensorItemV23.HWMID_PSU1_POWEROUT.value + 11 * i
            self._show_watts_v23(sid, cp)
            # PSU Fan 1
            sid = HWMSensorItemV23.HWMID_PSU1_FAN1.value + 11 * i
            self._show_rpm_v23(sid, cp)
            # PSU Fan 2
            sid = HWMSensorItemV23.HWMID_PSU1_FAN2.value + 11 * i
            self._show_rpm_v23(sid, cp)
            # PSU Temp 1
            sid = HWMSensorItemV23.HWMID_PSU1_TEMP1.value + 11 * i
            self._show_temperature_v23(sid, cp)
            # PSU Temp 2
            sid = HWMSensorItemV23.HWMID_PSU1_TEMP2.value + 11 * i
            self._show_temperature_v23(sid, cp)

    def _show_temperature_v23(self, sid: int, cp: ConfigParser) -> None:
        """
        For PSP version == '2.3.X'.
        """
        str_msg = create_string_buffer(30)
        str_disp = create_string_buffer(30)
        str_id_name = create_string_buffer(30)
        stu_sensor_info = IPMISensorInfo()
        udw_hi_critical = c_uint32()
        udw_lo_critical = c_uint32()
        f_flag_value = 0
        memset(str_msg, 0, 30)
        with PSP() as psp:
            if psp.lib.LMB_HWM_GetSensorReport(sid, str_msg) != ERR_NotSupport:
                psp.lib.LMB_HWM_GetSensorDisplay(sid, str_disp)
                psp.lib.LMB_HWM_GetSensorName(sid, str_id_name)
                min_ = self._str_replace(cp.get(str_id_name.value.decode(), "min", fallback="999999"))
                if min_ == 999999:  # hwm.conf not setting, read from SDK.
                    if self._dw_sensor_type.value == HWM_TYPE_IPMI:
                        i_ret = psp.lib.LMB_IPMI_InfoByName(str_disp, byref(stu_sensor_info))
                        if i_ret == ERR_Success:
                            min_ = stu_sensor_info.f_lo_critical
                            max_ = stu_sensor_info.f_hi_critical
                        else:
                            min_ = max_ = 0.0
                    else:  # read from hwm_table.h
                        psp.lib.LMB_HWM_GetSensorCritical(sid, byref(udw_lo_critical), byref(udw_hi_critical))
                        min_ = udw_lo_critical.value / 1000
                        max_ = udw_hi_critical.value / 1000
                else:
                    max_ = self._str_replace(cp.get(str_id_name.value.decode(), "max", fallback="999999"))
                if min_ in (99999, 999999):
                    f_flag_value |= 0x01
                if max_ in (99999, 999999):
                    f_flag_value |= 0x02
                space_len = self._calc_space_string(str_disp.value.decode())
                temp = self._atoll(str_msg.value.decode()) / 1000
                if f_flag_value == 0x01:  # min_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {int(temp):7d} C\t"
                          f"(min = --N/A-- C, max = {int(max_):7d} C)", end="")
                    if temp > max_:
                        print(f" {ALARM}", end="")
                elif f_flag_value == 0x02:  # max_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {int(temp):7d} C\t"
                          f"(min = {int(min_):7d} C, max = --N/A-- C)", end="")
                    if temp < min_:
                        print(f" {ALARM}", end="")
                elif f_flag_value == 0x03:  # min_ = N/A and max_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {int(temp):7d} C\t"
                          f"(min = --N/A-- C, max = --N/A-- C)", end="")
                else:
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {int(temp):7d} C\t"
                          f"(min = {int(min_):7d} C, max = {int(max_):7d} C)", end="")
                    if temp < min_ or temp > max_:
                        print(f" {ALARM}", end="")
                print()

    def _show_rpm_v23(self, sid: int, cp: ConfigParser) -> None:
        """
        For PSP version == '2.3.X'.
        """
        str_msg = create_string_buffer(30)
        str_disp = create_string_buffer(30)
        str_id_name = create_string_buffer(30)
        stu_sensor_info = IPMISensorInfo()
        udw_hi_critical = c_uint32()
        udw_lo_critical = c_uint32()
        f_flag_value = 0
        memset(str_msg, 0, 30)
        with PSP() as psp:
            if psp.lib.LMB_HWM_GetSensorReport(sid, str_msg) != ERR_NotSupport:
                psp.lib.LMB_HWM_GetSensorDisplay(sid, str_disp)
                psp.lib.LMB_HWM_GetSensorName(sid, str_id_name)
                min_ = self._str_replace(cp.get(str_id_name.value.decode(), "min", fallback="999999"))
                if min_ == 999999:  # hwm.conf not setting, read from SDK.
                    if self._dw_sensor_type.value == HWM_TYPE_IPMI:
                        i_ret = psp.lib.LMB_IPMI_InfoByName(str_disp, byref(stu_sensor_info))
                        if i_ret == ERR_Success:
                            min_ = stu_sensor_info.f_lo_critical
                            max_ = stu_sensor_info.f_hi_critical
                        else:
                            min_ = max_ = 0.0
                    else:  # read from hwm_table.h
                        psp.lib.LMB_HWM_GetSensorCritical(sid, byref(udw_lo_critical), byref(udw_hi_critical))
                        min_ = udw_lo_critical.value
                        max_ = udw_hi_critical.value
                else:
                    max_ = self._str_replace(cp.get(str_id_name.value.decode(), "max", fallback="999999"))
                if min_ in (99999, 999999):
                    f_flag_value |= 0x01
                if max_ in (99999, 999999):
                    f_flag_value |= 0x02
                space_len = self._calc_space_string(str_disp.value.decode())
                rpm = self._atoll(str_msg.value.decode())
                if f_flag_value == 0x01:  # min_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {int(rpm):5d} rpm\t"
                          f"(min = --N/A-- rpm, max = {int(max_):5d} rpm)", end="")
                    if rpm > max_:
                        print(f" {ALARM}", end="")
                elif f_flag_value == 0x02:  # max_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {int(rpm):5d} rpm\t"
                          f"(min = {int(min_):5d} rpm, max = --N/A-- rpm)", end="")
                    if rpm < min_:
                        print(f" {ALARM}", end="")
                elif f_flag_value == 0x03:  # min_ = N/A and max_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {int(rpm):5d} rpm\t"
                          f"(min = --N/A-- rpm, max = --N/A-- rpm)", end="")
                else:
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {int(rpm):5d} rpm\t"
                          f"(min = {int(min_):5d} rpm, max = {int(max_):5d} rpm)", end="")
                    if rpm < min_ or rpm > max_:
                        print(f" {ALARM}", end="")
                print()

    def _show_voltage_v23(self, sid: int, cp: ConfigParser) -> None:
        """
        For PSP version == '2.3.X'.
        """
        str_msg = create_string_buffer(30)
        str_disp = create_string_buffer(30)
        str_id_name = create_string_buffer(30)
        stu_sensor_info = IPMISensorInfo()
        udw_hi_critical = c_uint32()
        udw_lo_critical = c_uint32()
        f_flag_value = 0
        memset(str_msg, 0, 30)
        with PSP() as psp:
            if psp.lib.LMB_HWM_GetSensorReport(sid, str_msg) != ERR_NotSupport:
                psp.lib.LMB_HWM_GetSensorDisplay(sid, str_disp)
                psp.lib.LMB_HWM_GetSensorName(sid, str_id_name)
                min_ = self._str_replace(cp.get(str_id_name.value.decode(), "min", fallback="999999"))
                if min_ == 999999:  # hwm.conf not setting, read from SDK.
                    if self._dw_sensor_type.value == HWM_TYPE_IPMI:
                        i_ret = psp.lib.LMB_IPMI_InfoByName(str_disp, byref(stu_sensor_info))
                        if i_ret == ERR_Success:
                            min_ = stu_sensor_info.f_lo_critical
                            max_ = stu_sensor_info.f_hi_critical
                        else:
                            min_ = max_ = 0.0
                    else:  # read from hwm_table.h
                        psp.lib.LMB_HWM_GetSensorCritical(sid, byref(udw_lo_critical), byref(udw_hi_critical))
                        min_ = udw_lo_critical.value / 1000
                        max_ = udw_hi_critical.value / 1000
                else:
                    max_ = self._str_replace(cp.get(str_id_name.value.decode(), "max", fallback="999999"))
                if min_ in (99999, 999999):
                    f_flag_value |= 0x01
                if max_ in (99999, 999999):
                    f_flag_value |= 0x02
                space_len = self._calc_space_string(str_disp.value.decode())
                volt = self._atoll(str_msg.value.decode()) / 1000
                round_up_buffer = int(volt * 1000)
                if f_flag_value == 0x01:  # min_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {round_up_buffer * 0.001:7.3f} V\t"
                          f"(min = --N/A-- V, max = {max_:7.3f} V)", end="")
                    if round_up_buffer > int(max_ * 1000):
                        print(f" {ALARM}", end="")
                elif f_flag_value == 0x02:  # max_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {round_up_buffer * 0.001:7.3f} V\t"
                          f"(min = {min_:7.3f} V, max = --N/A-- V)", end="")
                    if round_up_buffer < int(min_ * 1000):
                        print(f" {ALARM}", end="")
                elif f_flag_value == 0x03:  # min_ = N/A and max_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {round_up_buffer * 0.001:7.3f} V\t"
                          f"(min = --N/A-- V, max = --N/A-- V)", end="")
                else:
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {round_up_buffer * 0.001:7.3f} V\t"
                          f"(min = {min_:7.3f} V, max = {max_:7.3f} V)", end="")
                    if round_up_buffer < int(min_ * 1000) or round_up_buffer > int(max_ * 1000):
                        print(f" {ALARM}", end="")
                print()

    def _show_current_v23(self, sid: int, cp: ConfigParser) -> None:
        """
        For PSP version == '2.3.X'.
        """
        str_msg = create_string_buffer(30)
        str_disp = create_string_buffer(30)
        str_id_name = create_string_buffer(30)
        stu_sensor_info = IPMISensorInfo()
        udw_hi_critical = c_uint32()
        udw_lo_critical = c_uint32()
        f_flag_value = 0
        memset(str_msg, 0, 30)
        with PSP() as psp:
            if psp.lib.LMB_HWM_GetSensorReport(sid, str_msg) != ERR_NotSupport:
                psp.lib.LMB_HWM_GetSensorDisplay(sid, str_disp)
                psp.lib.LMB_HWM_GetSensorName(sid, str_id_name)
                min_ = self._str_replace(cp.get(str_id_name.value.decode(), "min", fallback="999999"))
                if min_ == 999999:  # hwm.conf not setting, read from SDK.
                    if self._dw_sensor_type.value == HWM_TYPE_IPMI:
                        i_ret = psp.lib.LMB_IPMI_InfoByName(str_disp, byref(stu_sensor_info))
                        if i_ret == ERR_Success:
                            min_ = stu_sensor_info.f_lo_critical
                            max_ = stu_sensor_info.f_hi_critical
                        else:
                            min_ = max_ = 0.0
                    else:  # read from hwm_table.h
                        psp.lib.LMB_HWM_GetSensorCritical(sid, byref(udw_lo_critical), byref(udw_hi_critical))
                        min_ = udw_lo_critical.value / 1000
                        max_ = udw_hi_critical.value / 1000
                else:
                    max_ = self._str_replace(cp.get(str_id_name.value.decode(), "max", fallback="999999"))
                if min_ in (99999, 999999):
                    f_flag_value |= 0x01
                if max_ in (99999, 999999):
                    f_flag_value |= 0x02
                space_len = self._calc_space_string(str_disp.value.decode())
                current = self._atoll(str_msg.value.decode()) / 1000
                round_up_buffer = int(current * 1000)
                if f_flag_value == 0x01:  # min_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {round_up_buffer * 0.001:7.3f} A\t"
                          f"(min = --N/A-- A, max = {max_:7.3f} A)", end="")
                    if round_up_buffer > int(max_ * 1000):
                        print(f" {ALARM}", end="")
                elif f_flag_value == 0x02:  # max_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {round_up_buffer * 0.001:7.3f} A\t"
                          f"(min = {min_:7.3f} A, max = --N/A-- A)", end="")
                    if round_up_buffer < int(min_ * 1000):
                        print(f" {ALARM}", end="")
                elif f_flag_value == 0x03:  # min_ = N/A and max_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {round_up_buffer * 0.001:7.3f} A\t"
                          f"(min = --N/A-- A, max = --N/A-- A)", end="")
                else:
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {round_up_buffer * 0.001:7.3f} A\t"
                          f"(min = {min_:7.3f} A, max = {max_:7.3f} A)", end="")
                    if round_up_buffer < int(min_ * 1000) or round_up_buffer > int(max_ * 1000):
                        print(f" {ALARM}", end="")
                print()

    def _show_watts_v23(self, sid: int, cp: ConfigParser) -> None:
        """
        For PSP version == '2.3.X'.
        """
        str_msg = create_string_buffer(30)
        str_disp = create_string_buffer(30)
        str_id_name = create_string_buffer(30)
        stu_sensor_info = IPMISensorInfo()
        udw_hi_critical = c_uint32()
        udw_lo_critical = c_uint32()
        f_flag_value = 0
        memset(str_msg, 0, 30)
        with PSP() as psp:
            if psp.lib.LMB_HWM_GetSensorReport(sid, str_msg) != ERR_NotSupport:
                psp.lib.LMB_HWM_GetSensorDisplay(sid, str_disp)
                psp.lib.LMB_HWM_GetSensorName(sid, str_id_name)
                min_ = self._str_replace(cp.get(str_id_name.value.decode(), "min", fallback="999999"))
                if min_ == 999999:  # hwm.conf not setting, read from SDK.
                    if self._dw_sensor_type.value == HWM_TYPE_IPMI:
                        i_ret = psp.lib.LMB_IPMI_InfoByName(str_disp, byref(stu_sensor_info))
                        if i_ret == ERR_Success:
                            min_ = stu_sensor_info.f_lo_critical
                            max_ = stu_sensor_info.f_hi_critical
                        else:
                            min_ = max_ = 0.0
                    else:  # read from hwm_table.h
                        psp.lib.LMB_HWM_GetSensorCritical(sid, byref(udw_lo_critical), byref(udw_hi_critical))
                        min_ = udw_lo_critical.value / 1000
                        max_ = udw_hi_critical.value / 1000
                else:
                    max_ = self._str_replace(cp.get(str_id_name.value.decode(), "max", fallback="999999"))
                if min_ in (99999, 999999):
                    f_flag_value |= 0x01
                if max_ in (99999, 999999):
                    f_flag_value |= 0x02
                space_len = self._calc_space_string(str_disp.value.decode())
                watts = self._atoll(str_msg.value.decode()) / 1000
                round_up_buffer = int(watts * 1000)
                if f_flag_value == 0x01:  # min_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {round_up_buffer * 0.001:7.3f} W\t"
                          f"(min = --N/A-- W, max = {max_:7.3f} W)", end="")
                    if round_up_buffer > int(max_ * 1000):
                        print(f" {ALARM}", end="")
                elif f_flag_value == 0x02:  # max_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {round_up_buffer * 0.001:7.3f} W\t"
                          f"(min = {min_:7.3f} W, max = --N/A-- W)", end="")
                    if round_up_buffer < int(min_ * 1000):
                        print(f" {ALARM}", end="")
                elif f_flag_value == 0x03:  # min_ = N/A and max_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {round_up_buffer * 0.001:7.3f} W\t"
                          f"(min = --N/A-- W, max = --N/A-- W)", end="")
                else:
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {round_up_buffer * 0.001:7.3f} W\t"
                          f"(min = {min_:7.3f} W, max = {max_:7.3f} W)", end="")
                    if round_up_buffer < int(min_ * 1000) or round_up_buffer > int(max_ * 1000):
                        print(f" {ALARM}", end="")
                print()

    def _hwm_tst_v30(
            self,
            conf_path: Union[
                str, bytes, "PathLike[str]", "PathLike[bytes]",
                Iterable[Union[str, bytes, "PathLike[str]", "PathLike[bytes]"]],
            ],
    ) -> None:
        """
        For PSP version == '3.0.X'.
        """
        show_ipmi_only = False
        if os.path.isfile(conf_path):
            print(f"\033[1;31m<Note> found {conf_path} file, critical value will change !!!\033[m")
        else:
            conf_path = DEFAULT_HWM_CONF
            if os.path.isfile(conf_path):
                print(f"\033[1;31m<Note> found {conf_path} file, critical value will change !!!\033[m")
        cp = ConfigParser()
        cp.read(conf_path)

        with PSP() as psp:
            psp.lib.LMB_HWM_GetSensorType(byref(self._dw_sensor_type))

        if self._dw_sensor_type.value == HWM_TYPE_NONE:
            print("\033[1;31m<Warning> Hardware Monitor Type is Unknown !!!\033[m")
            return
        elif self._dw_sensor_type.value == HWM_TYPE_IPMI:
            show_ipmi_only = True
            print("\033[1;34m===> Hardware Monitor Type is IPMI <===\033[m")
        elif self._dw_sensor_type.value == HWM_TYPE_AST1400:
            print("\033[1;34m===> Hardware Monitor Type is AST-1400 <===\033[m")
        elif self._dw_sensor_type.value == HWM_TYPE_SMBUS:
            print("\033[1;34m===> Hardware Monitor Type is SMBus <===\033[m")
        elif self._dw_sensor_type.value == HWM_TYPE_SIO:
            print("\033[1;34m===> Hardware Monitor Type is SuperIO <===\033[m")
        else:
            print("\033[1;31m<Warning> Hardware Monitor Type is Unknown !!!\033[m")
            return

        print("Sensor Name        Value          LowCritical      UpperCritical   Result")
        print("-------------------------------------------------------------------------")

        # CPU Temperature
        sid = HWMSensorItemV30.HWMID_TEMP_CPU1.value
        for i in range(sid, sid + 4):
            self._show_temperature_v30(i, cp)
        # SYS Temperature
        sid = HWMSensorItemV30.HWMID_TEMP_SYS1.value
        for i in range(sid, sid + 4):
            self._show_temperature_v30(i, cp)

        # PCH Temperature
        sid = HWMSensorItemV30.HWMID_TEMP_PCH.value
        self._show_temperature_v30(sid, cp)

        # CPU DIMM Temperature
        sid = HWMSensorItemV30.HWMID_TEMP_DIMMP1A0.value
        for i in range(sid, sid + 32):
            self._show_temperature_v30(i, cp)

        # CPU Vcore
        sid = HWMSensorItemV30.HWMID_VCORE_CPU1.value
        for i in range(sid, sid + 4):
            self._show_voltage_v30(i, cp)
        # P12V
        sid = HWMSensorItemV30.HWMID_VOLT_P12V.value
        self._show_voltage_v30(sid, cp)
        # P5V
        sid = HWMSensorItemV30.HWMID_VOLT_P5V.value
        self._show_voltage_v30(sid, cp)
        # P3.3V
        sid = HWMSensorItemV30.HWMID_VOLT_P3V3.value
        self._show_voltage_v30(sid, cp)
        # P5VSB
        sid = HWMSensorItemV30.HWMID_VOLT_P5VSB.value
        self._show_voltage_v30(sid, cp)
        # P3.3VSB
        sid = HWMSensorItemV30.HWMID_VOLT_P3V3SB.value
        self._show_voltage_v30(sid, cp)
        # VBAT
        sid = HWMSensorItemV30.HWMID_VOLT_VBAT.value
        self._show_voltage_v30(sid, cp)
        # 1.05V
        sid = HWMSensorItemV30.HWMID_VOLT_P1V05.value
        self._show_voltage_v30(sid, cp)
        # VCCIO
        sid = HWMSensorItemV30.HWMID_VOLT_PVCCIO_CPU1.value
        for i in range(sid, sid + 4):
            self._show_voltage_v30(i, cp)

        # VCCSA
        sid = HWMSensorItemV30.HWMID_VOLT_PVCCSA_CPU1.value
        for i in range(sid, sid + 4):
            self._show_voltage_v30(i, cp)
        # VNN
        sid = HWMSensorItemV30.HWMID_VOLT_PVNN.value
        self._show_voltage_v30(sid, cp)

        # DDR Voltage
        sid = HWMSensorItemV30.HWMID_VOLT_DDRCH1.value
        for i in range(sid, sid + 8):
            self._show_voltage_v30(i, cp)
        # extern sensors
        sid = HWMSensorItemV30.HWMID_PSU2_TEMP2.value + 1
        for i in range(sid, HWMSensorItemV30.HWMID_TOTAL.value):
            self._show_voltage_v30(i, cp)

        sid = HWMSensorItemV30.HWMID_RPM_Fan1A.value
        for i in range(10):
            self._show_rpm_v30(i * 2 + sid, cp)
            self._show_rpm_v30(i * 2 + sid + 1, cp)

        # IPMI PSU
        for i in range(2):
            if show_ipmi_only:
                print("\033[2;31m================ For PSU when BMC exist ==========================\033[m")
                show_ipmi_only = False

            # PSU VIn
            sid = HWMSensorItemV30.HWMID_PSU1_VOLTIN.value + 11 * i
            self._show_voltage_v30(sid, cp)
            # PSU Vout
            sid = HWMSensorItemV30.HWMID_PSU1_VOLTOUT.value + 11 * i
            self._show_voltage_v30(sid, cp)
            # PSU Current In
            sid = HWMSensorItemV30.HWMID_PSU1_CURRENTIN.value + 11 * i
            self._show_current_v30(sid, cp)
            # PSU Current Out
            sid = HWMSensorItemV30.HWMID_PSU1_CURRENTOUT.value + 11 * i
            self._show_current_v30(sid, cp)
            # PSU Power In
            sid = HWMSensorItemV30.HWMID_PSU1_POWERIN.value + 11 * i
            self._show_watts_v30(sid, cp)
            # PSU Power Out
            sid = HWMSensorItemV30.HWMID_PSU1_POWEROUT.value + 11 * i
            self._show_watts_v30(sid, cp)
            # PSU Fan 1
            sid = HWMSensorItemV30.HWMID_PSU1_FAN1.value + 11 * i
            self._show_rpm_v30(sid, cp)
            # PSU Fan 2
            sid = HWMSensorItemV30.HWMID_PSU1_FAN2.value + 11 * i
            self._show_rpm_v30(sid, cp)
            # PSU Temp 1
            sid = HWMSensorItemV30.HWMID_PSU1_TEMP1.value + 11 * i
            self._show_temperature_v30(sid, cp)
            # PSU Temp 2
            sid = HWMSensorItemV30.HWMID_PSU1_TEMP2.value + 11 * i
            self._show_temperature_v30(sid, cp)

    def _show_temperature_v30(self, sid: int, cp: ConfigParser) -> None:
        """
        For PSP version == '3.0.X'.
        """
        str_msg = create_string_buffer(30)
        str_disp = create_string_buffer(30)
        str_id_name = create_string_buffer(30)
        stu_sensor_info = IPMISensorInfo()
        udw_hi_critical = c_uint32()
        dw_lo_critical = c_int32()
        f_flag_value = 0
        memset(str_msg, 0, 30)
        with PSP() as psp:
            if psp.lib.LMB_HWM_GetSensorReport(sid, str_msg, sizeof(str_msg)) != ERR_NotSupport:
                psp.lib.LMB_HWM_GetSensorDisplay(sid, str_disp, sizeof(str_disp))
                psp.lib.LMB_HWM_GetSensorName(sid, str_id_name, sizeof(str_id_name))
                min_ = self._str_replace(cp.get(str_id_name.value.decode(), "min", fallback="999999"))
                if min_ == 999999:  # hwm.conf not setting, read from SDK.
                    if self._dw_sensor_type.value == HWM_TYPE_IPMI:
                        i_ret = psp.lib.LMB_IPMI_InfoByName(str_disp, byref(stu_sensor_info))
                        if i_ret == ERR_Success:
                            min_ = stu_sensor_info.f_lo_critical
                            max_ = stu_sensor_info.f_hi_critical
                        else:
                            min_ = max_ = 0.0
                    else:  # read from hwm_table.h
                        psp.lib.LMB_HWM_GetSensorCritical(sid, byref(dw_lo_critical), byref(udw_hi_critical))
                        min_ = dw_lo_critical.value / 1000
                        max_ = udw_hi_critical.value / 1000
                else:
                    max_ = self._str_replace(cp.get(str_id_name.value.decode(), "max", fallback="999999"))
                if min_ in (99999, 999999):
                    f_flag_value |= 0x01
                if max_ in (99999, 999999):
                    f_flag_value |= 0x02
                space_len = self._calc_space_string(str_disp.value.decode())
                temp = self._atoll(str_msg.value.decode()) / 1000
                if f_flag_value == 0x01:  # min_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {int(temp):7d} C\t"
                          f"(min = --N/A-- C, max = {int(max_):7d} C)", end="")
                    if temp > max_:
                        print(f" {ALARM}", end="")
                elif f_flag_value == 0x02:  # max_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {int(temp):7d} C\t"
                          f"(min = {int(min_):7d} C, max = --N/A-- C)", end="")
                    if temp < min_:
                        print(f" {ALARM}", end="")
                elif f_flag_value == 0x03:  # min_ = N/A and max_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {int(temp):7d} C\t"
                          f"(min = --N/A-- C, max = --N/A-- C)", end="")
                else:
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {int(temp):7d} C\t"
                          f"(min = {int(min_):7d} C, max = {int(max_):7d} C)", end="")
                    if temp < min_ or temp > max_:
                        print(f" {ALARM}", end="")
                print()

    def _show_rpm_v30(self, sid: int, cp: ConfigParser) -> None:
        """
        For PSP version == '3.0.X'.
        """
        str_msg = create_string_buffer(30)
        str_disp = create_string_buffer(30)
        str_id_name = create_string_buffer(30)
        stu_sensor_info = IPMISensorInfo()
        udw_hi_critical = c_uint32()
        dw_lo_critical = c_int32()
        f_flag_value = 0
        memset(str_msg, 0, 30)
        with PSP() as psp:
            if psp.lib.LMB_HWM_GetSensorReport(sid, str_msg, sizeof(str_msg)) != ERR_NotSupport:
                psp.lib.LMB_HWM_GetSensorDisplay(sid, str_disp, sizeof(str_disp))
                psp.lib.LMB_HWM_GetSensorName(sid, str_id_name, sizeof(str_id_name))
                min_ = self._str_replace(cp.get(str_id_name.value.decode(), "min", fallback="999999"))
                if min_ == 999999:  # hwm.conf not setting, read from SDK.
                    if self._dw_sensor_type.value == HWM_TYPE_IPMI:
                        i_ret = psp.lib.LMB_IPMI_InfoByName(str_disp, byref(stu_sensor_info))
                        if i_ret == ERR_Success:
                            min_ = stu_sensor_info.f_lo_critical
                            max_ = stu_sensor_info.f_hi_critical
                        else:
                            min_ = max_ = 0.0
                    else:  # read from hwm_table.h
                        psp.lib.LMB_HWM_GetSensorCritical(sid, byref(dw_lo_critical), byref(udw_hi_critical))
                        min_ = dw_lo_critical.value
                        max_ = udw_hi_critical.value
                else:
                    max_ = self._str_replace(cp.get(str_id_name.value.decode(), "max", fallback="999999"))
                if min_ in (99999, 999999):
                    f_flag_value |= 0x01
                if max_ in (99999, 999999):
                    f_flag_value |= 0x02
                space_len = self._calc_space_string(str_disp.value.decode())
                rpm = self._atoll(str_msg.value.decode())
                if f_flag_value == 0x01:  # min_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {int(rpm):5d} rpm\t"
                          f"(min = --N/A-- rpm, max = {int(max_):5d} rpm)", end="")
                    if rpm > max_:
                        print(f" {ALARM}", end="")
                elif f_flag_value == 0x02:  # max_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {int(rpm):5d} rpm\t"
                          f"(min = {int(min_):5d} rpm, max = --N/A-- rpm)", end="")
                    if rpm < min_:
                        print(f" {ALARM}", end="")
                elif f_flag_value == 0x03:  # min_ = N/A and max_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {int(rpm):5d} rpm\t"
                          f"(min = --N/A-- rpm, max = --N/A-- rpm)", end="")
                else:
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {int(rpm):5d} rpm\t"
                          f"(min = {int(min_):5d} rpm, max = {int(max_):5d} rpm)", end="")
                    if rpm < min_ or rpm > max_:
                        print(f" {ALARM}", end="")
                print()

    def _show_voltage_v30(self, sid: int, cp: ConfigParser) -> None:
        """
        For PSP version == '3.0.X'.
        """
        str_msg = create_string_buffer(30)
        str_disp = create_string_buffer(30)
        str_id_name = create_string_buffer(30)
        stu_sensor_info = IPMISensorInfo()
        udw_hi_critical = c_uint32()
        dw_lo_critical = c_int32()
        f_flag_value = 0
        memset(str_msg, 0, 30)
        with PSP() as psp:
            if psp.lib.LMB_HWM_GetSensorReport(sid, str_msg, sizeof(str_msg)) != ERR_NotSupport:
                psp.lib.LMB_HWM_GetSensorDisplay(sid, str_disp, sizeof(str_disp))
                psp.lib.LMB_HWM_GetSensorName(sid, str_id_name, sizeof(str_id_name))
                min_ = self._str_replace(cp.get(str_id_name.value.decode(), "min", fallback="999999"))
                if min_ == 999999:  # hwm.conf not setting, read from SDK.
                    if self._dw_sensor_type.value == HWM_TYPE_IPMI:
                        i_ret = psp.lib.LMB_IPMI_InfoByName(str_disp, byref(stu_sensor_info))
                        if i_ret == ERR_Success:
                            min_ = stu_sensor_info.f_lo_critical
                            max_ = stu_sensor_info.f_hi_critical
                        else:
                            min_ = max_ = 0.0
                    else:  # read from hwm_table.h
                        psp.lib.LMB_HWM_GetSensorCritical(sid, byref(dw_lo_critical), byref(udw_hi_critical))
                        min_ = dw_lo_critical.value / 1000
                        max_ = udw_hi_critical.value / 1000
                else:
                    max_ = self._str_replace(cp.get(str_id_name.value.decode(), "max", fallback="999999"))
                if min_ in (99999, 999999):
                    f_flag_value |= 0x01
                if max_ in (99999, 999999):
                    f_flag_value |= 0x02
                space_len = self._calc_space_string(str_disp.value.decode())
                volt = self._atoll(str_msg.value.decode()) / 1000
                round_up_buffer = int(volt * 1000)
                if f_flag_value == 0x01:  # min_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {round_up_buffer * 0.001:7.3f} V\t"
                          f"(min = --N/A-- V, max = {max_:7.3f} V)", end="")
                    if round_up_buffer > int(max_ * 1000):
                        print(f" {ALARM}", end="")
                elif f_flag_value == 0x02:  # max_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {round_up_buffer * 0.001:7.3f} V\t"
                          f"(min = {min_:7.3f} V, max = --N/A-- V)", end="")
                    if round_up_buffer < int(min_ * 1000):
                        print(f" {ALARM}", end="")
                elif f_flag_value == 0x03:  # min_ = N/A and max_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {round_up_buffer * 0.001:7.3f} V\t"
                          f"(min = --N/A-- V, max = --N/A-- V)", end="")
                else:
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {round_up_buffer * 0.001:7.3f} V\t"
                          f"(min = {min_:7.3f} V, max = {max_:7.3f} V)", end="")
                    if round_up_buffer < int(min_ * 1000) or round_up_buffer > int(max_ * 1000):
                        print(f" {ALARM}", end="")
                print()

    def _show_current_v30(self, sid: int, cp: ConfigParser) -> None:
        """
        For PSP version == '3.0.X'.
        """
        str_msg = create_string_buffer(30)
        str_disp = create_string_buffer(30)
        str_id_name = create_string_buffer(30)
        stu_sensor_info = IPMISensorInfo()
        udw_hi_critical = c_uint32()
        dw_lo_critical = c_int32()
        f_flag_value = 0
        memset(str_msg, 0, 30)
        with PSP() as psp:
            if psp.lib.LMB_HWM_GetSensorReport(sid, str_msg, sizeof(str_msg)) != ERR_NotSupport:
                psp.lib.LMB_HWM_GetSensorDisplay(sid, str_disp, sizeof(str_disp))
                psp.lib.LMB_HWM_GetSensorName(sid, str_id_name, sizeof(str_id_name))
                min_ = self._str_replace(cp.get(str_id_name.value.decode(), "min", fallback="999999"))
                if min_ == 999999:  # hwm.conf not setting, read from SDK.
                    if self._dw_sensor_type.value == HWM_TYPE_IPMI:
                        i_ret = psp.lib.LMB_IPMI_InfoByName(str_disp, byref(stu_sensor_info))
                        if i_ret == ERR_Success:
                            min_ = stu_sensor_info.f_lo_critical
                            max_ = stu_sensor_info.f_hi_critical
                        else:
                            min_ = max_ = 0.0
                    else:  # read from hwm_table.h
                        psp.lib.LMB_HWM_GetSensorCritical(sid, byref(dw_lo_critical), byref(udw_hi_critical))
                        min_ = dw_lo_critical.value / 1000
                        max_ = udw_hi_critical.value / 1000
                else:
                    max_ = self._str_replace(cp.get(str_id_name.value.decode(), "max", fallback="999999"))
                if min_ in (99999, 999999):
                    f_flag_value |= 0x01
                if max_ in (99999, 999999):
                    f_flag_value |= 0x02
                space_len = self._calc_space_string(str_disp.value.decode())
                current = self._atoll(str_msg.value.decode()) / 1000
                round_up_buffer = int(current * 1000)
                if f_flag_value == 0x01:  # min_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {round_up_buffer * 0.001:7.3f} A\t"
                          f"(min = --N/A-- A, max = {max_:7.3f} A)", end="")
                    if round_up_buffer > int(max_ * 1000):
                        print(f" {ALARM}", end="")
                elif f_flag_value == 0x02:  # max_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {round_up_buffer * 0.001:7.3f} A\t"
                          f"(min = {min_:7.3f} A, max = --N/A-- A)", end="")
                    if round_up_buffer < int(min_ * 1000):
                        print(f" {ALARM}", end="")
                elif f_flag_value == 0x03:  # min_ = N/A and max_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {round_up_buffer * 0.001:7.3f} A\t"
                          f"(min = --N/A-- A, max = --N/A-- A)", end="")
                else:
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {round_up_buffer * 0.001:7.3f} A\t"
                          f"(min = {min_:7.3f} A, max = {max_:7.3f} A)", end="")
                    if round_up_buffer < int(min_ * 1000) or round_up_buffer > int(max_ * 1000):
                        print(f" {ALARM}", end="")
                print()

    def _show_watts_v30(self, sid: int, cp: ConfigParser) -> None:
        """
        For PSP version == '3.0.X'.
        """
        str_msg = create_string_buffer(30)
        str_disp = create_string_buffer(30)
        str_id_name = create_string_buffer(30)
        stu_sensor_info = IPMISensorInfo()
        udw_hi_critical = c_uint32()
        dw_lo_critical = c_int32()
        f_flag_value = 0
        memset(str_msg, 0, 30)
        with PSP() as psp:
            if psp.lib.LMB_HWM_GetSensorReport(sid, str_msg, sizeof(str_msg)) != ERR_NotSupport:
                psp.lib.LMB_HWM_GetSensorDisplay(sid, str_disp, sizeof(str_disp))
                psp.lib.LMB_HWM_GetSensorName(sid, str_id_name, sizeof(str_id_name))
                min_ = self._str_replace(cp.get(str_id_name.value.decode(), "min", fallback="999999"))
                if min_ == 999999:  # hwm.conf not setting, read from SDK.
                    if self._dw_sensor_type.value == HWM_TYPE_IPMI:
                        i_ret = psp.lib.LMB_IPMI_InfoByName(str_disp, byref(stu_sensor_info))
                        if i_ret == ERR_Success:
                            min_ = stu_sensor_info.f_lo_critical
                            max_ = stu_sensor_info.f_hi_critical
                        else:
                            min_ = max_ = 0.0
                    else:  # read from hwm_table.h
                        psp.lib.LMB_HWM_GetSensorCritical(sid, byref(dw_lo_critical), byref(udw_hi_critical))
                        min_ = dw_lo_critical.value / 1000
                        max_ = udw_hi_critical.value / 1000
                else:
                    max_ = self._str_replace(cp.get(str_id_name.value.decode(), "max", fallback="999999"))
                if min_ in (99999, 999999):
                    f_flag_value |= 0x01
                if max_ in (99999, 999999):
                    f_flag_value |= 0x02
                space_len = self._calc_space_string(str_disp.value.decode())
                watts = self._atoll(str_msg.value.decode()) / 1000
                round_up_buffer = int(watts * 1000)
                if f_flag_value == 0x01:  # min_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {round_up_buffer * 0.001:7.3f} W\t"
                          f"(min = --N/A-- W, max = {max_:7.3f} W)", end="")
                    if round_up_buffer > int(max_ * 1000):
                        print(f" {ALARM}", end="")
                elif f_flag_value == 0x02:  # max_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {round_up_buffer * 0.001:7.3f} W\t"
                          f"(min = {min_:7.3f} W, max = --N/A-- W)", end="")
                    if round_up_buffer < int(min_ * 1000):
                        print(f" {ALARM}", end="")
                elif f_flag_value == 0x03:  # min_ = N/A and max_ = N/A
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {round_up_buffer * 0.001:7.3f} W\t"
                          f"(min = --N/A-- W, max = --N/A-- W)", end="")
                else:
                    print(f"{str_disp.value.decode()}{' ' * space_len} = {round_up_buffer * 0.001:7.3f} W\t"
                          f"(min = {min_:7.3f} W, max = {max_:7.3f} W)", end="")
                    if round_up_buffer < int(min_ * 1000) or round_up_buffer > int(max_ * 1000):
                        print(f" {ALARM}", end="")
                print()

    @classmethod
    def _str_replace(cls, s: str) -> float:
        """Replace str to float from `hwm.conf`."""
        result = 1.0
        for element in s.split("*"):
            result *= float(element.strip())
        return result

    @classmethod
    def _atoll(cls, s: str) -> int:
        pattern = r"[\s]*[+-]?[\d]+"
        is_matched = match(pattern, s)
        if is_matched:
            result = int(is_matched.group(0))
            if result > 2 ** 31 - 1:
                result = 2 ** 31 - 1
            if result < -2 ** 31:
                result = -2 ** 31
        else:
            result = 0
        return result

    @classmethod
    def _calc_space_string(cls, s: str) -> int:
        max_len = 16
        if len(s) <= max_len:
            return max_len - len(s)
        else:
            return 0
