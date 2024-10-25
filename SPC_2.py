import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import time
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
from tkinter import ttk
import requests
import pyodbc

import os

# เชื่อมต่อไปยัง SQL Server
server = '192.168.101.216' 
database = 'DataforAnalysis' 
username = 'DATALYZER' 
password = 'NMB123456'  
df = None
def fetch_and_save_data():
    global df  # Declare df as a global variable
    
    # ตรวจสอบว่าไฟล์ของวันนั้นมีอยู่แล้วหรือไม่
    current_date = datetime.now().strftime("%Y_%m_%d")
    file_path = f"IP_{current_date}.txt"

    if os.path.exists(file_path):
        # If the file exists, load data from the file
        df = pd.read_csv(file_path)
        print(f"Data loaded from {file_path}")
    else:
        # If the file doesn't exist, fetch data from the database
        cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()

        # Create a query to select specific columns
        query = "SELECT [IP_Address] as ip, '\\\\' + [IP_Address] + [Folder_Path] as [Folder_Path], [Line_no], [Process] FROM [IP_Address].[dbo].[IP_Connect_FAC2] WHERE Process = 'AxialPlay_Auto_Fac2' order by [Line_no]"

        # Read data into a DataFrame.
        df = pd.read_sql(query, cnxn)

        # Close the connection
        cnxn.close()

        # Save the data to a txt file
        df.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")

    # ใช้ df ในโปรแกรมต่อไป
    # ตัวอย่าง: แสดงผล 5 แถวแรกของ DataFrame
    

# Call the function to fetch and save data
fetch_and_save_data()




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




def show_warning(message):
    print(message)
    warning_window = tk.Toplevel()
    warning_window.title("SPC Alert")
    warning_window.geometry("500x250")
    warning_window.configure(bg="red")

    label = ttk.Label(warning_window, text=message, background="red", foreground="white", font=("Helvetica", 20))
    label.pack(pady=20)

    ok_button = ttk.Button(warning_window, text="Close", command=warning_window.destroy)
    ok_button.pack()

