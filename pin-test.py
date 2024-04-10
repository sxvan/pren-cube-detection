from gpiozero import DigitalOutputDevice
import serial

if __name__ == '__main__':
    pin1 = DigitalOutputDevice(17)
    pin2 = DigitalOutputDevice(11)
    pin3 = DigitalOutputDevice(13)

    pin1.on()
    pin2.on()

    print(pin1.is_active)
    print(pin2.is_active)
    print(pin3.is_active)

    ser = serial.Serial('/dev/serial0', 19200)
    msg = "Hello World!".encode('utf-8')
    ser.write(msg)

