import logging
from configparser import ConfigParser
from ctypes import byref, c_float, c_uint16

from .lmbinc import PSP

logger = logging.getLogger(__name__)


class HWM:
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
            i_ret = psp.LMB_HWM_GetCpuTemp(num, byref(self._f_temp))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_HWM_GetCpuTemp", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.info(f"CPU-{num} temperature = {int(self._f_temp.value):d}")
            return int(self._f_temp.value)

    def get_sys_temp(self, num: int) -> int:
        """Get SYS temperature."""
        # Check type.
        if not isinstance(num, int):
            raise TypeError("'num' type must be int")
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_HWM_GetSysTemp(num, byref(self._f_temp))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_HWM_GetSysTemp", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.info(f"SYS-{num} temperature = {int(self._f_temp.value):d}")
            return int(self._f_temp.value)

    def get_vcore(self, num: int) -> float:
        """Get CPU core voltage."""
        # Check type.
        if not isinstance(num, int):
            raise TypeError("'num' type must be int")
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_HWM_GetVcore(num, byref(self._f_temp))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_HWM_GetVcore", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.info(f"CPU-{num} Vcore = {self._f_temp.value:2.3f}")
            return self._f_temp.value

    def get_12v(self) -> float:
        """Get 12V voltage."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_HWM_Get12V(byref(self._f_temp))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_HWM_Get12V", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.info(f"12V = {self._f_temp.value:2.3f}")
            return self._f_temp.value

    def get_5v(self) -> float:
        """Get 5V voltage."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_HWM_Get5V(byref(self._f_temp))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_HWM_Get5V", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.info(f"5V = {self._f_temp.value:2.3f}")
            return self._f_temp.value

    def get_3v3(self) -> float:
        """Get 3.3V voltage."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_HWM_Get3V3(byref(self._f_temp))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_HWM_Get3V3", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.info(f"3.3V = {self._f_temp.value:2.3f}")
            return self._f_temp.value

    def get_5vsb(self) -> float:
        """Get 5Vsb voltage."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_HWM_Get5Vsb(byref(self._f_temp))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_HWM_Get5Vsb", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.info(f"5VSB = {self._f_temp.value:2.3f}")
            return self._f_temp.value

    def get_3v3sb(self) -> float:
        """Get 3.3Vsb voltage."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_HWM_Get3V3sb(byref(self._f_temp))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_HWM_Get3V3sb", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.info(f"3.3VSB = {self._f_temp.value:2.3f}")
            return self._f_temp.value

    def get_vbat(self) -> float:
        """Get Vbat voltage."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_HWM_GetVbat(byref(self._f_temp))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_HWM_GetVbat", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.info(f"Vbat = {self._f_temp.value:2.3f}")
            return self._f_temp.value

    def get_power_supply(self, num: int) -> int:
        """Get Power Supply voltage."""
        # Check type.
        if not isinstance(num, int):
            raise TypeError("'num' type must be int")
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_HWM_GetPowerSupply(num, byref(self._w_data))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_HWM_GetPowerSupply", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.info(f"PowerSupply {num} AC voltage = {self._f_temp.value:d}")
            return self._w_data.value

    def testhwm(self, conf_path: str = "/opt/lanner/psp/bin/amd64/utils/hwm.conf") -> None:
        """For hardware monitor testing."""
        cp = ConfigParser()
        cp.read(conf_path)
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            # Temperature.
            if psp.LMB_HWM_GetCpuTemp(1, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_CPU1_Temp"]["min"])
                max_ = self._str_replace(cp["HWM_CPU1_Temp"]["max"])
                logger.info(f"CPU-1 temperature = {int(self._f_temp.value):3d} C\t"
                            f"(min = {min_:3.0f} C, max = {max_:3.0f} C)")
            if psp.LMB_HWM_GetCpuTemp(2, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_CPU2_Temp"]["min"])
                max_ = self._str_replace(cp["HWM_CPU2_Temp"]["max"])
                logger.info(f"CPU-2 temperature = {int(self._f_temp.value):3d} C\t"
                            f"(min = {min_:3.0f} C, max = {max_:3.0f} C)")
            if psp.LMB_HWM_GetSysTemp(1, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_SYS1_Temp"]["min"])
                max_ = self._str_replace(cp["HWM_SYS1_Temp"]["max"])
                logger.info(f"SYS-1 temperature = {int(self._f_temp.value):3d} C\t"
                            f"(min = {min_:3.0f} C, max = {max_:3.0f} C)")
            if psp.LMB_HWM_GetSysTemp(2, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_SYS2_Temp"]["min"])
                max_ = self._str_replace(cp["HWM_SYS2_Temp"]["max"])
                logger.info(f"SYS-2 temperature = {int(self._f_temp.value):3d} C\t"
                            f"(min = {min_:3.0f} C, max = {max_:3.0f} C)")
            # Voltage.
            if psp.LMB_HWM_GetVcore(1, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_Core1_volt"]["min"])
                max_ = self._str_replace(cp["HWM_Core1_volt"]["max"])
                logger.info(f"CPU-1 Vcore = {self._f_temp.value:7.3f} V\t\t"
                            f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.LMB_HWM_GetVcore(2, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_Core2_volt"]["min"])
                max_ = self._str_replace(cp["HWM_Core2_volt"]["max"])
                logger.info(f"CPU-2 Vcore = {self._f_temp.value:7.3f} V\t\t"
                            f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.LMB_HWM_Get12V(byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_12v_volt"]["min"])
                max_ = self._str_replace(cp["HWM_12v_volt"]["max"])
                logger.info(f"12V = {self._f_temp.value:7.3f} V\t\t\t"
                            f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.LMB_HWM_Get5V(byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_5v_volt"]["min"])
                max_ = self._str_replace(cp["HWM_5v_volt"]["max"])
                logger.info(f"5V = {self._f_temp.value:7.3f} V\t\t\t"
                            f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.LMB_HWM_Get3V3(byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_3v3_volt"]["min"])
                max_ = self._str_replace(cp["HWM_3v3_volt"]["max"])
                logger.info(f"3.3V = {self._f_temp.value:7.3f} V\t\t"
                            f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.LMB_HWM_Get5Vsb(byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_5vsb_volt"]["min"])
                max_ = self._str_replace(cp["HWM_5vsb_volt"]["max"])
                logger.info(f"5VSB = {self._f_temp.value:7.3f} V\t\t"
                            f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.LMB_HWM_Get3V3sb(byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_3v3sb_volt"]["min"])
                max_ = self._str_replace(cp["HWM_3v3sb_volt"]["max"])
                logger.info(f"3.3VSB = {self._f_temp.value:7.3f} V\t\t"
                            f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.LMB_HWM_GetVbat(byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_vBat_volt"]["min"])
                max_ = self._str_replace(cp["HWM_vBat_volt"]["max"])
                logger.info(f"Vbat = {self._f_temp.value:7.3f} V\t\t"
                            f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.LMB_HWM_GetVDDR(1, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_vddr_volt"]["min"])
                max_ = self._str_replace(cp["HWM_vddr_volt"]["max"])
                logger.info(f"VDDR = {self._f_temp.value:7.3f} V\t\t"
                            f"(min = {min_:7.3f} V, max = {max_:7.3f} V)")
            if psp.LMB_HWM_GetPowerSupply(1, byref(self._w_data)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_PSU1_volt"]["min"])
                max_ = self._str_replace(cp["HWM_PSU1_volt"]["max"])
                logger.info(f"PowerSupply 1 AC voltage = {self._w_data.value:3d} V\t"
                            f"(min = {min_:3.0f} V, max = {max_:3.0f} V)")
            if psp.LMB_HWM_GetPowerSupply(2, byref(self._w_data)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_PSU2_volt"]["min"])
                max_ = self._str_replace(cp["HWM_PSU2_volt"]["max"])
                logger.info(f"PowerSupply 2 AC voltage = {self._w_data.value:3d} V\t"
                            f"(min = {min_:3.0f} V, max = {max_:3.0f} V)")
            # Fan RPM.
            if psp.LMB_HWM_GetCpuFan(1, byref(self._w_rpm)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_CPU1_RPM"]["min"])
                max_ = self._str_replace(cp["HWM_CPU1_RPM"]["max"])
                logger.info(f"CPU FAN 1 speed = {self._w_rpm.value:5d} rpm\t"
                            f"(min = {min_:5.0f} rpm, max = {max_:5.0f} rpm)")
            if psp.LMB_HWM_GetCpuFan(2, byref(self._w_rpm)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_CPU2_RPM"]["min"])
                max_ = self._str_replace(cp["HWM_CPU2_RPM"]["max"])
                logger.info(f"CPU FAN 2 speed = {self._w_rpm.value:5d} rpm\t"
                            f"(min = {min_:5.0f} rpm, max = {max_:5.0f} rpm)")
            if psp.LMB_HWM_GetSysFan(1, byref(self._w_rpm)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_SYS1_RPM"]["min"])
                max_ = self._str_replace(cp["HWM_SYS1_RPM"]["max"])
                logger.info(f"SYS FAN 1 speed = {self._w_rpm.value:5d} rpm\t"
                            f"(min = {min_:5.0f} rpm, max = {max_:5.0f} rpm)")
            if psp.LMB_HWM_GetSysFan(2, byref(self._w_rpm)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_SYS2_RPM"]["min"])
                max_ = self._str_replace(cp["HWM_SYS2_RPM"]["max"])
                logger.info(f"SYS FAN 2 speed = {self._w_rpm.value:5d} rpm\t"
                            f"(min = {min_:5.0f} rpm, max = {max_:5.0f} rpm)")

    def get_all(self, conf_path: str = "/opt/lanner/psp/bin/amd64/utils/hwm.conf") -> dict:
        """Get all exist value to dict."""
        cp = ConfigParser()
        cp.read(conf_path)
        data = {}
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            # Temperature.
            if psp.LMB_HWM_GetCpuTemp(1, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_CPU1_Temp"]["min"])
                max_ = self._str_replace(cp["HWM_CPU1_Temp"]["max"])
                data["cpu_temp_1"] = {"min": int(f"{min_:3.0f}"),
                                      "max": int(f"{max_:3.0f}"),
                                      "current": int(self._f_temp.value)}
            if psp.LMB_HWM_GetCpuTemp(2, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_CPU2_Temp"]["min"])
                max_ = self._str_replace(cp["HWM_CPU2_Temp"]["max"])
                data["cpu_temp_2"] = {"min": int(f"{min_:3.0f}"),
                                      "max": int(f"{max_:3.0f}"),
                                      "current": int(self._f_temp.value)}
            if psp.LMB_HWM_GetSysTemp(1, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_SYS1_Temp"]["min"])
                max_ = self._str_replace(cp["HWM_SYS1_Temp"]["max"])
                data["sys_temp_1"] = {"min": int(f"{min_:3.0f}"),
                                      "max": int(f"{max_:3.0f}"),
                                      "current": int(self._f_temp.value)}
            if psp.LMB_HWM_GetSysTemp(2, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_SYS2_Temp"]["min"])
                max_ = self._str_replace(cp["HWM_SYS2_Temp"]["max"])
                data["sys_temp_2"] = {"min": int(f"{min_:3.0f}"),
                                      "max": int(f"{max_:3.0f}"),
                                      "current": int(self._f_temp.value)}
            # Voltage.
            if psp.LMB_HWM_GetVcore(1, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_Core1_volt"]["min"])
                max_ = self._str_replace(cp["HWM_Core1_volt"]["max"])
                data["vcore_1"] = {"min": float(f"{min_:7.3f}"),
                                   "max": float(f"{max_:7.3f}"),
                                   "current": float(f"{self._f_temp.value:7.3f}")}
            if psp.LMB_HWM_GetVcore(2, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_Core2_volt"]["min"])
                max_ = self._str_replace(cp["HWM_Core2_volt"]["max"])
                data["vcore_2"] = {"min": float(f"{min_:7.3f}"),
                                   "max": float(f"{max_:7.3f}"),
                                   "current": float(f"{self._f_temp.value:7.3f}")}
            if psp.LMB_HWM_Get12V(byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_12v_volt"]["min"])
                max_ = self._str_replace(cp["HWM_12v_volt"]["max"])
                data["12v"] = {"min": float(f"{min_:7.3f}"),
                               "max": float(f"{max_:7.3f}"),
                               "current": float(f"{self._f_temp.value:7.3f}")}
            if psp.LMB_HWM_Get5V(byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_5v_volt"]["min"])
                max_ = self._str_replace(cp["HWM_5v_volt"]["max"])
                data["5v"] = {"min": float(f"{min_:7.3f}"),
                              "max": float(f"{max_:7.3f}"),
                              "current": float(f"{self._f_temp.value:7.3f}")}
            if psp.LMB_HWM_Get3V3(byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_3v3_volt"]["min"])
                max_ = self._str_replace(cp["HWM_3v3_volt"]["max"])
                data["3v3"] = {"min": float(f"{min_:7.3f}"),
                               "max": float(f"{max_:7.3f}"),
                               "current": float(f"{self._f_temp.value:7.3f}")}
            if psp.LMB_HWM_Get5Vsb(byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_5vsb_volt"]["min"])
                max_ = self._str_replace(cp["HWM_5vsb_volt"]["max"])
                data["5vsb"] = {"min": float(f"{min_:7.3f}"),
                                "max": float(f"{max_:7.3f}"),
                                "current": float(f"{self._f_temp.value:7.3f}")}
            if psp.LMB_HWM_Get3V3sb(byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_3v3sb_volt"]["min"])
                max_ = self._str_replace(cp["HWM_3v3sb_volt"]["max"])
                data["3v3sb"] = {"min": float(f"{min_:7.3f}"),
                                 "max": float(f"{max_:7.3f}"),
                                 "current": float(f"{self._f_temp.value:7.3f}")}
            if psp.LMB_HWM_GetVbat(byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_vBat_volt"]["min"])
                max_ = self._str_replace(cp["HWM_vBat_volt"]["max"])
                data["vbat"] = {"min": float(f"{min_:7.3f}"),
                                "max": float(f"{max_:7.3f}"),
                                "current": float(f"{self._f_temp.value:7.3f}")}
            if psp.LMB_HWM_GetVDDR(1, byref(self._f_temp)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_vddr_volt"]["min"])
                max_ = self._str_replace(cp["HWM_vddr_volt"]["max"])
                data["vddr"] = {"min": float(f"{min_:7.3f}"),
                                "max": float(f"{max_:7.3f}"),
                                "current": float(f"{self._f_temp.value:7.3f}")}
            if psp.LMB_HWM_GetPowerSupply(1, byref(self._w_data)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_PSU1_volt"]["min"])
                max_ = self._str_replace(cp["HWM_PSU1_volt"]["max"])
                data["power_supply_1"] = {"min": int(f"{min_:3.0f}"),
                                          "max": int(f"{max_:3.0f}"),
                                          "current": int(self._w_data.value)}
            if psp.LMB_HWM_GetPowerSupply(2, byref(self._w_data)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_PSU2_volt"]["min"])
                max_ = self._str_replace(cp["HWM_PSU2_volt"]["max"])
                data["power_supply_2"] = {"min": int(f"{min_:3.0f}"),
                                          "max": int(f"{max_:3.0f}"),
                                          "current": int(self._w_data.value)}
            # Fan RPM.
            if psp.LMB_HWM_GetCpuFan(1, byref(self._w_rpm)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_CPU1_RPM"]["min"])
                max_ = self._str_replace(cp["HWM_CPU1_RPM"]["max"])
                data["cpu_fan_1"] = {"min": int(f"{min_:5.0f}"),
                                     "max": int(f"{max_:5.0f}"),
                                     "current": int(self._w_rpm.value)}
            if psp.LMB_HWM_GetCpuFan(2, byref(self._w_rpm)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_CPU2_RPM"]["min"])
                max_ = self._str_replace(cp["HWM_CPU2_RPM"]["max"])
                data["cpu_fan_2"] = {"min": int(f"{min_:5.0f}"),
                                     "max": int(f"{max_:5.0f}"),
                                     "current": int(self._w_rpm.value)}
            if psp.LMB_HWM_GetSysFan(1, byref(self._w_rpm)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_SYS1_RPM"]["min"])
                max_ = self._str_replace(cp["HWM_SYS1_RPM"]["max"])
                data["sys_fan_1"] = {"min": int(f"{min_:5.0f}"),
                                     "max": int(f"{max_:5.0f}"),
                                     "current": int(self._w_rpm.value)}
            if psp.LMB_HWM_GetSysFan(2, byref(self._w_rpm)) == PSP.ERR_Success:
                min_ = self._str_replace(cp["HWM_SYS2_RPM"]["min"])
                max_ = self._str_replace(cp["HWM_SYS2_RPM"]["max"])
                data["sys_fan_2"] = {"min": int(f"{min_:5.0f}"),
                                     "max": int(f"{max_:5.0f}"),
                                     "current": int(self._w_rpm.value)}
            return data
