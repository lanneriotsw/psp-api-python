import logging
from ctypes import byref, c_int16, Structure
from time import sleep
from typing import Optional

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
    """

    _stu_raw_data = AxisRawData()

    @classmethod
    def get_data(cls) -> Optional[AxisData]:
        """Get X/Y/Z direction accelerate value."""
        with PSP() as psp:
            i_ret = psp.LMB_GSR_GetAxisData(byref(cls._stu_raw_data))
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_GSR_GetAxisData", i_ret)
                return

            logger.info(f"get gsr w-range= ±{cls._stu_raw_data.wg_range:d}g")

            if cls._stu_raw_data.wg_range == 2:
                fmg_step = 2 / 255
            elif cls._stu_raw_data.wg_range == 4:
                fmg_step = 4 / 255
            elif cls._stu_raw_data.wg_range == 8:
                fmg_step = 8 / 255
            elif cls._stu_raw_data.wg_range == 16:
                fmg_step = 16 / 255

            f_x_mg = cls._stu_raw_data.w_x_axis * fmg_step
            f_y_mg = cls._stu_raw_data.w_y_axis * fmg_step
            f_z_mg = cls._stu_raw_data.w_z_axis * fmg_step

            logger.info(f"get gsr x-axis raw= {cls._stu_raw_data.w_x_axis:d}, accel= {f_x_mg:03.8f}")
            logger.info(f"get gsr x-axis raw= {cls._stu_raw_data.w_y_axis:d}, accel= {f_y_mg:03.8f}")
            logger.info(f"get gsr x-axis raw= {cls._stu_raw_data.w_z_axis:d}, accel= {f_z_mg:03.8f}")

            return AxisData(wg_range=cls._stu_raw_data.wg_range,
                            w_x_axis=cls._stu_raw_data.w_x_axis,
                            w_y_axis=cls._stu_raw_data.w_y_axis,
                            w_z_axis=cls._stu_raw_data.w_z_axis,
                            f_x_mg=f_x_mg,
                            f_y_mg=f_y_mg,
                            f_z_mg=f_z_mg)

    @classmethod
    def get_offset(cls) -> Optional[AxisOffset]:
        """Get X/Y/Z direction offset value."""
        with PSP() as psp:
            i_ret = psp.LMB_GSR_GetAxisOffset(byref(cls._stu_raw_data))
            if i_ret != PSP.ERR_Success:
                PSP.show_error("LMB_GSR_GetAxisOffset", i_ret)
                return

            logger.info(f"get gsr x-axis offset= {cls._stu_raw_data.w_x_axis:d}")
            logger.info(f"get gsr y-axis offset= {cls._stu_raw_data.w_y_axis:d}")
            logger.info(f"get gsr z-axis offset= {cls._stu_raw_data.w_z_axis:d}")

            return AxisOffset(w_x_axis=cls._stu_raw_data.w_x_axis,
                              w_y_axis=cls._stu_raw_data.w_y_axis,
                              w_z_axis=cls._stu_raw_data.w_z_axis)

    @classmethod
    def test(cls) -> None:
        """For testing."""
        with PSP() as psp:
            for i in range(100):
                logger.info(f"---------> {i:d}")

                # Get accel data.
                i_ret = psp.LMB_GSR_GetAxisData(byref(cls._stu_raw_data))
                if i_ret == PSP.ERR_Success:
                    logger.info(f"stuRawData.wRange= ±{cls._stu_raw_data.wg_range:d}g")

                    if cls._stu_raw_data.wg_range == 2:
                        fmg_step = 2 / 255
                    elif cls._stu_raw_data.wg_range == 4:
                        fmg_step = 4 / 255
                    elif cls._stu_raw_data.wg_range == 8:
                        fmg_step = 8 / 255
                    elif cls._stu_raw_data.wg_range == 16:
                        fmg_step = 16 / 255

                    f_x_mg = cls._stu_raw_data.w_x_axis * fmg_step
                    f_y_mg = cls._stu_raw_data.w_y_axis * fmg_step
                    f_z_mg = cls._stu_raw_data.w_z_axis * fmg_step

                    logger.info(f"Raw={cls._stu_raw_data.w_x_axis:d}\t, X-Axis= {f_x_mg:03.8f}")
                    logger.info(f"Raw={cls._stu_raw_data.w_y_axis:d}\t, Y-Axis= {f_y_mg:03.8f}")
                    logger.info(f"Raw={cls._stu_raw_data.w_z_axis:d}\t, Z-Axis= {f_z_mg:03.8f}")
                else:
                    PSP.show_error("LMB_GSR_GetAxisData", i_ret)

                # Get offset.
                i_ret = psp.LMB_GSR_GetAxisOffset(byref(cls._stu_raw_data))
                if i_ret == PSP.ERR_Success:
                    logger.info(f"Offset X-Axis={cls._stu_raw_data.w_x_axis:d}")
                    logger.info(f"Offset Y-Axis={cls._stu_raw_data.w_y_axis:d}")
                    logger.info(f"Offset Z-Axis={cls._stu_raw_data.w_z_axis:d}")
                else:
                    PSP.show_error("LMB_GSR_GetAxisOffset", i_ret)

                sleep(0.5)
