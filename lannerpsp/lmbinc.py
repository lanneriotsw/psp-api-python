import logging
from ctypes import cdll, CDLL
from os import geteuid

logger = logging.getLogger(__name__)


class PSP:
    """
    PSP.

    sdk/include/lmbinc.h

    :param lmb_io_path: path of liblmbio.so
    :param lmb_api_path: path of liblmbapi.so
    """

    """ Return Value """
    ERR_Success = 0
    ERR_Error = -1  # 0xFFFFFFFF
    ERR_NotExist = -2  # 0xFFFFFFFE
    ERR_NotOpened = -3  # 0xFFFFFFFD
    ERR_Invalid = -4  # 0xFFFFFFFC
    ERR_NotSupport = -5  # 0xFFFFFFFB
    ERR_BusyInUses = -6  # 0xFFFFFFFA
    ERR_BoardNotMatch = -7  # 0xFFFFFFF9
    ERR_DriverNotLoad = -8  # 0xFFFFFFF8
    """ IPMI access error """
    ERR_IPMI_IDLESTATE = -257  # 0xFFFFFEFF
    ERR_IPMI_WRITESTATE = -258  # 0xFFFFFEFE
    ERR_IPMI_READSTATE = -259  # 0xFFFFFEFD
    ERR_IPMI_IBF0 = -260  # 0xFFFFFEFC
    ERR_IPMI_OBF1 = -261  # 0xFFFFFEFB

    def __init__(self,
                 lmb_io_path: str = "/opt/lanner/psp/bin/amd64/lib/liblmbio.so",
                 lmb_api_path: str = "/opt/lanner/psp/bin/amd64/lib/liblmbapi.so") -> None:
        self._lmb_io_path = lmb_io_path
        self._lmb_api_path = lmb_api_path
        self._liblmbio = None
        self._liblmbapi = None

    def __enter__(self) -> CDLL:
        if geteuid() != 0:
            raise PermissionError("Please uses root user !!!")
        self._liblmbio = cdll.LoadLibrary(self._lmb_io_path)
        self._liblmbapi = cdll.LoadLibrary(self._lmb_api_path)
        i_ret = self._liblmbapi.LMB_DLL_Init()
        if i_ret != self.ERR_Success:
            # This can happen when the BIOS message is different or the driver is not loaded.
            error_message = self.get_error_message("LMB_DLL_Init", i_ret)
            logger.error(error_message)
            raise self.PSPError(f"{error_message}, please confirm the API libraries is matched this platform")
        return self._liblmbapi

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self._liblmbapi.LMB_DLL_DeInit()
        return False

    @classmethod
    def get_error_message(cls, function_name: str, error_code: int) -> str:
        message = f"{function_name}: 0x{error_code & 0xFFFFFFFF:08x}: "
        if error_code == cls.ERR_Error:
            message += "function failure"
        elif error_code == cls.ERR_NotExist:
            message += "library file not found or not exist"
        elif error_code == cls.ERR_NotOpened:
            message += "library not opened yet"
        elif error_code == cls.ERR_Invalid:
            message += "parameter invalid or out of range"
        elif error_code == cls.ERR_NotSupport:
            message += "this functions is not support of this platform"
        elif error_code == cls.ERR_BusyInUses:
            message += "busy"
        elif error_code == cls.ERR_BoardNotMatch:
            message += "the API library is not matched this platform"
        elif error_code == cls.ERR_DriverNotLoad:
            message += "the lmbiodrv driver or i2c-dev driver not loading"
        else:
            message += "unknown error"
        return message

    class PSPError(Exception):
        """Raised when any PSP error occurs."""

        def __init__(self, msg: str = "") -> None:
            self._message = msg

        def __repr__(self) -> str:
            return self._message

        __str__ = __repr__
