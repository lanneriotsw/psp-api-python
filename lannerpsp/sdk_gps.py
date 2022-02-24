import logging
from ctypes import c_char_p

from .lmbinc import PSP

logger = logging.getLogger(__name__)


class GPS:
    """
    GPS.

    sdk/src_utils/sdk_gps/sdk_gps.c

    :param lmb_io_path: path of liblmbio.so
    :param lmb_api_path: path of liblmbapi.so
    """

    DEFAULT_GPS_PORT = "/dev/ttyS1"

    def __init__(self,
                 lmb_io_path: str = "/opt/lanner/psp/bin/amd64/lib/liblmbio.so",
                 lmb_api_path: str = "/opt/lanner/psp/bin/amd64/lib/liblmbapi.so") -> None:
        self._lmb_io_path = lmb_io_path
        self._lmb_api_path = lmb_api_path
        self._str_gps_port = c_char_p(self.DEFAULT_GPS_PORT.encode())

    def search_port(self) -> str:
        """Search GPS port."""
        with PSP(self._lmb_io_path, self._lmb_api_path) as psp:
            i_ret = psp.lib.LMB_GPS_SearchPort(self._str_gps_port)
            if i_ret != PSP.ERR_Success:
                error_message = PSP.get_error_message("LMB_GPS_SearchPort", i_ret)
                logger.error(error_message)
                raise PSP.PSPError(error_message)
            gps_port = self._str_gps_port.value.decode()
            logger.debug(f"get gps port {gps_port}")
            return gps_port
