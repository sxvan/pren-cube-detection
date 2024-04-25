import serial
from gpiozero import OutputDevice, InputDevice, DigitalInputDevice

from models.cube_position import CubePosition


class ControlUnitService:
    def __init__(self, ready_pin, start_pin, uart_port, baud_rate, encoding,
                 max_retries, retry_delay_ms,
                 start_character, crc8_poly):
        self.__ready_pin = ready_pin
        self.__start_pin = start_pin
        self.__encoding = encoding
        self.__max_retries = max_retries
        self.__start_character = start_character
        self.__crc8_poly = crc8_poly
        self.__uart_port = uart_port
        self.__baud_rate = baud_rate
        self.__retry_delay_ms = retry_delay_ms

    def send_ready_signal(self):
        with OutputDevice(self.__ready_pin) as ready_output:
            ready_output.on()

    def send_unready_signal(self):
        with OutputDevice(self.__ready_pin) as ready_output:
            ready_output.off()

    def wait_for_start_signal(self):
        with DigitalInputDevice(self.__start_pin) as start_input:
            start_input.wait_for_active()

    def wait_for_end_signal(self):
        with DigitalInputDevice(self.__start_pin) as start_input:
            start_input.wait_for_inactive()

    def send_cube_config(self, cube_config):
        data_string = self.__get_data_string(cube_config)
        return self.__send_msg(data_string)

    def __send_msg(self, msg):
        msg_bytes = msg.encode(self.__encoding)
        crc8 = self.__get_crc8(msg_bytes)
        data_bytes = self.__start_character.encode(self.__encoding) + msg_bytes + crc8

        with serial.Serial(self.__uart_port, self.__baud_rate, timeout=self.__retry_delay_ms / 1000) as ser:
            success = False
            number_of_tries = 0
            while not success and number_of_tries < self.__max_retries:
                number_of_tries = number_of_tries + 1
                ser.write(data_bytes)

                try:
                    received_byte = ser.read(1).decode(self.__encoding)
                    success = received_byte == "A"
                except serial.SerialTimeoutException:
                    print("Timeout reached. Trying again...")

        return success

    def __get_crc8(self, data):
        crc = data[0]
        data = bytearray(data)
        data.append(0)
        for byte in data[1:]:
            for i in range(8):  # Iterate over the bits in each byte
                if crc & 0x80:  # Check if MSB of CRC is set
                    crc <<= 1
                    crc |= 0x01 & (byte >> (7 - i))
                    crc ^= self.__crc8_poly
                else:
                    crc <<= 1
                    crc |= 0x01 & (byte >> (7 - i))
            crc &= 0xFF  # Ensure CRC is 8 bits long
        return bytes([crc])

    @staticmethod
    def __get_data_string(cube_dict):
        sorted_cube_values = [cube_dict[key] for key in sorted(cube_dict.keys(), key=lambda x: x.value)]

        data = ''
        for color in sorted_cube_values:
            if len(color) < 1:
                data += 'X'
            else:
                data += color[0].upper()

        return data + '0'
