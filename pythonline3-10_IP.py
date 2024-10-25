# %%
import pandas as pd
import numpy as np

# %%
# import datetime
# Date= datetime.datetime.now().date()-datetime.timedelta(1)
# Line='3-6'
# Model='LONGSP'
# Startdate=datetime.datetime.now().date()-datetime.timedelta(1)-datetime.timedelta(150)
# finishDate=datetime.datetime.now().date()-datetime.timedelta(1)-datetime.timedelta(1)

# # %%
# import datetime
# Date= datetime.datetime.now().date()
# Line='3-10_IP'
# Model='LONGSP'
# Startdate=datetime.datetime.now().date()-datetime.timedelta(150)
# finishDate=datetime.datetime.now().date()-datetime.timedelta(1)

# %%
import datetime
Date= '2023-07-20'
Line='3-10_IP'
Model='LONGSP'
Startdate='2023-02-20'
finishDate='2023-07-19'

# %%
import pyodbc
import pandas as pd
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = '192.168.101.219' 
database = 'DataforAnalysis' 
username = 'DATALYZER' 
password = 'NMB54321'  
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
# select 26 rows from SQL table to insert in dataframe.
query = "SELECT [Projection1],[Datum_probe],convert(float,[Max_force]) as [Max_force],[Set_Dim_A],[Set_Dim_B],[Set_Dim_C],[Diecast_Pivot_2]FROM [Diecast].[dbo].[Pivot] join [TransportData].[dbo].[Matching_Auto_Unit1] on [Pivot].Diecast_S_N=[Matching_Auto_Unit1].Barcode_Base join [DataforAnalysis].[dbo].[DataML_Test] on [DataML_Test].Barcode_motor=[Matching_Auto_Unit1].Barcode_Motor   WHERE [DataML_Test].[Model] = '"+Model+"' AND [DataML_Test].[Line] = '3-10' AND [DataML_Test].[Date] BETWEEN '"+str(Startdate)+"' and '"+str(finishDate)+"'and ([Projection1] is not null and [Datum_probe] is not null and [Max_force] is not null and [Set_Dim_A] is not null and [Set_Dim_B] is not null and [Set_Dim_C] is not null and [Diecast_Pivot_2] is not null)and [Projection1] !='0' and [Projection1]>0 and [Projection1] < 1;"
datasets = pd.read_sql(query, cnxn)
print(datasets.head(100000))

# %%
query

# %%
import pyodbc
import pandas as pd
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = '192.168.101.219' 
database = 'DataforAnalysis' 
username = 'DATALYZER' 
password = 'NMB54321'  
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
# select 26 rows from SQL table to insert in dataframe.
query = "SELECT [Bin],[Bin2],[Datum_probe_Min],[Datum_probe_Max],[Max_force_Min],[Max_force_Max],[Set_Dim_A_Min],[Set_Dim_A_Max],[Set_Dim_B_Min],[Set_Dim_B_Max],[Set_Dim_C_Min],[Set_Dim_C_Max],[Pivot_Height_Min],[Pivot_Height_Max],[Pivot_2_Min],[Pivot_2_Max],[KPOV_Min],[KPOV_Max]FROM [DataforAnalysis].[dbo].[Reference];"
spec = pd.read_sql(query, cnxn)
print(spec.head(100000))

# %%
from pandas import DataFrame

data1 ={
'Date':Date,
'betweenDate':str(Startdate)+' - '+str(finishDate),
'Model':Model,
'Line':Line,

'describe1':['count','mean','std','min','25%','50%','75%','max'
],
'Datum_probe':datasets.describe()['Datum_probe'],
'Max_force':datasets.describe()['Max_force'],
'Set_Dim_A':datasets.describe()['Set_Dim_A'],
'Set_Dim_B':datasets.describe()['Set_Dim_B'],
'Set_Dim_C':datasets.describe()['Set_Dim_C'],
'Diecast_Pivot_2':datasets.describe()['Diecast_Pivot_2'],
'Projection':datasets.describe()['Projection1'],
}
dff1 = pd.DataFrame(data1,columns=['Date','betweenDate','Model','Line','describe1',str('Datum_probe'),str('Max_force'),str('Set_Dim_A'),str('Set_Dim_B'),str('Set_Dim_C'),str('Diecast_Pivot_2'),str('Projection')])
print("displaying the dataframe with data as record")
print(dff1)
print("-------------------------------Converting into csv file with a new a new file name ------------------------------------")
# dff1.to_csv("C:\\Users\\IT\\Desktop\\Date ML\\LSP3-10 Accuracy.csv")
# dff1=pd.read_csv("C:\\Users\\IT\\Desktop\\Date ML\\LSP3-10 Accuracy.csv")
# print(dff1)

