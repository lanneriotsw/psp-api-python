from time import sleep

import pytest

from lannerpsp import *

DELAY_TIME = 2  # Seconds.


class TestPSP:
    """Platform Support Package."""

    def test_init(self) -> None:
        with PSP() as psp:
            pass

    def test_sdk_version(self) -> None:
        with PSP() as psp:
            assert psp.sdk_version == "2.3.1"

    def test_iodrv_version(self) -> None:
        with PSP() as psp:
            assert psp.iodrv_version == "NCA-2510.1.1.0"

    def test_bios_version(self) -> None:
        with PSP() as psp:
            assert psp.bios_version == 'NCA-2510B BIOS V2.02 "08/09/2018"'


class TestSystemLED:
    """System/Status LED."""

    system_led = SystemLED()

    def test_green(self) -> None:
        self.system_led.green()
        sleep(DELAY_TIME)

    def test_red(self) -> None:
        self.system_led.red()
        sleep(DELAY_TIME)

    def test_off(self) -> None:
        self.system_led.off()
        sleep(DELAY_TIME)

    def test_test(self) -> None:
        self.system_led.test(DELAY_TIME)
        sleep(DELAY_TIME)


class TestHardwareMonitor:
    """Hardware Monitor."""

    hwm = HardwareMonitor()

    def test_get_cpu_temp(self) -> None:
        # CPU-1 temperature.
        with pytest.raises(PSP.PSPError) as e:
            self.hwm.get_cpu_temp(1)
        assert str(e.value) == "LMB_HWM_GetCpuTemp: 0xfffffffb: this functions is not support of this platform"
        # CPU-2 temperature.
        with pytest.raises(PSP.PSPError) as e:
            self.hwm.get_cpu_temp(2)
        assert str(e.value) == "LMB_HWM_GetCpuTemp: 0xfffffffb: this functions is not support of this platform"

        # Fool Proof.
        with pytest.raises(TypeError):
            self.hwm.get_cpu_temp(None)
        with pytest.raises(TypeError):
            self.hwm.get_cpu_temp(94.87)
        with pytest.raises(TypeError):
            self.hwm.get_cpu_temp("WTF")
        with pytest.raises(PSP.PSPError) as e:
            self.hwm.get_cpu_temp(666)
        assert str(e.value) == "LMB_HWM_GetCpuTemp: 0xffffffff: function failure"

    def test_get_sys_temp(self) -> None:
        # SYS-1 temperature.
        self.hwm.get_sys_temp(1)
        # SYS-2 temperature.
        self.hwm.get_sys_temp(2)

        # Fool Proof.
        with pytest.raises(TypeError):
            self.hwm.get_sys_temp(None)
        with pytest.raises(TypeError):
            self.hwm.get_sys_temp(94.87)
        with pytest.raises(TypeError):
            self.hwm.get_sys_temp("WTF")
        with pytest.raises(PSP.PSPError) as e:
            self.hwm.get_sys_temp(666)
        assert str(e.value) == "LMB_HWM_GetSysTemp: 0xffffffff: function failure"

    def test_get_vcore(self) -> None:
        # CPU-1 Vcore.
        self.hwm.get_vcore(1)
        # CPU-2 Vcore.
        with pytest.raises(PSP.PSPError) as e:
            self.hwm.get_vcore(2)
        assert str(e.value) == "LMB_HWM_GetVcore: 0xfffffffb: this functions is not support of this platform"

        # Fool Proof.
        with pytest.raises(TypeError):
            self.hwm.get_vcore(None)
        with pytest.raises(TypeError):
            self.hwm.get_vcore(94.87)
        with pytest.raises(TypeError):
            self.hwm.get_vcore("WTF")
        with pytest.raises(PSP.PSPError) as e:
            self.hwm.get_vcore(666)
        assert str(e.value) == "LMB_HWM_GetVcore: 0xffffffff: function failure"

    def test_get_12v(self) -> None:
        self.hwm.get_12v()

    def test_get_5v(self) -> None:
        self.hwm.get_5v()

    def test_get_3v3(self) -> None:
        with pytest.raises(PSP.PSPError) as e:
            self.hwm.get_3v3()
        assert str(e.value) == "LMB_HWM_Get3V3: 0xfffffffb: this functions is not support of this platform"

    def test_get_5vsb(self) -> None:
        self.hwm.get_5vsb()

    def test_get_3v3sb(self) -> None:
        self.hwm.get_3v3sb()

    def test_get_vbat(self) -> None:
        self.hwm.get_vbat()

    def test_get_power_supply(self) -> None:
        # PowerSupply 1 AC voltage.
        with pytest.raises(PSP.PSPError) as e:
            self.hwm.get_power_supply(1)
        assert str(e.value) == "LMB_HWM_GetPowerSupply: 0xfffffffb: this functions is not support of this platform"
        # PowerSupply 2 AC voltage.
        with pytest.raises(PSP.PSPError) as e:
            self.hwm.get_power_supply(2)
        assert str(e.value) == "LMB_HWM_GetPowerSupply: 0xfffffffb: this functions is not support of this platform"

        # Fool Proof.
        with pytest.raises(TypeError):
            self.hwm.get_power_supply(None)
        with pytest.raises(TypeError):
            self.hwm.get_power_supply(94.87)
        with pytest.raises(TypeError):
            self.hwm.get_power_supply("WTF")
        with pytest.raises(PSP.PSPError) as e:
            self.hwm.get_power_supply(666)
        assert str(e.value) == "LMB_HWM_GetPowerSupply: 0xfffffffc: parameter invalid or out of range"

    # def test_testhwm(self) -> None:
    #     self.hwm.testhwm()

    # def test_get_all(self) -> None:
    #     assert self.hwm.get_all()


class TestLCM:
    """Liquid Crystal Display Module."""

    lcm = LCM()

    def test_get_module_type(self) -> None:
        self.lcm.get_module_type()
        sleep(DELAY_TIME)

    def test_set_backlight(self) -> None:
        self.lcm.set_backlight(False)
        sleep(DELAY_TIME)
        self.lcm.set_backlight(True)
        sleep(DELAY_TIME)

    def test_integration(self) -> None:
        self.lcm.clear()
        self.lcm.write("Hello World!")
        sleep(DELAY_TIME)
        self.lcm.set_cursor(2, 5)
        sleep(DELAY_TIME)
        self.lcm.write("UFO handsome")
        sleep(DELAY_TIME)
        self.lcm.clear()
        sleep(DELAY_TIME)


class TestSoftwareReset:
    """Software Reset."""

    swr = SoftwareReset()


class TestWatchdogTimer:
    """Watchdog Timer."""

    wdt = WatchdogTimer()

    def test_enable(self) -> None:
        self.wdt.enable(10)

        # Fool Proof.
        with pytest.raises(TypeError):
            self.wdt.enable(None)
        with pytest.raises(TypeError):
            self.wdt.enable(94.87)
        with pytest.raises(TypeError):
            self.wdt.enable("WTF")
        with pytest.raises(ValueError):
            self.wdt.enable(-1)

    def test_reset(self) -> None:
        self.wdt.reset()

    def test_disable(self) -> None:
        self.wdt.disable()

    def test_integration(self) -> None:
        with pytest.raises(PSP.PSPError) as e:
            self.wdt.reset()
        assert str(e.value) == "LMB_WDT_Tick: 0xffffffff: function failure"
        self.wdt.enable(10)
        sleep(DELAY_TIME)
        self.wdt.reset()
        sleep(DELAY_TIME)
        self.wdt.disable()
