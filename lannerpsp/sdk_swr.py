import logging
from ctypes import byref, c_uint8, c_uint16, c_uint32, CFUNCTYPE, Structure
from time import sleep, time
from typing import Optional

from .lmbinc import PSP

logger = logging.getLogger(__name__)


class IntrusionTime(Structure):
    """Intrusion time (define in: sdk/include/lmbinc.h)."""
    _fields_ = [
        ("uw_year", c_uint16),
        ("ub_month", c_uint8),
        ("ub_day", c_uint8),
        ("ub_hour", c_uint8),
        ("ub_minute", c_uint8),
        ("ub_second", c_uint8),
    ]


class IntrusionMsg(Structure):
    """Intrusion callback function (define in: sdk/include/lmbinc.h)."""
    _fields_ = [
        ("udw_occur_item", c_uint32),
        ("udw_status", c_uint32),
        ("stu_time", IntrusionTime),
    ]


class SoftwareReset:
    """
    Software Reset.

    sdk/src_utils/sdk_sled/sdk_swr.c

    :param lmb_io_path: path of liblmbio.so
    :param lmb_api_path: path of liblmbapi.so
    """

    def __init__(self,
                 lmb_io_path: str = "/opt/lanner/psp/bin/amd64/lib/liblmbio.so",
                 lmb_api_path: str = "/opt/lanner/psp/bin/amd64/lib/liblmbapi.so") -> None:
        self._lmb_io_path = lmb_io_path
        self._lmb_api_path = lmb_api_path
        self._ub_read = c_uint8()

    def get_status(self) -> int:
        """Get software reset button status."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_SWR_GetStatus(byref(self._ub_read))
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_SWR_GetStatus", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            logger.info(f"SWReset button Status is {self._ub_read.value}")
            return self._ub_read.value

    @classmethod
    def _callback(cls, stu_intrusion_msg: IntrusionMsg) -> None:
        """Callback function for exec_callback()"""
        print(f"SWR Item = {stu_intrusion_msg.udw_occur_item:04X}, "
              f"Status = {stu_intrusion_msg.udw_status:04X}, "
              f"time is {stu_intrusion_msg.stu_time.uw_year:04d}/"
              f"{stu_intrusion_msg.stu_time.ub_month:02d}/"
              f"{stu_intrusion_msg.stu_time.ub_day:02d} "
              f"{stu_intrusion_msg.stu_time.ub_hour:02d}:"
              f"{stu_intrusion_msg.stu_time.ub_minute:02d}:"
              f"{stu_intrusion_msg.stu_time.ub_second:02d}")

    def exec_callback(self) -> None:
        """Use callback function to detect software reset button status (default 10 seconds)."""
        c_callback = CFUNCTYPE(None, IntrusionMsg)
        p_callback = c_callback(self._callback)
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.LMB_SWR_IntrCallback(p_callback, 150)
            if i_ret != PSP.ERR_Success:
                print("-----> hook Software-Reset button callback failure <-------")
                return
            print("----> hook Software-Reset button Callback OK <----")
            print("===> wait about 10 second time <===")
            sleep(10)
            i_ret = psp.LMB_SWR_IntrCallback(None, 150)
            if i_ret == PSP.ERR_Success:
                print("----> disabled Software-Reset button Callback hook <----")

    def test(self, seconds: int = 5) -> None:
        """For testing (default 5 seconds delay).

        :param seconds: seconds
        """
        # Check type.
        if not isinstance(seconds, int):
            raise TypeError("'seconds' type must be int")
        # Check value.
        if seconds <= 0:
            raise ValueError("'seconds' value must be > 0")
        print(f"===> wait {seconds} seconds for Software Reset Button trigger .......")
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            while seconds >= 0:
                if round(seconds % 1, 1) == 0.0:
                    print(f"{int(seconds):d}. ", end="", flush=True)
                psp.LMB_SWR_GetStatus(byref(self._ub_read))
                if self._ub_read.value == 1:
                    break
                seconds -= 0.1
                sleep(0.1)
        print()
        if self._ub_read.value == 1:
            print("Software/Reset button pressed ! --> OK")
        else:
            print("\033[1;31mSoftware/Reset button not detected ! --> ALARM\033[0m")

    @property
    def is_pressed(self) -> bool:
        """Returns `True` if the device is currently active and `False` otherwise."""
        return bool(self.get_status())

    def wait_for_press(self, timeout: Optional[float] = None) -> None:
        """Pause the script until the device is activated, or the timeout is reached.

        :param timeout: Number of seconds to wait before proceeding.
            If this is `None` (the default), then wait indefinitely until the device is active.
        """
        if timeout is not None:
            if not isinstance(timeout, float):
                raise TypeError("'timeout' type must be float or None")
            if timeout <= 0.0:
                raise ValueError("'timeout' value must be > 0.0")
        start_time = time()
        while True:
            if self.is_pressed:
                break
            if timeout and time() - start_time >= timeout:
                break
            sleep(0.1)

    def wait_for_release(self, timeout: Optional[float] = None) -> None:
        """Pause the script until the device is deactivated, or the timeout is reached.

        :param timeout: Number of seconds to wait before proceeding.
            If this is `None` (the default), then wait indefinitely until the device is active.
        """
        if timeout is not None:
            if not isinstance(timeout, float):
                raise TypeError("'timeout' type must be float or None")
            if timeout <= 0.0:
                raise ValueError("'timeout' value must be > 0.0")
        start_time = time()
        while True:
            if not self.is_pressed:
                break
            if timeout and time() - start_time >= timeout:
                break
            sleep(0.1)
