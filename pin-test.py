from time import sleep

from gpiozero import DigitalOutputDevice
import serial

if __name__ == '__main__':
    pin1 = DigitalOutputDevice(23)

    while True:
        pin1.toggle()
        sleep(0.2)

