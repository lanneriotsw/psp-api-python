import logging
from time import sleep

from lannerpsp import GPS, GSR, HWM, PSP

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


def low_level_api() -> None:
    with PSP() as psp:
        pass


def high_level_api() -> None:
    t = 2.0

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

    print("GPS:")
    GPS.search_port()
    sleep(t)

    print("G-Sensor:")
    GSR.get_data()
    GSR.get_offset()
    sleep(t)


def run_tests() -> None:
    print("Hardware Monitor:")
    HWM.testhwm()

    print("G-Sensor:")
    GSR.test()


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