import socket
import os

    
def process_data(folder_path, selected_duration,UCL_UP_1,LCL_UP_1,UCL_UP_2,LCL_UP_2,UCL_LOW_1,LCL_LOW_1,UCL_LOW_2,LCL_LOW_2):

    current_date_1 = datetime.now().strftime("%Y_%m_%d")
    current_date = f"{current_date_1}B"


    matching_files = find_files_by_date(folder_path, current_date)
    

  
    if not matching_files:
        messagebox.showerror("Error", f"No files found for the current date {current_date}. Exiting.")
        return
    
    for file_path in matching_files:
        stop_file_path = f'stop_time_{current_date_1}.txt'
        if os.path.exists(stop_file_path):
            with open(stop_file_path, 'r') as stop_file:
                stop_content = stop_file.read().strip()
    
            datetime_obj = datetime.strptime(stop_content, '%H:%M:%S')
            startrun = datetime_obj.time()
            stop_run = datetime.now().time()

            data_raed = pd.read_csv(file_path, delimiter=';', skiprows=3)
            df = pd.DataFrame(data_raed)

            df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time
            data = df[(df['Time'] > startrun) & (df['Time'] < stop_run)]
            ##print("Data:", data)
        else:
            data = pd.read_csv(file_path, delimiter=';', skiprows=3)
            ##print(f"Stop file '{stop_file_path}' not found. No data entered.")
        ##print("matching_files",matching_files)
        host_ip = socket.gethostbyname(socket.gethostname())
   
        oil_low_numbers = [1, 2]  # Add more Oil Low Numbers as needed
        oil_types = ["Oil Up duration", "Oil LOW duration"]
        new_entry = {}
        for oil_low_number in oil_low_numbers:
            data_oil_low = data[data['Oil Low number'] == oil_low_number]
            if oil_low_number == 1:
                USL = UCL_LOW_1
                LSL = LCL_LOW_1
              
            elif oil_low_number == 2:
                USL = UCL_LOW_2
                LSL = LCL_LOW_2
              
            data_oil_low['Time'] = pd.to_datetime(data_oil_low['Time'], format='%H:%M:%S')
   
            ##print("***********************************************",data_oil_low)
            data_oil_low['Hour'] = data_oil_low['Time'].dt.hour
            filtered_data = data_oil_low[['Oil Low duration', 'Hour']]
            data_oil_low['Oil Low duration'] = pd.to_numeric(data_oil_low['Oil Low duration'], errors='coerce')
            data_oil_low['Time'].fillna(pd.Timedelta(seconds=0), inplace=True)
            
            process_data = data_oil_low['Oil Low duration'].values
            ##print("process_data************************************************************",process_data)
            nan_mask = np.isnan(process_data)

            # Use boolean indexing to filter out NaN values
            filtered_process_data = process_data[~nan_mask]

            process_avg = filtered_process_data.mean()

            hourly_avg = data_oil_low.groupby('Hour')['Oil Low duration'].mean()
            spec_upper_limit = float(USL)
            spec_lower_limit = float(LSL)
            spec_avg = (spec_upper_limit + spec_lower_limit) / 2
            std_dev = filtered_process_data.std()

            spc_value = calculate_spc(process_data, spec_upper_limit - spec_lower_limit, process_avg, spec_avg, std_dev)

            print(process_avg)

            time = datetime.now()
            try:
                df_low = pd.read_csv(f"{current_date_1}_Oil_Low_duration.csv")
            except FileNotFoundError:
    # If the file doesn't exist, create a new DataFrame
                columns = ['ip', 'Time', 'Process', 'Average', 'Head']
                df_low = pd.DataFrame(columns=columns)
            
            print( f"ip : {host_ip}\n"
                        f"Time : {time} \n"
                        f"Process : Oil Low duration \n"
                        f"Average :{round(process_avg, 2)}\n"
                        f"Head : {oil_low_number}")

            if process_avg > spec_upper_limit or process_avg < spec_lower_limit:
                        message = (
                        f"ip : {host_ip}\n"
                        f"Time : {time} \n"
                        f"Process : Oil Low duration \n"
                        f"Average :{round(process_avg, 2)}\n"
                        f"Head : {oil_low_number}")
                        
                        new_entry = {
                        'ip': [host_ip],
                        'Time': [time],
                        'Process': ['Oil Low duration'],
                        'Average': [round(process_avg, 2)],
                        'Head': [oil_low_number]}
            
            df = df_low.append(pd.DataFrame(new_entry), ignore_index=True)


    # Save the DataFrame to a CSV file
            file_name = f"{current_date_1}_Oil_Low_duration.csv"
            df_low.to_csv(file_name, index=False)
                        
            with open(f"{host_ip}_Oil_Low_duration_{oil_low_number}.txt", "a") as output_file:
                    output_file.truncate(0)  # This line truncates the file, removing old data
                    output_file.write(message)
                    show_warning(message)
            
        for oil_low_number in oil_low_numbers:
            data_oil_low = data[data['Oil Up number'] == oil_low_number]
            if oil_low_number == 1:
                USL = UCL_LOW_1
                LSL = LCL_LOW_1
              
            elif oil_low_number == 2:
                USL = UCL_LOW_2
                LSL = LCL_LOW_2
              
            data_oil_low['Time'] = pd.to_datetime(data_oil_low['Time'], format='%H:%M:%S')
   
            ##print("***********************************************",data_oil_low)
            data_oil_low['Hour'] = data_oil_low['Time'].dt.hour
            filtered_data = data_oil_low[['Oil Up duration', 'Hour']]
            data_oil_low['Oil Up duration'] = pd.to_numeric(data_oil_low['Oil Up duration'], errors='coerce')
            data_oil_low['Time'].fillna(pd.Timedelta(seconds=0), inplace=True)
            
            process_data = data_oil_low['Oil Up duration'].values
            ##print("process_data************************************************************",process_data)
            nan_mask = np.isnan(process_data)

            # Use boolean indexing to filter out NaN values
            filtered_process_data = process_data[~nan_mask]

            process_avg = filtered_process_data.mean()

            hourly_avg = data_oil_low.groupby('Hour')['Oil Up duration'].mean()
            spec_upper_limit = float(USL)
            spec_lower_limit = float(LSL)
            spec_avg = (spec_upper_limit + spec_lower_limit) / 2
            std_dev = filtered_process_data.std()

            spc_value = calculate_spc(process_data, spec_upper_limit - spec_lower_limit, process_avg, spec_avg, std_dev)
         

            time = datetime.now()
            try:
                df = pd.read_csv(f"{current_date_1}_Oil_Up_duration.csv")
            except FileNotFoundError:
    # If the file doesn't exist, create a new DataFrame
                columns = ['ip', 'Time', 'Process', 'Average', 'Head']
                df = pd.DataFrame(columns=columns)

            if process_avg > spec_upper_limit or process_avg < spec_lower_limit:
                        message = (
                        f"ip : {host_ip}\n"
                        f"Time : {time} \n"
                        f"Process : Oil Up duration \n"
                        f"Average :{round(process_avg, 2)}\n"
                        f"Head : {oil_low_number}")
                        
                        new_entry = {
                        'ip': [host_ip],
                        'Time': [time],
                        'Process': ['Oil Up duration'],
                        'Average': [round(process_avg, 2)],
                        'Head': [oil_low_number]}
            df = df.append(pd.DataFrame(new_entry), ignore_index=True)

    # Save the DataFrame to a CSV file
            file_name = f"{current_date_1}_Oil_Up_duration.csv"
            df.to_csv(file_name, index=False)
                        
            with open(f"{host_ip}_Oil_Up_duration_{oil_low_number}.txt", "a") as output_file:
                    output_file.truncate(0)  # This line truncates the file, removing old data
                    output_file.write(message)
                    show_warning(message)
     

    submit_action()      
            



