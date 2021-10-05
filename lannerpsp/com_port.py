import logging
import subprocess

from .lmbinc import PSP

logger = logging.getLogger(__name__)


class ComPort:
    """
    COM Port.

    tool/gpio_config_tool.c

    :param config_tool_path: path of config_tool binary file
    """

    def __init__(self, config_tool_path: str = "/opt/lanner/psp/tool/config_tool"):
        self._config_tool_path = config_tool_path

    def set_com1_mode(self, mode: int) -> None:
        """Set COM1 mode.

        :param mode: 232/422/485
        """
        # Check type.
        if not isinstance(mode, int):
            raise TypeError("'mode' type must be int")
        # Check value.
        if mode not in (232, 422, 485):
            raise ValueError("'mode' value must be 232 or 422 or 485")
        # Set mode.
        result = subprocess.check_output(
            [self._config_tool_path, "-com1", f"-{mode}"]
        ).decode(encoding="utf-8").strip()
        # Check result.
        if result != "set muti function into gpio":
            error_message = "set com1 mode failure"
            logger.error(error_message)
            raise PSP.PSPError(error_message)
        logger.info(f"set com1 mode {mode}")

    def set_com1_termination(self, enable: bool) -> None:
        """Enable/Disable COM1 termination.

        :param enable: True = enable, False = disable
        """
        # Check type.
        if not isinstance(enable, bool):
            raise TypeError("'enable' type must be bool")
        if enable:
            # Enable termination.
            subprocess.check_output(
                [self._config_tool_path, "-com1", "-termon"]
            )
            logger.info("enable com1 termination")
        else:
            # Disable termination.
            subprocess.check_output(
                [self._config_tool_path, "-com1", "-termoff"]
            )
            logger.info("disable com1 termination")
