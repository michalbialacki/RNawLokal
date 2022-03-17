import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import confusion_matrix,classification_report
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import cProfile
import pstats

with cProfile.Profile() as pr:
    headers = 'DIST,ANCHS,AN0,ID0,X0,Y0,Z0,DIS0,AN1,ID1,X1,Y1,Z1,DIS1,AN2,ID2,X2,Y2,Z2,DIS2,AN3,ID3,X3,Y3,Z3,DIS3,POS,X,Y,Z,PREC'.split(',')
    dist_df = pd.read_csv('D:/01Kody/PythonKody/GitSucked/do_loop.csv',names=headers)
    dist_df.drop(['DIST','ANCHS','AN0','ID0','AN1','ID1','AN2','ID2','AN3','ID3','POS'],axis=1,inplace=True)
    dist_df.drop([195,109,110],axis=0,inplace=True) #110 damy jako sprawdzenie
    df_OLS = pd.read_csv('OLSData.csv')
    df_OLS = df_OLS.drop(df_OLS.index[64:])
    X_sig = []
    Y_sig = []
    noise = np.random.normal(0,0.1,212)
    for index in range(0,212):
        X_sig.append(0.65+noise[index])
        Y_sig.append(-0.45+noise[index])

    dist_df['Xrand'] = X_sig
    dist_df['Yrand'] = Y_sig

    dist_frame = dist_df[['DIS0','DIS1','DIS2','DIS3']]
    X_train, X_test, y_train, y_test = train_test_split(dist_frame,dist_df['Xrand'],test_size=0.3,random_state=101)
    lin_reg = LinearRegression()
    lin_reg.fit(X_train,y_train)
    pred_Xrand = lin_reg.predict(X_test)
    with open('D:/01Kody/PythonKody/GitSucked/MLTest/indexXrand.csv',mode='a+') as ind_csvXrand:
        for index in range(0,len(pred_Xrand)):
            ind_csvXrand.write(f'{pred_Xrand[index]}\n')
    X_train, X_test, y_train, y_test = train_test_split(dist_frame,dist_df['Yrand'],test_size=0.3,random_state=101)
    lin_reg.fit(X_train,y_train)
    pred_Yrand = lin_reg.predict(X_test)
    with open('D:/01Kody/PythonKody/GitSucked/MLTest/indexYrand.csv',mode='a+') as ind_csvYrand:
        for index in range(0,len(pred_Yrand)):
            ind_csvYrand.write(f'{pred_Yrand[index]}\n')


    MLRand_df = pd.DataFrame()
    MLRand_df['XMLPred'] = pred_Xrand
    MLRand_df['YMLPred'] = pred_Yrand
    coor_df = pd.concat([MLRand_df,df_OLS],axis=1)
    print(coor_df.describe())
    sns.jointplot(x='XMLPred',y='YMLPred',data=coor_df, kind = 'hex')
    plt.plot(0.65,-0.45,'r*')
    sns.jointplot(x='X',y='Y',data=coor_df,kind = 'hex')
    plt.plot(0.65,-0.45,'r*')
    plt.show()
# stats = pstats.Stats(pr)
# stats.sort_stats(pstats.SortKey.TIME)
# stats.dump_stats(filename='MLTestProfile.prof')