from datetime import datetime

def process_graph(folder_path, selected_duration,UCL_UP_1,LCL_UP_1,UCL_UP_2,LCL_UP_2,UCL_LOW_1,LCL_LOW_1,UCL_LOW_2,LCL_LOW_2):

    current_date_1 = datetime.now().strftime("%Y_%m_%d")
    current_date = f"{current_date_1}B"

    # Find all files based on the current date
    matching_files = find_files_by_date(folder_path, current_date)

    # Check if there are any matching files
    if not matching_files:
        messagebox.showerror("Error", f"No files found for the current date {current_date}. Exiting.")
        return

    for file_path in matching_files:
        # Select the file for processing
        data = pd.read_csv(file_path, delimiter=';', skiprows=3)
        

        ##print("*********************************************data", data)

        oil_low_numbers = [1, 2]  # Add more Oil Low Numbers as needed
        head = "Oil Low duration"
        for oil_low_number in oil_low_numbers:
            data_oil_low = data[data['Oil Low number'] == oil_low_number]
            if oil_low_number == 1:
                USL = UCL_LOW_1
                LSL = LCL_LOW_1
              
            elif oil_low_number == 2:
                USL = UCL_LOW_2
                LSL = LCL_LOW_2

            data_oil_low['Time'] = pd.to_datetime(data_oil_low['Time'], format='%H:%M:%S')
            data_oil_low['Hour'] = data_oil_low['Time'].dt.hour
            filtered_data = data_oil_low[['Oil Low duration', 'Hour']]
            data_oil_low['Oil Low duration'] = pd.to_numeric(data_oil_low['Oil Low duration'], errors='coerce')
            data_oil_low['Time'].fillna(pd.Timedelta(seconds=0), inplace=True)
            process_data = data_oil_low['Oil Low duration'].values

            nan_mask = np.isnan(process_data)

            # Use boolean indexing to filter out NaN values
            filtered_process_data = process_data[~nan_mask]

            process_avg = filtered_process_data.mean()

            hourly_avg = data_oil_low.groupby('Hour')['Oil Low duration'].mean()
            if oil_low_number == 1:
                spec_upper_limit_1 = float(USL)
                spec_lower_limit_1 = float(LSL)
            elif oil_low_number == 2:
                spec_upper_limit_2 = float(USL)
                spec_lower_limit_2 = float(LSL)

