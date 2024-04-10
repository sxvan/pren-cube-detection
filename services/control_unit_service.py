import serial
from gpiozero import DigitalInputDevice, DigitalOutputDevice

from models.cube_position import CubePosition


class ControlUnitService:
    def __init__(self, ready_pin: DigitalOutputDevice, start_pin: DigitalInputDevice, uart_port, baud_rate, encoding,
                 max_retries, retry_delay_ms,
                 start_character, crc8_poly):
        self.__ready_pin = ready_pin
        self.__start_pin = start_pin
        self.__uart_port = uart_port
        self.__baud_rate = baud_rate
        self.__encoding = encoding
        self.__max_retries = max_retries
        self.__retry_delay_ms = retry_delay_ms
        self.__start_character = start_character
        self.__crc8_poly = crc8_poly

    def send_ready_signal(self):
        self.__ready_pin.on()

    def send_unready_signal(self):
        self.__ready_pin.off()

    def wait_for_start_signal(self):
        self.__start_pin.wait_for_active()

    def wait_for_end_signal(self):
        self.__start_pin.wait_for_inactive()

    def send_cube_config(self, orientation, cube_config: (CubePosition, str)):

        ser = serial.Serial(self.__uart_port, self.__baud_rate, timeout=self.__retry_delay_ms * 1000)
        data = self.__get_data_string(cube_config)
        data = self.__start_character + data
        data_bytes = data.encode(self.__encoding)
        crc = self.__get_crc8(data_bytes)
        data_bytes += bytes([crc])

        tries = 0
        success = False

        while tries < self.__max_retries and not success:
            tries = tries + 1
            ser.write(data_bytes)

            received_data = ser.readline().decode(self.__encoding).strip()

            if received_data == "A":
                success = True

    def __get_crc8(self, data):
        crc = 0
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc >> 1) ^ self.__crc8_poly
                else:
                    crc <<= 1
                crc &= 0xFF

        return crc

    def __get_data_string(self, cube_dict):
        sorted_cube_values = [cube_dict[key] for key in sorted(cube_dict.keys(), key=lambda x: x.value)] # orientation missing

        data = ''
        for color in sorted_cube_values:
            data += color[0].upper()

        return data
