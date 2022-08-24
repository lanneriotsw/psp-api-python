"""
Platform: LEC-7230
PSP version: 3.0.0
OS version:
- Debian 10: All pass
SDK:
- sdk_dll: Done.
- sdk_gpio: Not implement yet, don't know how to use this SDK.
- sdk_hwm: Done, except `-testop [seconds]`, don't know how to use this function.
- sdk_odm: Done.
- sdk_swr: Not implement yet, don't know how to set the button from hardware reset to software reset.
- sdk_wdt: Done.
"""
from time import sleep

import pytest

from lannerpsp import *

DELAY_TIME = 2  # Seconds.


class TestPSP:

    def test_init(self):
        with PSP():
            pass


class TestDLL:
    dll = DLL()

    def test_get_version(self):
        version = self.dll.get_version()
        assert version.dll_major == 3
        assert version.dll_minor == 0
        assert version.dll_build == 0
        assert version.platform_id == "LEC-7230"
        assert version.board_major == 1
        assert version.board_minor == 1
        assert version.board_build == 0

    def test_get_bios_id(self):
        assert self.dll.get_bios_id() == 'LEB-7230L Ver.MI0 04/10/2018'


class TestHWM:
    hwm = HWM()

    def test_list_supported_sensors(self):
        supported_sensors = self.hwm.list_supported_sensors()
        assert [s.sid for s in supported_sensors] == [4, 5, 41, 42, 45, 46, 47, 49, 50]
        assert supported_sensors[0].sid == 4
        assert supported_sensors[0].name == "HWMID_TEMP_SYS1"
        assert supported_sensors[1].sid == 5
        assert supported_sensors[1].name == "HWMID_TEMP_SYS2"
        assert supported_sensors[2].sid == 41
        assert supported_sensors[2].name == "HWMID_VCORE_CPU1"
        assert supported_sensors[3].sid == 42
        assert supported_sensors[3].name == "HWMID_VCORE_CPU2"
        assert supported_sensors[4].sid == 45
        assert supported_sensors[4].name == "HWMID_VOLT_P12V"
        assert supported_sensors[5].sid == 46
        assert supported_sensors[5].name == "HWMID_VOLT_P5V"
        assert supported_sensors[6].sid == 47
        assert supported_sensors[6].name == "HWMID_VOLT_P3V3"
        assert supported_sensors[7].sid == 49
        assert supported_sensors[7].name == "HWMID_VOLT_P3V3SB"
        assert supported_sensors[8].sid == 50
        assert supported_sensors[8].name == "HWMID_VOLT_VBAT"


class TestComPort:

    def test_set_all(self):
        com1 = COMPort(1)
        com1.set_mode(232)
        com1.set_termination(False)
        com1_info = com1.get_info()
        assert com1_info.num == 1
        assert com1_info.mode == 232
        assert com1_info.mode_str == "RS-232"
        assert com1_info.termination is False
        assert com1_info.termination_str == "Disabled"
        com2 = COMPort(2)
        com2.set_mode(485)
        com2.set_termination(True)
        com2_info = com2.get_info()
        assert com2_info.num == 2
        assert com2_info.mode == 485
        assert com2_info.mode_str == "RS-485"
        assert com2_info.termination is True
        assert com2_info.termination_str == "Enabled"

    def test_init_out_of_range(self):
        with pytest.raises(PSPInvalid) as e:
            COMPort(3)
        assert str(e.value) == "'num' can only be set to (1~2) on this platform"

    def test_set_mode_out_of_range(self):
        com1 = COMPort(1)
        with pytest.raises(ValueError):
            com1.set_mode(666)


class TestWDT:
    wdt = WDT()

    def test_get_info(self):
        wdt_info = self.wdt.get_info()
        assert wdt_info.type == "SuperIO"
        assert wdt_info.max_count == 255
        assert wdt_info.is_minute_support is True

    def test_enable(self):
        self.wdt.enable(10, 2)

    def test_reset(self):
        self.wdt.reset()

    def test_disable(self):
        self.wdt.disable()

    def test_config_out_of_range(self):
        with pytest.raises(PSPInvalid):
            self.wdt.config(256)
        with pytest.raises(PSPInvalid):
            self.wdt.config(10, 3)

    def test_integration(self):
        with pytest.raises(PSPError):
            self.wdt.reset()
        self.wdt.enable(200)
        sleep(DELAY_TIME)
        self.wdt.reset()
        sleep(DELAY_TIME)
        self.wdt.disable()