# Calculate spec_avg and std_dev based on the selected oil_low_number
            if oil_low_number == 1:
                spec_avg_1 = (spec_upper_limit_1 + spec_lower_limit_1) / 2
                
            elif oil_low_number == 2:
                spec_avg_2 = (spec_upper_limit_2 + spec_lower_limit_2) / 2
               

            # Extract hourly averages for each Oil Low Number
            if oil_low_number == 1:
                hourly_avg_1 = hourly_avg
            elif oil_low_number == 2:
                hourly_avg_2 = hourly_avg
        
        plot_graph(hourly_avg_1, hourly_avg_2, spec_upper_limit_1, spec_lower_limit_1, spec_avg_1,
           spec_upper_limit_2, spec_lower_limit_2, spec_avg_2, head)

            
    for file_path in matching_files:
        # Select the file for processing
        data = pd.read_csv(file_path, delimiter=';', skiprows=3)

        ##print("*********************************************data", data)

        oil_low_numbers = [1, 2]  # Add more Oil Low Numbers as needed
        head = "Oil Up duration"
        for oil_low_number in oil_low_numbers:
            data_oil_low = data[data['Oil Up number'] == oil_low_number]
            if oil_low_number == 1:
                USL = UCL_UP_1
                LSL = LCL_UP_1
              
            elif oil_low_number == 2:
                USL = UCL_UP_2
                LSL = LCL_UP_2

            data_oil_low['Time'] = pd.to_datetime(data_oil_low['Time'], format='%H:%M:%S')
            data_oil_low['Hour'] = data_oil_low['Time'].dt.hour
            filtered_data = data_oil_low[['Oil Up duration', 'Hour']]
            data_oil_low['Oil Up duration'] = pd.to_numeric(data_oil_low['Oil Up duration'], errors='coerce')
            data_oil_low['Time'].fillna(pd.Timedelta(seconds=0), inplace=True)
            process_data = data_oil_low['Oil Up duration'].values

            nan_mask = np.isnan(process_data)

            # Use boolean indexing to filter out NaN values
            filtered_process_data = process_data[~nan_mask]

            process_avg = filtered_process_data.mean()

            hourly_avg = data_oil_low.groupby('Hour')['Oil Up duration'].mean()
            if oil_low_number == 1:
                spec_upper_limit_1 = float(USL)
                spec_lower_limit_1 = float(LSL)
            elif oil_low_number == 2:
                spec_upper_limit_2 = float(USL)
                spec_lower_limit_2 = float(LSL)

# Calculate spec_avg and std_dev based on the selected oil_low_number
            if oil_low_number == 1:
                spec_avg_1 = (spec_upper_limit_1 + spec_lower_limit_1) / 2
                
            elif oil_low_number == 2:
                spec_avg_2 = (spec_upper_limit_2 + spec_lower_limit_2) / 2
               

            # Extract hourly averages for each Oil Low Number
            if oil_low_number == 1:
                hourly_avg_1 = hourly_avg
            elif oil_low_number == 2:
                hourly_avg_2 = hourly_avg
        
        plot_graph(hourly_avg_1, hourly_avg_2, spec_upper_limit_1, spec_lower_limit_1, spec_avg_1,
           spec_upper_limit_2, spec_lower_limit_2, spec_avg_2, head)

import matplotlib.pyplot as plt