# %%
import pyodbc
import pandas as pd
# insert data from csv file into dataframe.
# working directory for csv file: type "pwd" in Azure Data Studio or Linux
# working directory in Windows c:\users\username
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = '192.168.101.219' 
database = 'DataforAnalysis' 
username = 'DATALYZER' 
password = 'NMB54321'  
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
# Insert Dataframe into SQL Server:
for index, row in dff1.iterrows():
     cursor.execute("INSERT INTO [DataforAnalysis].[dbo].[DescribeML](Date,betweenDate,Model,Line,describe1,Datum_probe,Max_force,Set_Dim_A,Set_Dim_B,Set_Dim_C,Diecast_Pivot_2,Projection) values ('"+str(row.Date)+"','"+row.betweenDate+"','"+row.Model+"','"+row.Line+"','"+str(row.describe1)+"','"+str(row.Datum_probe)+"','"+str(row.Max_force)+"','"+str(row.Set_Dim_A)+"','"+str(row.Set_Dim_B)+"','"+str(row.Set_Dim_C)+"','"+str(row.Diecast_Pivot_2)+"','"+str(row.Projection)+"')")

cnxn.commit()
cursor.close()

# %%
datasets['Projection1']=pd.cut(datasets['Projection1'],bins=[-np.inf,spec['KPOV_Max'][9],spec['KPOV_Max'][8],np.inf],labels=['fail_low','pass','fail_high'])
datasets['Projection1'].replace('fail_low','fail',inplace=True)
datasets['Projection1'].replace('fail_high','fail',inplace=True)

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
Datum_3LCL = spec['Datum_probe_Max'][0]
Datum_2LCL = spec['Datum_probe_Max'][1]
Datum_LCL = spec['Datum_probe_Max'][2]
Datum_CL = spec['Datum_probe_Max'][3]
Datum_UCL = spec['Datum_probe_Max'][4]
Datum_2UCL = spec['Datum_probe_Max'][5]
Datum_3UCL = spec['Datum_probe_Max'][6]

Max_3LCL = spec['Max_force_Max'][0]
Max_2LCL = spec['Max_force_Max'][1]
Max_LCL = spec['Max_force_Max'][2]
Max_CL = spec['Max_force_Max'][3]
Max_UCL = spec['Max_force_Max'][4]
Max_2UCL = spec['Max_force_Max'][5]
Max_3UCL = spec['Max_force_Max'][6]

Set_Dim_A_3LCL = spec['Set_Dim_A_Max'][0]
Set_Dim_A_2LCL = spec['Set_Dim_A_Max'][1]
Set_Dim_A_LCL = spec['Set_Dim_A_Max'][2]
Set_Dim_A_CL = spec['Set_Dim_A_Max'][3]
Set_Dim_A_UCL = spec['Set_Dim_A_Max'][4]
Set_Dim_A_2UCL = spec['Set_Dim_A_Max'][5]
Set_Dim_A_3UCL = spec['Set_Dim_A_Max'][6]


Set_Dim_B_3LCL = spec['Set_Dim_B_Max'][0]
Set_Dim_B_2LCL = spec['Set_Dim_B_Max'][1]
Set_Dim_B_LCL = spec['Set_Dim_B_Max'][2]
Set_Dim_B_CL = spec['Set_Dim_B_Max'][3]
Set_Dim_B_UCL = spec['Set_Dim_B_Max'][4]
Set_Dim_B_2UCL = spec['Set_Dim_B_Max'][5]
Set_Dim_B_3UCL = spec['Set_Dim_B_Max'][6]

