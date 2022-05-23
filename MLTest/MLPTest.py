import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

import SortCommunicates

np.set_printoptions(precision=2)
headers0 = 'DIST,ANCHS,AN0,ID0,X0,Y0,Z0,DIS0,AN1,ID1,X1,Y1,Z1,DIS1,AN2,ID2,X2,Y2,Z2,DIS2,AN3,ID3,X3,Y3,Z3,DIS3,POS,X,' \
           'Y,Z,PREC'.split(
    ',')
headers1 = 'DIST,ANCHS,AN1,ID1,X1,Y1,Z1,DIS1,AN2,ID2,X2,Y2,Z2,DIS2,AN0,ID0,X0,Y0,Z0,DIS0,AN3,ID3,X3,Y3,Z3,DIS3,POS,X,Y,Z,PREC'.split(
    ',')
headers2 = 'DIST,ANCHS,AN3,ID3,X3,Y3,Z3,DIS3,AN2,ID2,X2,Y2,Z2,DIS2,AN0,ID0,X0,Y0,Z0,DIS0,AN1,ID1,X1,Y1,Z1,DIS1,POS,X,Y,Z,PREC'.split(
    ',')
headers5 = 'DIST,ANCHS,AN0,ID0,X0,Y0,Z0,DIS0,AN1,ID1,X1,Y1,Z1,DIS1,AN3,ID3,X3,Y3,Z3,DIS3,AN2,ID2,X2,Y2,Z2,DIS2,POS,X,Y,Z,PREC'.split(
    ',')
headersSORTED = 'DIST,ANCHS,AN0,ID0,X0,Y0,Z0,DIS0,AN1,ID1,X1,Y1,Z1,DIS1,AN2,ID2,X2,Y2,Z2,DIS2,AN3,ID3,X3,Y3,Z3,DIS3,POS,X,Y,Z,PREC'.split(
    ',')

meas_csv = pd.read_csv('D:/01Kody/PythonKody/GitSucked/logi/08042022/mob2.csv', names=headers0, on_bad_lines='skip')
dirty_indices = meas_csv.index[meas_csv["ANCHS"] < 4].tolist()


def createDF():
    noise = np.random.normal(0, 0.1, 1200)

    first_meas_df = pd.read_csv('D:/01Kody/PythonKody/GitSucked/logi/18052022/stacjo/1meas.csv', names=headers1,
                                on_bad_lines='skip')
    snd_meas_df = pd.read_csv('D:/01Kody/PythonKody/GitSucked/logi/18052022/stacjo/2meas.csv', names=headers2,
                              on_bad_lines='skip')
    trd_meas_df = pd.read_csv('D:/01Kody/PythonKody/GitSucked/logi/18052022/stacjo/3meas.csv', names=headers0,
                              on_bad_lines='skip')
    frth_meas_df = pd.read_csv('D:/01Kody/PythonKody/GitSucked/logi/18052022/stacjo/4meas.csv', names=headers0,
                               on_bad_lines='skip')
    fith_meas_df = pd.read_csv('D:/01Kody/PythonKody/GitSucked/logi/18052022/stacjo/5meas.csv', names=headers5,
                               on_bad_lines='skip')

    test_df = first_meas_df[headersSORTED]
    # sns.heatmap(fith_meas_df.isnull(),yticklabels=False,cbar=False,cmap='viridis') #sprawdzanie ktory wiersz nie jest pelny

    first_meas_df = first_meas_df[first_meas_df['POS'].notna()]
    snd_meas_df = snd_meas_df[snd_meas_df['POS'].notna()]
    trd_meas_df = trd_meas_df[trd_meas_df['POS'].notna()]
    frth_meas_df = frth_meas_df[frth_meas_df['DIS3'].notna()]
    fith_meas_df = fith_meas_df[fith_meas_df['POS'].notna()]

    first_meas_df.drop(
        ['DIST', 'ANCHS', 'AN0', 'Z0', 'ID0', 'AN1', 'Z1', 'ID1', 'AN2', 'Z2', 'ID2', 'AN3', 'ID3', 'POS', 'X', 'Y',
         'Z', 'PREC'],
        axis=1, inplace=True)  # (0.3;-0.15)
    snd_meas_df.drop(
        ['DIST', 'ANCHS', 'AN0', 'ID0', 'AN1', 'Z1', 'ID1', 'AN2', 'Z2', 'ID2', 'AN3', 'Z3', 'ID3', 'POS', 'X', 'Y',
         'Z', 'PREC'],
        axis=1,
        inplace=True)  # (0.0;-0.2)
    trd_meas_df.drop(
        ['DIST', 'ANCHS', 'AN0', 'Z0', 'ID0', 'AN1', 'Z1', 'ID1', 'AN2', 'Z2', 'ID2', 'AN3', 'Z3', 'ID3', 'POS', 'X',
         'Y', 'Z', 'PREC'],
        axis=1, inplace=True)  # (1.9;2.4)
    frth_meas_df.drop(
        ['DIST', 'ANCHS', 'AN0', 'Z0', 'ID0', 'AN1', 'Z1', 'ID1', 'AN2', 'Z2', 'ID2', 'AN3', 'Z3', 'ID3', 'X', 'Y',
         'Z', ], axis=1,
        inplace=True)  # (0.3;2,45)

    fith_meas_df.drop(
        ['DIST', 'ANCHS', 'AN0', 'Z0', 'ID0', 'AN1', 'Z1', 'ID1', 'AN2', 'Z2', 'ID2', 'AN3', 'Z3', 'ID3', 'POS', 'X',
         'Y', 'Z', 'PREC'],
        axis=1,
        inplace=True)  # (1.1;1.1)

    first_meas_df = first_meas_df[:550]  # wchodzi
    snd_meas_df = snd_meas_df[:550]  # wchodzi
    trd_meas_df = trd_meas_df[:550]
    frth_meas_df = frth_meas_df[:550]
    fith_meas_df = fith_meas_df[:550]  # wchodzi

    for index in range(0, 550):
        first_meas_df['X'] = 0.3
        first_meas_df['Y'] = -0.15
        snd_meas_df['X'] = 0.0
        snd_meas_df['Y'] = -0.2
        trd_meas_df['X'] = 1.9
        trd_meas_df['Y'] = 2.4
        frth_meas_df['X'] = 1.9
        frth_meas_df['Y'] = 2.45
        fith_meas_df['X'] = 1.1
        fith_meas_df['Y'] = 1.1

    dist_df = pd.concat([first_meas_df, snd_meas_df, trd_meas_df, frth_meas_df])
    dist_df.to_csv(index=False)
    return dist_df, fith_meas_df