def plot_graph(hourly_avg_1, hourly_avg_2, spec_upper_limit_1, spec_lower_limit_1, spec_avg_1,
               spec_upper_limit_2, spec_lower_limit_2, spec_avg_2, head):

    # First Graph
    plt.figure(figsize=(10, 6))
    plt.plot(hourly_avg_1.index, hourly_avg_1.values, marker='o', label=f'Hourly Averages 1')
    plt.axhline(y=spec_upper_limit_1, color='r', linestyle='--', label='Spec Upper Limit 1')
    plt.axhline(y=spec_lower_limit_1, color='r', linestyle='--', label='Spec Lower Limit 1')
    plt.axhline(y=spec_avg_1, color='g', linestyle='--', label='Spec Average 1')
    annotate_values(hourly_avg_1)
    plt.title(f'Hourly Process Averages {head} - Graph 1')
    plt.xlabel('Hour')
    plt.ylabel(f'Average {head}')
    plt.grid(True)
    plt.legend()
    plt.savefig(f'Graph1_{head}.png')
    plt.close()

    # Second Graph
    plt.figure(figsize=(10, 6))
    plt.plot(hourly_avg_2.index, hourly_avg_2.values, marker='o', label=f'Hourly Averages 2')
    plt.axhline(y=spec_upper_limit_2, color='r', linestyle='--', label='Spec Upper Limit 2')
    plt.axhline(y=spec_lower_limit_2, color='r', linestyle='--', label='Spec Lower Limit 2')
    plt.axhline(y=spec_avg_2, color='g', linestyle='--', label='Spec Average 2')
    annotate_values(hourly_avg_2)
    plt.title(f'Hourly Process Averages {head} - Graph 2')
    plt.xlabel('Hour')
    plt.ylabel(f'Average {head}')
    plt.grid(True)
    plt.legend()
    plt.savefig(f'Graph2_{head}.png')
    plt.close()

    # Display the images in Tkinter window
    show_image(f'Graph1_{head}.png')
    show_image(f'Graph2_{head}.png')

# Helper function to annotate values
def annotate_values(hourly_avg):
    for i, value in enumerate(hourly_avg.values):
        plt.annotate(f'{value:.2f}', (hourly_avg.index[i], value), textcoords="offset points", xytext=(0, 10), ha='center')






from PIL import Image
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import pandas as pd

def show_image(image_path):
    # Create a new Tkinter window
    image_window = tk.Toplevel(window)
    image_window.title("Graph Viewer")

    # Load the image using Pillow
    image = Image.open(image_path)
    tk_image = ImageTk.PhotoImage(image)

    # Create a Label and display the image
    label_image = ttk.Label(image_window, image=tk_image)
    label_image.image = tk_image
    label_image.pack()
    


def show_graph_button():
    # Call process_data with your desired parameters
    folder_path = folder_var.get()
    selected_duration = duration_var.get()

   
    process_graph(
    folder_path, selected_duration,
    UCL_UP_1.get(), LCL_UP_1.get(), UCL_UP_2.get(), LCL_UP_2.get(),
    UCL_LOW_1.get(), LCL_LOW_1.get(), UCL_LOW_2.get(), LCL_LOW_2.get()
)

    

is_set_allowed = False   
          
