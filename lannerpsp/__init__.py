# python -m build
# twine upload dist/*
"""
==========================
Python API for Lanner PSP.
==========================
"""
from .core import PSP, get_psp_exc_msg
from .exc import (
    IPMIError,
    IPMIIBF0,
    IPMIIdleState,
    IPMIOBF1,
    IPMIReadState,
    IPMIWriteState,
    PSPBoardNotMatch,
    PSPBusyInUses,
    PSPDriverNotLoad,
    PSPError,
    PSPInvalid,
    PSPNotExist,
    PSPNotOpened,
    PSPNotSupport,
    PSPWarning,
)
from .sdk_dll import DLL, DLLVersionModel
from .sdk_gps import GPS
from .sdk_gsr import GSR, GSRDataModel, GSROffsetModel
from .sdk_hwm import HWM, HWMSensorModel
from .sdk_lcm import LCM
from .sdk_odm_com_port import COMPort, COMPortInfoModel
from .sdk_rfm import RFM
from .sdk_sled import SystemLED
from .sdk_sled_gps import GPSStatusLED
from .sdk_sled_lte import LTEStatusLED
from .sdk_sled_lte_stress import LTEStressLED
from .sdk_swr import SWR
from .sdk_wdt import WDT, WDTInfoModel

__version__ = "0.0.11"
__all__ = [
    # Functions
    "get_psp_exc_msg",
    # Classes
    "COMPort",
    "DLL",
    "GPS",
    "GPSStatusLED",
    "GSR",
    "HWM",
    "LCM",
    "LTEStatusLED",
    "LTEStressLED",
    "PSP",
    "RFM",
    "SWR",
    "SystemLED",
    "WDT",
    # Models
    "COMPortInfoModel",
    "DLLVersionModel",
    "GSRDataModel",
    "GSROffsetModel",
    "HWMSensorModel",
    "WDTInfoModel",
    # Exceptions & Warnings
    "IPMIError",
    "IPMIIBF0",
    "IPMIIdleState",
    "IPMIOBF1",
    "IPMIReadState",
    "IPMIWriteState",
    "PSPBoardNotMatch",
    "PSPBusyInUses",
    "PSPDriverNotLoad",
    "PSPError",
    "PSPInvalid",
    "PSPNotExist",
    "PSPNotOpened",
    "PSPNotSupport",
    "PSPWarning",
]
