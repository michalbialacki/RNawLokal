import serial
from time import sleep


class MobileUnit:
    ser = ''

    def __init__(self, com='COM17', baudrate=115200):
        self.com = com
        self.baudrate = baudrate
        self.ser = serial.Serial(self.com, self.baudrate)

    def check(self):
        self.ser.open()
        self.ser.write(chr(13))
        self.ser.write(chr(13))
        print(self.ser.readline())
        self.ser.close()

    def start_comm(self):
        self.ser.open()
        self.ser.write(chr(13))
        self.ser.write(chr(13))
        sleep(0.05)
        self.ser.write('lec')

    def get_lines(self):
        return self.ser.readline()

    def kill_com(self):
        self.ser.close()


if __name__ == '__main__':
    unit = MobileUnit().check()
