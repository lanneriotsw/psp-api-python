from ctypes import c_float, c_int8, c_uint8, c_uint16, Structure

# HWM type
HWM_TYPE_NONE = 0
HWM_TYPE_SIO = 1
HWM_TYPE_IPMI = 2
HWM_TYPE_SMBUS = 3
HWM_TYPE_AST1400 = 4

IPMI_INVALID_VALUE = 0x01  # bit 0
IPMI_INVALID_UC = 0x02  # bit 1
IPMI_INVALID_LC = 0x04  # bit 2

IPMI_NAME_MAX_SIZE = 16


# IPMI API Group
class IPMISensorInfo(Structure):
    """IPMI_SENSOR_INFO"""
    _fields_ = [
        ("str_name", c_int8 * (IPMI_NAME_MAX_SIZE + 1)),
        ("f_invalid_flag", c_int8),
        ("f_value", c_float),
        ("f_hi_critical", c_float),
        ("f_lo_critical", c_float),
        ("str_unit", c_int8 * (IPMI_NAME_MAX_SIZE + 1)),
    ]


class IPMISDRMap(Structure):
    """IPMI_SDRMAP"""
    _fields_ = [
        ("uw_id_num", c_uint16),
        ("str_name", c_int8 * (IPMI_NAME_MAX_SIZE + 1)),
        ("ub_kcs_reg", c_uint8),
    ]