Set_Dim_C_3LCL = spec['Set_Dim_C_Max'][0]
Set_Dim_C_2LCL = spec['Set_Dim_C_Max'][1]
Set_Dim_C_LCL = spec['Set_Dim_C_Max'][2]
Set_Dim_C_CL = spec['Set_Dim_C_Max'][3]
Set_Dim_C_UCL = spec['Set_Dim_C_Max'][4]
Set_Dim_C_2UCL = spec['Set_Dim_C_Max'][5]
Set_Dim_C_3UCL = spec['Set_Dim_C_Max'][6]


Diecast_Pivot_2_3LCL = spec['Pivot_2_Max'][0]
Diecast_Pivot_2_2LCL = spec['Pivot_2_Max'][1]
Diecast_Pivot_2_LCL = spec['Pivot_2_Max'][2]
Diecast_Pivot_2_CL = spec['Pivot_2_Max'][3]
Diecast_Pivot_2_UCL = spec['Pivot_2_Max'][4]
Diecast_Pivot_2_2UCL = spec['Pivot_2_Max'][5]
Diecast_Pivot_2_3UCL = spec['Pivot_2_Max'][6]


datasets['Datum_probe']=pd.cut(datasets['Datum_probe'],bins=[-np.inf, float(Datum_3LCL), float(Datum_2LCL), float(Datum_LCL), float(Datum_CL), float(Datum_UCL), float(Datum_2UCL), float(Datum_3UCL), np.inf],labels=[-4,-3,-2,-1,1,2,3,4])

datasets['Max_force']=pd.cut(datasets['Max_force'],bins=[-np.inf, float(Max_3LCL), float(Max_2LCL), float(Max_LCL), float(Max_CL),float(Max_UCL),float(Max_2UCL),float(Max_3UCL), np.inf],labels=[-4,-3,-2,-1,1,2,3,4])

datasets['Set_Dim_A']=pd.cut(datasets['Set_Dim_A'],bins=[-np.inf, float(Set_Dim_A_3LCL), float(Set_Dim_A_2LCL), float(Set_Dim_A_LCL),float(Set_Dim_A_CL),float(Set_Dim_A_UCL),float(Set_Dim_A_2UCL),float(Set_Dim_A_3UCL),np.inf],labels=[-4,-3,-2,-1,1,2,3,4])

datasets['Set_Dim_B']=pd.cut(datasets['Set_Dim_B'],bins=[-np.inf, float(Set_Dim_B_3LCL), float(Set_Dim_B_2LCL), float(Set_Dim_B_LCL), float(Set_Dim_B_CL), Set_Dim_B_UCL, Set_Dim_B_2UCL, Set_Dim_B_3UCL, np.inf],labels=[-4,-3,-2,-1,1,2,3,4])

datasets['Set_Dim_C']=pd.cut(datasets['Set_Dim_C'],bins=[-np.inf, float(Set_Dim_C_3LCL), float(Set_Dim_C_2LCL), float(Set_Dim_C_LCL), float(Set_Dim_C_CL), float(Set_Dim_C_UCL),float(Set_Dim_C_2UCL),float(Set_Dim_C_3UCL), np.inf],labels=[-4,-3,-2,-1,1,2,3,4])

datasets['Diecast_Pivot_2']=pd.cut(datasets['Diecast_Pivot_2'],bins=[-np.inf, float(Diecast_Pivot_2_3LCL), float(Diecast_Pivot_2_2LCL),float(Diecast_Pivot_2_LCL),float(Diecast_Pivot_2_CL),float(Diecast_Pivot_2_UCL),float(Diecast_Pivot_2_2UCL),float(Diecast_Pivot_2_3UCL),np.inf],labels=[-4,-3,-2,-1,1,2,3,4])


# %%
datasets

# %%
from pyarc import CBA, TransactionDB
from sklearn.model_selection import train_test_split 
from sklearn.metrics import classification_report

train, test = train_test_split(datasets, test_size=0.1)

txns_train = TransactionDB.from_DataFrame(train)
txns_test = TransactionDB.from_DataFrame(test)

cba = CBA (support = 0.08, confidence = 0.7, algorithm ='m1')
cba.fit(txns_train)

y_pred = cba.predict(txns_test)
y_test = test['Projection1']
print ((classification_report(y_test,y_pred)))


# %%
cba.clf.rules

