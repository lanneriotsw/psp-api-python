"""
Platform: LEC-2680(IIoT-I530)
PSP version: 2.3.7
OS version:
- Debian 11: All pass
SDK:
- sdk_dll: Done.
- sdk_hwm: Done.
- sdk_ign: Not implement yet, don't know how to use this SDK.
- sdk_mcu: Only completed the `GPIO` functions.
- sdk_odm: Done.
- sdk_poe: Done.
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
        assert version.dll_minor == 3
        assert version.dll_build == 7
        assert version.platform_id == "LEB-2680"
        assert version.board_major == 1
        assert version.board_minor == 1
        assert version.board_build == 0

    def test_get_bios_id(self):
        assert self.dll.get_bios_id() == 'LEB-2680A BIOS V2.00 "06/17/2022"'


class TestGPIO:
    # TODO: Tooling is required.
    pass


class TestHWM:
    hwm = HWM()

    def test_list_supported_sensors(self):
        supported_sensors = self.hwm.list_supported_sensors()
        assert sorted([s.sid for s in supported_sensors]) == sorted([
            0, 2, 4, 7, 8, 11,
        ])
        assert supported_sensors[0].sid == 0
        assert supported_sensors[0].name == "HWMID_TEMP_CPU1"
        assert supported_sensors[1].sid == 2
        assert supported_sensors[1].name == "HWMID_TEMP_SYS1"
        assert supported_sensors[2].sid == 4
        assert supported_sensors[2].name == "HWMID_VCORE_CPU1"
        assert supported_sensors[3].sid == 7
        assert supported_sensors[3].name == "HWMID_VOLT_P5V"
        assert supported_sensors[4].sid == 8
        assert supported_sensors[4].name == "HWMID_VOLT_P3V3"
        assert supported_sensors[5].sid == 11
        assert supported_sensors[5].name == "HWMID_VOLT_VBAT"


class TestComPort:

    def test_init_out_of_range(self):
        with pytest.raises(PSPInvalid) as e:
            COMPort(3)
        assert str(e.value) == "'num' can only be set to (1~2) on this platform"

    def test_set_mode_out_of_range(self):
        com1 = COMPort(1)
        with pytest.raises(ValueError):
            com1.set_mode(666)


class TestPoE:

    def test_get_supported_ports(self):
        poe_info = PoE.get_info()
        assert poe_info.number_of_poe_ports == 6

    def test_set_all(self):
        for i in range(6):
            poe1 = PoE(i + 1)
            poe1.enable()
            assert poe1.get_power_status() is True
            assert PoE.get_info().power_status[i + 1] is True
            poe1.disable()
            assert poe1.get_power_status() is False
            assert PoE.get_info().power_status[i + 1] is False

    def test_init_out_of_range(self):
        with pytest.raises(PSPInvalid) as e:
            PoE(7)
        assert str(e.value) == "'num' can only be set to (1~6) on this platform"


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
