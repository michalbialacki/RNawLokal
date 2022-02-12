import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import classification_report
import seaborn as sns

pd.set_option("display.max_rows", None, "display.max_columns", None)

"""
The code below represents getting the results
of ML approach to predict navigational data based
on range measurements from CSV file (log of DecaWave MDEK-1001)
"""



XY_df = pd.read_csv('OLSData.csv', sep=',')
headers = 'DIST,ANCHS,AN0,ID0,X0,Y0,Z0,DIS0,AN1,ID1,X1,Y1,Z1,DIS1,AN2,ID2,X2,Y2,Z2,DIS2,AN3,ID3,X3,Y3,Z3,DIS3,POS,X,Y,Z,PREC'.split(',')
dist_df = pd.read_csv('D:/01Kody/PythonKody/GitSucked/do_loop.csv',names=headers)
dist_df.drop(['DIST','ANCHS','AN0','ID0','AN1','ID1','AN2','ID2','AN3','ID3','POS'],axis=1,inplace=True)
dist_df.drop([195,109],axis=0,inplace=True)
# plt.figure(figsize=(12,5))
# sns.heatmap(dist_df.isnull(),cbar=False)
# plt.show()
# print(dist_df.info())


dist_frame = dist_df[['DIS0','DIS1','DIS2','DIS3']]
X_train, X_test, y_train, y_test = train_test_split(dist_frame,XY_df['X'],test_size=0.3,random_state=101)
lin_reg = LinearRegression()
lin_reg.fit(X_train,y_train)
with open('indexX.csv',mode='a+') as ind_csvX:
    ind_csvX.write(f'{X_test}')
pred = lin_reg.predict(X_test)
X_train, X_test, y_train, y_test = train_test_split(dist_frame,XY_df['Y'],test_size=0.3,random_state=101)
with open('indexY.csv',mode='a+') as ind_csvY:
    ind_csvY.write(f'{X_test}')
lin_reg.fit(X_train,y_train)
pred_y = lin_reg.predict(X_test)