def learnMLP(dist_df, test_df):
    # X
    dist_frame = dist_df[['DIS0', 'DIS1', 'DIS2', 'DIS3']]
    X_trainX, X_testX, y_trainX, y_testX = train_test_split(dist_frame, dist_df['X'], test_size=0.3)
    model = MLPRegressor(activation='tanh', solver='adam', )
    model.fit(X_trainX, y_trainX)
    predX = model.predict(X_testX)

    checkResult_df = test_df[['DIS0', 'DIS1', 'DIS2', 'DIS3']]
    pred_testX = model.predict(checkResult_df)
    for num in pred_testX:
        print(num)

    # Y
    X_trainY, X_testY, y_trainY, y_testY = train_test_split(dist_frame, dist_df['Y'], test_size=0.3)
    model.fit(X_trainY, y_trainY)
    predY = model.predict(X_testY)

    pred_testY = model.predict(checkResult_df)

    return pred_testX, pred_testY


def sortDF(dist_df=pd.DataFrame([])):
    dist_df.drop(['Z3', 'Z0'], axis=1, inplace=True)
    dist_df.round(2)
    dist_list = dist_df.values.tolist()
    temp_list = []
    for num in range(0, len(dist_list)):
        temp = []
        for index in range(0, len(dist_list[num])):
            temp.append(str(dist_list[num][index]))
        dist_list[num] = temp
    for comm in dist_list:
        passive_dists = [str(comm[2]), str(comm[5]), str(comm[8]), str(comm[11])]
        passive_xy = [[str(comm[0]), str(comm[1])], [str(comm[3]), str(comm[4])], [str(comm[6]), str(comm[7])],
                      [str(comm[9]), str(comm[10])]]
        passive_xy, passive_dists = SortCommunicates.XYsSort(passive_xy, passive_dists)
        temp_list.append(passive_dists)
    sorted_result = pd.DataFrame(data=temp_list, columns=['DIS0', 'DIS1', 'DIS2', 'DIS3'])
    new_df = dist_df[['X', 'Y']].copy()
    sorted_result['X'] = new_df['X'].tolist()
    sorted_result['Y'] = new_df['Y'].tolist()
    return sorted_result


def sortDFTest(dist_df=pd.DataFrame([])):
    dist_df.drop(['X', 'Y'], axis=1, inplace=True)
    dist_df.round(2)
    dist_list = dist_df.values.tolist()
    temp_list = []
    for num in range(0, len(dist_list)):
        temp = []
        for index in range(0, len(dist_list[num])):
            temp.append(str(dist_list[num][index]))
        dist_list[num] = temp
    for comm in dist_list:
        passive_dists = [str(comm[2]), str(comm[5]), str(comm[8]), str(comm[11])]
        passive_xy = [[str(comm[0]), str(comm[1])], [str(comm[3]), str(comm[4])], [str(comm[6]), str(comm[7])],
                      [str(comm[9]), str(comm[10])]]
        passive_xy, passive_dists = SortCommunicates.XYsSort(passive_xy, passive_dists)
        temp_list.append(passive_dists)
    sorted_result = pd.DataFrame(data=temp_list, columns=['DIS0', 'DIS1', 'DIS2', 'DIS3'])

    return sorted_result


if __name__ == '__main__':
    fit_df, test_df = createDF()
    fit_df = sortDF(fit_df)
    test_df = sortDFTest(test_df)
    pred_x, pred_y = learnMLP(fit_df, test_df)
    sns.jointplot(x=pred_x, y=pred_y, kind="hex", color="#4CB391")
    plt.show()