# %%
datasp =(classification_report(y_test,y_pred))

# %%
from pandas import DataFrame

data1 ={
'Date':str(Date),
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
import pyodbc
import pandas as pd
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
# Insert Dataframe into SQL Server:
for index, row in dff.iterrows():

     cursor.execute("INSERT INTO [DataforAnalysis].[dbo].[accuracyDataML_Test] (Date,Line,Model,Details,Procision,recall,f1_score,support) values ('"+row.Date+"','"+row.Line+"','"+row.Model+"','"+row.Details+"','"+row.Procision+"','"+row.recall+"','"+row.f1_score+"','"+row.support+"')")
     # ,(row.Date,row.betweenDate,row.Model,)Procision
                    # ('"+row.Date+"','"+row.betweenDate+"','"+row.Model+"','"+row.Line+"','"+row.Datum_probe+"','"+ a +"','"+row.Set_Dim_A+"','"+row.Set_Dim_B+"','"+row.Set_Dim_C+"','"+row.Diecast_Pivot_2+"','"+row.Projection+"','"+row.Support+"','"+row.Confidence+"')")
cnxn.commit()
cursor.close()

# %%
cba1 =cba.clf.rules

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
indexok=[]
for i in range(len(my_array)):
    indexok+=([i+1])

# %%
import pandas as pd
indexok=[]
for i in range(len(my_array)):
    indexok+=([i+1])
data ={
'Date':Date,
'betweenDate':str(Startdate)+' - '+str(finishDate),
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

df.loc[df['Cl1'] == 'Diecast_Pivot_2', 'Diecast_Pivot_2'] = df['Cl2']
df.loc[df['Cl3'] == 'Diecast_Pivot_2', 'Diecast_Pivot_2'] = df['Cl4']
df.loc[df['Cl5'] == 'Diecast_Pivot_2', 'Diecast_Pivot_2'] = df['Cl6']

df = df.sort_values('Projection')


# for column
# df['Datum_probe'] = df['Datum_probe'].replace(np.nan, 0)

# for whole dataframe
df = df.replace(np.nan, '')
# inplace
df.replace(np.nan, 0, inplace=True)

df = pd.DataFrame(df,columns=['Date','betweenDate','Model','Line','Rangeindex','Datum_probe','Max_force','Set_Dim_A','Set_Dim_B','Set_Dim_C','Diecast_Pivot_2','Projection','Support','Confidence'])
print("displaying the dataframe with data as record")
print(df)
print("-------------------------------Converting into csv file with a new a new file name ------------------------------------")
# df.to_csv("C:\\Users\\IT\\Desktop\\3-6 KPIV.csv")
# df=pd.read_csv("C:\\Users\\IT\\Desktop\\3-6 KPIV.csv")
# print(df)


# %%
import pyodbc
import pandas as pd
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
# Insert Dataframe into SQL Server:
for index, row in df.iterrows():
     cursor.execute("INSERT INTO [DataforAnalysis].[dbo].[Sample_Data_ML_TEST](Date,betweenDate,Model,Line,Rangeindex,Datum_probe,Max_force,Set_Dim_A,Set_Dim_B,Set_Dim_C,Diecast_Pivot_2,Projection,Support,Confidence) values ('"+str(row.Date)+"','"+row.betweenDate+"','"+row.Model+"','"+row.Line+"','"+str(row.Rangeindex)+"','"+str(row.Datum_probe)+"','"+str(row.Max_force)+"','"+str(row.Set_Dim_A)+"','"+str(row.Set_Dim_B)+"','"+str(row.Set_Dim_C)+"','"+str(row.Diecast_Pivot_2)+"','"+str(row.Projection)+"','"+str(row.Support)+"','"+str(row.Confidence)+"')")
     # ,(row.Date,row.betweenDate,row.Model,)
                    # ('"+row.Date+"','"+row.betweenDate+"','"+row.Model+"','"+row.Line+"','"+row.Datum_probe+"','"+ a +"','"+row.Set_Dim_A+"','"+row.Set_Dim_B+"','"+row.Set_Dim_C+"','"+row.Diecast_Pivot_2+"','"+row.Projection+"','"+row.Support+"','"+row.Confidence+"')")
cnxn.commit()
cursor.close()


