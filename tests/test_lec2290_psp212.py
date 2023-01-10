"""
Platform: LEC-2290
PSP version: 2.1.2
OS version:
- Debian 11: All pass
SDK:
- sdk_dll: Done.
- sdk_gpio: Not implement yet, don't know how to use this SDK.
- sdk_hwm: Done.
- sdk_ign: Not implement yet, don't know how to use this SDK.
- sdk_poe: Not implement yet, don't know how to use this SDK.
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
        assert version.dll_major == 2
        assert version.dll_minor == 1
        assert version.dll_build == 2
        assert version.platform_id == "LEC-2290"
        assert version.board_major == 1
        assert version.board_minor == 0
        assert version.board_build == 2

    def test_get_bios_id(self):
        assert self.dll.get_bios_id() == 'LEB-2291B BIOS V2.02 "06/08/2021"'


class TestHWM:
    hwm = HWM()

    def test_list_supported_sensors(self):
        supported_sensors = self.hwm.list_supported_sensors()
        assert sorted([s.sid for s in supported_sensors]) == sorted([
            0, 2, 4, 6, 7, 10, 11, 72,
            225, 226, 227, 228, 229, 230, 232, 233,
        ])
        assert supported_sensors[0].sid == 0
        assert supported_sensors[0].name == "HWMID_TEMP_CPU1"
        assert supported_sensors[1].sid == 2
        assert supported_sensors[1].name == "HWMID_TEMP_SYS1"
        assert supported_sensors[2].sid == 4
        assert supported_sensors[2].name == "HWMID_VCORE_CPU1"
        assert supported_sensors[3].sid == 6
        assert supported_sensors[3].name == "HWMID_VOLT_P12V"
        assert supported_sensors[4].sid == 7
        assert supported_sensors[4].name == "HWMID_VOLT_P5V"
        assert supported_sensors[5].sid == 10
        assert supported_sensors[5].name == "HWMID_VOLT_P3V3SB"
        assert supported_sensors[6].sid == 11
        assert supported_sensors[6].name == "HWMID_VOLT_VBAT"
        assert supported_sensors[7].sid == 72
        assert supported_sensors[7].name == "HWMID_VOLT_VCCGT"


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
        # PSP version 2.1 has a bug in the WDT `reset` function
        # that stops the timer like `disable`.
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
