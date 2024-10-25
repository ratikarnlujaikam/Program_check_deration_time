import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import time
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
from tkinter import ttk
import pyodbc

import os

import pyodbc
import pandas as pd

import pyodbc
import pandas as pd

# เชื่อมต่อไปยัง SQL Server
server = '192.168.101.216' 
database = 'DataforAnalysis' 
username = 'DATALYZER' 
password = 'NMB123456'  

df = pd.DataFrame()

def fetch_and_save_data():
    global df  # ประกาศ df เป็นตัวแปร global
    
    # ตรวจสอบว่าไฟล์ของวันนั้นมีอยู่แล้วหรือไม่
    current_date = datetime.now().strftime("%Y_%m_%d")
    file_path = f"output_{current_date}.txt"


    
    if os.path.exists(file_path):
        # ถ้ามีไฟล์แล้วให้โหลดข้อมูลจากไฟล์
        df = pd.read_csv(file_path)
        print(f"Data loaded from {file_path}")
    else:
        # ถ้ายังไม่มีไฟล์ให้ดึงข้อมูลจากฐานข้อมูล
        cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()

        # สร้าง query
        query = "SELECT '\\\\'+[IP_Address]+[Folder_Path] as [Folder_Path],[Line_no],[Process] FROM [IP_Address].[dbo].[IP_Connect_FAC2] where Process = 'AxialPlay_Auto_Fac2'"

        # อ่านข้อมูลไปยัง DataFrame
        df = pd.read_sql(query, cnxn)

        # ปิดการเชื่อมต่อ
        cnxn.close()

        # บันทึกข้อมูลลงในไฟล์ txt
        df.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")

    # ใช้ df ในโปรแกรมต่อไป
    # ตัวอย่าง: แสดงผล 5 แถวแรกของ DataFrame
    print(df.head())

# เรียกใช้ฟังก์ชันเพื่อดึงข้อมูลและบันทึกลงในไฟล์ txt
fetch_and_save_data()



def fetch_and_save_spec():
    global spec  # ประกาศ df เป็นตัวแปร global
    
    # ตรวจสอบว่าไฟล์ของวันนั้นมีอยู่แล้วหรือไม่
    current_date = datetime.now().strftime("%Y_%m_%d")
    file_path = f"spec_{current_date}.txt"

    # กำหนดค่าเริ่มต้นของ 'spec' เป็น DataFrame เปล่า
    spec = pd.DataFrame(columns=['LSL', 'USL'])

    if os.path.exists(file_path):
        # ถ้ามีไฟล์แล้วให้โหลดข้อมูลจากไฟล์
        spec = pd.read_csv(file_path)
        print(f"Data loaded from {file_path}")
    else:
        # ถ้ายังไม่มีไฟล์ให้ดึงข้อมูลจากฐานข้อมูล
        server = '192.168.101.219' 
        database = 'DataforAnalysis' 
        username = 'DATALYZER' 
        password = 'NMB54321'  
        cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()

        # สร้าง query
        query = "SELECT [LSL],[USL] FROM [Component_Master].[dbo].[Master_matchings] where [Part]='Oil Low duration'"

        # อ่านข้อมูลไปยัง DataFrame
        spec = pd.read_sql(query, cnxn)

        # ปิดการเชื่อมต่อ
        cnxn.close()

        # บันทึกข้อมูลลงในไฟล์ txt
        spec.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")

    # ใช้ df ในโปรแกรมต่อไป
    # ตัวอย่าง: แสดงผล 5 แถวแรกของ DataFrame
    print(spec.head())

    # Return ค่า spec ออกมา
    return spec

# เรียกใช้ฟังก์ชันเพื่อดึงข้อมูลและบันทึกลงในไฟล์ txt
spec = fetch_and_save_spec()
import os
import pandas as pd

print(df.head())




def find_files_by_date(base_folder, current_date):
    matching_files = []

    for folder_path, _, files in os.walk(base_folder):
        for file in files:
            full_path = os.path.join(folder_path, file)
            if current_date in file:
                matching_files.append(full_path)

    return matching_files



def calculate_spc(process_data, spec_limits, process_avg, spec_avg, std_dev):
    spc = (process_avg - spec_avg) / spec_limits * std_dev
    return spc




for index, row in df.iterrows():
    folder_path = row['Folder_Path']
    line_no = row['Line_no']
    process = row['Process']
    
    current_date_1 = datetime.now().strftime("%Y_%m_%d")
    current_date = f"{current_date_1}B"

    matching_files = find_files_by_date(folder_path, current_date)
    print(matching_files)
    for file_path in matching_files:
        # Select the file for processing
        data = pd.read_csv(file_path, delimiter=';', skiprows=3)

        data['Time'] = pd.to_datetime(data['Time'], format='%H:%M:%S')
        data['Hour'] = data['Time'].dt.hour
        filtered_data = data[['Oil Low duration', 'Hour']]
        data['Oil Low duration'] = pd.to_numeric(data['Oil Low duration'], errors='coerce')
        data['Time'].fillna(pd.Timedelta(seconds=0), inplace=True)
        process_data = data['Oil Low duration'].values

        nan_mask = np.isnan(process_data)

        # Use boolean indexing to filter out NaN values
        filtered_process_data = process_data[~nan_mask]

        process_avg = filtered_process_data.mean()
   

        hourly_avg = data.groupby('Hour')['Oil Low duration'].mean()
        process_avg_hourly = hourly_avg.mean()
        spec_upper_limit = spec['USL'].iloc[0]
        spec_lower_limit = spec['LSL'].iloc[0]
        spec_avg = (spec_upper_limit + spec_lower_limit) / 2
        std_dev = filtered_process_data.std()

        spc_value = calculate_spc(process_data, spec_upper_limit - spec_lower_limit, process_avg, spec_avg, std_dev)

        # Display results for each file
        print(f"File: {file_path}")
        print(f"Hourly Process Average: {hourly_avg}")
        print(f"Overall Process Average: {process_avg}")
        print(f"Spec Average: {spec_avg}")
        print(f"Standard Deviation: {std_dev}")
        print(f"SPC Value: {spc_value}")
        print(f"Spec Upper Limit: {spec_upper_limit}")
        print(f"Spec Lower Limit: {spec_lower_limit}")
        from datetime import datetime


        dateerror = datetime.now()

        if process_avg > spec_upper_limit or process_avg < spec_lower_limit:
            messagebox.showwarning(
        "SPC Alert",
        f"Time Alert {dateerror}\n"
        f"Line {line_no} \n"
        f"Hourly Process Average: {round(hourly_avg,2)}\n"
        f"Overall Process Average: {round(process_avg, 2)}\n"
        f"Spec Average: {round(spec_avg, 2)}\n"
        f"Spec Upper Limit: {round(spec_upper_limit, 2)}\n"
        f"Spec Lower Limit: {round(spec_lower_limit, 2)}"
        
    )


