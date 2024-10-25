# %%
import pandas as pd
import numpy as np

# %%
Date='2023-03-17'
Line='3-10'
Model='LONGSP'
Startdate='2022-11-01'
finishDate='2023-03-16'

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
query = "SELECT [Projection1],[Datum_probe],[Max_force],[Set_Dim_A],[Set_Dim_B],[Set_Dim_C],[Pivot_Height]FROM [DataforAnalysis].[dbo].[DataML] WHERE [Model] = 'LONGSP' AND [Line] = '"+Line+"' AND [Date] BETWEEN '"+Startdate+"' and '"+finishDate+"'and ([Projection1] is not null and [Datum_probe] is not null and [Max_force] is not null and [Set_Dim_A] is not null and [Set_Dim_B] is not null and [Set_Dim_C] is not null and [Pivot_Height] is not null)and [Projection1] !='0' and [Max_force] >=100 and [Set_Dim_A] >=0.3775 and [Set_Dim_B] >=0.3775 and [Set_Dim_C] >=0.3775 and [Max_force] <= 3700.00 and [Set_Dim_A] <= 0.6537 and [Set_Dim_B] <= 0.6537 and  [Set_Dim_C] <= 0.6537;"
df = pd.read_sql(query, cnxn)
print(df.head(100000))

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
Datum_3LCL = 124.99
Datum_2LCL = 249.99
Datum_LCL = 374.99
Datum_CL = 499.99
Datum_UCL = 624.99
Datum_2UCL = 749.99
Datum_3UCL = 875

Max_3LCL = 299.99
Max_2LCL = 833.32
Max_LCL = 1366.66
Max_CL = 1899.99
Max_UCL = 2433.32
Max_2UCL = 2966.66
Max_3UCL = 3500

Set_Dim_A_3LCL = 0.4774
Set_Dim_A_2LCL = 0.4901
Set_Dim_A_LCL = 0.5028
Set_Dim_A_CL = 0.5155
Set_Dim_A_UCL = 0.5282
Set_Dim_A_2UCL = 0.5409
Set_Dim_A_3UCL = 0.5537


Set_Dim_B_3LCL = 0.4774
Set_Dim_B_2LCL = 0.4901
Set_Dim_B_LCL = 0.5058
Set_Dim_B_CL = 0.5155
Set_Dim_B_UCL = 0.5282
Set_Dim_B_2UCL =0.5409
Set_Dim_B_3UCL = 0.5537

Set_Dim_C_3LCL = 0.4774
Set_Dim_C_2LCL = 0.4901
Set_Dim_C_LCL = 0.5028
Set_Dim_C_CL = 0.5155
Set_Dim_C_UCL = 0.5282
Set_Dim_C_2UCL =0.5409
Set_Dim_C_3UCL = 0.5537

Pivot_Height_3LCL = -9.4030
Pivot_Height_2LCL = -9.3945
Pivot_Height_LCL = -9.3860
Pivot_Height_CL = -9.3776
Pivot_Height_UCL = -9.3691
Pivot_Height_2UCL = -9.3606
Pivot_Height_3UCL = -9.3523


datasets['Datum_probe']=pd.cut(datasets['Datum_probe'],bins=[-np.inf, Datum_3LCL, Datum_2LCL, Datum_LCL, Datum_CL, Datum_UCL, Datum_2UCL, Datum_3UCL, np.inf],labels=['A','B','C','D','E','F','G','H'])

datasets['Max_force']=pd.cut(datasets['Max_force'],bins=[-np.inf, Max_3LCL, Max_2LCL, Max_LCL, Max_CL, Max_UCL, Max_2UCL, Max_3UCL, np.inf],labels=['A','B','C','D','E','F','G','H'])

datasets['Set_Dim_A']=pd.cut(datasets['Set_Dim_A'],bins=[-np.inf, Set_Dim_A_3LCL, Set_Dim_A_2LCL, Set_Dim_A_LCL, Set_Dim_A_CL, Set_Dim_A_UCL, Set_Dim_A_2UCL, Set_Dim_A_3UCL,np.inf],labels=['A','B','C','D','E','F','G','H'])