def submit_action():
    global stop_flag
    stop_flag = False  # Reset the stop flag
    global is_set_allowed  # Use global to modify the variable

    selected_folder = folder_var.get()
    selected_duration = duration_var.get()

    # Validate if the duration is a positive integer
    try:
        duration_seconds = int(selected_duration) * 60  # Convert to seconds
        if duration_seconds <= 0:
            raise ValueError("Duration must be a positive integer.")
    except ValueError:
        messagebox.showerror("Error", "Invalid duration. Please enter a positive integer.")
        return

    # Save the selected path to a file
    save_path(selected_folder)

    # Allow set to be modified after submitting
    is_set_allowed = True

    # Disable Entry widgets and buttons during countdown
    entry_folder.config(state=tk.DISABLED)
    duration_entry.config(state=tk.DISABLED)
    browse_button.config(state=tk.DISABLED)

    button_submit.config(state=tk.DISABLED)
    button_stoprun.config(state=tk.DISABLED)
    UCL_UP_1_label.config(state=tk.DISABLED)
    LCL_UP_1_label.config(state=tk.DISABLED)
    UCL_UP_2_label.config(state=tk.DISABLED)
    LCL_UP_2_label.config(state=tk.DISABLED)
    UCL_LOW_1_label.config(state=tk.DISABLED)
    LCL_LOW_1_label.config(state=tk.DISABLED)
    UCL_LOW_2_label.config(state=tk.DISABLED)
    LCL_LOW_2_label.config(state=tk.DISABLED)
    


    # Function to update countdown and trigger processing
    def update_countdown(remaining):
        nonlocal selected_duration  # Use nonlocal to modify the variable in the outer scope
        global stop_flag
        if stop_flag or remaining <= 0:
            window.title("Data Processing App")  # Restore window title after countdown

            if not stop_flag:
                process_data(
                    selected_folder, selected_duration,
                    UCL_UP_1.get(), LCL_UP_1.get(), UCL_UP_2.get(), LCL_UP_2.get(),
                    UCL_LOW_1.get(), LCL_LOW_1.get(), UCL_LOW_2.get(), LCL_LOW_2.get()
                )


            

            is_set_allowed = True
            duration_var.set(selected_duration)
        else:
            window.title(f"Countdown: {remaining // 60} minutes {remaining % 60} seconds")
            window.after(500, update_countdown, remaining - 1)

    # Check if countdown is already running and reset it
    if 'countdown_id' in globals() and window.after_cancel(countdown_id):
        print("Countdown reset")
    
    # Start the countdown
    countdown_id = window.after(500, update_countdown, duration_seconds)

stop_flag = False
    
def submit_stop():
    Time = datetime.now()
    Time_format = Time.strftime('%H:%M:%S')
    formatted_current_time = Time.strftime('%Y_%m_%d')
    with open(f"stop_time_{formatted_current_time}.txt", "w") as file:
        file.write(str(Time_format))

    # Update the stop time label
    stop_time_var.set(Time_format)

    ##print(f"Stop time has been saved to 'stop_time.txt'")
    global stop_flag
    stop_flag = True

def browse_folder():
    folder_selected = filedialog.askdirectory()
    folder_var.set(folder_selected)

# Function to save the selected path to a file
def save_path(path):
    file_path = os.path.join(os.path.expanduser("~"), ".selected_path.txt")
    with open(file_path, "w") as file:
        file.write(path)

# Function to load the selected path from a file
def load_path():
    file_path = os.path.join(os.path.expanduser("~"), ".selected_path.txt")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return file.read().strip()
    else:
        return ""
    
def save_duration(duration):
    file_path = os.path.join(os.path.expanduser("~"), ".selected_duration.txt")
    with open(file_path, "w") as file:
        file.write(duration)

# Function to load the selected duration from a file
def load_duration():
    file_path = os.path.join(os.path.expanduser("~"), ".selected_duration.txt")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return file.read().strip()
    else:
        return ""
    
import tkinter.simpledialog

from tkinter import simpledialog, messagebox

import tkinter.simpledialog
from tkinter import simpledialog, messagebox

