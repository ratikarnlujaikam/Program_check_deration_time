# %%
import pandas as pd
import numpy as np
from tkinter import filedialog
import tkinter as tk
import pandas as pd
import os


# %%
Date='2023-03-27'
Line='3-14'
Model='LONGSP'
Startdate='2022-11-01'
finishDate='2023-03-24'

#%%
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    typ = [('txt file', '*.csv')]
    di = "../data/"
    file = filedialog.askopenfilename(filetypes=typ, initialdir=di)

    df = pd.read_csv(file)


# %%
datasets = df

# %%
datasets['Projection1']=pd.cut(datasets['Projection1'],bins=[-np.inf,0.4647,0.5664,np.inf],labels=['fail_low','pass','fail_high'])
datasets['Projection1'].replace('fail_low','fail',inplace=True)
datasets['Projection1'].replace('fail_high','fail',inplace=True)

# %%
datasets

# %%
from collections import Counter
print(Counter(datasets['Projection1']))

# %%
from imblearn.over_sampling import SMOTE
# over_sampling คือการทำค่า fail 1284 ให้เท่ากับค่า pass 271k เพื่อให้ data ในการ train เพิ่มมากขึ้น
from collections import Counter

k = 3
X = datasets.loc[:, datasets.columns != 'Projection1']
y = datasets.Projection1

# sampling_strategy=0.1 oversampling 10%
sm = SMOTE(sampling_strategy='minority', k_neighbors=k, random_state=100)
X_res, y_res = sm.fit_resample(X, y)

datasets = pd.concat([pd.DataFrame(X_res), pd.DataFrame(y_res)], axis=1)

# %%
from collections import Counter
print(Counter(datasets['Projection1']))

# %%
datasets

# %%
from pyarc import CBA, TransactionDB
from sklearn.model_selection import train_test_split 
from sklearn.metrics import classification_report

train, test = train_test_split(datasets, test_size=0.1)

txns_train = TransactionDB.from_DataFrame(train)
txns_test = TransactionDB.from_DataFrame(test)

cba = CBA (support = 0.07, confidence = 0.8, algorithm ='m1')
cba.fit(txns_train)

y_pred = cba.predict(txns_test)
y_test = test['Projection1']
print ((classification_report(y_test,y_pred)))


# %%
datasp =(classification_report(y_test,y_pred))

# %%
da=datasp.split("\n")

# %%
from pandas import DataFrame

data1 ={
'Date':Date,
'Line':Line,
'Model':Model,
'Details':[(datasp[63:67]),(datasp[117:121]),(datasp[168:176]),(datasp[221:230]),(datasp[272:284])
],
'Procision':[datasp[74:78],datasp[128:132],(''),datasp[128:132],datasp[237:241]
],
'recall':[datasp[84:88],datasp[138:142],(''),datasp[247:251],datasp[301:305]
],
'f1_score':[datasp[94:98],datasp[148:152],(datasp[203:207]),datasp[257:261],datasp[311:315]
],

'support':[datasp[103:108],datasp[157:162],datasp[209:217],datasp[265:271],datasp[319:325]
],
}
dff = pd.DataFrame(data1,columns=['Date','Line','Model','Details','Procision','recall','f1_score','support'])
print("displaying the dataframe with data as record")
print(dff)
print("-------------------------------Converting into csv file with a new a new file name ------------------------------------")
# df.to_csv("C:\\Users\\IT\\Desktop\\Date ML\\Accuracy ML\\LSP3-14 Accuracy.csv")
# df=pd.read_csv("C:\\Users\\IT\\Desktop\\Date ML\\Accuracy ML\\LSP3-14 Accuracy.csv")
# print(df)

# %%
dff

# %%
cba1 =cba.clf.rules

# %%
cba1

# %%
aa =" "
dd=[]
for  x in range(len(cba1)):
    aa += str (cba1[x]).replace("{","").replace("}","").replace("Projection1=","")
    dd=aa.split("CAR")
print(dd)

# %%
fid=[]
fid01=[]
Sup=[]
Conf=[]
for op in range(len(dd)):
    dat=(dd[op].split())
    fid+=(dat[0:1])
    fid01+=dat[2:3]
    Sup+=dat[4:5]
    Conf+=dat[6:7]


# %%
my_array=[]
ok =[]
i=0
while i < len(fid):
    my_array+= fid[i].split()
    ok +=[my_array[i]+','+'Null=Null'+','+'Null=Null'+','+'Null=Null'+','+'Null=Null']
    i=i+1

# %%
Sp=[]
KPIV1=[]
KPIV2=[]
KPIV3=[]
KPIV4=[]
for i in ok:
    Sp1=i.split(',')
    KPIV1+=[Sp1[0]]
    KPIV2+=[Sp1[1]]
    KPIV3+=[Sp1[2]]
    KPIV4+=[Sp1[3]]

