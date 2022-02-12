import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df_ML = pd.read_csv('MLResults.csv',names=['MLX','MLY'])
df_OLS = pd.read_csv('OLSData.csv')
df_OLS = df_OLS.drop(df_OLS.index[64:])

coor_df = pd.concat([df_ML,df_OLS],axis=1)

sns.jointplot(x='MLX',y='MLY',data=coor_df, kind = 'hex')
sns.jointplot(x='X',y='Y',data=coor_df,kind = 'hex')
plt.show()