def settings_action():
    # Prompt the user for a password
    password = simpledialog.askstring("Password", "Enter your password:")

    # Check if the password is correct
    if password and password == '1a2b3d4e':  # Replace 'your_password' with the actual password
        # Enable Entry widgets and buttons after correct password
        entry_folder.config(state=tk.NORMAL)
        duration_entry.config(state=tk.NORMAL)
        browse_button.config(state=tk.NORMAL)
   
        button_submit.config(state=tk.NORMAL)
        button_stoprun.config(state=tk.NORMAL)
  
        show_graph_button.config(state=tk.NORMAL)
        
        # Enable UCL and LCL Entry widgets
        UCL_UP_1_label.config(state=tk.NORMAL)
        LCL_UP_1_label.config(state=tk.NORMAL)
        UCL_UP_2_label.config(state=tk.NORMAL)
        LCL_UP_2_label.config(state=tk.NORMAL)
        UCL_LOW_1_label.config(state=tk.NORMAL)
        LCL_LOW_1_label.config(state=tk.NORMAL)
        UCL_LOW_2_label.config(state=tk.NORMAL)
        LCL_LOW_2_label.config(state=tk.NORMAL)
        
        messagebox.showinfo("Success", "Settings button clicked. Password is correct.")
    elif not password:
        # Password not entered, do nothing
        return
    else:
        # Disable Entry widgets and buttons if password is incorrect
        entry_folder.config(state=tk.DISABLED)
        duration_entry.config(state=tk.DISABLED)
        browse_button.config(state=tk.DISABLED)

        button_stoprun.config(state=tk.DISABLED)

        # Disable UCL and LCL Entry widgets
        UCL_UP_1_label.config(state=tk.DISABLED)
        LCL_UP_1_label.config(state=tk.DISABLED)
        UCL_UP_2_label.config(state=tk.DISABLED)
        LCL_UP_2_label.config(state=tk.DISABLED)
        UCL_LOW_1_label.config(state=tk.DISABLED)
        LCL_LOW_1_label.config(state=tk.DISABLED)
        UCL_LOW_2_label.config(state=tk.DISABLED)
        LCL_LOW_2_label.config(state=tk.DISABLED)
        
        messagebox.showerror("Access Denied", "Incorrect password. Access denied.")

import winsound  # Import winsound module
def check_code_before_close():
    user_input = simpledialog.askstring("Exit", "Enter code to close:")
    # Add your code verification logic here
    if user_input == "1a2b3d4e":
        window.destroy()
    else:
        # Play a notification sound if the code is incorrect
        messagebox.showerror("Close","ไม่อนุญาติ ให้ปิด")
 

# Function to handle the close button event
def on_close_button():
    check_code_before_close()









# Create main window
window = tk.Tk()
window.title("Data Processing App")
window.geometry("550x230")
window.resizable(False, False)

# Frame
frame = ttk.Frame(window, padding="10")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Label
label = ttk.Label(frame, text="Select Folder:")
label.grid(column=0, row=0, sticky=tk.W)




# Label for Duration
duration_label = ttk.Label(frame, text="Enter Duration (minutes):")
duration_label.grid(column=0, row=1, sticky=tk.W)

# Entry for Duration
duration_var = tk.StringVar()

duration_entry = ttk.Entry(frame, textvariable=duration_var, state=tk.DISABLED)  # Disabled initially
duration_entry.grid(column=1, row=1, sticky=(tk.W, tk.E))


button_submit = ttk.Button(frame, text="START RUN", command=submit_action,state=tk.DISABLED)
button_submit.grid(column=2, row=1, sticky=tk.W)

button_set = ttk.Button(frame, text="Setting", command=settings_action)
button_set.grid(column=3, row=2, sticky=tk.W)

# Browse Button
browse_button = ttk.Button(frame, text="Browse", command=browse_folder, state=tk.DISABLED)  # Disabled initially
browse_button.grid(column=2, row=0, sticky=tk.W)

options = list(df['Folder_Path'].unique())
display_values = list(df['Line_no'].unique())

# Create a Combobox (Dropdown)
folder_var = tk.StringVar()
entry_folder = ttk.Combobox(frame, textvariable=folder_var, values=display_values)
entry_folder.grid(column=1, row=0, sticky=tk.W, padx=10)

# Bind the selected value to the actual 'Folder_Path'
entry_folder.bind("<<ComboboxSelected>>", lambda event: folder_var.set(options[display_values.index(entry_folder.get())]))


# Show Graph Button
show_graph_button = ttk.Button(frame, text="Show Graph", command=show_graph_button)  # Disabled initially
show_graph_button.grid(column=3, row=1, sticky=tk.W)


