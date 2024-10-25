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
    file_path = f"IP_{current_date}.txt"


    
    if os.path.exists(file_path):
        # ถ้ามีไฟล์แล้วให้โหลดข้อมูลจากไฟล์
        df = pd.read_csv(file_path)
        print(f"Data loaded from {file_path}")
    else:
        # ถ้ายังไม่มีไฟล์ให้ดึงข้อมูลจากฐานข้อมูล
        cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()

        # สร้าง query
        query = "SELECT [IP_Address] as ip,'\\\\'+[IP_Address]+[Folder_Path] as [Folder_Path],[Line_no],[Process] FROM [IP_Address].[dbo].[IP_Connect_FAC2] where Process = 'AxialPlay_Auto_Fac2'"

        # อ่านข้อมูลไปยัง DataFrame.
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




import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
from datetime import datetime
from tkinter import filedialog, messagebox

# Define the find_files_by_date function
def find_files_by_date(base_folder, current_date):
    matching_files = []
    for folder_path, _, files in os.walk(base_folder):
        for file in files:
            full_path = os.path.join(folder_path, file)
            if current_date in file:
                matching_files.append(full_path)
    return matching_files

# Function to read and display data for a specific IP
from datetime import datetime

from datetime import datetime

def read_and_display_low(ip, file_paths, line_no):
    for file_path in file_paths:
        full_file_path = os.path.join(ip, file_path)
        if os.path.exists(full_file_path):
            try:
                with open(full_file_path, "r") as file:
                    content = file.readlines()
                    data_dict = {}
                    for idx, line in enumerate(content):
                        if line.startswith("Line"):
                            continue

                        key, value = map(str.strip, line.split(':', 1))
                        data_dict[key] = value
                        IP_MC = data_dict.get("ip", "")
                        time_value_str = data_dict.get("Time", "")
                        process = data_dict.get("Process", "")
                        average = data_dict.get("Average", "")
                        head = data_dict.get("Head", "")

                    # Convert time_value_str to a datetime object
                    try:
                        time_value = datetime.strptime(time_value_str, "%Y-%m-%d %H:%M:%S.%f")

                        # Check if the date part of time_value matches the current date
                        if time_value.date() == datetime.now().date():
                            tree1.insert("", idx, text=str(idx + 1), values=(ip, line_no, time_value_str, process, average, head))
                    except ValueError as e:
                        print(f"Error processing time value for IP {ip}, Line {line_no}: {e}")
            except FileNotFoundError:
                tree1.insert("", 0, text=f"File not found for IP {ip}: {full_file_path}")
        else:
            tree1.insert("", 0, text=f"File not found for IP {ip}: {full_file_path}")


def read_and_display_up(ip, file_paths, line_no):
    for file_path in file_paths:
        full_file_path = os.path.join(ip, file_path)
        if os.path.exists(full_file_path):
            try:
                with open(full_file_path, "r") as file:
                    content = file.readlines()
                    data_dict = {}
                    for idx, line in enumerate(content):
                        if line.startswith("Line"):
                            continue

                        key, value = map(str.strip, line.split(':', 1))
                        data_dict[key] = value
                        IP_MC = data_dict.get("ip", "")
                        time_value_str = data_dict.get("Time", "")
                        process = data_dict.get("Process", "")
                        average = data_dict.get("Average", "")
                        head = data_dict.get("Head", "")

                    # Convert time_value_str to a datetime object
                    try:
                        time_value = datetime.strptime(time_value_str, "%Y-%m-%d %H:%M:%S.%f")

                        # Check if the date part of time_value matches the current date
                        if time_value.date() == datetime.now().date():
                            tree2.insert("", idx, text=str(idx + 1), values=(ip, line_no, time_value_str, process, average, head))
                    except ValueError as e:
                        print(f"Error processing time value for IP {ip}, Line {line_no}: {e}")
            except FileNotFoundError:
                tree2.insert("", 0, text=f"File not found for IP {ip}: {full_file_path}")
        else:
            tree2.insert("", 0, text=f"File not found for IP {ip}: {full_file_path}")

  
    
