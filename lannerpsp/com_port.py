import logging
import subprocess

logger = logging.getLogger(__name__)


class ComPort:
    """
    COM Port.

    tool/gpio_config_tool.c
    """

    _gpio_config_tool_path = "/opt/lanner/psp/tool/config_tool"

    @classmethod
    def set_com1_mode(cls, mode: int) -> None:
        """Set com1 mode.

        :param mode: 232/422/485
        """
        result = subprocess.check_output(
            [cls._gpio_config_tool_path, "-com1", f"-{mode}"]
        ).decode(encoding="utf-8").strip()
        if result == "set muti function into gpio":
            logger.info(f"set com1 mode {mode}")
        else:
            logger.error("set com1 mode failure")

    @classmethod
    def set_com1_termination(cls, enable: bool) -> None:
        """Enable/Disable com1 termination.

        :param enable: True = enable, False = disable
        """
        if enable:
            subprocess.check_output(
                [cls._gpio_config_tool_path, "-com1", "-termon"]
            )
            logger.info("enable com1 termination")
        else:
            subprocess.check_output(
                [cls._gpio_config_tool_path, "-com1", "-termoff"]
            )
            logger.info("disable com1 termination")