stop_time_label = ttk.Label(frame, text="Last Stop Time:")
stop_time_label.grid(column=0, row=2, sticky=tk.W)

stop_time_var = tk.StringVar()
stop_time_entry = ttk.Entry(frame, textvariable=stop_time_var, state=tk.DISABLED)
stop_time_entry.grid(column=1, row=2, sticky=(tk.W, tk.E))

button_stoprun = ttk.Button(frame, text="STOP RUN", command=submit_stop,state=tk.DISABLED)
button_stoprun.grid(column=2, row=2, sticky=tk.W)

duration_label = ttk.Label(frame, text="Control UCL")
duration_label.grid(column=1, row=3, sticky=tk.W)
duration_label = ttk.Label(frame, text="Control LCL")
duration_label.grid(column=2, row=3, sticky=tk.W)

duration_label = ttk.Label(frame, text="Oil UP duration  1")
duration_label.grid(column=0, row=4, sticky=tk.W)

UCL_UP_1 = tk.StringVar()
UCL_UP_1_label = ttk.Entry(frame, textvariable=UCL_UP_1, state=tk.DISABLED)  # Disabled initially
UCL_UP_1_label.grid(column=1, row=4, sticky=(tk.W, tk.E))

LCL_UP_1 = tk.StringVar()
LCL_UP_1_label = ttk.Entry(frame, textvariable=LCL_UP_1, state=tk.DISABLED)  # Disabled initially
LCL_UP_1_label.grid(column=2, row=4, sticky=(tk.W, tk.E))

duration_label = ttk.Label(frame, text="Oil UP duration 2")
duration_label.grid(column=0, row=5, sticky=tk.W)

UCL_UP_2 = tk.StringVar()
UCL_UP_2_label = ttk.Entry(frame, textvariable=UCL_UP_2, state=tk.DISABLED)  # Disabled initially
UCL_UP_2_label.grid(column=1, row=5, sticky=(tk.W, tk.E))

LCL_UP_2 = tk.StringVar()
LCL_UP_2_label = ttk.Entry(frame, textvariable=LCL_UP_2, state=tk.DISABLED)  # Disabled initially
LCL_UP_2_label.grid(column=2, row=5, sticky=(tk.W, tk.E))

duration_label = ttk.Label(frame, text="Oil Low duration 1")
duration_label.grid(column=0, row=6, sticky=tk.W)

UCL_LOW_1 = tk.StringVar()
UCL_LOW_1_label = ttk.Entry(frame, textvariable=UCL_LOW_1, state=tk.DISABLED)  # Disabled initially
UCL_LOW_1_label.grid(column=1, row=6, sticky=(tk.W, tk.E))

LCL_LOW_1 = tk.StringVar()
LCL_LOW_1_label = ttk.Entry(frame, textvariable=LCL_LOW_1, state=tk.DISABLED)  # Disabled initially
LCL_LOW_1_label.grid(column=2, row=6, sticky=(tk.W, tk.E))

duration_label = ttk.Label(frame, text="Oil Low duration 2")
duration_label.grid(column=0, row=7, sticky=tk.W)

UCL_LOW_2 = tk.StringVar()
UCL_LOW_2_label = ttk.Entry(frame, textvariable=UCL_LOW_2, state=tk.DISABLED)  # Disabled initially
UCL_LOW_2_label.grid(column=1, row=7, sticky=(tk.W, tk.E))

LCL_LOW_2 = tk.StringVar()
LCL_LOW_2_label = ttk.Entry(frame, textvariable=LCL_LOW_2, state=tk.DISABLED)  # Disabled initially
LCL_LOW_2_label.grid(column=2, row=7, sticky=(tk.W, tk.E))

# Bind the close button event to the check_code_before_close function
window.protocol("WM_DELETE_WINDOW", on_close_button)

# Run the Tkinter main loop
window.mainloop()






