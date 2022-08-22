import logging
from ctypes import c_char_p

from .core import PSP, get_psp_exc_msg
from .exc import (
    PSPError,
    PSPNotExist,
    PSPNotSupport,
)
from .lmbinc import (
    ERR_NotExist,
    ERR_NotSupport,
    ERR_Success,
)
from .sdk_dll import DLL

logger = logging.getLogger(__name__)

DEFAULT_GPS_PORT = "/dev/ttyS1"


class GPS:
    """
    Global Positioning System.
    """

    def __init__(self) -> None:
        self._version = DLL().get_version()

    def search_port(self) -> str:
        """
        Search GPS port.

        Example:

        .. code-block:: python

            >>> gps = GPS()
            >>> gps.search_port()
            '/dev/ttyS3'

        :return: GPS port
        :rtype: str
        :raises PSPNotSupport: This function is not supported.
        :raises PSPNotExist: The device does not exist.
        :raises PSPError: General function error.
        """
        str_gps_port = c_char_p(DEFAULT_GPS_PORT.encode())
        with PSP() as psp:
            i_ret = psp.lib.LMB_GPS_SearchPort(str_gps_port)
        msg = get_psp_exc_msg("LMB_GPS_SearchPort", i_ret)
        if i_ret == ERR_Success:
            gps_port = str_gps_port.value.decode()
            return gps_port
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        elif i_ret == ERR_NotExist:
            raise PSPNotExist(msg)
        else:
            raise PSPError(msg)
