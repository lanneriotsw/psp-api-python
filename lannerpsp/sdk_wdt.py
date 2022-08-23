import logging
from ctypes import byref
from typing import Any, Dict, NamedTuple

from .core import PSP, get_psp_exc_msg
from .exc import (
    PSPBusyInUses,
    PSPError,
    PSPInvalid,
    PSPNotOpened,
    PSPNotSupport,
)
from .lmbinc import (
    BASE_SECOND,
    BASE_MINUTE,
    ERR_BusyInUses,
    ERR_Invalid,
    ERR_NotOpened,
    ERR_NotSupport,
    ERR_Success,
    WDT_TYPE_SIO,
    WDT_TYPE_TCO,
    WDT_TYPE_UNKNOWN,
    WDTInfo,
)
from .sdk_dll import DLL

logger = logging.getLogger(__name__)


class WDTInfoModel(NamedTuple):
    """To store WDT info values."""
    type: str
    max_count: int
    is_minute_support: bool

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict."""
        return dict(self._asdict())


class WDT:
    """
    Watch Dog Timer.
    """

    def __init__(self) -> None:
        self._version = DLL().get_version()

    def get_info(self) -> WDTInfoModel:
        """
        Get Watch Dog Timer information.

        Example:

        .. code-block:: python

            >>> wdt = WDT()
            >>> wdt.get_info()
            WDTInfoModel(type='SuperIO', max_count=255, is_minute_support=True)

        :return: WDT information
        :rtype: WDTInfoModel
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPError: This function failed.
        """
        stu_wdt_info = WDTInfo()
        type_mapping = {WDT_TYPE_UNKNOWN: "Unknown", WDT_TYPE_SIO: "SuperIO", WDT_TYPE_TCO: "TCO"}
        with PSP() as psp:
            i_ret = psp.lib.LMB_WDT_QueryInfo(byref(stu_wdt_info))
        msg = get_psp_exc_msg("LMB_WDT_QueryInfo", i_ret)
        if i_ret == ERR_Success:
            return WDTInfoModel(
                type=type_mapping[stu_wdt_info.ub_type],
                max_count=stu_wdt_info.uw_count_max,
                is_minute_support=bool(stu_wdt_info.ub_minute_support),
            )
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def config(self, count: int, time_base: int = 1) -> None:
        """
        Configure the Watch Dog Timer for specific time.

        Example for 200 seconds:

        .. code-block:: python

            >>> wdt = WDT()
            >>> wdt.config(200)

        Example for 2 minutes:

        .. code-block:: python

            >>> wdt = WDT()
            >>> wdt.config(2, 2)

        :param int count:
            The value sets the timer count down.

        :param int time_base:
            The value selects time base. Set :data:`1` to select SECOND base,
            Set :data:`2` to select MINUTE base. Defaults to 1 (SECOND base).

        :raises TypeError: The input parameters type error.
        :raises PSPInvalid: Invalid parameter value.
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPBusyInUses: This step is skipped because WDT is already starting now.
        :raises PSPError: This function failed.
        """
        # Check type.
        if not isinstance(count, int):
            raise TypeError("'count' type must be int")
        if not isinstance(time_base, int):
            raise TypeError("'time_base' type must be int")
        # Check value.
        info = self.get_info()
        if not 0 <= count <= info.max_count:
            raise PSPInvalid(f"'count' value must be between 0 and {info.max_count}")
        if time_base not in (BASE_SECOND, BASE_MINUTE):
            raise PSPInvalid(f"'time_base' value must be {BASE_SECOND}"
                             f" for SECOND base or {BASE_MINUTE} for MINUTE base")
        if not info.is_minute_support and time_base == BASE_MINUTE:
            raise PSPInvalid("WDT only support SECOND base")
        # Run.
        time_base_mapping = {BASE_SECOND: "seconds", BASE_MINUTE: "minutes"}
        with PSP() as psp:
            i_ret = psp.lib.LMB_WDT_Config(count, time_base)
        msg = get_psp_exc_msg("LMB_WDT_Config", i_ret)
        if i_ret == ERR_Success:
            logger.debug(f"configure the watchdog timer for {count:d} {time_base_mapping[time_base]}")
        elif i_ret == ERR_Invalid:
            raise PSPInvalid(msg)
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        elif i_ret == ERR_BusyInUses:
            raise PSPBusyInUses(msg)
        else:
            raise PSPError(msg)

    def enable(self, count: int = 0, time_base: int = 1) -> None:
        """
        Configure the Watch Dog Timer for specific time and start the WDT countdown.

        You can :func:`enable` dircetly by a given time:

        .. code-block:: python

            >>> wdt = WDT()
            >>> wdt.enable(200)

        Or :func:`config` first then :func:`enable`

        .. code-block:: python

            >>> wdt = WDT()
            >>> wdt.config(200)
            >>> wdt.enable()

        :param int count:
            The value sets the timer count down. Defaults to 0.

        :param int time_base:
            The value selects time base. Set :data:`1` to select SECOND base,
            Set :data:`2` to select MINUTE base. Defaults to 1.

        :raises TypeError: The input parameters type error.
        :raises PSPInvalid: Invalid parameter value.
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPBusyInUses: This step is skipped because WDT is already starting now.
        :raises PSPError: This function failed.
        """
        if count != 0:
            self.config(count, time_base)
        with PSP() as psp:
            i_ret = psp.lib.LMB_WDT_Start()
        msg = get_psp_exc_msg("LMB_WDT_Start", i_ret)
        if i_ret == ERR_Success:
            logger.debug("enable watchdog timer")
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def disable(self) -> None:
        """
        Stop the WDT countdown.

        Example:

        .. code-block:: python

            >>> wdt = WDT()
            >>> wdt.enable(10)
            >>>
            >>> wdt.disable()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPError: This function failed.
        """
        with PSP() as psp:
            i_ret = psp.lib.LMB_WDT_Stop()
        msg = get_psp_exc_msg("LMB_WDT_Stop", i_ret)
        if i_ret == ERR_Success:
            logger.debug("disable watchdog timer")
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def reset(self) -> None:
        """
        Reload the timer and then re-computes it.

        Example:

        .. code-block:: python

            >>> wdt = WDT()
            >>> wdt.enable(10)
            >>>
            >>> wdt.reset()

        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPError: This function failed.
        """
        with PSP() as psp:
            i_ret = psp.lib.LMB_WDT_Tick()
        msg = get_psp_exc_msg("LMB_WDT_Tick", i_ret)
        if i_ret == ERR_Success:
            logger.debug("reset watchdog timer")
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)
