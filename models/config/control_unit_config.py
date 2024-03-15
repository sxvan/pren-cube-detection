from models.config.uart_config import UartConfig


class ControlUnitConfig:
    def __init__(self, ready_pin, start_pin, uart):
        self.ready_pin = ready_pin
        self.start_pin = start_pin
        self.uart = UartConfig(**uart)
