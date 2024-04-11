from time import sleep

from gpiozero import DigitalOutputDevice, DigitalInputDevice, InputDevice
import serial

if __name__ == '__main__':
    ready = DigitalOutputDevice(23)
    start = InputDevice(24)
    ser = serial.Serial("/dev/ttyS0", 19200, timeout=0.2)

    while True:
        # if start.value:
        #     ready.toggle()
        #     sleep(0.2)

        if ser.in_waiting > 0:
            data = ser.read(1)
            if data.decode("ascii") == "A":
                ready.on()
            elif data.decode("ascii") == "N":
                ready.off()
            ser.write(data)




    #
    # ser = serial.Serial("/dev/serial0", 19200, timeout=0.2)
    # while True:
    #     ser.write("ABC".encode("ascii"))
    #     sleep(1)




