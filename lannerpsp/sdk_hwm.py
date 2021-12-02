import logging
from configparser import ConfigParser
from ctypes import byref, c_float, c_uint16
from typing import List

from .lmbinc import PSP

logger = logging.getLogger(__name__)


class HardwareMonitor:
    """
    Hardware Monitor.

    sdk/src_utils/sdk_hwm/sdk_hwm.c

    :param lmb_io_path: path of liblmbio.so
    :param lmb_api_path: path of liblmbapi.so
    """

    def __init__(self,
                 lmb_io_path: str = "/opt/lanner/psp/bin/amd64/lib/liblmbio.so",
                 lmb_api_path: str = "/opt/lanner/psp/bin/amd64/lib/liblmbapi.so") -> None:
        self._lmb_io_path = lmb_io_path
        self._lmb_api_path = lmb_api_path
        self._f_temp = c_float()
        self._w_data = c_uint16()
        self._w_rpm = c_uint16()

    @classmethod
    def _str_replace(cls, source: str) -> float:
        """Replace str to float from hwm.conf"""
        result = 1.0
        for element in source.split("*"):
            result *= float(element.strip())
        return result

    def get_cpu_temp(self, num: int) -> int:
        """Get CPU temperature."""
        # Check type.
        if not isinstance(num, int):
            raise TypeError("'num' type must be int")
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_HWM_GetCpuTemp(num, byref(self._f_temp))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_HWM_GetCpuTemp", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.debug(f"CPU-{num} temperature = {int(self._f_temp.value):d}")
            return int(self._f_temp.value)

    def get_sys_temp(self, num: int) -> int:
        """Get SYS temperature."""
        # Check type.
        if not isinstance(num, int):
            raise TypeError("'num' type must be int")
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_HWM_GetSysTemp(num, byref(self._f_temp))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_HWM_GetSysTemp", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.debug(f"SYS-{num} temperature = {int(self._f_temp.value):d}")
            return int(self._f_temp.value)

    def get_vcore(self, num: int) -> float:
        """Get CPU core voltage."""
        # Check type.
        if not isinstance(num, int):
            raise TypeError("'num' type must be int")
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_HWM_GetVcore(num, byref(self._f_temp))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_HWM_GetVcore", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.debug(f"CPU-{num} Vcore = {self._f_temp.value:2.3f}")
            return self._f_temp.value

    def get_12v(self) -> float:
        """Get 12V voltage."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_HWM_Get12V(byref(self._f_temp))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_HWM_Get12V", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.debug(f"12V = {self._f_temp.value:2.3f}")
            return self._f_temp.value

    def get_5v(self) -> float:
        """Get 5V voltage."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_HWM_Get5V(byref(self._f_temp))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_HWM_Get5V", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.debug(f"5V = {self._f_temp.value:2.3f}")
            return self._f_temp.value

    def get_3v3(self) -> float:
        """Get 3.3V voltage."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_HWM_Get3V3(byref(self._f_temp))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_HWM_Get3V3", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.debug(f"3.3V = {self._f_temp.value:2.3f}")
            return self._f_temp.value

    def get_5vsb(self) -> float:
        """Get 5Vsb voltage."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_HWM_Get5Vsb(byref(self._f_temp))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_HWM_Get5Vsb", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.debug(f"5VSB = {self._f_temp.value:2.3f}")
            return self._f_temp.value

    def get_3v3sb(self) -> float:
        """Get 3.3Vsb voltage."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_HWM_Get3V3sb(byref(self._f_temp))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_HWM_Get3V3sb", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.debug(f"3.3VSB = {self._f_temp.value:2.3f}")
            return self._f_temp.value

    def get_vbat(self) -> float:
        """Get Vbat voltage."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_HWM_GetVbat(byref(self._f_temp))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_HWM_GetVbat", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.debug(f"Vbat = {self._f_temp.value:2.3f}")
            return self._f_temp.value

    def get_power_supply(self, num: int) -> int:
        """Get Power Supply voltage."""
        # Check type.
        if not isinstance(num, int):
            raise TypeError("'num' type must be int")
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_HWM_GetPowerSupply(num, byref(self._w_data))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_HWM_GetPowerSupply", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.debug(f"PowerSupply {num} AC voltage = {self._f_temp.value:d}")
            return self._w_data.value

    def testhwm(self, conf_path: str = "/opt/lanner/psp/bin/amd64/utils/hwm.conf") -> None:
        """For hardware monitor testing."""
        cp = ConfigParser()
        cp.read(conf_path)
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            # Temperature.
            if psp.lib.LMB_HWM_GetCpuTemp(1, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_CPU1_Temp"]["min"])
                max_ = self._str_replace(cp["HWM_CPU1_Temp"]["max"])
                print(f"CPU-1 temperature = {int(self._f_temp.value):3d} C\t"
                      f"(min = {min_:3.0f} C, max = {max_:3.0f} C)")
            if psp.lib.LMB_HWM_GetCpuTemp(2, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_CPU2_Temp"]["min"])
                max_ = self._str_replace(cp["HWM_CPU2_Temp"]["max"])
                print(f"CPU-2 temperature = {int(self._f_temp.value):3d} C\t"
                      f"(min = {min_:3.0f} C, max = {max_:3.0f} C)")
            if psp.lib.LMB_HWM_GetSysTemp(1, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_SYS1_Temp"]["min"])
                max_ = self._str_replace(cp["HWM_SYS1_Temp"]["max"])
                print(f"SYS-1 temperature = {int(self._f_temp.value):3d} C\t"
                      f"(min = {min_:3.0f} C, max = {max_:3.0f} C)")
            if psp.lib.LMB_HWM_GetSysTemp(2, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_SYS2_Temp"]["min"])
                max_ = self._str_replace(cp["HWM_SYS2_Temp"]["max"])
                print(f"SYS-2 temperature = {int(self._f_temp.value):3d} C\t"
                      f"(min = {min_:3.0f} C, max = {max_:3.0f} C)")
            # Voltage.
            if psp.lib.LMB_HWM_GetVcore(1, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_Core1_volt"]["min"])
                max_ = self._str_replace(cp["HWM_Core1_volt"]["max"])
                print(f"CPU-1 Vcore = {self._f_temp.value:7.3f} V\t\t"
                      f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.lib.LMB_HWM_GetVcore(2, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_Core2_volt"]["min"])
                max_ = self._str_replace(cp["HWM_Core2_volt"]["max"])
                print(f"CPU-2 Vcore = {self._f_temp.value:7.3f} V\t\t"
                      f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.lib.LMB_HWM_Get12V(byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_12v_volt"]["min"])
                max_ = self._str_replace(cp["HWM_12v_volt"]["max"])
                print(f"12V = {self._f_temp.value:7.3f} V\t\t\t"
                      f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.lib.LMB_HWM_Get5V(byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_5v_volt"]["min"])
                max_ = self._str_replace(cp["HWM_5v_volt"]["max"])
                print(f"5V = {self._f_temp.value:7.3f} V\t\t\t"
                      f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.lib.LMB_HWM_Get3V3(byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_3v3_volt"]["min"])
                max_ = self._str_replace(cp["HWM_3v3_volt"]["max"])
                print(f"3.3V = {self._f_temp.value:7.3f} V\t\t"
                      f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.lib.LMB_HWM_Get5Vsb(byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_5vsb_volt"]["min"])
                max_ = self._str_replace(cp["HWM_5vsb_volt"]["max"])
                print(f"5VSB = {self._f_temp.value:7.3f} V\t\t"
                      f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.lib.LMB_HWM_Get3V3sb(byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_3v3sb_volt"]["min"])
                max_ = self._str_replace(cp["HWM_3v3sb_volt"]["max"])
                print(f"3.3VSB = {self._f_temp.value:7.3f} V\t\t"
                      f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.lib.LMB_HWM_GetVbat(byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_vBat_volt"]["min"])
                max_ = self._str_replace(cp["HWM_vBat_volt"]["max"])
                print(f"Vbat = {self._f_temp.value:7.3f} V\t\t"
                      f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.lib.LMB_HWM_GetVDDR(1, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_vddr_volt"]["min"])
                max_ = self._str_replace(cp["HWM_vddr_volt"]["max"])
                print(f"VDDR = {self._f_temp.value:7.3f} V\t\t"
                      f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.lib.LMB_HWM_GetPowerSupply(1, byref(self._w_data)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_PSU1_volt"]["min"])
                max_ = self._str_replace(cp["HWM_PSU1_volt"]["max"])
                print(f"PowerSupply 1 AC voltage = {self._w_data.value:3d} V\t"
                      f"(min = {min_:3.0f} V, max = {max_:3.0f} V)")
            if psp.lib.LMB_HWM_GetPowerSupply(2, byref(self._w_data)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_PSU2_volt"]["min"])
                max_ = self._str_replace(cp["HWM_PSU2_volt"]["max"])
                print(f"PowerSupply 2 AC voltage = {self._w_data.value:3d} V\t"
                      f"(min = {min_:3.0f} V, max = {max_:3.0f} V)")
            # Fan RPM.
            if psp.lib.LMB_HWM_GetCpuFan(1, byref(self._w_rpm)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_CPU1_RPM"]["min"])
                max_ = self._str_replace(cp["HWM_CPU1_RPM"]["max"])
                print(f"CPU FAN 1 speed = {self._w_rpm.value:5d} rpm\t"
                      f"(min = {min_:5.0f} rpm, max = {max_:5.0f} rpm)")
            if psp.lib.LMB_HWM_GetCpuFan(2, byref(self._w_rpm)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_CPU2_RPM"]["min"])
                max_ = self._str_replace(cp["HWM_CPU2_RPM"]["max"])
                print(f"CPU FAN 2 speed = {self._w_rpm.value:5d} rpm\t"
                      f"(min = {min_:5.0f} rpm, max = {max_:5.0f} rpm)")
            if psp.lib.LMB_HWM_GetSysFan(1, byref(self._w_rpm)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_SYS1_RPM"]["min"])
                max_ = self._str_replace(cp["HWM_SYS1_RPM"]["max"])
                print(f"SYS FAN 1 speed = {self._w_rpm.value:5d} rpm\t"
                      f"(min = {min_:5.0f} rpm, max = {max_:5.0f} rpm)")
            if psp.lib.LMB_HWM_GetSysFan(2, byref(self._w_rpm)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_SYS2_RPM"]["min"])
                max_ = self._str_replace(cp["HWM_SYS2_RPM"]["max"])
                print(f"SYS FAN 2 speed = {self._w_rpm.value:5d} rpm\t"
                      f"(min = {min_:5.0f} rpm, max = {max_:5.0f} rpm)")

    def get_all(self, conf_path: str = "/opt/lanner/psp/bin/amd64/utils/hwm.conf") -> List[dict]:
        """Get all exist value to list."""
        cp = ConfigParser()
        cp.read(conf_path)
        data = []
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            # Temperature.
            if psp.lib.LMB_HWM_GetCpuTemp(1, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_CPU1_Temp"]["min"])
                max_ = self._str_replace(cp["HWM_CPU1_Temp"]["max"])
                data.append({
                    "name": "CPU-1 temperature",
                    "current": int(self._f_temp.value),
                    "min": int(f"{min_:3.0f}"),
                    "max": int(f"{max_:3.0f}"),
                })
            if psp.lib.LMB_HWM_GetCpuTemp(2, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_CPU2_Temp"]["min"])
                max_ = self._str_replace(cp["HWM_CPU2_Temp"]["max"])
                data.append({
                    "name": "CPU-2 temperature",
                    "current": int(self._f_temp.value),
                    "min": int(f"{min_:3.0f}"),
                    "max": int(f"{max_:3.0f}"),
                })
            if psp.lib.LMB_HWM_GetSysTemp(1, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_SYS1_Temp"]["min"])
                max_ = self._str_replace(cp["HWM_SYS1_Temp"]["max"])
                data.append({
                    "name": "SYS-1 temperature",
                    "current": int(self._f_temp.value),
                    "min": int(f"{min_:3.0f}"),
                    "max": int(f"{max_:3.0f}"),
                })
            if psp.lib.LMB_HWM_GetSysTemp(2, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_SYS2_Temp"]["min"])
                max_ = self._str_replace(cp["HWM_SYS2_Temp"]["max"])
                data.append({
                    "name": "SYS-2 temperature",
                    "current": int(self._f_temp.value),
                    "min": int(f"{min_:3.0f}"),
                    "max": int(f"{max_:3.0f}"),
                })
            # Voltage.
            if psp.lib.LMB_HWM_GetVcore(1, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_Core1_volt"]["min"])
                max_ = self._str_replace(cp["HWM_Core1_volt"]["max"])
                data.append({
                    "name": "CPU-1 Vcore",
                    "current": float(f"{self._f_temp.value:7.3f}"),
                    "min": float(f"{min_:7.3f}"),
                    "max": float(f"{max_:7.3f}"),
                })
            if psp.lib.LMB_HWM_GetVcore(2, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_Core2_volt"]["min"])
                max_ = self._str_replace(cp["HWM_Core2_volt"]["max"])
                data.append({
                    "name": "CPU-2 Vcore",
                    "current": float(f"{self._f_temp.value:7.3f}"),
                    "min": float(f"{min_:7.3f}"),
                    "max": float(f"{max_:7.3f}"),
                })
            if psp.lib.LMB_HWM_Get12V(byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_12v_volt"]["min"])
                max_ = self._str_replace(cp["HWM_12v_volt"]["max"])
                data.append({
                    "name": "12V",
                    "current": float(f"{self._f_temp.value:7.3f}"),
                    "min": float(f"{min_:7.3f}"),
                    "max": float(f"{max_:7.3f}"),
                })
            if psp.lib.LMB_HWM_Get5V(byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_5v_volt"]["min"])
                max_ = self._str_replace(cp["HWM_5v_volt"]["max"])
                data.append({
                    "name": "5V",
                    "current": float(f"{self._f_temp.value:7.3f}"),
                    "min": float(f"{min_:7.3f}"),
                    "max": float(f"{max_:7.3f}"),
                })
            if psp.lib.LMB_HWM_Get3V3(byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_3v3_volt"]["min"])
                max_ = self._str_replace(cp["HWM_3v3_volt"]["max"])
                data.append({
                    "name": "3.3V",
                    "current": float(f"{self._f_temp.value:7.3f}"),
                    "min": float(f"{min_:7.3f}"),
                    "max": float(f"{max_:7.3f}"),
                })
            if psp.lib.LMB_HWM_Get5Vsb(byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_5vsb_volt"]["min"])
                max_ = self._str_replace(cp["HWM_5vsb_volt"]["max"])
                data.append({
                    "name": "5VSB",
                    "current": float(f"{self._f_temp.value:7.3f}"),
                    "min": float(f"{min_:7.3f}"),
                    "max": float(f"{max_:7.3f}"),
                })
            if psp.lib.LMB_HWM_Get3V3sb(byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_3v3sb_volt"]["min"])
                max_ = self._str_replace(cp["HWM_3v3sb_volt"]["max"])
                data.append({
                    "name": "3.3VSB",
                    "current": float(f"{self._f_temp.value:7.3f}"),
                    "min": float(f"{min_:7.3f}"),
                    "max": float(f"{max_:7.3f}"),
                })
            if psp.lib.LMB_HWM_GetVbat(byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_vBat_volt"]["min"])
                max_ = self._str_replace(cp["HWM_vBat_volt"]["max"])
                data.append({
                    "name": "Vbat",
                    "current": float(f"{self._f_temp.value:7.3f}"),
                    "min": float(f"{min_:7.3f}"),
                    "max": float(f"{max_:7.3f}"),
                })
            if psp.lib.LMB_HWM_GetVDDR(1, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_vddr_volt"]["min"])
                max_ = self._str_replace(cp["HWM_vddr_volt"]["max"])
                data.append({
                    "name": "VDDR",
                    "current": float(f"{self._f_temp.value:7.3f}"),
                    "min": float(f"{min_:7.3f}"),
                    "max": float(f"{max_:7.3f}"),
                })
            if psp.lib.LMB_HWM_GetPowerSupply(1, byref(self._w_data)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_PSU1_volt"]["min"])
                max_ = self._str_replace(cp["HWM_PSU1_volt"]["max"])
                data.append({
                    "name": "PowerSupply 1 AC voltage",
                    "current": int(self._w_data.value),
                    "min": int(f"{min_:3.0f}"),
                    "max": int(f"{max_:3.0f}"),
                })
            if psp.lib.LMB_HWM_GetPowerSupply(2, byref(self._w_data)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_PSU2_volt"]["min"])
                max_ = self._str_replace(cp["HWM_PSU2_volt"]["max"])
                data.append({
                    "name": "PowerSupply 2 AC voltage",
                    "current": int(self._w_data.value),
                    "min": int(f"{min_:3.0f}"),
                    "max": int(f"{max_:3.0f}"),
                })
            # Fan RPM.
            if psp.lib.LMB_HWM_GetCpuFan(1, byref(self._w_rpm)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_CPU1_RPM"]["min"])
                max_ = self._str_replace(cp["HWM_CPU1_RPM"]["max"])
                data.append({
                    "name": "CPU FAN 1 speed",
                    "current": int(self._w_rpm.value),
                    "min": int(f"{min_:5.0f}"),
                    "max": int(f"{max_:5.0f}"),
                })
            if psp.lib.LMB_HWM_GetCpuFan(2, byref(self._w_rpm)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_CPU2_RPM"]["min"])
                max_ = self._str_replace(cp["HWM_CPU2_RPM"]["max"])
                data.append({
                    "name": "CPU FAN 2 speed",
                    "current": int(self._w_rpm.value),
                    "min": int(f"{min_:5.0f}"),
                    "max": int(f"{max_:5.0f}"),
                })
            if psp.lib.LMB_HWM_GetSysFan(1, byref(self._w_rpm)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_SYS1_RPM"]["min"])
                max_ = self._str_replace(cp["HWM_SYS1_RPM"]["max"])
                data.append({
                    "name": "SYS FAN 1 speed",
                    "current": int(self._w_rpm.value),
                    "min": int(f"{min_:5.0f}"),
                    "max": int(f"{max_:5.0f}"),
                })
            if psp.lib.LMB_HWM_GetSysFan(2, byref(self._w_rpm)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_SYS2_RPM"]["min"])
                max_ = self._str_replace(cp["HWM_SYS2_RPM"]["max"])
                data.append({
                    "name": "SYS FAN 2 speed",
                    "current": int(self._w_rpm.value),
                    "min": int(f"{min_:5.0f}"),
                    "max": int(f"{max_:5.0f}"),
                })
            return data