def process_files_for_ip_low(ip, folder_path, line_no, process, duration):
    current_date = f"{ip}_Oil_Low_duration_{duration}.txt"

    matching_files = find_files_by_date(folder_path, current_date)
    print(matching_files)
    print(f"IP: {ip}, Line: {line_no}, Process: {process}")

    # Call the read_and_display function for each IP
    read_and_display_low(ip, matching_files, line_no)
    
def process_files_for_ip_up(ip, folder_path, line_no, process, duration):
    current_date = f"{ip}_Oil_Up_duration_{duration}.txt"

    matching_files = find_files_by_date(folder_path, current_date)
    print(matching_files)
    print(f"IP: {ip}, Line: {line_no}, Process: {process}")

    # Call the read_and_display function for each IP
    read_and_display_up(ip, matching_files, line_no)



def button_ip_low():
    for item in tree1.get_children():
        tree1.delete(item)
    for item in tree2.get_children():
        tree2.delete(item)
    # Now, use a for loop to process files for each IP from the DataFrame
    for index, row in df.iterrows():
        ip = row['ip']
        folder_path = row['Folder_Path']
        line_no = row['Line_no']
        process = row['Process']

# Usage example for low duration 1
        process_files_for_ip_low(ip, folder_path, line_no, process, duration=1)

# Usage example for low duration 2
        process_files_for_ip_low(ip, folder_path, line_no, process, duration=2)
        
        
        # Usage example for low duration 1
        process_files_for_ip_up(ip, folder_path, line_no, process, duration=1)

# Usage example for low duration 2
        process_files_for_ip_up(ip, folder_path, line_no, process, duration=2)
  



        
# Create main window and Treeviews
window = tk.Tk()
window.title("Data Display App")
window.geometry("1000x600")
window.resizable(False, False)

label1 = tk.Label(window, text="Process Oil Low duration", font=("Arial", 12, "bold"))
label1.grid(column=0, row=0, pady=(0, 5))

tree1 = ttk.Treeview(window)
tree1["columns"] = ("IP","line_no","Time", "Process", "Average", "Head")
tree1.heading("#0", text="Index")
tree1.heading("IP", text="IP")
tree1.heading("line_no", text="line_no")
tree1.heading("Time", text="Time")
tree1.heading("Process", text="Process")
tree1.heading("Average", text="Average")
tree1.heading("Head", text="Head")

tree1.column("#0", width=50)
tree1.column("IP", anchor=tk.CENTER, width=100)
tree1.column("line_no", anchor=tk.CENTER, width=100)
tree1.column("Time", anchor=tk.CENTER, width=170)
tree1.column("Process", anchor=tk.CENTER, width=150)
tree1.column("Average", anchor=tk.CENTER, width=100)
tree1.column("Head", anchor=tk.CENTER, width=100)

tree1.grid(column=0, row=1, padx=10, pady=10)


label2 = tk.Label(window, text="Process Oil UP duration", font=("Arial", 12, "bold"))
label2.grid(column=0, row=2, pady=(0, 5))
# Second Treeview
tree2 = ttk.Treeview(window)
tree2["columns"] = ("IP","line_no","Time", "Process", "Average", "Head")
tree2.heading("#0", text="Index")
tree2.heading("IP", text="IP")
tree2.heading("line_no", text="line_no")
tree2.heading("Time", text="Time")
tree2.heading("Process", text="Process")
tree2.heading("Average", text="Average")
tree2.heading("Head", text="Head")

tree2.column("#0", width=50)
tree2.column("IP", anchor=tk.CENTER, width=100)
tree2.column("line_no", anchor=tk.CENTER, width=100)
tree2.column("Time", anchor=tk.CENTER, width=170)
tree2.column("Process", anchor=tk.CENTER, width=150)
tree2.column("Average", anchor=tk.CENTER, width=100)
tree2.column("Head", anchor=tk.CENTER, width=100)

tree2.grid(column=0, row=3, padx=10, pady=10)



# Create a "Process All IPs" button
process_all_ips_button = ttk.Button(window, text="Process All IPs", command=button_ip_low)
process_all_ips_button.grid(column=0, row=4, padx=10, pady=10)

# Run the Tkinter main loop
window.mainloop()







