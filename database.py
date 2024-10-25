import pandas as pd
import numpy as np
import pyodbc
import pandas as pd

server = '192.168.101.216' 
database = 'DataforAnalysis' 
username = 'DATALYZER' 
password = 'NMB123456'  
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
# select 26 rows from SQL table to insert in dataframe.
query = "SELECT [IP_Address]+[Folder_Path] as [Folder_Path],[Line_no],[Process] FROM [IP_Address].[dbo].[IP_Connect_FAC2]"
df = pd.read_sql(query, cnxn)
print(df.head(100000))

 
