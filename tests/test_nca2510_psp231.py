"""
Platform: NCA-2510
PSP version: 2.3.1
OS version:
- Ubuntu 18.04: All pass
SDK:
- sdk_bios: Done.
- sdk_dll: Done.
- sdk_eep: Not implement yet, don't know how to use this SDK.
- sdk_gpio: Done.
- sdk_hwm: Done.
- sdk_lbp: Not implement yet, don't know how to use this SDK.
- sdk_lcm: Done, except UART type device.
- sdk_sled: Done.
- sdk_swr: Done.
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
        assert version.dll_build == 1
        assert version.platform_id == "NCA-2510"
        assert version.board_major == 1
        assert version.board_minor == 1
        assert version.board_build == 0

    def test_get_bios_id(self):
        assert self.dll.get_bios_id() == '*LIID NCA-2510B BIOS V2.02 "08/09/2018"'


class TestGPIO:
    # TODO: Tooling is required.
    pass


class TestHWM:
    hwm = HWM()

    def test_list_supported_sensors(self):
        supported_sensors = self.hwm.list_supported_sensors()
        assert sorted([s.sid for s in supported_sensors]) == sorted([4, 5, 41, 45, 46, 48, 49, 50, 51, 73, 75])
        assert supported_sensors[0].sid == 4
        assert supported_sensors[0].name == "HWMID_TEMP_SYS1"
        assert supported_sensors[1].sid == 5
        assert supported_sensors[1].name == "HWMID_TEMP_SYS2"
        assert supported_sensors[2].sid == 41
        assert supported_sensors[2].name == "HWMID_VCORE_CPU1"
        assert supported_sensors[3].sid == 45
        assert supported_sensors[3].name == "HWMID_VOLT_P12V"
        assert supported_sensors[4].sid == 46
        assert supported_sensors[4].name == "HWMID_VOLT_P5V"
        assert supported_sensors[5].sid == 48
        assert supported_sensors[5].name == "HWMID_VOLT_P5VSB"
        assert supported_sensors[6].sid == 49
        assert supported_sensors[6].name == "HWMID_VOLT_P3V3SB"
        assert supported_sensors[7].sid == 50
        assert supported_sensors[7].name == "HWMID_VOLT_VBAT"
        assert supported_sensors[8].sid == 51
        assert supported_sensors[8].name == "HWMID_VOLT_DDRCH1"
        assert supported_sensors[9].sid == 73
        assert supported_sensors[9].name == "HWMID_RPM_Fan1A"
        assert supported_sensors[10].sid == 75
        assert supported_sensors[10].name == "HWMID_RPM_Fan2A"


class TestLCM:
    lcm = LCM()

    def test_set_backlight(self):
        self.lcm.set_backlight(False)
        sleep(DELAY_TIME)
        self.lcm.set_backlight(True)
        sleep(DELAY_TIME)

    def test_integration(self):
        self.lcm.clear()
        self.lcm.write("Hello Kitty!")
        sleep(DELAY_TIME)
        self.lcm.set_cursor(2, 5)
        sleep(DELAY_TIME)
        self.lcm.write("UFO handsome")
        sleep(DELAY_TIME)
        self.lcm.clear()
        sleep(DELAY_TIME)


class TestSystemLED:
    system_led = SystemLED()

    def test_green(self):
        self.system_led.green()
        sleep(DELAY_TIME)

    def test_red(self):
        self.system_led.red()
        sleep(DELAY_TIME)

    def test_off(self):
        self.system_led.off()
        sleep(DELAY_TIME)


class TestSWR:
    swr = SWR()


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
