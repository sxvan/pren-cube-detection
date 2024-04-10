class UartConfig:
    def __init__(self, port, baud_rate, encoding, max_retries, retry_delay_ms, start_character, crc8_poly,
                 ack_character, not_ack_character):
        self.port = port
        self.baud_rate = baud_rate
        self.encoding = encoding
        self.max_retries = max_retries
        self.retry_delay_ms = retry_delay_ms
        self.start_character = start_character
        self.crc8_poly = crc8_poly
        self.ack_character = ack_character
        self.not_ack_character = not_ack_character
