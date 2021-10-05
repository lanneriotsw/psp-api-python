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
        ("wg_range", c_int16),
    ]


class AxisData:
    """To store axis data."""

    def __init__(self, wg_range: int, w_x_axis: int, w_y_axis: int, w_z_axis: int,
                 f_x_mg: float, f_y_mg: float, f_z_mg: float) -> None:
        self._wg_range = wg_range
        self._w_x_axis = w_x_axis
        self._w_y_axis = w_y_axis
        self._w_z_axis = w_z_axis
        self._f_x_mg = f_x_mg
        self._f_y_mg = f_y_mg
        self._f_z_mg = f_z_mg

    @property
    def wg_range(self) -> int:
        return self._wg_range

    @property
    def w_x_axis(self) -> int:
        return self._w_x_axis

    @property
    def w_y_axis(self) -> int:
        return self._w_y_axis

    @property
    def w_z_axis(self) -> int:
        return self._w_z_axis

    @property
    def f_x_mg(self) -> float:
        return self._f_x_mg

    @property
    def f_y_mg(self) -> float:
        return self._f_y_mg

    @property
    def f_z_mg(self) -> float:
        return self._f_z_mg


class AxisOffset:
    """To store axis offset."""

    def __init__(self, w_x_axis: int, w_y_axis: int, w_z_axis: int) -> None:
        self._w_x_axis = w_x_axis
        self._w_y_axis = w_y_axis
        self._w_z_axis = w_z_axis

    @property
    def w_x_axis(self) -> int:
        return self._w_x_axis

    @property
    def w_y_axis(self) -> int:
        return self._w_y_axis

    @property
    def w_z_axis(self) -> int:
        return self._w_z_axis


class GSR:
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

    def get_axis_data(self) -> AxisData:
        """Get X/Y/Z direction accelerate value."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_GSR_GetAxisData(byref(self._stu_raw_data))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_GSR_GetAxisData", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)

            logger.info(f"get gsr w-range= ±{self._stu_raw_data.wg_range:d}g")

            if self._stu_raw_data.wg_range == 2:
                fmg_step = 2 / 255
            elif self._stu_raw_data.wg_range == 4:
                fmg_step = 4 / 255
            elif self._stu_raw_data.wg_range == 8:
                fmg_step = 8 / 255
            elif self._stu_raw_data.wg_range == 16:
                fmg_step = 16 / 255

            f_x_mg = self._stu_raw_data.w_x_axis * fmg_step
            f_y_mg = self._stu_raw_data.w_y_axis * fmg_step
            f_z_mg = self._stu_raw_data.w_z_axis * fmg_step

            logger.info(f"get gsr x-axis raw= {self._stu_raw_data.w_x_axis:d}, accel= {f_x_mg:03.8f}")
            logger.info(f"get gsr x-axis raw= {self._stu_raw_data.w_y_axis:d}, accel= {f_y_mg:03.8f}")
            logger.info(f"get gsr x-axis raw= {self._stu_raw_data.w_z_axis:d}, accel= {f_z_mg:03.8f}")

            return AxisData(wg_range=self._stu_raw_data.wg_range,
                            w_x_axis=self._stu_raw_data.w_x_axis,
                            w_y_axis=self._stu_raw_data.w_y_axis,
                            w_z_axis=self._stu_raw_data.w_z_axis,
                            f_x_mg=f_x_mg,
                            f_y_mg=f_y_mg,
                            f_z_mg=f_z_mg)

    def get_axis_offset(self) -> AxisOffset:
        """Get X/Y/Z direction offset value."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_GSR_GetAxisOffset(byref(self._stu_raw_data))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_GSR_GetAxisOffset", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)

            logger.info(f"get gsr x-axis offset= {self._stu_raw_data.w_x_axis:d}")
            logger.info(f"get gsr y-axis offset= {self._stu_raw_data.w_y_axis:d}")
            logger.info(f"get gsr z-axis offset= {self._stu_raw_data.w_z_axis:d}")

            return AxisOffset(w_x_axis=self._stu_raw_data.w_x_axis,
                              w_y_axis=self._stu_raw_data.w_y_axis,
                              w_z_axis=self._stu_raw_data.w_z_axis)

    def test(self) -> None:
        """For testing."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            for i in range(100):
                logger.info(f"---------> {i:d}")

                # Get accel data.
                i_ret = psp.LMB_GSR_GetAxisData(byref(self._stu_raw_data))
                if i_ret != PSP.ERR_Success:
                    error_message = PSP.get_error_message("LMB_GSR_GetAxisData", i_ret)
                    logger.error(error_message)
                else:
                    logger.info(f"stuRawData.wRange= ±{self._stu_raw_data.wg_range:d}g")

                    if self._stu_raw_data.wg_range == 2:
                        fmg_step = 2 / 255
                    elif self._stu_raw_data.wg_range == 4:
                        fmg_step = 4 / 255
                    elif self._stu_raw_data.wg_range == 8:
                        fmg_step = 8 / 255
                    elif self._stu_raw_data.wg_range == 16:
                        fmg_step = 16 / 255

                    f_x_mg = self._stu_raw_data.w_x_axis * fmg_step
                    f_y_mg = self._stu_raw_data.w_y_axis * fmg_step
                    f_z_mg = self._stu_raw_data.w_z_axis * fmg_step

                    logger.info(f"Raw={self._stu_raw_data.w_x_axis:d}\t, X-Axis= {f_x_mg:03.8f}")
                    logger.info(f"Raw={self._stu_raw_data.w_y_axis:d}\t, Y-Axis= {f_y_mg:03.8f}")
                    logger.info(f"Raw={self._stu_raw_data.w_z_axis:d}\t, Z-Axis= {f_z_mg:03.8f}")

                # Get offset.
                i_ret = psp.LMB_GSR_GetAxisOffset(byref(self._stu_raw_data))
                if i_ret != PSP.ERR_Success:
                    error_message = PSP.get_error_message("LMB_GSR_GetAxisOffset", i_ret)
                    logger.error(error_message)
                else:
                    logger.info(f"Offset X-Axis={self._stu_raw_data.w_x_axis:d}")
                    logger.info(f"Offset Y-Axis={self._stu_raw_data.w_y_axis:d}")
                    logger.info(f"Offset Z-Axis={self._stu_raw_data.w_z_axis:d}")

                sleep(0.5)
