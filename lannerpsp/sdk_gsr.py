import logging
from ctypes import byref
from time import sleep
from typing import Any, Dict, NamedTuple

from .core import PSP, get_psp_exc_msg
from .exc import (
    PSPError,
    PSPNotSupport,
)
from .lmbinc import (
    AxisRawData,
    ERR_NotSupport,
    ERR_Success,
)
from .sdk_dll import DLL

logger = logging.getLogger(__name__)

SUPPORTED_PLATFORMS = ("V3S", "V6S",)
UNSUPPORTED_PLATFORMS = ("LEB-7242", "LEC-7230", "NCA-2510",)


class GSRDataModel(NamedTuple):
    """To store G-Sensor data."""
    g_range: int
    raw_x: int
    raw_y: int
    raw_z: int
    mg_x: float
    mg_y: float
    mg_z: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict."""
        return dict(self._asdict())


class GSROffsetModel(NamedTuple):
    """To store G-Sensor offset data."""
    raw_x: int
    raw_y: int
    raw_z: int

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict."""
        return dict(self._asdict())


class GSR:
    """
    G-Sensor.

    :param bool check_platform:
        Set to :data:`True` to check if the platform supports this feature.
        Defaults to :data:`False` for better compatibility.
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

    def get_data(self) -> GSRDataModel:
        """
        Get the X-Axis, Y-Axis and Z-Axis data.

        Example:

        .. code-block:: pycon

            >>> gsr = GSR()
            >>> gsr_data = gsr.get_data()
            >>> gsr_data.g_range
            2
            >>> gsr_data.raw_x
            -4
            >>> gsr_data.raw_y
            -9
            >>> gsr_data.raw_z
            -214
            >>> gsr_data.mg_x
            -0.03137254901960784
            >>> gsr_data.mg_y
            -0.07058823529411765
            >>> gsr_data.mg_z
            -1.6784313725490196
            >>> gsr_data.to_dict()
            {'g_range': 2, 'raw_x': -3, 'raw_y': -9, 'raw_z': -218, 'mg_x': -0.023529411764705882, 'mg_y': -0.07058823529411765, 'mg_z': -1.7098039215686274}

        :return: X/Y/Z Axis data and range with ±g
        :rtype: GSRDataModel
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPError: General PSP functional error.
        """
        stu_raw_data = AxisRawData()
        with PSP() as psp:
            i_ret = psp.lib.LMB_GSR_GetAxisData(byref(stu_raw_data))
        msg = get_psp_exc_msg("LMB_GSR_GetAxisData", i_ret)
        if i_ret == ERR_Success:
            pass
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

        if stu_raw_data.w_g_range == 2:
            f_mg_step = 2 / 255
        elif stu_raw_data.w_g_range == 4:
            f_mg_step = 4 / 255
        elif stu_raw_data.w_g_range == 8:
            f_mg_step = 8 / 255
        elif stu_raw_data.w_g_range == 16:
            f_mg_step = 16 / 255
        else:
            raise PSPError(f"'w_g_range' = {stu_raw_data.w_g_range}")

        f_x_mg = stu_raw_data.w_x_axis * f_mg_step
        f_y_mg = stu_raw_data.w_y_axis * f_mg_step
        f_z_mg = stu_raw_data.w_z_axis * f_mg_step

        return GSRDataModel(g_range=stu_raw_data.w_g_range,
                            raw_x=stu_raw_data.w_x_axis,
                            raw_y=stu_raw_data.w_y_axis,
                            raw_z=stu_raw_data.w_z_axis,
                            mg_x=f_x_mg,
                            mg_y=f_y_mg,
                            mg_z=f_z_mg)

    def get_offset(self) -> GSROffsetModel:
        """
        Get the X-Axis, Y-Axis and Z-Axis offset data.

        Example:

        .. code-block:: pycon

            >>> gsr = GSR()
            >>> gsr_offset = gsr.get_offset()
            >>> gsr_offset.raw_x
            0
            >>> gsr_offset.raw_y
            0
            >>> gsr_offset.raw_z
            0
            >>> gsr_offset.to_dict()
            {'raw_x': 0, 'raw_y': 0, 'raw_z': 0}

        :return: X/Y/Z Axis offset data
        :rtype: GSROffsetModel
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPError: General PSP functional error.
        """
        stu_raw_data = AxisRawData()
        with PSP() as psp:
            i_ret = psp.lib.LMB_GSR_GetAxisOffset(byref(stu_raw_data))
        msg = get_psp_exc_msg("LMB_GSR_GetAxisOffset", i_ret)
        if i_ret == ERR_Success:
            return GSROffsetModel(
                raw_x=stu_raw_data.w_x_axis,
                raw_y=stu_raw_data.w_y_axis,
                raw_z=stu_raw_data.w_z_axis,
            )
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def test(self) -> None:
        """
        For testing.

        Example:

        .. code-block:: pycon

            >>> gsr = GSR()
            >>> gsr.test()
            ---------> 0
            stuRawData.wRange= ±2g
            Raw=-5  , X-Axis= -0.03921569
            Raw=-9  , Y-Axis= -0.07058824
            Raw=-216        , Z-Axis= -1.69411765
            Offset X-Axis=0
            Offset Y-Axis=0
            Offset Z-Axis=0
            ---------> 1
            stuRawData.wRange= ±2g
            Raw=-5  , X-Axis= -0.03921569
            Raw=-8  , Y-Axis= -0.06274510
            Raw=-215        , Z-Axis= -1.68627451
            Offset X-Axis=0
            Offset Y-Axis=0
            Offset Z-Axis=0
            ---------> 2
            stuRawData.wRange= ±2g
            Raw=-4  , X-Axis= -0.03137255
            Raw=-10 , Y-Axis= -0.07843137
            Raw=-216        , Z-Axis= -1.69411765
            Offset X-Axis=0
            Offset Y-Axis=0
            Offset Z-Axis=0
            .
            .
            .
            ---------> 99
            stuRawData.wRange= ±2g
            Raw=-7  , X-Axis= -0.05490196
            Raw=-9  , Y-Axis= -0.07058824
            Raw=-218        , Z-Axis= -1.70980392
            Offset X-Axis=0
            Offset Y-Axis=0
            Offset Z-Axis=0
        """
        stu_raw_data = AxisRawData()
        with PSP() as psp:
            for i in range(100):
                print(f"---------> {i:d}")

                # Get accel data.
                i_ret = psp.lib.LMB_GSR_GetAxisData(byref(stu_raw_data))
                if i_ret != ERR_Success:
                    msg = get_psp_exc_msg("LMB_GSR_GetAxisData", i_ret)
                    print(f"\033[1;31m{msg}\033[0m")
                else:
                    print(f"stuRawData.wRange= ±{stu_raw_data.w_g_range:d}g")

                    if stu_raw_data.w_g_range == 2:
                        f_mg_step = 2 / 255
                    elif stu_raw_data.w_g_range == 4:
                        f_mg_step = 4 / 255
                    elif stu_raw_data.w_g_range == 8:
                        f_mg_step = 8 / 255
                    elif stu_raw_data.w_g_range == 16:
                        f_mg_step = 16 / 255

                    f_x_mg = stu_raw_data.w_x_axis * f_mg_step
                    f_y_mg = stu_raw_data.w_y_axis * f_mg_step
                    f_z_mg = stu_raw_data.w_z_axis * f_mg_step

                    print(f"Raw={stu_raw_data.w_x_axis:d}\t, X-Axis= {f_x_mg:03.8f}")
                    print(f"Raw={stu_raw_data.w_y_axis:d}\t, Y-Axis= {f_y_mg:03.8f}")
                    print(f"Raw={stu_raw_data.w_z_axis:d}\t, Z-Axis= {f_z_mg:03.8f}")

                # Get offset.
                i_ret = psp.lib.LMB_GSR_GetAxisOffset(byref(stu_raw_data))
                if i_ret != ERR_Success:
                    msg = get_psp_exc_msg("LMB_GSR_GetAxisOffset", i_ret)
                    print(f"\033[1;31m{msg}\033[0m")
                else:
                    print(f"Offset X-Axis={stu_raw_data.w_x_axis:d}")
                    print(f"Offset Y-Axis={stu_raw_data.w_y_axis:d}")
                    print(f"Offset Z-Axis={stu_raw_data.w_z_axis:d}")

                sleep(0.5)
