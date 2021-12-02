import logging
from ctypes import addressof, byref, c_char_p, c_int8, c_uint16, cdll, CDLL, Structure
from mmap import mmap, PROT_READ, MAP_SHARED

from .utils import is_root

logger = logging.getLogger(__name__)


class DLLVersion(Structure):
    """DLL version (define in: sdk/include/lmbinc.h)."""
    _fields_ = [
        ("uw_dll_major", c_uint16),
        ("uw_dll_minor", c_uint16),
        ("uw_dll_build", c_uint16),
        ("str_platform_id", c_int8 * 15),
        ("uw_board_major", c_uint16),
        ("uw_board_minor", c_uint16),
        ("uw_board_build", c_uint16),
    ]


class PSP:
    """
    PSP.

    sdk/include/lmbinc.h
    sdk/src_utils/sdk_gsr/sdk_dll.c
    sdk/src_utils/sdk_gsr/sdk_bios.c

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
        if not is_root():
            raise PermissionError("Please uses root user !!!")
        self._liblmbio = cdll.LoadLibrary(lmb_io_path)
        self._liblmbapi = cdll.LoadLibrary(lmb_api_path)
        self._stu_dll_ver = DLLVersion()

    def __enter__(self):
        i_ret = self._liblmbapi.LMB_DLL_Init()
        if i_ret != self.ERR_Success:
            # This can happen when the BIOS message is different or the driver is not loaded.
            error_message = self.get_error_message("LMB_DLL_Init", i_ret)
            logger.error(error_message)
            raise self.PSPError(f"{error_message}, please confirm the API libraries is matched this platform")
        i_ret = self._liblmbapi.LMB_DLL_Version(byref(self._stu_dll_ver))
        if i_ret != self.ERR_Success:
            error_message = self.get_error_message("LMB_DLL_Version", i_ret)
            logger.error(error_message)
            raise self.PSPError(error_message)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self._liblmbapi.LMB_DLL_DeInit()
        return False

    @property
    def lib(self) -> CDLL:
        """The DLL/SO to call C functions."""
        return self._liblmbapi

    @property
    def sdk_version(self) -> str:
        """PSP/SDK version."""
        return f"{self._stu_dll_ver.uw_dll_major:d}." \
               f"{self._stu_dll_ver.uw_dll_minor:d}." \
               f"{self._stu_dll_ver.uw_dll_build:d}"

    @property
    def iodrv_version(self) -> str:
        """IODRV version."""
        # https://stackoverflow.com/a/29293102/9611854
        return f"{c_char_p(addressof(self._stu_dll_ver.str_platform_id)).value.decode():s}." \
               f"{self._stu_dll_ver.uw_board_major:d}." \
               f"{self._stu_dll_ver.uw_board_minor:d}." \
               f"{self._stu_dll_ver.uw_board_build:d}"

    @property
    def bios_version(self) -> str:
        """BIOS version."""
        # `sudo usermod -g kmem yourID`
        # `sudo busybox devmem 0x00ff58b 8 | xxd -r -p`
        key = "*LIID "
        with open("/dev/mem", "rb") as f:
            mem = mmap(f.fileno(), 0x10000, MAP_SHARED, PROT_READ, offset=0x000f0000)
        if mem is None:
            return ""
        if not mem.read(33 + len(key)).startswith(key.encode("utf-8")):
            # not found "*LIID"
            # add here for BIOS uses traditional position F000:F58B
            mem.seek(0xF58B)
        msg = mem.read(33 + len(key)).decode("utf-8").replace(key, "")
        li = msg.split('"')
        return li[0] + '"' + li[1] + '"'

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
