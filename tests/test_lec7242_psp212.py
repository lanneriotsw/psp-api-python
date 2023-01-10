"""
Platform: LEC-7242
PSP version: 2.1.2
OS version:
- Debian 10: All pass
- Debian 11: All pass
SDK:
- sdk_bios: Done.
- sdk_dll: Done.
- sdk_hwm: Done.
- sdk_rfm: Done.
- sdk_sled: Done.
- sdk_sled_gps: Done.
- sdk_sled_lte: Done.
- sdk_sled_lte_stress: Done.
- sdk_swr: Done.
- sdk_wdt: Done.
- config_tool: Done.
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
        assert version.platform_id == "LEB-7242"
        assert version.board_major == 1
        assert version.board_minor == 0
        assert version.board_build == 2

    def test_get_bios_id(self):
        assert self.dll.get_bios_id() == 'LEB-7242B BIOS V1.12 "03/09/2022"'


class TestHWM:
    hwm = HWM()

    def test_list_supported_sensors(self):
        supported_sensors = self.hwm.list_supported_sensors()
        assert sorted([s.sid for s in supported_sensors]) == sorted([0, 2, 4, 7, 8, 11, 12])
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
        assert supported_sensors[6].sid == 12
        assert supported_sensors[6].name == "HWMID_VOLT_DDRCH1"


class TestRFM:
    rfm = RFM()

    def test_get_sim_status(self):
        assert self.rfm.get_sim_status() in range(4)

    def test_set_sim_status(self):
        self.rfm.set_sim_status(3)
        assert self.rfm.get_sim_status() == 3
        sleep(DELAY_TIME)
        self.rfm.set_sim_status(2)
        assert self.rfm.get_sim_status() == 2
        sleep(DELAY_TIME)
        self.rfm.set_sim_status(1)
        assert self.rfm.get_sim_status() == 1
        sleep(DELAY_TIME)
        self.rfm.set_sim_status(0)
        assert self.rfm.get_sim_status() == 0
        sleep(DELAY_TIME)

    def test_get_power_status(self):
        assert self.rfm.get_power_status() in range(4)

    def test_set_power_status(self):
        self.rfm.set_power_status(0)
        assert self.rfm.get_power_status() == 0
        sleep(DELAY_TIME)
        self.rfm.set_power_status(1)
        assert self.rfm.get_power_status() == 1
        sleep(DELAY_TIME)
        self.rfm.set_power_status(2)
        assert self.rfm.get_power_status() == 2
        sleep(DELAY_TIME)
        self.rfm.set_power_status(3)
        assert self.rfm.get_power_status() == 3
        sleep(DELAY_TIME)

    def test_set_sim_status_out_of_range(self):
        with pytest.raises(PSPInvalid):
            self.rfm.set_sim_status(-1)
        with pytest.raises(PSPError):
            self.rfm.set_sim_status(666)

    def test_set_power_status_out_of_range(self):
        with pytest.raises(PSPError):
            self.rfm.set_power_status(-1)
        with pytest.raises(PSPError):
            self.rfm.set_power_status(666)


class TestSystemLED:
    system_led = SystemLED()

    def test_green(self):
        with pytest.raises(PSPError):
            self.system_led.green()
        sleep(DELAY_TIME)

    def test_red(self):
        self.system_led.red()
        sleep(DELAY_TIME)

    def test_off(self):
        self.system_led.off()
        sleep(DELAY_TIME)


class TestGPSStatusLED:
    gps_status_led = GPSStatusLED()

    def test_on(self):
        self.gps_status_led.on()
        sleep(DELAY_TIME)

    def test_blink(self):
        self.gps_status_led.blink()
        sleep(DELAY_TIME)

    def test_off(self):
        self.gps_status_led.off()
        sleep(DELAY_TIME)


class TestLTEStatusLED:
    lte_status_led = LTEStatusLED()

    def test_red(self):
        self.lte_status_led.red()
        sleep(DELAY_TIME)

    def test_red_blink(self):
        self.lte_status_led.red_blink()
        sleep(DELAY_TIME)

    def test_green(self):
        self.lte_status_led.green()
        sleep(DELAY_TIME)

    def test_green_blink(self):
        self.lte_status_led.green_blink()
        sleep(DELAY_TIME)

    def test_yellow(self):
        self.lte_status_led.yellow()
        sleep(DELAY_TIME)

    def test_yellow_blink(self):
        self.lte_status_led.yellow_blink()
        sleep(DELAY_TIME)

    def test_off(self):
        self.lte_status_led.off()
        sleep(DELAY_TIME)


class TestLTEStressLED:
    lte_stress_led = LTEStressLED()

    def test_set_strength(self):
        self.lte_stress_led.set_strength(90)
        sleep(DELAY_TIME)
        self.lte_stress_led.set_strength(78)
        sleep(DELAY_TIME)
        self.lte_stress_led.set_strength(66)
        sleep(DELAY_TIME)
        self.lte_stress_led.set_strength(54)
        sleep(DELAY_TIME)
        self.lte_stress_led.set_strength(42)
        sleep(DELAY_TIME)
        self.lte_stress_led.set_strength(30)
        sleep(DELAY_TIME)
        self.lte_stress_led.set_strength(18)
        sleep(DELAY_TIME)
        self.lte_stress_led.set_strength(6)
        sleep(DELAY_TIME)

    def test_set_strength_out_of_range(self):
        with pytest.raises(PSPInvalid):
            self.lte_stress_led.set_strength(-1)
        with pytest.raises(PSPInvalid):
            self.lte_stress_led.set_strength(101)

    def test_off(self):
        self.lte_stress_led.off()
        sleep(DELAY_TIME)


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


class TestComPort:

    def test_set_all(self):
        com1 = COMPort(1)
        com1.set_mode(232)
        com1.set_mode(422)
        com1.set_mode(485)
        com1.set_termination(True)
        com1.set_termination(False)
        with pytest.raises(PSPNotSupport):
            com1.get_info()

    def test_init_out_of_range(self):
        with pytest.raises(PSPInvalid) as e:
            COMPort(2)
        assert str(e.value) == "'num' can only be set to (1) on this platform"

    def test_set_mode_out_of_range(self):
        com1 = COMPort(1)
        with pytest.raises(ValueError):
            com1.set_mode(666)
