import struct

import serial
from time import sleep


class MobileUnit:
    ser = ''

    def __init__(self, com='COM7', baudrate=115200):
        self.com = com
        self.baudrate = baudrate
        self.ser = serial.Serial(self.com, self.baudrate)

    def check(self):
        # print(self.ser.readline())
        return self.ser.readline()

    def start_comm(self):
        #self.ser.open()
        self.ser.write(str.encode(chr(13)))
        self.ser.write(str.encode(chr(13)))
        sleep(0.01)
        self.ser.write('lec')

    def get_line(self):
        return self.ser.readline()


    def kill_com(self):
        self.ser.close()


if __name__ == '__main__':
    while True:
        unit = MobileUnit().check()
        print(str(unit[:len(unit)-2]))


