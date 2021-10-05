from time import sleep

import pytest

from lannerpsp import *

DELAY_TIME = 2.0  # Second.


class TestPSP:
    """Platform Support Package."""

    def test_init(self) -> None:
        with PSP() as psp:
            pass


class TestSystemLED:
    """System/Status LED."""

    system_led = SystemLED()

    def test_green(self) -> None:
        with pytest.raises(PSP.PSPError) as e:
            self.system_led.green()
        assert str(e.value) == "LMB_SLED_SetSystemLED: 0xffffffff: function failure"
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


class TestGPSLED:
    """GPS Status LED."""

    gps_led = GPSLED()

    def test_on(self) -> None:
        self.gps_led.on()
        sleep(DELAY_TIME)

    def test_blink(self) -> None:
        self.gps_led.blink()
        sleep(DELAY_TIME)

    def test_off(self) -> None:
        self.gps_led.off()
        sleep(DELAY_TIME)

    def test_test(self) -> None:
        self.gps_led.test(DELAY_TIME)
        sleep(DELAY_TIME)


class TestLteStateLED:
    """LTE Status LED."""

    lte_state_led = LteStateLED()

    def test_red(self) -> None:
        self.lte_state_led.red()
        sleep(DELAY_TIME)

    def test_red_blink(self) -> None:
        self.lte_state_led.red_blink()
        sleep(DELAY_TIME)

    def test_green(self) -> None:
        self.lte_state_led.green()
        sleep(DELAY_TIME)

    def test_green_blink(self) -> None:
        self.lte_state_led.green_blink()
        sleep(DELAY_TIME)

    def test_yellow(self) -> None:
        self.lte_state_led.yellow()
        sleep(DELAY_TIME)

    def test_yellow_blink(self) -> None:
        self.lte_state_led.yellow_blink()
        sleep(DELAY_TIME)

    def test_off(self) -> None:
        self.lte_state_led.off()
        sleep(DELAY_TIME)

    def test_test(self) -> None:
        self.lte_state_led.test(DELAY_TIME)
        sleep(DELAY_TIME)


class TestLteStressLED:
    """LTE Stress LED."""

    lte_stress_led = LteStressLED()

    def test_set_strength(self) -> None:
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

        # Fool Proof.
        with pytest.raises(TypeError):
            self.lte_stress_led.set_strength(None)
        with pytest.raises(TypeError):
            self.lte_stress_led.set_strength(94.87)
        with pytest.raises(TypeError):
            self.lte_stress_led.set_strength("WTF")
        with pytest.raises(ValueError):
            self.lte_stress_led.set_strength(-1)
        with pytest.raises(ValueError):
            self.lte_stress_led.set_strength(101)

    def test_off(self) -> None:
        self.lte_stress_led.off()
        sleep(DELAY_TIME)

    def test_test(self) -> None:
        self.lte_stress_led.test(DELAY_TIME)
        sleep(DELAY_TIME)


class TestRFM:
    """Radio Frequency Module."""

    rfm = RFM()

    def test_get_sim(self) -> None:
        assert self.rfm.get_sim() in range(4)

    def test_set_sim(self) -> None:
        self.rfm.set_sim(3)
        assert self.rfm.get_sim() == 3
        sleep(DELAY_TIME)
        self.rfm.set_sim(2)
        assert self.rfm.get_sim() == 2
        sleep(DELAY_TIME)
        self.rfm.set_sim(1)
        assert self.rfm.get_sim() == 1
        sleep(DELAY_TIME)
        self.rfm.set_sim(0)
        assert self.rfm.get_sim() == 0
        sleep(DELAY_TIME)

        # Fool Proof.
        with pytest.raises(TypeError):
            self.rfm.set_sim(None)
        with pytest.raises(TypeError):
            self.rfm.set_sim(94.87)
        with pytest.raises(TypeError):
            self.rfm.set_sim("WTF")
        with pytest.raises(PSP.PSPError) as e:
            self.rfm.set_sim(-1)
        assert str(e.value) == "LMB_RFM_SetSIM: 0xfffffffc: parameter invalid or out of range"
        with pytest.raises(PSP.PSPError) as e:
            self.rfm.set_sim(666)
        assert str(e.value) == "LMB_RFM_SetSIM: 0xfffffffc: parameter invalid or out of range"

    def test_get_module(self) -> None:
        assert self.rfm.get_module() in range(4)

    def test_set_module(self) -> None:
        self.rfm.set_module(0)
        assert self.rfm.get_module() == 0
        sleep(DELAY_TIME)
        self.rfm.set_module(1)
        assert self.rfm.get_module() == 1
        sleep(DELAY_TIME)
        self.rfm.set_module(2)
        assert self.rfm.get_module() == 2
        sleep(DELAY_TIME)
        self.rfm.set_module(3)
        assert self.rfm.get_module() == 3
        sleep(DELAY_TIME)

        # Fool Proof.
        with pytest.raises(TypeError):
            self.rfm.set_module(None)
        with pytest.raises(TypeError):
            self.rfm.set_module(94.87)
        with pytest.raises(TypeError):
            self.rfm.set_module("WTF")
        with pytest.raises(PSP.PSPError) as e:
            self.rfm.set_module(-1)
        assert str(e.value) == "LMB_RFM_SetModule: 0xfffffffc: parameter invalid or out of range"
        with pytest.raises(PSP.PSPError) as e:
            self.rfm.set_module(666)
        assert str(e.value) == "LMB_RFM_SetModule: 0xfffffffc: parameter invalid or out of range"