datasets['Set_Dim_B']=pd.cut(datasets['Set_Dim_B'],bins=[-np.inf, Set_Dim_B_3LCL, Set_Dim_B_2LCL, Set_Dim_B_LCL, Set_Dim_B_CL, Set_Dim_B_UCL, Set_Dim_B_2UCL, Set_Dim_B_3UCL, np.inf],labels=['A','B','C','D','E','F','G','H'])

datasets['Set_Dim_C']=pd.cut(datasets['Set_Dim_C'],bins=[-np.inf, Set_Dim_C_3LCL, Set_Dim_C_2LCL, Set_Dim_C_LCL, Set_Dim_C_CL, Set_Dim_C_UCL, Set_Dim_C_2UCL, Set_Dim_C_3UCL, np.inf],labels=['A','B','C','D','E','F','G','H'])

datasets['Pivot_Height']=pd.cut(datasets['Pivot_Height'],bins=[-np.inf, Pivot_Height_3LCL, Pivot_Height_2LCL, Pivot_Height_LCL, Pivot_Height_CL, Pivot_Height_UCL, Pivot_Height_2UCL, Pivot_Height_3UCL,np.inf],labels=['A','B','C','D','E','F','G','H'])


# %%
datasets

# %%
from pyarc import CBA, TransactionDB
from sklearn.model_selection import train_test_split 
from sklearn.metrics import classification_report

train, test = train_test_split(datasets, test_size=0.1)

txns_train = TransactionDB.from_DataFrame(train)
txns_test = TransactionDB.from_DataFrame(test)

cba = CBA (support = 0.09, confidence = 0.8, algorithm ='m1')
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
for index, row in dff.iterrows():

     cursor.execute("INSERT INTO [DataforAnalysis].[dbo].[accuracyDataML] (Date,Line,Model,Details,Procision,recall,f1_score,support) values ('"+row.Date+"','"+row.Line+"','"+row.Model+"','"+row.Details+"','"+row.Procision+"','"+row.recall+"','"+row.f1_score+"','"+row.support+"')")
     # ,(row.Date,row.betweenDate,row.Model,)Procision
                    # ('"+row.Date+"','"+row.betweenDate+"','"+row.Model+"','"+row.Line+"','"+row.Datum_probe+"','"+ a +"','"+row.Set_Dim_A+"','"+row.Set_Dim_B+"','"+row.Set_Dim_C+"','"+row.Pivot_Height+"','"+row.Projection+"','"+row.Support+"','"+row.Confidence+"')")
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


# %%

# importing pandas as pd
import pandas as pd
from IPython.display import HTML

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

# %%
result = df.to_html()
print(result)

html = df.to_html()
  
# write html to file
text_file = open("index.html", "w")
text_file.write(html)
text_file.close()

# %%
html = df.to_html()
  
# write html to file
text_file = open("index.html", "w")
text_file.write(html)
text_file.close()

# %%
HTML(df.to_html(classes='table table-stripped'))

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
for index, row in df.iterrows():

     

     cursor.execute("INSERT INTO [DataforAnalysis].[dbo].[Sample_DataML] (Date,betweenDate,Model,Line,Rangeindex,Datum_probe,Max_force,Set_Dim_A,Set_Dim_B,Set_Dim_C,Pivot_Height,Projection,Support,Confidence) values ('"+row.Date+"','"+row.betweenDate+"','"+row.Model+"','"+row.Line+"','"+str(row.Rangeindex)+"','"+str(row.Datum_probe)+"','"+str(row.Max_force)+"','"+str(row.Set_Dim_A)+"','"+str(row.Set_Dim_B)+"','"+str(row.Set_Dim_C)+"','"+str(row.Pivot_Height)+"','"+str(row.Projection)+"','"+str(row.Support)+"','"+str(row.Confidence)+"')")
     # ,(row.Date,row.betweenDate,row.Model,)
                    # ('"+row.Date+"','"+row.betweenDate+"','"+row.Model+"','"+row.Line+"','"+row.Datum_probe+"','"+ a +"','"+row.Set_Dim_A+"','"+row.Set_Dim_B+"','"+row.Set_Dim_C+"','"+row.Pivot_Height+"','"+row.Projection+"','"+row.Support+"','"+row.Confidence+"')")
cnxn.commit()
cursor.close()


