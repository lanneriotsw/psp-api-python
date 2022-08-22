from ctypes import c_int8, c_int16, c_uint8, c_uint16, c_uint32, Structure

# Return Value
ERR_Success = 0
ERR_Error = -1  # 0xFFFFFFFF
ERR_NotExist = -2  # 0xFFFFFFFE
ERR_NotOpened = -3  # 0xFFFFFFFD
ERR_Invalid = -4  # 0xFFFFFFFC
ERR_NotSupport = -5  # 0xFFFFFFFB
ERR_BusyInUses = -6  # 0xFFFFFFFA
ERR_BoardNotMatch = -7  # 0xFFFFFFF9
ERR_DriverNotLoad = -8  # 0xFFFFFFF8
# IPMI access error
ERR_IPMI_IDLESTATE = -257  # 0xFFFFFEFF
ERR_IPMI_WRITESTATE = -258  # 0xFFFFFEFE
ERR_IPMI_READSTATE = -259  # 0xFFFFFEFD
ERR_IPMI_IBF0 = -260  # 0xFFFFFEFC
ERR_IPMI_OBF1 = -261  # 0xFFFFFEFB

# Timer Function
BASE_SECOND = 1
BASE_MINUTE = 2

# WDT Type define
WDT_TYPE_UNKNOWN = 0
WDT_TYPE_SIO = 1
WDT_TYPE_TCO = 2

DLL_VERSION_ID_SIZE = 15


class DLLVersion(Structure):
    """DLL_VERSION"""
    _fields_ = [
        ("uw_dll_major", c_uint16),
        ("uw_dll_minor", c_uint16),
        ("uw_dll_build", c_uint16),
        ("str_platform_id", c_int8 * DLL_VERSION_ID_SIZE),
        ("uw_board_major", c_uint16),
        ("uw_board_minor", c_uint16),
        ("uw_board_build", c_uint16),
    ]


class WDTInfo(Structure):
    """WDT_INFO"""
    _fields_ = [
        ("ub_type", c_uint8),
        ("uw_count_max", c_uint16),
        ("ub_minute_support", c_uint8),
    ]


class IntrusionTime(Structure):
    """INTRUSION_TIME"""
    _fields_ = [
        ("uw_year", c_uint16),
        ("ub_month", c_uint8),
        ("ub_day", c_uint8),
        ("ub_hour", c_uint8),
        ("ub_minute", c_uint8),
        ("ub_second", c_uint8),
    ]


# Intrusion Callback Function
class IntrusionMsg(Structure):
    """INTRUSION_MSG"""
    _fields_ = [
        ("udw_occur_item", c_uint32),  # Occur item
        ("udw_status", c_uint32),  # Occur status
        ("stu_time", IntrusionTime),  # Occur time
    ]


class LCMInfo(Structure):
    """LCM_INFO"""
    _fields_ = [
        ("uw_mode_no", c_uint16),
        ("uw_version", c_uint16),
        ("udw_baud_rate", c_uint32),
    ]


# LCM Keys Callback Function
class LCMKeyMsg(Structure):
    """LCMKEY_MSG"""
    _fields_ = [
        ("ub_keys", c_uint8),  # Occur Keys
        ("ub_status", c_uint8),  # Occur status
        ("stu_time", IntrusionTime),  # Occur time
    ]


# G-Sensor X,Y,Z Axis
class AxisRawData(Structure):
    """AXIS_RAWDATA"""
    _fields_ = [
        ("w_x_axis", c_int16),
        ("w_y_axis", c_int16),
        ("w_z_axis", c_int16),
        ("w_g_range", c_int16),
    ]


# ODM API Functions
URMODE_LOOPBACK = 0
URMODE_RS232 = 1
URMODE_RS485 = 2
URMODE_RS422 = 3
