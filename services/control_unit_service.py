import time

import serial
from gpiozero import OutputDevice, InputDevice, DigitalInputDevice, DigitalOutputDevice, Button

from models.cube_position import CubePosition


class ControlUnitService:
    def __init__(self, ready_pin, start_pin, uart_port, baud_rate, encoding,
                 max_retries, retry_delay_ms,
                 start_character, crc8_poly):
        self._ready_pin = ready_pin
        self._start_pin = start_pin
        self._encoding = encoding
        self._max_retries = max_retries
        self._start_character = start_character
        self._crc8_poly = crc8_poly
        self._uart_port = uart_port
        self._baud_rate = baud_rate
        self._retry_delay_ms = retry_delay_ms
        self._ready_output = DigitalOutputDevice(self._ready_pin)
        self._start_input = DigitalInputDevice(self._start_pin)

    def send_ready_signal(self):
        self._ready_output.on()

    def send_unready_signal(self):
        self._ready_output.off()

    def wait_for_start_signal(self):
        self._start_input.wait_for_active()

    def wait_for_end_signal(self):
        self._start_input.wait_for_inactive()

    def send_cube_config(self, cube_config):
        data_string = self._get_data_string(cube_config)
        return self.__send_msg(data_string)

    def __send_msg(self, msg):
        msg_bytes = msg.encode(self._encoding)
        crc8 = self._get_crc8(msg_bytes)
        data_bytes = self._start_character.encode(self._encoding) + msg_bytes + crc8

        with serial.Serial(self._uart_port, self._baud_rate, timeout=self._retry_delay_ms / 1000) as ser:
            success = False
            number_of_tries = 0
            while not success and number_of_tries < self._max_retries:
                number_of_tries = number_of_tries + 1
                ser.write(data_bytes)

                try:
                    received_byte = ser.read(1).decode(self._encoding)
                    success = received_byte == "A"
                except serial.SerialTimeoutException:
                    print("Timeout reached. Trying again...")

        return success

    def _get_crc8(self, data):
        crc = data[0]
        data = bytearray(data)
        data.append(0)
        for byte in data[1:]:
            for i in range(8):
                if crc & 0x80:
                    crc <<= 1
                    crc |= 0x01 & (byte >> (7 - i))
                    crc ^= self._crc8_poly
                else:
                    crc <<= 1
                    crc |= 0x01 & (byte >> (7 - i))
            crc &= 0xFF
        return bytes([crc])

    @staticmethod
    def _get_data_string(cube_dict):
        sorted_cube_values = [cube_dict[key] for key in sorted(cube_dict.keys(), key=lambda x: x.value)]

        data = ''
        for color in sorted_cube_values:
            if len(color) < 1:
                data += 'X'
            else:
                data += color[0].upper()

        return data + '0'
