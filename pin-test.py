from time import sleep

from gpiozero import DigitalOutputDevice, DigitalInputDevice, InputDevice
import serial

if __name__ == '__main__':
    ready = DigitalOutputDevice(23)
    start = InputDevice(24)
    ser = serial.Serial("/dev/ttyUSB0", 19200, timeout=0.2)

    while True:
        if start.value:
            ready.toggle()
            ser.write("@ABC".encode("ascii"))
        sleep(0.2)



    #
    # ser = serial.Serial("/dev/serial0", 19200, timeout=0.2)
    # while True:
    #     ser.write("ABC".encode("ascii"))
    #     sleep(1)




