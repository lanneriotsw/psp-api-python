import logging
from ctypes import c_char_p
from typing import Optional

from .lmbinc import PSP

logger = logging.getLogger(__name__)


class GPS:
    """
    GPS.

    sdk/src_utils/sdk_gps/sdk_gps.c
    """

    @classmethod
    def search_port(cls) -> Optional[str]:
        """Search GPS port."""
        with PSP() as psp:
            default_gps_port = "/dev/ttyS1"
            str_gps_port = c_char_p(default_gps_port.encode())
            i_ret = psp.LMB_GPS_SearchPort(str_gps_port)
            if i_ret == PSP.ERR_Success:
                gps_port = str_gps_port.value.decode()
                logger.info(f"get gps port {gps_port}")
                return gps_port
            else:
                PSP.show_error("LMB_GPS_SearchPort", i_ret)
