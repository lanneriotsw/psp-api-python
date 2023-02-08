import logging
from ctypes import addressof, byref, c_char_p, c_int8, sizeof
from mmap import mmap, PROT_READ, MAP_SHARED
from typing import Any, Dict, NamedTuple

from .core import PSP, get_psp_exc_msg
from .exc import (
    PSPError,
    PSPNotOpened,
    PSPNotSupport,
)
from .lmbinc import (
    DLLVersion,
    ERR_Success,
    ERR_NotOpened,
    ERR_NotSupport,
)

logger = logging.getLogger(__name__)


class DLLVersionModel(NamedTuple):
    """To store DLL and Board Library version information."""
    dll_major: int
    dll_minor: int
    dll_build: int
    platform_id: str
    board_major: int
    board_minor: int
    board_build: int

    def __str__(self) -> str:
        return f"PSP/SDK version: {self.dll_major}.{self.dll_minor}.{self.dll_build}\n" \
               f"IODRV   version: {self.platform_id}.{self.board_major}.{self.board_minor}.{self.board_build}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict."""
        return dict(self._asdict())


class DLL:
    """
    Dynamic Link Library.
    """

    def __init__(self) -> None:
        pass

    def get_version(self) -> DLLVersionModel:
        """
        Load the Lanner board-level library.

        Example:

        .. code-block:: pycon

            >>> dll = DLL()
            >>> version = dll.get_version()
            >>> version
            DLLVersionModel(dll_major=2, dll_minor=1, dll_build=2, platform_id='LEB-7242', board_major=1, board_minor=0, board_build=2)
            >>> version.to_dict()
            {'dll_major': 2, 'dll_minor': 1, 'dll_build': 2, 'platform_id': 'LEB-7242', 'board_major': 1, 'board_minor': 0, 'board_build': 2}
            >>> str(version)
            'PSP/SDK version: 2.1.2\\nIODRV   version: LEB-7242.1.0.2'
            >>> version.dll_major
            2
            >>> version.dll_minor
            1
            >>> version.dll_build
            2
            >>> version.platform_id
            'LEB-7242'
            >>> version.board_major
            1
            >>> version.board_minor
            0
            >>> version.board_build
            2

        :return: the DLL and Board Library version information
        :rtype: DLLVersionModel
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPError: General PSP functional error.
        """
        stu_dll_ver = DLLVersion()
        with PSP() as psp:
            i_ret = psp.lib.LMB_DLL_Version(byref(stu_dll_ver))
        msg = get_psp_exc_msg("LMB_DLL_Version", i_ret)
        if i_ret == ERR_Success:
            return DLLVersionModel(
                dll_major=stu_dll_ver.uw_dll_major,
                dll_minor=stu_dll_ver.uw_dll_minor,
                dll_build=stu_dll_ver.uw_dll_build,
                # https://stackoverflow.com/a/29293102/9611854
                platform_id=c_char_p(addressof(stu_dll_ver.str_platform_id)).value.decode(),
                board_major=stu_dll_ver.uw_board_major,
                board_minor=stu_dll_ver.uw_board_minor,
                board_build=stu_dll_ver.uw_board_build,
            )
        elif i_ret == ERR_NotOpened:
            raise PSPNotOpened(msg)
        elif i_ret == ERR_NotSupport:
            raise PSPNotSupport(msg)
        else:
            raise PSPError(msg)

    def get_bios_id(self) -> str:
        """
        Get the Lanner mother-board BIOS infromation.

        Example:

        .. code-block:: pycon

            >>> dll = DLL()
            >>> dll.get_bios_id()
            'LEB-7242B BIOS V1.12 "03/09/2022"'

        :return: the mother board BIOS information
        :rtype: str
        :raises PSPNotOpened: The library is not ready or opened yet.
        :raises PSPNotSupport: This platform does not support this function.
        :raises PSPError: General PSP functional error.
        """
        try:
            str_bios_id = (c_int8 * 50)(*range(50))  # str_bios_id = create_string_buffer(50)
            with PSP() as psp:
                i_ret = psp.lib.LMB_DLL_BIOSID(str_bios_id, sizeof(str_bios_id))
            msg = get_psp_exc_msg("LMB_DLL_BIOSID", i_ret)
            if i_ret == ERR_Success:
                return c_char_p(addressof(str_bios_id)).value.decode().strip()
            elif i_ret == ERR_NotOpened:
                raise PSPNotOpened(msg)
            elif i_ret == PSPNotSupport:
                raise PSPNotSupport(msg)
            else:
                raise PSPError(msg)
        except AttributeError:
            # `sudo usermod -g kmem yourID`
            # `sudo busybox devmem 0x00ff58b 8 | xxd -r -p`
            key = "*LIID "
            with open("/dev/mem", "rb") as f:
                mem = mmap(f.fileno(), 0x10000, MAP_SHARED, PROT_READ, offset=0x000f0000)
            if mem is None:
                return ""
            if not mem.read(33 + len(key)).startswith(key.encode()):
                # not found "*LIID"
                # add here for BIOS uses traditional position F000:F58B
                mem.seek(0xF58B)
            return mem.read(33 + len(key)).decode().replace(key, "").strip().rsplit('"', 1)[0] + '"'