KPIVOK=[KPIV1],[KPIV2],[KPIV3],[KPIV4]

# %%
dataok=[]
for i in range(len(KPIVOK)):
    dataok+=(KPIVOK[i])

# %%
sp1=[]
for i in (dataok[0]):
    sp1+=[(i.split('='))]

sp2=[]
for i in (dataok[1]):
    sp2+=[(i.split('='))]

sp3=[]
for i in (dataok[2]):
    sp3+=[(i.split('='))]

sp4=[]
for i in (dataok[3]):
    sp4+=[(i.split('='))]

# %%
Cl1=[]
for i in sp1:
    Cl1+=([i[0]])

Cl2=[]
for i in sp1:
    Cl2+=([i[1]])

Cl3=[]
for i in sp2:
    Cl3+=([i[0]])

Cl4=[]
for i in sp2:
    Cl4+=([i[1]])

Cl5=[]
for i in sp3:
    Cl5+=([i[0]])

Cl6=[]
for i in sp3:
    Cl6+=([i[1]])

# %%
for i in Cl5:
    CL05=i.replace("Null", "-")
    print(CL05)


# %%
betweenDate = Startdate+' - '+finishDate

# %%
indexok=[]
for i in range(len(my_array)):
    indexok+=([i+1])

# %%
import pandas as pd
data ={
'Date':Date,
'betweenDate':betweenDate,
'Model':Model,
'Line':Line,
'Rangeindex':indexok,
'Cl1':Cl1,
'Cl2':Cl2,
'Cl3':Cl3,
'Cl4':Cl4,
'Cl5':Cl5,
'Cl6':Cl6,
'Projection':fid01,
'Support':Sup,
'Confidence':Conf,}
df = pd.DataFrame(data)


df.loc[df['Cl1'] == 'Datum_probe', 'Datum_probe'] = df['Cl2']
df.loc[df['Cl3'] == 'Datum_probe', 'Datum_probe'] = df['Cl4']
df.loc[df['Cl5'] == 'Datum_probe', 'Datum_probe'] = df['Cl6']

df.loc[df['Cl1'] == 'Max_force', 'Max_force'] = df['Cl2']
df.loc[df['Cl3'] == 'Max_force', 'Max_force'] = df['Cl4']
df.loc[df['Cl5'] == 'Max_force', 'Max_force'] = df['Cl6']

df.loc[df['Cl1'] == 'Set_Dim_A', 'Set_Dim_A'] = df['Cl2']
df.loc[df['Cl3'] == 'Set_Dim_A', 'Set_Dim_A'] = df['Cl4']
df.loc[df['Cl5'] == 'Set_Dim_A', 'Set_Dim_A'] = df['Cl6']

df.loc[df['Cl1'] == 'Set_Dim_B', 'Set_Dim_B'] = df['Cl2']
df.loc[df['Cl3'] == 'Set_Dim_B', 'Set_Dim_B'] = df['Cl4']
df.loc[df['Cl5'] == 'Set_Dim_B', 'Set_Dim_B'] = df['Cl6']

df.loc[df['Cl1'] == 'Set_Dim_C', 'Set_Dim_C'] = df['Cl2']
df.loc[df['Cl3'] == 'Set_Dim_C', 'Set_Dim_C'] = df['Cl4']
df.loc[df['Cl5'] == 'Set_Dim_C', 'Set_Dim_C'] = df['Cl6']

df.loc[df['Cl1'] == 'Pivot_Height', 'Pivot_Height'] = df['Cl2']
df.loc[df['Cl3'] == 'Pivot_Height', 'Pivot_Height'] = df['Cl4']
df.loc[df['Cl5'] == 'Pivot_Height', 'Pivot_Height'] = df['Cl6']

# for column
# df['Datum_probe'] = df['Datum_probe'].replace(np.nan, 0)

# for whole dataframe
df = df.replace(np.nan, '')
# inplace
df.replace(np.nan, 0, inplace=True)

df = pd.DataFrame(df,columns=['Date','betweenDate','Model','Line','Rangeindex','Datum_probe','Max_force','Set_Dim_A','Set_Dim_B','Set_Dim_C','Pivot_Height','Projection','Support','Confidence'])
print("displaying the dataframe with data as record")
print(df)
print("-------------------------------Converting into csv file with a new a new file name ------------------------------------")
# df.to_csv("C:\\Users\\IT\\Desktop\\Date ML\\3-14 KPIV.csv")
# df=pd.read_csv("C:\\Users\\IT\\Desktop\\Date ML\\3-14 KPIV.csv")
# print(df)