class TestComPort:
    """COM Port."""

    com_port = ComPort()

    def test_set_com1_mode(self) -> None:
        # Set COM1 to RS232 mode.
        self.com_port.set_com1_mode(232)
        sleep(DELAY_TIME)
        # Set COM1 to RS422 mode.
        self.com_port.set_com1_mode(422)
        sleep(DELAY_TIME)
        # Set COM1 to RS485 mode.
        self.com_port.set_com1_mode(485)
        sleep(DELAY_TIME)

        # Fool Proof.
        with pytest.raises(TypeError):
            self.com_port.set_com1_mode(None)
        with pytest.raises(TypeError):
            self.com_port.set_com1_mode(94.87)
        with pytest.raises(TypeError):
            self.com_port.set_com1_mode("WTF")
        with pytest.raises(ValueError):
            self.com_port.set_com1_mode(666)

    def test_set_com1_termination(self) -> None:
        # Enable COM1 termination.
        self.com_port.set_com1_termination(True)
        sleep(DELAY_TIME)
        # Disable COM1 termination.
        self.com_port.set_com1_termination(False)
        sleep(DELAY_TIME)

        # Fool Proof.
        with pytest.raises(TypeError):
            self.com_port.set_com1_termination(None)
        with pytest.raises(TypeError):
            self.com_port.set_com1_termination(94.87)
        with pytest.raises(TypeError):
            self.com_port.set_com1_termination("WTF")
        with pytest.raises(TypeError):
            self.com_port.set_com1_termination(666)


class TestHWM:
    """Hardware Monitor."""

    hwm = HWM()

    def test_get_cpu_temp(self) -> None:
        # CPU-1 temperature.
        self.hwm.get_cpu_temp(1)
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
        with pytest.raises(PSP.PSPError) as e:
            self.hwm.get_sys_temp(2)
        assert str(e.value) == "LMB_HWM_GetSysTemp: 0xfffffffb: this functions is not support of this platform"

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
        with pytest.raises(PSP.PSPError) as e:
            self.hwm.get_12v()
        assert str(e.value) == "LMB_HWM_Get12V: 0xfffffffb: this functions is not support of this platform"

    def test_get_5v(self) -> None:
        self.hwm.get_5v()

    def test_get_3v3(self) -> None:
        self.hwm.get_3v3()

    def test_get_5vsb(self) -> None:
        with pytest.raises(PSP.PSPError) as e:
            self.hwm.get_5vsb()
        assert str(e.value) == "LMB_HWM_Get5Vsb: 0xfffffffb: this functions is not support of this platform"

    def test_get_3v3sb(self) -> None:
        with pytest.raises(PSP.PSPError) as e:
            self.hwm.get_3v3sb()
        assert str(e.value) == "LMB_HWM_Get3V3sb: 0xfffffffb: this functions is not support of this platform"

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

    def test_testhwm(self) -> None:
        self.hwm.testhwm()

    def test_get_all(self) -> None:
        assert self.hwm.get_all()


class TestGPS:
    """GPS."""

    gps = GPS()

    def test_search_port(self) -> None:
        with pytest.raises(AttributeError) as e:
            self.gps.search_port()
        assert "undefined symbol: LMB_GPS_SearchPort" in str(e.value)


class TestGSR:
    """G-Sensor."""

    gsr = GSR()

    def test_get_axis_data(self) -> None:
        with pytest.raises(AttributeError) as e:
            self.gsr.get_axis_data()
        assert "undefined symbol: LMB_GSR_GetAxisData" in str(e.value)

    def test_get_axis_offset(self) -> None:
        with pytest.raises(AttributeError) as e:
            self.gsr.get_axis_offset()
        assert "undefined symbol: LMB_GSR_GetAxisOffset" in str(e.value)

    def test_test(self) -> None:
        with pytest.raises(AttributeError) as e:
            self.gsr.test()
        assert "undefined symbol: LMB_GSR_GetAxisData" in str(e.value)
