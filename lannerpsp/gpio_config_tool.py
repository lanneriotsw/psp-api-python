import logging

from portio import inb, ioperm, outb

from .exc import PSPInvalid
from .utils import is_root

logger = logging.getLogger(__name__)


class GPIOConfigTool:
    """
    GPIO config tool for LEC-7242.
    """

    SIO_UART5_DEVICE = 0x14
    SIO_UART_EN = 0x30

    SIO_GPIO_DEVICE = 0x06
    SIO_GPIO_EN = 0x30
    REG_GPIO0_IRQ_SEL = 0x70
    REG_GPIO_IRQ_EN = 0x7E
    REG_GPIO_IRQ_MODE = 0x7F

    REG_GPIO0_OUT_EN = 0xF0
    REG_GPIO0_OUT_DATA = 0xF1
    REG_GPIO0_PIN_STAT = 0xF2
    REG_GPIO0_DRIVE = 0xF3
    REG_GPIO0_SMI_EN = 0xF8
    REG_GPIO0_SMI_STATUS = 0xF9

    REG_GPIO1_OUT_EN = 0xE0
    REG_GPIO1_OUT_DATA = 0xE1
    REG_GPIO1_PIN_STAT = 0xE2
    REG_GPIO1_DRIVE = 0xE3

    REG_GPIO2_OUT_EN = 0xD0
    REG_GPIO2_OUT_DATA = 0xD1
    REG_GPIO2_PIN_STAT = 0xD2
    REG_GPIO2_DRIVE = 0xD3

    SIO_INDEX = 0x2e
    SIO_DATA = 0x2f

    def __init__(self):
        pass

    def set_com1_mode(self, mode: int) -> None:
        """
        Set COM1 mode to RS-232, RS-422 or RS-485.

        Example:

        .. code-block:: pycon

            >>> GPIOConfigTool().set_com1_mode(232)

        :param int mode: 232/422/485
        :raises PermissionError: if not running as root user
        :raises TypeError: The input parameters type error.
        :raises PSPInvalid: The input parameter is out of range.
        """
        # Check permission.
        if not is_root():
            raise PermissionError("Please uses root user !!!")
        # Check type.
        if not isinstance(mode, int):
            raise TypeError("'mode' type must be int")
        # Set mode.
        if mode == 232:
            self._com3_switch_mode(1)
        elif mode == 422:
            self._com3_switch_mode(3)
        elif mode == 485:
            self._com3_switch_mode(2)
        else:
            raise PSPInvalid("'mode' value must be 232 or 422 or 485")
        logger.debug(f"set com1 mode {mode}")

    def set_com1_termination(self, enable: bool) -> None:
        """
        Set COM1 RS-422/RS-485 termination.

        Example:

        .. code-block:: pycon

            >>> GPIOConfigTool().set_com1_termination(True)

        :param bool enable: ``True`` = enable, ``False`` = disable
        :raises PermissionError: if not running as root user
        :raises TypeError: The input parameters type error.
        """
        # Check permission.
        if not is_root():
            raise PermissionError("Please uses root user !!!")
        # Check type.
        if not isinstance(enable, bool):
            raise TypeError("'enable' type must be bool")
        # Set termination.
        if enable:
            self._com3_term_ctrl(1)
        else:
            self._com3_term_ctrl(0)
        logger.debug(f"set com1 termination {enable}")

    def _sio_unlock(self) -> None:
        ioperm(self.SIO_INDEX, 2, 1)
        outb(0x87, self.SIO_INDEX)
        outb(0x87, self.SIO_INDEX)

    def _sio_lock(self) -> None:
        outb(0xaa, self.SIO_INDEX)
        ioperm(self.SIO_INDEX, 2, 0)

    def _com3_switch_mode(self, mode: int) -> None:
        """
        mode 0: loop back
        mode 1: rs232
        mode 2: rs485
        mode 3: rs422
        """
        self._sio_unlock()

        # set multi function into gpio1x (13/16)
        outb(0x27, self.SIO_INDEX)
        xch = (inb(self.SIO_DATA) & 0xF2) | 0x04
        outb(0x27, self.SIO_INDEX)
        outb(xch, self.SIO_DATA)

        outb(0x29, self.SIO_INDEX)
        xch = inb(self.SIO_DATA) & 0xF9
        outb(0x29, self.SIO_INDEX)
        outb(xch, self.SIO_DATA)

        outb(0x2c, self.SIO_INDEX)
        xch = inb(self.SIO_DATA) | 0x48
        outb(0x2c, self.SIO_INDEX)
        outb(xch, self.SIO_DATA)

        # set multi function into gpio2x (20)
        outb(0x27, self.SIO_INDEX)
        xch = (inb(self.SIO_DATA) & 0xF2) | 0x08
        outb(0x27, self.SIO_INDEX)
        outb(xch, self.SIO_DATA)

        outb(0x29, self.SIO_INDEX)
        xch = inb(self.SIO_DATA) & 0xF7
        outb(0x29, self.SIO_INDEX)
        outb(xch, self.SIO_DATA)

        outb(0x2c, self.SIO_INDEX)
        xch = inb(self.SIO_DATA) | 0x01
        outb(0x2c, self.SIO_INDEX)
        outb(xch, self.SIO_DATA)
        # print("set multi function into gpio")

        # enable GPIO logical device
        outb(0x07, self.SIO_INDEX)
        outb(self.SIO_GPIO_DEVICE, self.SIO_DATA)

        # active GPIO logic device
        outb(self.SIO_GPIO_EN, self.SIO_INDEX)
        xch = inb(self.SIO_DATA) | 0x01
        outb(self.SIO_GPIO_EN, self.SIO_INDEX)
        outb(xch, self.SIO_DATA)  # active GPIO
        # print("active gpio function")

        outb(self.REG_GPIO1_OUT_EN, self.SIO_INDEX)
        xch = inb(self.SIO_DATA) | 0x48  # set gpio13/gpio16 output pins
        outb(xch, self.SIO_DATA)

        outb(self.REG_GPIO2_OUT_EN, self.SIO_INDEX)
        xch = inb(self.SIO_DATA) | 0x01  # set gpio20 output pins
        outb(xch, self.SIO_DATA)

        outb(self.REG_GPIO1_OUT_DATA, self.SIO_INDEX)  # GPIO1 Output Data Register
        xch = inb(self.SIO_DATA) & 0xBF  # clear gpio16 output pins
        xch |= (mode << 5)  # set gpio16 output value
        xch |= 0x08  # set gpio13 output 1
        outb(xch, self.SIO_DATA)

        outb(self.REG_GPIO2_OUT_DATA, self.SIO_INDEX)  # GPIO2 Output Data Register
        xch = inb(self.SIO_DATA) & 0xFE  # clear gpio20 output pins
        xch |= mode  # set gpio20 output value
        outb(xch, self.SIO_DATA)

        self._sio_lock()

    def _com3_term_ctrl(self, on_off: int) -> None:
        self._sio_unlock()

        # enable GPIO logical device
        outb(0x07, self.SIO_INDEX)
        outb(self.SIO_GPIO_DEVICE, self.SIO_DATA)

        outb(self.REG_GPIO1_OUT_DATA, self.SIO_INDEX)  # GPIO1 Output Data Register
        xch = inb(self.SIO_DATA) & 0xF7  # clear gpio13 output pins
        if on_off:
            xch |= 0x08  # set gpio13 output pins, enable term
        outb(xch, self.SIO_DATA)

        self._sio_lock()
