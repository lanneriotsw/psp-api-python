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

SUPPORTED_PLATFORMS = ("V3S", "V6S",)
UNSUPPORTED_PLATFORMS = ("LEB-2680", "LEB-7242", "LEC-2290", "LEC-7230", "NCA-2510",)

DEFAULT_GPS_PORT = "/dev/ttyS1"


class GPS:
    """
    Global Positioning System.

    :param bool check_platform:
        Set to :data:`True` to check if the platform supports this feature.
        Defaults to :data:`False` for better compatibility.
    :raises PSPNotSupport: This function is not supported
        (when ``check_platform`` is set to :data:`True`).
    :raises NotImplementedError: It has not been verified to run on this platform
        (when ``check_platform`` is set to :data:`True`).
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

    def search_port(self) -> str:
        """
        Search GPS port.

        Example:

        .. code-block:: pycon

            >>> gps = GPS()
            >>> gps.search_port()
            '/dev/ttyS3'

        :return: the GPS port on the platform
        :rtype: str
        :raises PSPNotSupport: This function is not supported.
        :raises PSPNotExist: The device does not exist.
        :raises PSPError: General PSP functional error.
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
