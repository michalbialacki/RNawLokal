import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from math import sqrt

# DF creation + clean
headers0 = 'DIST,ANCHS,AN0,ID0,X0,Y0,Z0,DIS0,AN1,ID1,X1,Y1,Z1,DIS1,AN2,ID2,X2,Y2,Z2,DIS2,AN3,ID3,X3,Y3,Z3,DIS3,POS,X,Y,Z,PREC'.split(
    ',')
headers1 = 'DIST,ANCHS,AN0,ID0,X0,Y0,Z0,DIS0,AN1,ID1,X1,Y1,Z1,DIS1,AN2,ID2,X2,Y2,Z2,DIS2,AN3,ID3,X3,Y3,Z3,DIS3,POS,X,Y,Z,PREC'.split(
    ',')
headers2 = 'DIST,ANCHS,AN0,ID0,X0,Y0,Z0,DIS0,AN1,ID1,X1,Y1,Z1,DIS1,AN2,ID2,X2,Y2,Z2,DIS2,AN3,ID3,X3,Y3,Z3,DIS3,POS,X,Y,Z,PREC'.split(
    ',')
headers3 = 'DIST,ANCHS,AN0,ID0,X0,Y0,Z0,DIS0,AN1,ID1,X1,Y1,Z1,DIS1,AN2,ID2,X2,Y2,Z2,DIS2,AN3,ID3,X3,Y3,Z3,DIS3,POS,X,Y,Z,PREC'.split(
    ',')
headers4 = 'DIST,ANCHS,AN0,ID0,X0,Y0,Z0,DIS0,AN1,ID1,X1,Y1,Z1,DIS1,AN2,ID2,X2,Y2,Z2,DIS2,AN3,ID3,X3,Y3,Z3,DIS3,POS,X,Y,Z,PREC'.split(
    ',')

noise = np.random.normal(0, 0.1, 1200)

first_meas_df = pd.read_csv('1stMeas.log', names=headers0, on_bad_lines='skip')
snd_meas_df = pd.read_csv('2ndMeas.log', names=headers1, on_bad_lines='skip')
trd_meas_df = pd.read_csv('3rdMeas.log', names=headers2, on_bad_lines='skip')
frth_meas_df = pd.read_csv('4thMeas.log', names=headers3[:-5], on_bad_lines='skip')
fith_meas_df = pd.read_csv('5thMeas.log', names=headers4, on_bad_lines='skip')

first_meas_df = first_meas_df[first_meas_df['POS'].notna()]
snd_meas_df = snd_meas_df[snd_meas_df['POS'].notna()]
trd_meas_df = trd_meas_df[trd_meas_df['POS'].notna()]
frth_meas_df = frth_meas_df[frth_meas_df['DIS3'].notna()]
fith_meas_df = fith_meas_df[fith_meas_df['POS'].notna()]

first_meas_df.drop(['DIST', 'ANCHS', 'AN0', 'ID0', 'AN1', 'ID1', 'AN2', 'ID2', 'AN3', 'ID3', 'POS', 'PREC', 'Z'],
                   axis=1, inplace=True)  # (0.75;0.95)
snd_meas_df.drop(['DIST', 'ANCHS', 'AN0', 'ID0', 'AN1', 'ID1', 'AN2', 'ID2', 'AN3', 'ID3', 'POS', 'PREC', 'Z'], axis=1,
                 inplace=True)  # (0.9;2.6)
trd_meas_df.drop(['DIST', 'ANCHS', 'AN0', 'ID0', 'AN1', 'ID1', 'AN2', 'ID2', 'AN3', 'ID3', 'POS', 'PREC', 'Z'], axis=1,
                 inplace=True)  # (1.45;0.45)
frth_meas_df.drop(['DIST', 'ANCHS', 'AN0', 'ID0', 'AN1', 'ID1', 'AN2', 'ID2', 'AN3', 'ID3'], axis=1, inplace=True)
fith_meas_df.drop(['DIST', 'ANCHS', 'AN0', 'ID0', 'AN1', 'ID1', 'AN2', 'ID2', 'AN3', 'ID3', 'POS', 'PREC', 'Z'], axis=1,
                  inplace=True)  # (1.6;2.0)

first_meas_df = first_meas_df[:1200]
snd_meas_df = snd_meas_df[:1200]
trd_meas_df = trd_meas_df[:1200]
frth_meas_df = frth_meas_df[:1200]
fith_meas_df = fith_meas_df[:1200]

for index in range(0, 1200):
    first_meas_df['X'] = 0.75
    first_meas_df['Y'] = 0.95
    snd_meas_df['X'] = 0.9
    snd_meas_df['Y'] = 2.6
    trd_meas_df['X'] = 1.45
    trd_meas_df['Y'] = 0.45
    fith_meas_df['X'] = 1.6
    fith_meas_df['Y'] = 2.0

dist_df = pd.concat([first_meas_df, snd_meas_df, trd_meas_df, fith_meas_df])

frth_meas_df = frth_meas_df[:360]

dist_df.to_csv("dist_df.csv")

# tu mam problem z wyrzuceniem wiersza, rozwiazanie tymczasowe bo trzeba wyrzucic zly wiersz
dist_df = pd.read_csv('dist_df.csv')
dist_df = dist_df.iloc[:, 1:]
dist_df.drop([3657], axis=0, inplace=True)

# nauka modeli
# X
dist_frame = dist_df[['DIS0', 'DIS1', 'DIS2', 'DIS3']]
X_trainX, X_testX, y_trainX, y_testX = train_test_split(dist_frame, dist_df['X'], test_size=0.3, random_state=101)
scaler = StandardScaler()  # skalowanie data setow
train_scaledX = scaler.fit_transform(X_trainX)
tested_scalerX = scaler.fit_transform(X_testX)
model = KNeighborsRegressor()
model.fit(train_scaledX, y_trainX)
predX = model.predict(tested_scalerX)

checkResult_df = frth_meas_df[['DIS0', 'DIS1', 'DIS2', 'DIS3']]
frth_X_scaled = scaler.fit_transform(checkResult_df)

pred_frthX = model.predict(frth_X_scaled)

mse = mean_squared_error(y_trainX, model.predict(train_scaledX))
mae = mean_absolute_error(y_trainX, model.predict(train_scaledX))
print(f"Dla X\nmse = {mse}; mae = {mae}; rmse = {sqrt(mse)}")

# Y
X_trainY, X_testY, y_trainY, y_testY = train_test_split(dist_frame, dist_df['Y'], test_size=0.3, random_state=101)
scalerY = StandardScaler()  # skalowanie data setow
train_scaledY = scalerY.fit_transform(X_trainY)
tested_scalerY = scalerY.fit_transform(X_testY)
model.fit(train_scaledY, y_trainY)
predY = model.predict(tested_scalerY)

pred_frthY = model.predict(frth_X_scaled)

mseY = mean_squared_error(y_trainY, model.predict(train_scaledY))
maeY = mean_absolute_error(y_trainY, model.predict(train_scaledY))
print(f"Dla Y\nmse = {mseY}; mae = {maeY}; rmse = {sqrt(mseY)}")

sns.kdeplot(x=pred_frthX, y=pred_frthY, fill=True)
plt.show()
