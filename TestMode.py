import csv
import numpy as np

import USB_comm
import UserTag
import SortCommunicates
from time import sleep
from matplotlib import pyplot as plt
import Firebase_Communication
from matplotlib.animation import FuncAnimation


class CommunicationSource:
    def __init__(self, option):
        self.option = option
        if self.option == 'csv':
            self.try_method()
        else:
            self.serial_port_comm()

    def try_method(self):
        with open('do_loop2.csv','r') as fp:
            passive_unit_com = csv.reader(fp)
            for value in passive_unit_com:
                try:
                    tb_spl = value[0].split(';')
                except:
                    print('Błędne odczytanie paczki, transmisja zakłócona')
                else:
                    if tb_spl[1] == '4':
                        passive_unit_xy = np.array(
                            [[tb_spl[4], tb_spl[5]], [tb_spl[10], tb_spl[11]], [tb_spl[16], tb_spl[17]], [tb_spl[22], tb_spl[23]]])
                        passive_xs = []
                        passive_ys = []
                        passive_unit_dist = np.array([tb_spl[7], tb_spl[13], tb_spl[19], tb_spl[25]])
                        passive_unit_xy, passive_unit_dist = SortCommunicates.XYsSort(passive_unit_xy, passive_unit_dist)
                        if len(passive_ys) < 4 and len(passive_xs) < 4:
                            for index, value in enumerate(passive_unit_xy):
                                passive_xs.append(value[0])
                                passive_ys.append(value[1])
                        user1 = UserTag.MobileTag(passive_unit_xy, passive_unit_dist)
                        user1.active_unit_pos = user1.OLSAlgorythm()
                        print(user1)
                        Firebase_Communication.update_firebase(user1.active_unit_pos[0], user1.active_unit_pos[1])
                        print('==============')
                        plt.plot(passive_xs, passive_ys, 'bo')
                        plt.plot(user1.active_unit_pos[0], user1.active_unit_pos[1], 'r+')
                        plt.pause(0.01)
                        plt.clf()

    def from_csv(self):
        with open('do_loop2.csv', 'r') as fp:
            passive_unit_com = csv.reader(fp)
            for value in passive_unit_com:
                tb_spl = value[0].split(';')
                if tb_spl[1] == '4':
                    passive_unit_xy = np.array(
                        [[tb_spl[4], tb_spl[5]], [tb_spl[10], tb_spl[11]], [tb_spl[16], tb_spl[17]], [tb_spl[22], tb_spl[23]]])
                    passive_xs = []
                    passive_ys = []
                    passive_unit_dist = np.array([tb_spl[7], tb_spl[13], tb_spl[19], tb_spl[25]])
                    passive_unit_xy, passive_unit_dist = SortCommunicates.XYsSort(passive_unit_xy, passive_unit_dist)
                    if len(passive_ys) < 4 and len(passive_xs) < 4:
                        for index, value in enumerate(passive_unit_xy):
                            passive_xs.append(value[0])
                            passive_ys.append(value[1])
                    user1 = UserTag.MobileTag(passive_unit_xy, passive_unit_dist)
                    user1.active_unit_pos = user1.OLSAlgorythm()
                    print(user1)
                    Firebase_Communication.update_firebase(user1.active_unit_pos[0], user1.active_unit_pos[1])
                    print('==============')
                    plt.plot(passive_xs, passive_ys, 'bo')
                    plt.plot(user1.active_unit_pos[0], user1.active_unit_pos[1], 'r+')
                    plt.pause(0.01)
                    plt.clf()

                else:
                    print('Tu jest za malo anchorow ')

        plt.show()

    def serial_port_comm(self):
        user_tag = USB_comm.MobileUnit()
        user_tag.check()
        while True:
            passive_unit_com = str(user_tag.check())
            tb_spl = passive_unit_com[2:len(passive_unit_com)-5].split(',')
            if tb_spl[1] == '4':
                passive_unit_xy = np.array(
                    [[tb_spl[4], tb_spl[5]], [tb_spl[10], tb_spl[11]], [tb_spl[16], tb_spl[17]], [tb_spl[22], tb_spl[23]]])
                passive_xs = []
                passive_ys = []
                passive_unit_dist = np.array([tb_spl[7], tb_spl[13], tb_spl[19], tb_spl[25]])
                passive_unit_xy, passive_unit_dist = SortCommunicates.XYsSort(passive_unit_xy, passive_unit_dist)
                if len(passive_ys) < 4 and len(passive_xs) < 4:
                    for index, value in enumerate(passive_unit_xy):
                        passive_xs.append(value[0])
                        passive_ys.append(value[1])
                user1 = UserTag.MobileTag(passive_unit_xy, passive_unit_dist)
                user1.active_unit_pos = user1.OLSAlgorythm()
                print(user1)
                Firebase_Communication.update_firebase(user1.active_unit_pos[0], user1.active_unit_pos[1])
                print('==============')
