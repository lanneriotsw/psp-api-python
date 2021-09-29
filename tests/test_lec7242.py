import logging
from time import sleep

from lannerpsp import ComPort, HWM, PSP, RFM, SLED, SLEDGPS, SLEDLTE, SLEDLTEStress

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


def low_level_api() -> None:
    with PSP() as psp:
        # Set LTE Status LED to off (clear color).
        i_ret = psp.LMB_SLED_SetLteStateLED(0)
        if i_ret != PSP.ERR_Success:
            PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
            return
        # Set LTE Status LED to green blink.
        i_ret = psp.LMB_SLED_SetLteStateLED(4)
        if i_ret != PSP.ERR_Success:
            PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
            return
        logger.info("set lte led green blink")

        sleep(3.0)

        # Set LTE Status LED to off (clear color).
        i_ret = psp.LMB_SLED_SetLteStateLED(0)
        if i_ret != PSP.ERR_Success:
            PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
            return
        # Set LTE Status LED to red.
        i_ret = psp.LMB_SLED_SetLteStateLED(1)
        if i_ret != PSP.ERR_Success:
            PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
            return
        logger.info("set lte led red on")

        sleep(3.0)

        # Set LTE Status LED to off.
        i_ret = psp.LMB_SLED_SetLteStateLED(0)
        if i_ret != PSP.ERR_Success:
            PSP.show_error("LMB_SLED_SetLteStateLED", i_ret)
            return
        logger.info("set lte led off")


def high_level_api() -> None:
    t = 2.0

    print("System/Status LED:")
    SLED.green()
    sleep(t)
    SLED.red()
    sleep(t)
    SLED.off()
    sleep(t)

    print("GPS Status LED:")
    SLEDGPS.on()
    sleep(t)
    SLEDGPS.blink()
    sleep(t)
    SLEDGPS.off()
    sleep(t)

    print("LTE Status LED:")
    SLEDLTE.red()
    sleep(t)
    SLEDLTE.red_blink()
    sleep(t)
    SLEDLTE.off()
    sleep(t)
    SLEDLTE.green()
    sleep(t)
    SLEDLTE.green_blink()
    sleep(t)
    SLEDLTE.off()
    sleep(t)
    SLEDLTE.yellow()
    sleep(t)
    SLEDLTE.yellow_blink()
    sleep(t)
    SLEDLTE.off()
    sleep(t)

    print("LTE Stress LED:")
    SLEDLTEStress.set_strength(90)
    sleep(t)
    SLEDLTEStress.set_strength(78)
    sleep(t)
    SLEDLTEStress.set_strength(66)
    sleep(t)
    SLEDLTEStress.set_strength(54)
    sleep(t)
    SLEDLTEStress.set_strength(42)
    sleep(t)
    SLEDLTEStress.set_strength(30)
    sleep(t)
    SLEDLTEStress.set_strength(18)
    sleep(t)
    SLEDLTEStress.set_strength(6)
    sleep(t)
    SLEDLTEStress.off()
    sleep(t)

    print("Radio Frequency Module:")
    RFM.get_sim()
    RFM.set_sim(0)
    RFM.get_sim()
    sleep(t)
    RFM.set_sim(1)
    RFM.get_sim()
    sleep(t)
    RFM.set_sim(2)
    RFM.get_sim()
    sleep(t)
    RFM.set_sim(3)
    RFM.get_sim()
    sleep(t)
    RFM.get_module()
    RFM.set_module(0)
    RFM.get_module()
    sleep(t)
    RFM.set_module(1)
    RFM.get_module()
    sleep(t)
    RFM.set_module(2)
    RFM.get_module()
    sleep(t)
    RFM.set_module(3)
    RFM.get_module()
    sleep(t)

    print("COM Port:")
    ComPort.set_com1_mode(232)
    sleep(t)
    ComPort.set_com1_mode(422)
    sleep(t)
    ComPort.set_com1_mode(485)
    sleep(t)
    ComPort.set_com1_mode(123)
    sleep(t)
    ComPort.set_com1_termination(True)
    sleep(t)
    ComPort.set_com1_termination(False)
    sleep(t)

    print("Hardware Monitor:")
    HWM.get_cpu_temp(1)
    HWM.get_cpu_temp(2)
    HWM.get_sys_temp(1)
    HWM.get_sys_temp(2)
    HWM.get_vcore(1)
    HWM.get_vcore(2)
    HWM.get_12v()
    HWM.get_5v()
    HWM.get_3v3()
    HWM.get_5vsb()
    HWM.get_3v3sb()
    HWM.get_vbat()
    HWM.get_power_supply(1)
    HWM.get_power_supply(2)
    sleep(t)


def run_tests() -> None:
    print("System/Status LED:")
    SLED.test()

    print("GPS Status LED:")
    SLEDGPS.test()

    print("LTE Status LED:")
    SLEDLTE.test()

    print("LTE Stress LED:")
    SLEDLTEStress.test()

    print("Hardware Monitor:")
    HWM.testhwm()


def main() -> None:
    print("[Low Level API]")
    low_level_api()

    print()

    print("[High Level API]")
    high_level_api()

    print()

    print("[Run tests]")
    run_tests()


if __name__ == '__main__':
    main()
