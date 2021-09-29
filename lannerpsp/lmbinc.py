import logging
from ctypes import cdll, CDLL
from os import geteuid

logger = logging.getLogger(__name__)


class PSP:
    """
    PSP.

    sdk/include/lmbinc.h

    :param lmb_io_path: Path of liblmbio.so
    :param lmb_api_path: Path of liblmbapi.so
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
        if i_ret != 0:
            self.show_error("LMB_DLL_Init", i_ret)
            # TODO: raise OSError(i_ret, "please confirm the API libraries is matched this platform")
        return self._liblmbapi

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self._liblmbapi.LMB_DLL_DeInit()
        return True

    @classmethod
    def show_error(cls, function_name: str, code: int) -> None:
        message = f"{function_name} return error code = 0x{code & 0xFFFFFFFF:08x}"
        if code == cls.ERR_Error:
            logger.error(f"{message}, Function Failure")
        elif code == cls.ERR_NotExist:
            logger.error(f"{message}, Library file not found or not exist")
        elif code == cls.ERR_NotOpened:
            logger.error(f"{message}, Library not opened yet")
        elif code == cls.ERR_Invalid:
            logger.error(f"{message}, Parameter invalid or out of range")
        elif code == cls.ERR_NotSupport:
            logger.error(f"{message}, This functions is not support of this platform")
        elif code == cls.ERR_BusyInUses:
            logger.error(f"{message}, busy")
        elif code == cls.ERR_BoardNotMatch:
            logger.error(f"{message}, the API library is not matched this platform")
        elif code == cls.ERR_DriverNotLoad:
            logger.error(f"{message}, the lmbiodrv driver or i2c-dev driver not loading")
        else:
            pass
