import logging
from ctypes import byref, c_int16, Structure
from time import sleep

from .lmbinc import PSP

logger = logging.getLogger(__name__)


class AxisRawData(Structure):
    """G-Sensor X,Y,Z Axis (define in: sdk/include/lmbinc.h)."""
    _fields_ = [
        ("w_x_axis", c_int16),
        ("w_y_axis", c_int16),
        ("w_z_axis", c_int16),
        ("w_g_range", c_int16),
    ]


class AccelValues:
    """To store accelerate values."""

    def __init__(self, g_range: int, raw_x: int, raw_y: int, raw_z: int,
                 mg_x: float, mg_y: float, mg_z: float) -> None:
        self._g_range = g_range
        self._raw_x = raw_x
        self._raw_y = raw_y
        self._raw_z = raw_z
        self._mg_x = mg_x
        self._mg_y = mg_y
        self._mg_z = mg_z

    @property
    def g_range(self) -> int:
        return self._g_range

    @property
    def raw_x(self) -> int:
        return self._raw_x

    @property
    def raw_y(self) -> int:
        return self._raw_y

    @property
    def raw_z(self) -> int:
        return self._raw_z

    @property
    def mg_x(self) -> float:
        return self._mg_x

    @property
    def mg_y(self) -> float:
        return self._mg_y

    @property
    def mg_z(self) -> float:
        return self._mg_z


class OffsetValues:
    """To store offset values."""

    def __init__(self, raw_x: int, raw_y: int, raw_z: int) -> None:
        self._raw_x = raw_x
        self._raw_y = raw_y
        self._raw_z = raw_z

    @property
    def raw_x(self) -> int:
        return self._raw_x

    @property
    def raw_y(self) -> int:
        return self._raw_y

    @property
    def raw_z(self) -> int:
        return self._raw_z


class GSensor:
    """
    G-Sensor.

    sdk/src_utils/sdk_gsr/sdk_gsr.c

    :param lmb_io_path: path of liblmbio.so
    :param lmb_api_path: path of liblmbapi.so
    """

    def __init__(self,
                 lmb_io_path: str = "/opt/lanner/psp/bin/amd64/lib/liblmbio.so",
                 lmb_api_path: str = "/opt/lanner/psp/bin/amd64/lib/liblmbapi.so") -> None:
        self._lmb_io_path = lmb_io_path
        self._lmb_api_path = lmb_api_path
        self._stu_raw_data = AxisRawData()

    def get_accel(self) -> AccelValues:
        """Get X/Y/Z direction accelerate value."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_GSR_GetAxisData(byref(self._stu_raw_data))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_GSR_GetAxisData", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)

            if self._stu_raw_data.w_g_range == 2:
                f_mg_step = 2 / 255
            elif self._stu_raw_data.w_g_range == 4:
                f_mg_step = 4 / 255
            elif self._stu_raw_data.w_g_range == 8:
                f_mg_step = 8 / 255
            elif self._stu_raw_data.w_g_range == 16:
                f_mg_step = 16 / 255

            f_x_mg = self._stu_raw_data.w_x_axis * f_mg_step
            f_y_mg = self._stu_raw_data.w_y_axis * f_mg_step
            f_z_mg = self._stu_raw_data.w_z_axis * f_mg_step

            return AccelValues(g_range=self._stu_raw_data.w_g_range,
                               raw_x=self._stu_raw_data.w_x_axis,
                               raw_y=self._stu_raw_data.w_y_axis,
                               raw_z=self._stu_raw_data.w_z_axis,
                               mg_x=f_x_mg,
                               mg_y=f_y_mg,
                               mg_z=f_z_mg)

    def get_offset(self) -> OffsetValues:
        """Get X/Y/Z direction offset value."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_GSR_GetAxisOffset(byref(self._stu_raw_data))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_GSR_GetAxisOffset", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)

            return OffsetValues(raw_x=self._stu_raw_data.w_x_axis,
                                raw_y=self._stu_raw_data.w_y_axis,
                                raw_z=self._stu_raw_data.w_z_axis)

    def test(self) -> None:
        """For testing."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            for i in range(100):
                print(f"---------> {i:d}")

                # Get accel data.
                i_ret = psp.lib.LMB_GSR_GetAxisData(byref(self._stu_raw_data))
                if i_ret != PSP.ERR_Success:
                    error_message = PSP.get_error_message("LMB_GSR_GetAxisData", i_ret)
                    print(f"\033[1;31m{error_message}\033[0m")
                else:
                    print(f"stuRawData.wRange= ±{self._stu_raw_data.w_g_range:d}g")

                    if self._stu_raw_data.w_g_range == 2:
                        f_mg_step = 2 / 255
                    elif self._stu_raw_data.w_g_range == 4:
                        f_mg_step = 4 / 255
                    elif self._stu_raw_data.w_g_range == 8:
                        f_mg_step = 8 / 255
                    elif self._stu_raw_data.w_g_range == 16:
                        f_mg_step = 16 / 255

                    f_x_mg = self._stu_raw_data.w_x_axis * f_mg_step
                    f_y_mg = self._stu_raw_data.w_y_axis * f_mg_step
                    f_z_mg = self._stu_raw_data.w_z_axis * f_mg_step

                    print(f"Raw={self._stu_raw_data.w_x_axis:d}\t, X-Axis= {f_x_mg:03.8f}")
                    print(f"Raw={self._stu_raw_data.w_y_axis:d}\t, Y-Axis= {f_y_mg:03.8f}")
                    print(f"Raw={self._stu_raw_data.w_z_axis:d}\t, Z-Axis= {f_z_mg:03.8f}")

                # Get offset.
                i_ret = psp.lib.LMB_GSR_GetAxisOffset(byref(self._stu_raw_data))
                if i_ret != PSP.ERR_Success:
                    error_message = PSP.get_error_message("LMB_GSR_GetAxisOffset", i_ret)
                    print(f"\033[1;31m{error_message}\033[0m")
                else:
                    print(f"Offset X-Axis={self._stu_raw_data.w_x_axis:d}")
                    print(f"Offset Y-Axis={self._stu_raw_data.w_y_axis:d}")
                    print(f"Offset Z-Axis={self._stu_raw_data.w_z_axis:d}")

                sleep(0.5)
