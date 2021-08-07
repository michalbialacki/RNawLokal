import csv
import numpy as np
import OLS
import SortCommunicates
from time import sleep
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

with open('do_loop2.csv','r') as fp:
    passiveUnitCom= csv.reader(fp)
    for value in passiveUnitCom:
        tbSpl=value[0].split(';')
        if tbSpl[1]=='4':
#doot2
            passiveUnitXYs= np.array([[tbSpl[4],tbSpl[5]],[tbSpl[10],tbSpl[11]],[tbSpl[16],tbSpl[17]],[tbSpl[22],tbSpl[23]]])
            passiveXs=[]
            passiveYs=[]
            passiveUnitDist=np.array([tbSpl[7],tbSpl[13],tbSpl[19],tbSpl[25]])
            passiveUnitXYs,passiveUnitDist=SortCommunicates.XYsSort(passiveUnitXYs,passiveUnitDist)
            if len(passiveYs)<4 and len(passiveXs)<4:
                for index,value in enumerate(passiveUnitXYs):
                    passiveXs.append(value[0])
                    passiveYs.append(value[1])
            tagLoc=OLS.OLSAlgorythm(passiveUnitXYs,passiveUnitDist)
            comLog= 'Pozycja: {:.2f};{:.2f}'.format(tagLoc[0], tagLoc[1])
            print(comLog)
            sleep(0.1)
            print('==============')
            plt.plot(passiveXs,passiveYs,'bo')
            plt.plot(tagLoc[0],tagLoc[1],'r+')
            plt.pause(0.05)
            plt.clf()

        else:
            print('Tu jest za malo anchorow ')

plt.show()


