class PSPError(Exception):
    """Generic error message (Base class for all exceptions in Lanner PSP)"""


class PSPNotExist(PSPError, FileNotFoundError):
    """Error raised when library file is not found/plugged, or the device does not exist"""


class PSPNotOpened(PSPError, RuntimeError):
    """Error raised when library is not opened or not ready yet"""


class PSPInvalid(PSPError, ValueError):
    """Error raised when the Parameter is not a valid value or out of range"""


class PSPNotSupport(PSPError, RuntimeError):
    """Error raised when this function is not supported in this platform"""


class PSPBusyInUses(PSPError, RuntimeError):
    """Error raised when library is being used now or device IO is busy now"""


class PSPBoardNotMatch(PSPError, RuntimeError):
    """Error raised when the board library and the board do not match"""


class PSPDriverNotLoad(PSPError, RuntimeError):
    """Error raised when the lmbiodrv driver or i2c-dev driver not loading"""


class IPMIError(PSPError):
    """Base class for errors related to the IPMI implementation"""


class IPMIIdleState(IPMIError, RuntimeError):
    """Error raised when IPMI KCS interface is not in IDLE State"""


class IPMIWriteState(IPMIError, RuntimeError):
    """Error raised when IPMI KCS interface WRITE State check failure"""


class IPMIReadState(IPMIError, RuntimeError):
    """Error raised when IPMI KCS interface READ State check failure"""


class IPMIIBF0(IPMIError, RuntimeError):
    """Error raised when IPMI KCS interface wait IBF ‘0’ State failure"""


class IPMIOBF1(IPMIError, RuntimeError):
    """Error raised when IPMI KCS interface wait OBF ‘1’ State failure"""


class PSPWarning(Warning):
    """Base class for all warnings in Lanner PSP"""
