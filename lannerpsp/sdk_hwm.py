import configparser
import logging
from ctypes import byref, c_float, c_uint16
from typing import Optional

from .lmbinc import PSP

logger = logging.getLogger(__name__)


class HWM:
    """
    Hardware Monitor.

    sdk/src_utils/sdk_hwm/sdk_hwm.c
    """

    _f_temp = c_float()
    _w_data = c_uint16()
    _w_rpm = c_uint16()
    _hwm_conf_path = "/opt/lanner/psp/bin/amd64/utils/hwm.conf"
    _config = configparser.ConfigParser()
    _config.read(_hwm_conf_path)

    @classmethod
    def _str_replace(cls, source: str) -> float:
        result = 1.0
        for element in source.split("*"):
            result *= float(element.strip())
        return result

    @classmethod
    def get_cpu_temp(cls, num: int) -> Optional[int]:
        """Get CPU temperature."""
        with PSP() as psp:
            i_ret = psp.LMB_HWM_GetCpuTemp(num, byref(cls._f_temp))
            if i_ret == PSP.ERR_Success:
                logger.info(f"CPU-{num} temperature = {int(cls._f_temp.value):d}")
                return int(cls._f_temp.value)
            PSP.show_error("LMB_HWM_GetCpuTemp", i_ret)

    @classmethod
    def get_sys_temp(cls, num: int) -> Optional[int]:
        """Get SYS temperature."""
        with PSP() as psp:
            i_ret = psp.LMB_HWM_GetSysTemp(num, byref(cls._f_temp))
            if i_ret == PSP.ERR_Success:
                logger.info(f"SYS-{num} temperature = {int(cls._f_temp.value):d}")
                return int(cls._f_temp.value)
            PSP.show_error("LMB_HWM_GetSysTemp", i_ret)

    @classmethod
    def get_vcore(cls, num: int) -> Optional[float]:
        """Get CPU core voltage."""
        with PSP() as psp:
            i_ret = psp.LMB_HWM_GetVcore(num, byref(cls._f_temp))
            if i_ret == PSP.ERR_Success:
                logger.info(f"CPU-{num} Vcore = {cls._f_temp.value:2.3f}")
                return cls._f_temp.value
            PSP.show_error("LMB_HWM_GetVcore", i_ret)

    @classmethod
    def get_12v(cls) -> Optional[float]:
        """Get 12V voltage."""
        with PSP() as psp:
            i_ret = psp.LMB_HWM_Get12V(byref(cls._f_temp))
            if i_ret == PSP.ERR_Success:
                logger.info(f"12V = {cls._f_temp.value:2.3f}")
                return cls._f_temp.value
            PSP.show_error("LMB_HWM_Get12V", i_ret)

    @classmethod
    def get_5v(cls) -> Optional[float]:
        """Get 5V voltage."""
        with PSP() as psp:
            i_ret = psp.LMB_HWM_Get5V(byref(cls._f_temp))
            if i_ret == PSP.ERR_Success:
                logger.info(f"5V = {cls._f_temp.value:2.3f}")
                return cls._f_temp.value
            PSP.show_error("LMB_HWM_Get5V", i_ret)

    @classmethod
    def get_3v3(cls) -> Optional[float]:
        """Get 3.3V voltage."""
        with PSP() as psp:
            i_ret = psp.LMB_HWM_Get3V3(byref(cls._f_temp))
            if i_ret == PSP.ERR_Success:
                logger.info(f"3.3V = {cls._f_temp.value:2.3f}")
                return cls._f_temp.value
            PSP.show_error("LMB_HWM_Get3V3", i_ret)

    @classmethod
    def get_5vsb(cls) -> Optional[float]:
        """Get 5Vsb voltage."""
        with PSP() as psp:
            i_ret = psp.LMB_HWM_Get5Vsb(byref(cls._f_temp))
            if i_ret == PSP.ERR_Success:
                logger.info(f"5VSB = {cls._f_temp.value:2.3f}")
                return cls._f_temp.value
            PSP.show_error("LMB_HWM_Get5Vsb", i_ret)

    @classmethod
    def get_3v3sb(cls) -> Optional[float]:
        """Get 3.3Vsb voltage."""
        with PSP() as psp:
            i_ret = psp.LMB_HWM_Get3V3sb(byref(cls._f_temp))
            if i_ret == PSP.ERR_Success:
                logger.info(f"3.3VSB = {cls._f_temp.value:2.3f}")
                return cls._f_temp.value
            PSP.show_error("LMB_HWM_Get3V3sb", i_ret)

    @classmethod
    def get_vbat(cls) -> Optional[float]:
        """Get Vbat voltage."""
        with PSP() as psp:
            i_ret = psp.LMB_HWM_GetVbat(byref(cls._f_temp))
            if i_ret == PSP.ERR_Success:
                logger.info(f"Vbat = {cls._f_temp.value:2.3f}")
                return cls._f_temp.value
            PSP.show_error("LMB_HWM_GetVbat", i_ret)

    @classmethod
    def get_power_supply(cls, num: int) -> Optional[int]:
        """Get Power Supply voltage."""
        with PSP() as psp:
            i_ret = psp.LMB_HWM_GetPowerSupply(num, byref(cls._w_data))
            if i_ret == PSP.ERR_Success:
                logger.info(f"PowerSupply {num} AC voltage = {cls._f_temp.value:d}")
                return cls._w_data.value
            PSP.show_error("LMB_HWM_GetPowerSupply", i_ret)

    @classmethod
    def testhwm(cls) -> None:
        """For hardware monitor testing."""
        with PSP() as psp:
            if psp.LMB_HWM_GetCpuTemp(1, byref(cls._f_temp)) != PSP.ERR_NotSupport:
                min_ = cls._str_replace(cls._config["HWM_CPU1_Temp"]["min"])
                max_ = cls._str_replace(cls._config["HWM_CPU1_Temp"]["max"])
                logger.info(f"CPU-1 temperature = {int(cls._f_temp.value):3d} C\t"
                            f"(min = {min_:3.0f} C, max = {max_:3.0f} C)")
            if psp.LMB_HWM_GetCpuTemp(2, byref(cls._f_temp)) != PSP.ERR_NotSupport:
                min_ = cls._str_replace(cls._config["HWM_CPU2_Temp"]["min"])
                max_ = cls._str_replace(cls._config["HWM_CPU2_Temp"]["max"])
                logger.info(f"CPU-2 temperature = {int(cls._f_temp.value):3d} C\t"
                            f"(min = {min_:3.0f} C, max = {max_:3.0f} C)")
            if psp.LMB_HWM_GetSysTemp(1, byref(cls._f_temp)) != PSP.ERR_NotSupport:
                min_ = cls._str_replace(cls._config["HWM_SYS1_Temp"]["min"])
                max_ = cls._str_replace(cls._config["HWM_SYS1_Temp"]["max"])
                logger.info(f"SYS-1 temperature = {int(cls._f_temp.value):3d} C\t"
                            f"(min = {min_:3.0f} C, max = {max_:3.0f} C)")
            if psp.LMB_HWM_GetSysTemp(2, byref(cls._f_temp)) != PSP.ERR_NotSupport:
                min_ = cls._str_replace(cls._config["HWM_SYS2_Temp"]["min"])
                max_ = cls._str_replace(cls._config["HWM_SYS2_Temp"]["max"])
                logger.info(f"SYS-2 temperature = {int(cls._f_temp.value):3d} C\t"
                            f"(min = {min_:3.0f} C, max = {max_:3.0f} C)")

            if psp.LMB_HWM_GetVcore(1, byref(cls._f_temp)) != PSP.ERR_NotSupport:
                min_ = cls._str_replace(cls._config["HWM_Core1_volt"]["min"])
                max_ = cls._str_replace(cls._config["HWM_Core1_volt"]["max"])
                logger.info(f"CPU-1 Vcore = {cls._f_temp.value:7.3f} V\t\t"
                            f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.LMB_HWM_GetVcore(2, byref(cls._f_temp)) != PSP.ERR_NotSupport:
                min_ = cls._str_replace(cls._config["HWM_Core2_volt"]["min"])
                max_ = cls._str_replace(cls._config["HWM_Core2_volt"]["max"])
                logger.info(f"CPU-2 Vcore = {cls._f_temp.value:7.3f} V\t\t"
                            f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.LMB_HWM_Get12V(byref(cls._f_temp)) != PSP.ERR_NotSupport:
                min_ = cls._str_replace(cls._config["HWM_12v_volt"]["min"])
                max_ = cls._str_replace(cls._config["HWM_12v_volt"]["max"])
                logger.info(f"12V = {cls._f_temp.value:7.3f} V\t\t\t"
                            f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.LMB_HWM_Get5V(byref(cls._f_temp)) != PSP.ERR_NotSupport:
                min_ = cls._str_replace(cls._config["HWM_5v_volt"]["min"])
                max_ = cls._str_replace(cls._config["HWM_5v_volt"]["max"])
                logger.info(f"5V = {cls._f_temp.value:7.3f} V\t\t\t"
                            f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.LMB_HWM_Get3V3(byref(cls._f_temp)) != PSP.ERR_NotSupport:
                min_ = cls._str_replace(cls._config["HWM_3v3_volt"]["min"])
                max_ = cls._str_replace(cls._config["HWM_3v3_volt"]["max"])
                logger.info(f"3.3V = {cls._f_temp.value:7.3f} V\t\t"
                            f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.LMB_HWM_Get5Vsb(byref(cls._f_temp)) != PSP.ERR_NotSupport:
                min_ = cls._str_replace(cls._config["HWM_5vsb_volt"]["min"])
                max_ = cls._str_replace(cls._config["HWM_5vsb_volt"]["max"])
                logger.info(f"5VSB = {cls._f_temp.value:7.3f} V\t\t"
                            f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.LMB_HWM_Get3V3sb(byref(cls._f_temp)) != PSP.ERR_NotSupport:
                min_ = cls._str_replace(cls._config["HWM_3v3sb_volt"]["min"])
                max_ = cls._str_replace(cls._config["HWM_3v3sb_volt"]["max"])
                logger.info(f"3.3VSB = {cls._f_temp.value:7.3f} V\t\t"
                            f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.LMB_HWM_GetVbat(byref(cls._f_temp)) != PSP.ERR_NotSupport:
                min_ = cls._str_replace(cls._config["HWM_vBat_volt"]["min"])
                max_ = cls._str_replace(cls._config["HWM_vBat_volt"]["max"])
                logger.info(f"Vbat = {cls._f_temp.value:7.3f} V\t\t"
                            f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.LMB_HWM_GetVDDR(1, byref(cls._f_temp)) != PSP.ERR_NotSupport:
                min_ = cls._str_replace(cls._config["HWM_vddr_volt"]["min"])
                max_ = cls._str_replace(cls._config["HWM_vddr_volt"]["max"])
                logger.info(f"VDDR = {cls._f_temp.value:7.3f} V\t\t"
                            f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.LMB_HWM_GetPowerSupply(1, byref(cls._w_data)) != PSP.ERR_NotSupport:
                min_ = cls._str_replace(cls._config["HWM_PSU1_volt"]["min"])
                max_ = cls._str_replace(cls._config["HWM_PSU1_volt"]["max"])
                logger.info(f"PowerSupply 1 AC voltage = {cls._w_data.value:3d} V\t"
                            f"(min = {min_:3.0f} V, max = {max_:3.0f} V)")
            if psp.LMB_HWM_GetPowerSupply(2, byref(cls._w_data)) != PSP.ERR_NotSupport:
                min_ = cls._str_replace(cls._config["HWM_PSU2_volt"]["min"])
                max_ = cls._str_replace(cls._config["HWM_PSU2_volt"]["max"])
                logger.info(f"PowerSupply 2 AC voltage = {cls._w_data.value:3d} V\t"
                            f"(min = {min_:3.0f} V, max = {max_:3.0f} V)")
            if psp.LMB_HWM_GetCpuFan(1, byref(cls._w_rpm)) != PSP.ERR_NotSupport:
                min_ = cls._str_replace(cls._config["HWM_CPU1_RPM"]["min"])
                max_ = cls._str_replace(cls._config["HWM_CPU1_RPM"]["max"])
                logger.info(f"CPU FAN 1 speed = {cls._w_rpm.value:5d} rpm\t"
                            f"(min = {min_:5.0f} rpm, max = {max_:5.0f} rpm)")
            if psp.LMB_HWM_GetCpuFan(2, byref(cls._w_rpm)) != PSP.ERR_NotSupport:
                min_ = cls._str_replace(cls._config["HWM_CPU2_RPM"]["min"])
                max_ = cls._str_replace(cls._config["HWM_CPU2_RPM"]["max"])
                logger.info(f"CPU FAN 2 speed = {cls._w_rpm.value:5d} rpm\t"
                            f"(min = {min_:5.0f} rpm, max = {max_:5.0f} rpm)")
            if psp.LMB_HWM_GetSysFan(1, byref(cls._w_rpm)) != PSP.ERR_NotSupport:
                min_ = cls._str_replace(cls._config["HWM_SYS1_RPM"]["min"])
                max_ = cls._str_replace(cls._config["HWM_SYS1_RPM"]["max"])
                logger.info(f"SYS FAN 1 speed = {cls._w_rpm.value:5d} rpm\t"
                            f"(min = {min_:5.0f} rpm, max = {max_:5.0f} rpm)")
            if psp.LMB_HWM_GetSysFan(2, byref(cls._w_rpm)) != PSP.ERR_NotSupport:
                min_ = cls._str_replace(cls._config["HWM_SYS2_RPM"]["min"])
                max_ = cls._str_replace(cls._config["HWM_SYS2_RPM"]["max"])
                logger.info(f"SYS FAN 2 speed = {cls._w_rpm.value:5d} rpm\t"
                            f"(min = {min_:5.0f} rpm, max = {max_:5.0f} rpm)")
