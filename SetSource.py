import csv
import numpy as np
import USB_comm
import UserTag
import SortCommunicates
from matplotlib import pyplot as plt
import Firebase_Communication
import cProfile
import pstats


class CommunicationSource:


    def __init__(self, option):
        self.option = option
        if self.option == 'OLS':
            with cProfile.Profile() as pr:
                self.from_csvOLS()

            stats = pstats.Stats(pr)
            stats.sort_stats(pstats.SortKey.TIME)
            stats.dump_stats(filename='OLSProf.prof')
        elif self.option == 'EKF':
            with cProfile.Profile() as pr:
                self.from_csvEKF()

            stats = pstats.Stats(pr)
            stats.sort_stats(pstats.SortKey.TIME)
            stats.dump_stats(filename='profile_MastersEKF.prof')
        elif self.option =='EKF_COM':
            self.serial_port_commEKF()
        else:
            self.serial_port_comm()

    def from_csvOLS(self):
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
                        if 'Transmission error' in passive_unit_xy:
                            print(f'*****\n{passive_unit_xy}\n*****')
                        else:
                            if len(passive_ys) < 4 and len(passive_xs) < 4:
                                for index, value in enumerate(passive_unit_xy):
                                    passive_xs.append(value[0])
                                    passive_ys.append(value[1])
                            user1 = UserTag.MobileTag(passive_unit_xy, passive_unit_dist)
                            user1.active_unit_pos = user1.OLSAlgorythm()
                            print(user1)
                            # Firebase_Communication.update_firebase(user1.active_unit_pos[0], user1.active_unit_pos[1])
                            # with open('wyniki.csv',mode='a') as wyniki:
                            #     wyniki.writelines(f'{user1.active_unit_pos}')
                            print('==============')
                            plt.grid(True)
                            plt.plot(passive_xs, passive_ys, 'bo')
                            plt.plot(user1.active_unit_pos[0], user1.active_unit_pos[1], 'r+')
                            plt.pause(0.001)
                            plt.clf()
        plt.show()


    def from_csvEKF(self):
        with open('logi/08042022/mobilny.csv','r') as fp:
            passive_unit_com = csv.reader(fp)
            for value in passive_unit_com:
                try:
                    tb_spl = value
                except:
                    print('Błędne odczytanie paczki, transmisja zakłócona')
                else:
                    try:
                        tb_spl[1] == '4'
                        passive_unit_xy = np.array(
                            [[tb_spl[4], tb_spl[5]], [tb_spl[10], tb_spl[11]], [tb_spl[16], tb_spl[17]], [tb_spl[22], tb_spl[23]]])
                        passive_xs = []
                        passive_ys = []
                        passive_unit_dist = np.array([tb_spl[7], tb_spl[13], tb_spl[19], tb_spl[25]])
                        passive_unit_xy, passive_unit_dist = SortCommunicates.XYsSort(passive_unit_xy, passive_unit_dist)
                        if 'Transmission error' in passive_unit_xy:
                            print(f'*****\n{passive_unit_xy}\n*****')
                        else:
                            if len(passive_ys) < 4 and len(passive_xs) < 4:
                                for index, value in enumerate(passive_unit_xy):
                                    passive_xs.append(value[0])
                                    passive_ys.append(value[1])
                            user1 = UserTag.MobileTag(passive_unit_xy, passive_unit_dist)
                            user1.active_unit_pos = user1.EKFAlgorythm()
                            print(f'{user1.active_unit_pos[0]};{user1.active_unit_pos[2]}')
                            # Firebase_Communication.update_firebase(user1.active_unit_pos[0], user1.active_unit_pos[2])
                            print('==============')
                            plt.grid(True)
                            plt.xlim((-1*passive_xs[2], 2*passive_xs[2]))
                            plt.ylim((-1*passive_ys[2], 2*passive_ys[2]))
                            plt.plot(passive_xs, passive_ys, 'bo')
                            plt.plot(user1.active_unit_pos[0], user1.active_unit_pos[2], 'r+')
                            plt.pause(0.001)
                            plt.clf()
                    except IndexError:
                        "IndexError"
        plt.show()


    def serial_port_comm(self):
        user_tag = USB_comm.MobileUnit()
        user_tag.check()
        while True:
            passive_unit_com = str(user_tag.check())
            try:
                tb_spl = passive_unit_com[2:len(passive_unit_com)-5].split(',')
            except:
                print("Zakłócenie transmisji. Pobieram kolejną paczkę danych")
            else:
                if tb_spl[1] == '4':
                    try:
                        passive_unit_xy = np.array(
                            [[tb_spl[4], tb_spl[5]], [tb_spl[10], tb_spl[11]], [tb_spl[16], tb_spl[17]], [tb_spl[22], tb_spl[23]]])
                    except:
                        user_tag.kill_com()
                        self.serial_port_comm()
                    else:
                        passive_xs = []
                        passive_ys = []
                        try:
                            passive_unit_dist = np.array([tb_spl[7], tb_spl[13], tb_spl[19], tb_spl[25]])
                        except:
                            user_tag.kill_com()
                            self.serial_port_comm()
                        else:
                            passive_unit_xy, passive_unit_dist = SortCommunicates.XYsSort(passive_unit_xy, passive_unit_dist)
                            try:
                                if len(passive_ys) < 4 and len(passive_xs) < 4:
                                    for index, value in enumerate(passive_unit_xy):
                                        passive_xs.append(value[0])
                                        passive_ys.append(value[1])
                            except:
                                user_tag.kill_com()
                                self.serial_port_comm()
                            else:
                                user1 = UserTag.MobileTag(passive_unit_xy, passive_unit_dist)
                                user1.active_unit_pos = user1.OLSAlgorythm()
                                print(user1)
                                Firebase_Communication.update_firebase(user1.active_unit_pos[0], user1.active_unit_pos[1])
                                print('==============')
                                plt.grid(True)
                                plt.plot(passive_xs, passive_ys, 'bo')
                                plt.plot(user1.active_unit_pos[0], user1.active_unit_pos[1], 'r+')
                                plt.pause(0.001)
                                plt.clf()
        plt.show()

    def serial_port_commEKF(self):
        user_tag = USB_comm.MobileUnit()
        user_tag.check()
        while True:
            passive_unit_com = str(user_tag.check())
            try:
                tb_spl = passive_unit_com[2:len(passive_unit_com)-5].split(',')
            except:
                print("Zakłócenie transmisji. Pobieram kolejną paczkę danych")
            else:
                if tb_spl[1] == '4':
                    try:
                        passive_unit_xy = np.array(
                            [[tb_spl[4], tb_spl[5]], [tb_spl[10], tb_spl[11]], [tb_spl[16], tb_spl[17]], [tb_spl[22], tb_spl[23]]])
                    except:
                        user_tag.kill_com()
                        self.serial_port_comm()
                    else:
                        passive_xs = []
                        passive_ys = []
                        try:
                            passive_unit_dist = np.array([tb_spl[7], tb_spl[13], tb_spl[19], tb_spl[25]])
                        except:
                            user_tag.kill_com()
                            self.serial_port_comm()
                        else:
                            passive_unit_xy, passive_unit_dist = SortCommunicates.XYsSort(passive_unit_xy, passive_unit_dist)
                            try:
                                if len(passive_ys) < 4 and len(passive_xs) < 4:
                                    for index, value in enumerate(passive_unit_xy):
                                        passive_xs.append(value[0])
                                        passive_ys.append(value[1])
                            except:
                                user_tag.kill_com()
                                self.serial_port_comm()
                            else:
                                user1 = UserTag.MobileTag(passive_unit_xy, passive_unit_dist)
                                user1.EKF.set_anchors(np.array([[0, 0], [2.15, 0], [2.15, 3.0], [2.15, 3.0]]))
                                user1.active_unit_pos = user1.EKFAlgorythm()
                                print(f'{user1.active_unit_pos[0]};{user1.active_unit_pos[2]}')
                                # Firebase_Communication.update_firebase(user1.active_unit_pos[0], user1.active_unit_pos[2])
                                # with open('wyniki.csv',mode='a') as wyniki:
                                #     wyniki.writelines(f'{user1.active_unit_pos}')
                                print('==============')
                                plt.grid(True)
                                plt.plot(passive_xs, passive_ys, 'bo')
                                plt.plot(user1.active_unit_pos[0], user1.active_unit_pos[2], 'r+')
                                plt.pause(0.001)
                                plt.clf()
        plt.show()
