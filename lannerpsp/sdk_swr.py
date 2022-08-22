import logging
from ctypes import byref, c_uint8, CFUNCTYPE
from time import sleep, time
from typing import Optional, Union

from .core import PSP, get_psp_exc_msg
from .exc import (
    PSPError,
    PSPInvalid,
    PSPNotSupport,
)
from .lmbinc import (
    ERR_NotSupport,
    ERR_Success,
    IntrusionMsg,
)
from .sdk_dll import DLL

logger = logging.getLogger(__name__)


class SWR:
    """
    Software Reset Button.
    """

    def __init__(self) -> None:
        self._version = DLL().get_version()

    def get_status(self) -> int:
        """
        Get software reset button status.

        Example:

        .. code-block:: python

            >>> swr = SWR()
            >>> swr.get_status()
            1

        :return: software reset button status
        :rtype: int
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: General function error.
        """
        ub_read = c_uint8()
        with PSP() as psp:
            i_ret = psp.lib.LMB_SWR_GetStatus(byref(ub_read))
        msg = get_psp_exc_msg("LMB_SWR_GetStatus", i_ret)
        if i_ret == ERR_Success:
            return ub_read.value
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    @classmethod
    def _callback(cls, stu_intrusion_msg: IntrusionMsg) -> None:
        """Callback function for :func:`exec_callback`."""
        print(f"SWR Item = {stu_intrusion_msg.udw_occur_item:04X}, "
              f"Status = {stu_intrusion_msg.udw_status:04X}, "
              f"time is {stu_intrusion_msg.stu_time.uw_year:04d}/"
              f"{stu_intrusion_msg.stu_time.ub_month:02d}/"
              f"{stu_intrusion_msg.stu_time.ub_day:02d} "
              f"{stu_intrusion_msg.stu_time.ub_hour:02d}:"
              f"{stu_intrusion_msg.stu_time.ub_minute:02d}:"
              f"{stu_intrusion_msg.stu_time.ub_second:02d}")

    def exec_callback(self) -> None:
        """
        Use callback function to detect software reset button status (default 10 seconds).

        Example:

        .. code-block:: python

            >>> swr = SWR()
            >>> swr.exec_callback()
            ----> hook Software-Reset button Callback OK <----
            ===> wait about 10 second time <===
            SWR Item = 0001, Status = 0001, time is 2022/08/01 17:45:12
            SWR Item = 0001, Status = 0000, time is 2022/08/01 17:45:13
            SWR Item = 0001, Status = 0001, time is 2022/08/01 17:45:14
            SWR Item = 0001, Status = 0000, time is 2022/08/01 17:45:14
            SWR Item = 0001, Status = 0001, time is 2022/08/01 17:45:15
            SWR Item = 0001, Status = 0000, time is 2022/08/01 17:45:16
            ----> disabled Software-Reset button Callback hook <----
        """
        c_callback = CFUNCTYPE(None, IntrusionMsg)
        p_callback = c_callback(self._callback)
        with PSP() as psp:
            i_ret = psp.lib.LMB_SWR_IntrCallback(p_callback, 150)
            if i_ret != ERR_Success:
                print("-----> hook Software-Reset button callback failure <-------")
                return
            print("----> hook Software-Reset button Callback OK <----")
            print("===> wait about 10 second time <===")
            sleep(10)
            i_ret = psp.lib.LMB_SWR_IntrCallback(None, 150)
            if i_ret == ERR_Success:
                print("----> disabled Software-Reset button Callback hook <----")

    def test(self, secs: int = 5) -> None:
        """
        For testing (default 5 seconds delay).

        Example:

        .. code-block:: python

            >>> swr = SWR()
            >>> swr.test(5)
            >>> swr.test()
            ===> wait 5 seconds for Software Reset Button trigger .......
            5. 4. 3. 2. 1. 0.
            Software/Reset button not detected ! --> ALARM

        .. code-block:: python

            >>> swr.test()
            ===> wait 5 seconds for Software Reset Button trigger .......
            5. 4.
            Software/Reset button pressed ! --> OK

        :param int secs: seconds for test
        :raises TypeError: The input parameters type error.
        :raises ValueError: The input parameters value error.
        """
        # Check type.
        if not isinstance(secs, int):
            raise TypeError("'secs' type must be int")
        # Check value.
        if secs <= 0:
            raise ValueError("'secs' value must be > 0")
        # Run.
        ub_read = c_uint8()
        dw_cnt = 0
        index = int(secs)
        i_time = int(secs)
        print(f"===> wait {secs:d} seconds for Software Reset Button trigger .......")
        with PSP() as psp:
            while True:
                if dw_cnt % 10 == 0:
                    print(f"{index}. ", end="", flush=True)
                    index -= 1
                psp.lib.LMB_SWR_GetStatus(byref(ub_read))
                if ub_read.value == 1:
                    break
                dw_cnt += 1
                if dw_cnt > i_time * 10:
                    break
                sleep(0.1)
        print()
        if ub_read.value == 1:
            print("Software/Reset button pressed ! --> OK")
        else:
            print("\033[1;31mSoftware/Reset button not detected ! --> ALARM\033[0m")

    @property
    def is_pressed(self) -> bool:
        """
        Returns ``True`` if the device is currently active and ``False`` otherwise.

        Example:

        .. code-block:: python

            >>> swr = SWR()
            >>> swr.is_pressed
            True

        :return: if is pressed or not
        :rtype: bool
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: General function error.
        """
        return bool(self.get_status())

    def wait_for_press(self, timeout: Optional[Union[float, int]] = None) -> None:
        """
        Pause the script until the device is activated, or the timeout is reached.

        Example:

        .. code-block:: python

            >>> swr = SWR()
            >>> swr.wait_for_press()

        :type timeout: float or int or None
        :param timeout: Number of seconds to wait before proceeding.
            If this is ``None`` (the default), then wait indefinitely until the device is active.
        :raises TypeError: The input parameters type error.
        :raises PSPInvalid: The input parameters value error.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: General function error.
        """
        if timeout is not None:
            # Check type.
            if not isinstance(timeout, Union[float, int]):
                raise TypeError("'timeout' type must be float or int or None")
            # Check value.
            if timeout <= 0:
                raise PSPInvalid("'timeout' value must be > 0")
        # Run.
        start_time = time()
        while True:
            if self.is_pressed:
                break
            if timeout and time() - start_time >= timeout:
                break
            sleep(0.1)

    def wait_for_release(self, timeout: Optional[Union[float, int]] = None) -> None:
        """
        Pause the script until the device is deactivated, or the timeout is reached.

        Example:

        .. code-block:: python

            >>> swr = SWR()
            >>> swr.wait_for_release()

        :type timeout: float or int or None
        :param timeout: Number of seconds to wait before proceeding.
            If this is ``None`` (the default), then wait indefinitely until the device is active.
        :raises TypeError: The input parameters type error.
        :raises PSPInvalid: The input parameters value error.
        :raises PSPNotSupport: This function is not supported.
        :raises PSPError: General function error.
        """
        if timeout is not None:
            # Check type.
            if not isinstance(timeout, Union[float, int]):
                raise TypeError("'timeout' type must be float or int or None")
            # Check value.
            if timeout <= 0:
                raise PSPInvalid("'timeout' value must be > 0")
        # Run.
        start_time = time()
        while True:
            if not self.is_pressed:
                break
            if timeout and time() - start_time >= timeout:
                break
            sleep(0.1)
