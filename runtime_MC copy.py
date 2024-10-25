import tkinter as tk
from tkinter import ttk
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
data = fetch_and_save_data()
print(data)
import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
import pyodbc

# Other imports...

# Function to read and display data for a specific IP
def read_and_display(ip, file_paths):
    for file_path in file_paths:
        full_file_path = os.path.join(ip, file_path)  # Combine IP and file path
        if os.path.exists(full_file_path):
            try:
                with open(full_file_path, "r") as file:
                    content = file.readlines()
                    data_dict = {}
                    for idx, line in enumerate(content):
                        if line.startswith("Line"):
                            continue  # Skip lines without relevant information

                        # Split the line into key and value based on the colon
                        key, value = map(str.strip, line.split(':', 1))

                        # Print or use the key and value as needed
                        print(f"Key: {key}, Value: {value}")
                        data_dict[key] = value
                        IP_MC = data_dict.get("ip", "")
                        time_value = data_dict.get("Time", "")
                        process = data_dict.get("Process", "")
                        average = data_dict.get("Average", "")
                        head = data_dict.get("Head", "")

                    tree.insert("", idx, text=str(idx + 1), values=(ip, time_value, process, average, head))
            except FileNotFoundError:
                # This block should not be reached since we already checked file existence
                pass
        else:
            tree.insert("", 0, text=f"File not found for IP {ip}: {full_file_path}")

# Create main window and Treeview
window = tk.Tk()
window.title("Data Display App")
window.geometry("1000x600")
window.resizable(False, False)

tree = ttk.Treeview(window)
tree["columns"] = ("IP", "Time", "Process", "Average", "Head")
tree.heading("#0", text="Index")
tree.heading("IP", text="IP")
tree.heading("Time", text="Time")
tree.heading("Process", text="Process")
tree.heading("Average", text="Average")
tree.heading("Head", text="Head")

tree.column("#0", width=50)
tree.column("Time", anchor=tk.CENTER, width=150)
tree.column("Process", anchor=tk.CENTER, width=150)
tree.column("Average", anchor=tk.CENTER, width=100)
tree.column("Head", anchor=tk.CENTER, width=100)

tree.grid(column=0, row=0, padx=10, pady=10)

# Example usage for a single IP
ip_file_paths = {
    "\\192.168.101.204\d": ["192.168.101.67_Oil_Low_duration_2.txt", "192.168.101.67_Oil_Up_duration_2.txt"],
}
print(ip_file_paths)

# Process data for each IP and update the Treeview
for ip, file_paths in ip_file_paths.items():
    read_and_display(ip, file_paths)

# Run the Tkinter main loop
window.mainloop()


