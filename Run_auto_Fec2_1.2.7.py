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

import os





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

import pyodbc
import pandas as pd

# def show_warning(message):
#     print("message----------------------------------------------------------------------",message)
#     warning_window = tk.Toplevel()
#     warning_window.title("SPC Alert")
#     warning_window.geometry("600x280")
#     warning_window.configure(bg="red")

#     label = ttk.Label(warning_window, text=message, background="red", foreground="white", font=("Helvetica", 20))
#     label.pack(pady=20)

#     ok_button = ttk.Button(warning_window, text="Close", command=warning_window.destroy)
#     ok_button.pack()

import os
import sys
import pygame
    
pygame.mixer.init()

# Get the current directory
current_directory = os.getcwd()

# Define the path to the audio file
audio_file_path = os.path.join(current_directory, "Alam.mp3")

# List to keep track of warning windows
warning_windows = []

def show_warning(message):
    global warning_windows

    print("message----------------------------------------------------------------------", message)

    # Load and play the warning sound
    pygame.mixer.music.load(audio_file_path)
    pygame.mixer.music.play(loops=-1)

    # Create a new warning window
    warning_window = tk.Toplevel()
    warning_window.title("SPC Alert")
    warning_window.geometry("600x280")
    warning_window.configure(bg="red")

    label = ttk.Label(warning_window, text=message, background="red", foreground="white", font=("Helvetica", 20))
    label.pack(pady=20)

    def close_warning_window():
        pygame.mixer.music.stop()  # Stop the warning sound
        warning_window.destroy()  # Close the warning window

    ok_button = ttk.Button(warning_window, text="Close", command=close_warning_window)
    ok_button.pack()

    # Add the new warning window to the list
    warning_windows.append(warning_window)
def close_all_warnings():
    global warning_windows
    pygame.mixer.music.stop()  # Stop the warning soundwarning_window.destroy()  # Close the warning window
    for window in warning_windows:
        if window.winfo_exists():  # Check if the window still exists
            window.destroy()
    warning_windows = []  # Clear the list of windows


def read_stop_time(stop_time_filename):
    try:
        with open(stop_time_filename, 'r') as file:
            stop_time = file.readline().strip()
        if stop_time:
            try:
                # Parse the hour from the time string
                return int(datetime.strptime(stop_time, '%H:%M:%S').strftime('%H'))
            except ValueError:
                raise ValueError(f"time data '{stop_time}' does not match expected format '%H:%M:%S'")
        else:
            return None
    except FileNotFoundError:
        return None





def process_data(folder_path, selected_duration,UCL_UP_1,LCL_UP_1,UCL_UP_2,LCL_UP_2,UCL_LOW_1,LCL_LOW_1,UCL_LOW_2,LCL_LOW_2):

    current_date_1 = datetime.now().strftime("%Y_%m_%d")
    current_date = f"{current_date_1}B"

    matching_files = find_files_by_date(folder_path, current_date)
  
    if not matching_files:
        messagebox.showerror("Error", f"No files found for the current date {current_date}. Exiting.")
        return
    
    for file_path in matching_files:

        
        ################################################อ่านไฟล์ CSV
        data = pd.read_csv(file_path, delimiter=';', skiprows=3)
        for column in data.columns:
            print(f'Column: {column}, Type: {data[column].dtype}')

        ################################################อ่านค่าindex ล่าสุด + เวลาล่าสุด
        last_index = data.tail(1).index.item()
        last_timestamp = data['Time'].iloc[-1]
        next_index = last_index + 1
       
        # print(last_timestamp)
        #################################################อ่าน
        with open('last_index.txt', 'r') as file:
            read_content = file.read()
        

# Split the content into last_index and next_index
        read_values = read_content.split(',')
        read_last_index = int(read_values[0])
        read_next_index = int(read_values[1])
        read_last_timestamp = datetime.strptime(read_values[2], '%H:%M:%S').time()

# Print the read values
        print("Read Last Index:", read_last_index)
        print("Read Next Index:", read_next_index)
        print("Read Last Timestamp:", read_last_timestamp)
        
        data['Time'] = pd.to_datetime(data['Time']).dt.time
        

        read_last_timestamp = datetime.strptime(str(read_last_timestamp), '%H:%M:%S').time()
        datafilter_ok = data[data['Time'] > read_last_timestamp]
        datafilter_ok.reset_index(drop=True, inplace=True)
        # print(datafilter_ok)
        
        
        from datetime import time
 
        formatted_time_dt = datetime.strptime(last_timestamp, '%H:%M:%S').time()
# Check if read_last_timestamp is greater than the current time
        if read_last_timestamp > formatted_time_dt :
            read_last_timestamp = time(0, 0, 0).strftime('%H:%M:%S')
        else:
            read_last_timestamp = formatted_time_dt
            pass


        oil_low_numbers = [1,2]  # Add more Oil Low Numbers as needed
        data = data[data['Oil Up duration'] != '.0']
        oil_types = ["Oil Up duration", "Oil Upduration"]
        for oil_low_number in oil_low_numbers:
            data_oil_up = data[data['Oil Up number'] == oil_low_number]
            print("data_oil_up",data_oil_up)
            barcode = str(data_oil_up['Barcode'].iloc[0]) 
            data_oil_up['Time'] = pd.to_datetime(data_oil_up['Time'], format='%H:%M:%S')

            data_oil_up['Oil Up duration'] = pd.to_numeric(data_oil_up['Oil Up duration'], errors='coerce')
            data_oil_up = data_oil_up[(data_oil_up['Oil Up duration'] != 0) & (~data_oil_up['Oil Up duration'].isna())]

            data_oil_up['Hour'] = data_oil_up['Time'].dt.hour
            last_value = data_oil_up[data_oil_up['Oil Up number'] == oil_low_number]['Oil Up duration'].iloc[-1]
            
            
            data_oil_up['Hour'] = data_oil_up['Time'].dt.hour
            filtered_data = data_oil_up[['Oil Up duration', 'Hour']]
            data_oil_up['Oil Up duration'] = pd.to_numeric(data_oil_up['Oil Up duration'], errors='coerce')
            data_oil_up['Time'].fillna(pd.Timedelta(seconds=0), inplace=True)
            
            process_data = data_oil_up['Oil Up duration'].values
          
            nan_mask = np.isnan(process_data)

            # Use boolean indexing to filter out NaN values
            filtered_process_data = process_data[~nan_mask]


            hourly_avg = data_oil_up.groupby('Hour')['Oil Up duration'].mean()
            print("hourly_avg",{oil_low_number},hourly_avg)

            latest_hour = hourly_avg.index[-1]
            latest_value = hourly_avg.iloc[-1]
            print("latest_hour***********************************************************************",latest_hour)
            print("latest_value**********************************************************************",latest_value)
            
            stop_file_path = f'stop_time_{current_date_1}.txt'
            stop_hour = read_stop_time(stop_file_path)
            print("stop_hour",stop_hour)

            if stop_hour is not None and stop_hour == latest_hour:
                hour_to_use = latest_hour
                print("Stop hour found, using latest hour:", hour_to_use)
            else:
                previous_hour = (latest_hour - 1) % 24 if latest_hour > 0 else latest_hour
                hour_to_use = previous_hour
                print("No stop hour found, using previous hour:", hour_to_use)
            max_hour_value = hourly_avg.loc[hour_to_use]


            Diff = abs(last_value - max_hour_value)

            print("last_value",last_value)
            print("max_hour_value",max_hour_value)
            print("Diff",Diff)
            
            filename = f'max_hour_value_up{oil_low_number}.txt'

            with open(filename, 'w') as file:
                file.write(str(max_hour_value))

            time = datetime.now()
            formatted_time = time.strftime("%Y-%m-%d %H:%M")

         


            datafilter_ok_1 = datafilter_ok[datafilter_ok['Oil Up number'] == oil_low_number]


            result_array = datafilter_ok_1['Oil Up duration'].values
            result_array = result_array.astype(float)
            result_array = result_array[result_array != 0]
            
            with open(f'max_hour_value_up{oil_low_number}.txt', 'r') as file:
                max_hour_value = file.read()
                print(f"max_hour_value_up:",{oil_low_number},max_hour_value)
                max_hour_value = float(max_hour_value)
      
            result_array -= max_hour_value
         

            for value in result_array:  
                print("Current value:", value)
                print("oil_low_number:", oil_low_number)
                print("Diff before calculation:", Diff)
                Diff = abs(value)
                print("Diff after calculation:", Diff)
 
                time = datetime.now()
                formatted_time = time.strftime("%Y-%m-%d %H:%M")
                message = ""
                if oil_low_number == 1:
                    
                    print("Entered oil_low_number == 1 block")
                    U_Low_1 = float(UCL_UP_1)
                    L_Low_1 = float(LCL_UP_1)
                        
                    if Diff > U_Low_1 or Diff > L_Low_1:
                        
                        print("Diff is greater than U_Low_1 or L_Low_1")
                        message = (
                            f"Time : {formatted_time} \n"
                            f"Process : Oil Up duration \n"
                            f"Head : {oil_low_number} \n"
                            f"Avg last hour: {max_hour_value:.4f} \n"
                            f"Diff: {Diff:.4f} \n"
                        )
                            
                        with open(f"Oil_Up_duration_{oil_low_number}.txt", "a") as output_file:
                               
                            output_file.write(message)
                            show_warning(message)
                        break  

                if oil_low_number == 2:
                    print("Entered oil_low_number == 2 block")
                    U_Low_2 = float(UCL_UP_2)
                    L_Low_2 = float(LCL_UP_2)
            
              
                    if Diff > U_Low_2 or Diff > L_Low_2:
                        print("Diff is greater than U_Low_2 or L_Low_2")
                        message = (
                                f"Time : {formatted_time} \n"
                                f"Process : Oil Up duration \n"
                                f"Head : {oil_low_number} \n"
                                f"Avg last hour: {max_hour_value:.4f} \n"
                                f"Diff: {Diff:.4f} \n"
                        )
                        with open(f"Oil_Up_duration_{oil_low_number}.txt", "a") as output_file:
                              
                            output_file.write(message)
                            show_warning(message)
                        break  
        

        oil_low_numbers = [1,2]  # Add more Oil Low Numbers as needed
        data = data[data['Oil Low duration'] != '.0']
        oil_types = ["Oil Up duration", "Oil Low duration"]
        for oil_low_number in oil_low_numbers:
            data_oil_low = data[data['Oil Low number'] == oil_low_number]
            print("Data**********************************************************",data_oil_low)
            data_oil_low['Time'] = pd.to_datetime(data_oil_low['Time'], format='%H:%M:%S')

            data_oil_low['Oil Low duration'] = pd.to_numeric(data_oil_low['Oil Low duration'], errors='coerce')
          
            data_oil_low['Hour'] = data_oil_low['Time'].dt.hour
            last_value = data_oil_low[data_oil_low['Oil Low number'] == oil_low_number]['Oil Low duration'].iloc[-1]
            
            
            data_oil_low['Hour'] = data_oil_low['Time'].dt.hour
            filtered_data = data_oil_low[['Oil Low duration', 'Hour']]
            data_oil_low['Oil Low duration'] = pd.to_numeric(data_oil_low['Oil Low duration'], errors='coerce')
            data_oil_low['Time'].fillna(pd.Timedelta(seconds=0), inplace=True)
            
            process_data = data_oil_low['Oil Low duration'].values
          
            nan_mask = np.isnan(process_data)

            # Use boolean indexing to filter out NaN values
            filtered_process_data = process_data[~nan_mask]


            hourly_avg = data_oil_low.groupby('Hour')['Oil Low duration'].mean()
            print("hourly_avg",{oil_low_number},hourly_avg)

            latest_hour = hourly_avg.index[-1]
            latest_value = hourly_avg.iloc[-1]

            stop_file_path = f'stop_time_{current_date_1}.txt'
            stop_hour = read_stop_time(stop_file_path)
            print("stop_hour",stop_hour)

            if stop_hour is not None and stop_hour == latest_hour:
                hour_to_use = latest_hour
                print("Stop hour found, using latest hour:", hour_to_use)
            else:
                previous_hour = (latest_hour - 1) % 24 if latest_hour > 0 else latest_hour
                hour_to_use = previous_hour
                print("No stop hour found, using previous hour:", hour_to_use)
            max_hour_value = hourly_avg.loc[hour_to_use]


            Diff = abs(last_value - max_hour_value)

            print("last_value",last_value)
            print("max_hour_value",max_hour_value)
            print("Diff",Diff)
            
            filename = f'max_hour_value{oil_low_number}.txt'

            with open(filename, 'w') as file:
                file.write(str(max_hour_value))

            time = datetime.now()
            formatted_time = time.strftime("%Y-%m-%d %H:%M")



            datafilter_ok_1 = datafilter_ok[datafilter_ok['Oil Low number'] == oil_low_number]

            
            result_array = datafilter_ok_1['Oil Low duration'].values
            
            result_array = result_array.astype(float)
            result_array = result_array[result_array != 0]
           
            print(f"Average for Oil Low Number {oil_low_number}: {result_array}")
            
            with open(f'max_hour_value{oil_low_number}.txt', 'r') as file:
                max_hour_value = file.read()
                print(f"max_hour_value:",{oil_low_number},max_hour_value)
                max_hour_value = float(max_hour_value)
                
      
            result_array -= max_hour_value
            print(result_array)
            
            for value in result_array:
               
                Diff = abs(value)
                time = datetime.now()
                formatted_time = time.strftime("%Y-%m-%d %H:%M")
                message = ""
                if oil_low_number == 1:
                    U_Low_1 = float(UCL_LOW_1)
                    L_Low_1 = float(LCL_LOW_1)
       
              
                    if Diff > U_Low_1 or Diff > L_Low_1:
                        message = (
                            f"Time : {formatted_time} \n"
                            f"Process : Oil Low duration \n"
                            f"Head : {oil_low_number} \n"
                            f"Avg last hour: {max_hour_value:.4f} \n"
                            f"Diff: {Diff:.4f} \n"
                   
                        )
                        with open(f"Oil_Low_duration_{oil_low_number}.txt", "a") as output_file:
                               
                            output_file.write(message)
                            show_warning(message)
                        break  
                if oil_low_number == 2:
                    U_Low_2 = float(UCL_LOW_2)
                    L_Low_2 = float(LCL_LOW_2)
           
                 
                    if Diff > U_Low_2 or Diff > L_Low_2:
                        message = (
                                f"Time : {formatted_time} \n"
                                f"Process : Oil Low duration \n"
                                f"Head : {oil_low_number} \n"
                                f"Avg last hour: {max_hour_value:.4f} \n"
                                f"Diff: {Diff:.4f} \n"
                        )
                        with open(f"Oil_Low_duration_{oil_low_number}.txt", "a") as output_file:
                              
                                output_file.write(message)
                                show_warning(message)
                        break  

        with open('last_index.txt', 'w') as file:
            file.write(f"{last_index},{next_index},{read_last_timestamp}")   
       
            

    submit_action()      
            
from tkinter import Tk, messagebox
def plot_graph(hourly_avg_1, hourly_avg_2, spec_upper_limit_1, spec_lower_limit_1, spec_avg_1,
               spec_upper_limit_2, spec_lower_limit_2, spec_avg_2, head):
    try:
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
        graph1_path = f'Graph1_{head}.png'
        plt.savefig(graph1_path)
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
        graph2_path = f'Graph2_{head}.png'
        plt.savefig(graph2_path)
        plt.close()

        # Display the images in Tkinter window
        show_image(graph1_path)
        show_image(graph2_path)

    except Exception as e:
        root = Tk()
        root.withdraw()
        messagebox.showerror("Error", str(e))
        root.destroy()

from datetime import datetime

def process_graph(folder_path, selected_duration,UCL_UP_1,LCL_UP_1,UCL_UP_2,LCL_UP_2,UCL_LOW_1,LCL_LOW_1,UCL_LOW_2,LCL_LOW_2):
    with open(f'max_hour_value_Up1.txt', 'r') as file:
                    max_up_1 = file.read()
    with open(f'max_hour_value_Up2.txt', 'r') as file:
                    max_up_2 = file.read()
    with open(f'max_hour_value1.txt', 'r') as file:
                    max_low_1 = file.read()
    with open(f'max_hour_value2.txt', 'r') as file:
                    max_low_2 = file.read()

    
    UCL_UP_1   = float(max_up_1) + float(UCL_UP_1)
    LCL_UP_1   = float(max_up_1) - float(LCL_UP_1)
    
    UCL_UP_2   = float(max_up_2) + float(UCL_UP_2)
    LCL_UP_2   = float(max_up_2) - float(LCL_UP_2)
     
    UCL_LOW_1  = float(max_low_1) + float(UCL_LOW_1)
    LCL_LOW_1  = float(max_low_1) - float(LCL_LOW_1)
    
    UCL_LOW_2   = float(max_low_2) + float(UCL_LOW_2)
    LCL_LOW_2   = float(max_low_2) - float(LCL_LOW_2)

    
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


        ##print("*********************************************data", data)

        oil_up_numbers = [1, 2]  # Add more Oil Low Numbers as needed
        head = "Oil Up duration"
        for oil_up_number in oil_up_numbers:
            data_oil_low = data[data['Oil Up number'] == oil_up_number]
            if oil_up_number == 1:
                USL = UCL_UP_1
                LSL = LCL_UP_1
              
            elif oil_up_number == 2:
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
            if oil_up_number == 1:
                spec_upper_limit_1 = float(USL)
                spec_lower_limit_1 = float(LSL)
            elif oil_up_number == 2:
                spec_upper_limit_2 = float(USL)
                spec_lower_limit_2 = float(LSL)

# Calculate spec_avg and std_dev based on the selected oil_low_number
            if oil_up_number == 1:
                spec_avg_1 = (spec_upper_limit_1 + spec_lower_limit_1) / 2
                
            elif oil_up_number == 2:
                spec_avg_2 = (spec_upper_limit_2 + spec_lower_limit_2) / 2
               

            # Extract hourly averages for each Oil Low Number
            if oil_up_number == 1:
                hourly_avg_up_1 = hourly_avg
            elif oil_up_number == 2:
                hourly_avg_up_2 = hourly_avg
                print(hourly_avg_up_1)
                print(hourly_avg_up_2)
        
        plot_graph(hourly_avg_up_1, hourly_avg_up_2, spec_upper_limit_1, spec_lower_limit_1, spec_avg_1,
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

    
import tkinter as tk
from tkinter import messagebox

# Global variables
stop_flag = False
is_set_allowed = False
countdown_id = None

def submit_action():
    global stop_flag, is_set_allowed, countdown_id
    stop_flag = True  # Set the stop flag to stop any ongoing processes

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
    save_values()
    # Load saved values
    loaded_values = load_values()
    print("loaded_values",loaded_values)
    if len(loaded_values) == 9:
        duration_var.set(loaded_values[0])
        UCL_UP_1.set(loaded_values[1])
        LCL_UP_1.set(loaded_values[2])
        UCL_UP_2.set(loaded_values[3])
        LCL_UP_2.set(loaded_values[4])
        UCL_LOW_1.set(loaded_values[5])
        LCL_LOW_1.set(loaded_values[6])
        UCL_LOW_2.set(loaded_values[7])
        LCL_LOW_2.set(loaded_values[8])
    else:
        # Handle case where saved values are incomplete
        messagebox.showwarning("Warning", "Saved values file is incomplete or corrupted.")
        # You may decide how to handle this scenario, e.g., resetting to defaults

    # Allow set to be modified after submitting
    is_set_allowed = True

    # Disable Entry widgets and buttons during countdown
    entry_folder.config(state=tk.DISABLED)
    duration_entry.config(state=tk.DISABLED)
    browse_button.config(state=tk.DISABLED)
    button_stoprun.config(state=tk.NORMAL)
 
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
        global stop_flag, is_set_allowed, countdown_id

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
            countdown_id = window.after(1000, update_countdown, remaining - 1)

    # Check if countdown is already running and cancel it
    if countdown_id is not None:
        window.after_cancel(countdown_id)
        print("Countdown reset")

    # Start the countdown
    stop_flag = False  # Reset the stop flag for the new countdown
    countdown_id = window.after(1000, update_countdown, duration_seconds)

    
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


def save_values():
    file_path = os.path.join(os.path.expanduser("~"), "saved_values.txt")
    with open(file_path, "w") as file:
        file.write(duration_var.get() + "\n")
        file.write(UCL_UP_1.get() + "\n")
        file.write(LCL_UP_1.get() + "\n")
        file.write(UCL_UP_2.get() + "\n")
        file.write(LCL_UP_2.get() + "\n")
        file.write(UCL_LOW_1.get() + "\n")
        file.write(LCL_LOW_1.get() + "\n")
        file.write(UCL_LOW_2.get() + "\n")
        file.write(LCL_LOW_2.get() + "\n")
        
def load_values():
    file_path = os.path.join(os.path.expanduser("~"), "saved_values.txt")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
            if len(lines) >= 9:
                return [line.strip() for line in lines]
    return [""] * 9  # Return empty values if file doesn't exist or is incomplete

# Function to initialize values
def initialize_values():
    loaded_values = load_values()
    if len(loaded_values) == 9:
        duration_var.set(loaded_values[0])
        UCL_UP_1.set(loaded_values[1])
        LCL_UP_1.set(loaded_values[2])
        UCL_UP_2.set(loaded_values[3])
        LCL_UP_2.set(loaded_values[4])
        UCL_LOW_1.set(loaded_values[5])
        LCL_LOW_1.set(loaded_values[6])
        UCL_LOW_2.set(loaded_values[7])
        LCL_LOW_2.set(loaded_values[8])
    else:
        messagebox.showwarning("Warning", "Saved values file is incomplete or corrupted.")

import tkinter.simpledialog

from tkinter import simpledialog, messagebox

import tkinter.simpledialog
from tkinter import simpledialog, messagebox

def settings_action():
    
    password = simpledialog.askstring("Password", "Enter your password:")
    if password and password == '1a2b3d4e':
        entry_folder.config(state=tk.NORMAL)
        duration_entry.config(state=tk.NORMAL)
        browse_button.config(state=tk.NORMAL)
        button_submit.config(state=tk.NORMAL)
        button_stoprun.config(state=tk.NORMAL)
        show_graph_button.config(state=tk.NORMAL)
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
        return
    else:
        entry_folder.config(state=tk.DISABLED)
        duration_entry.config(state=tk.DISABLED)
        browse_button.config(state=tk.DISABLED)
        button_submit.config(state=tk.DISABLED)
        button_stoprun.config(state=tk.DISABLED)
        show_graph_button.config(state=tk.DISABLED)
        UCL_UP_1_label.config(state=tk.DISABLED)
        LCL_UP_1_label.config(state=tk.DISABLED)
        UCL_UP_2_label.config(state=tk.DISABLED)
        LCL_UP_2_label.config(state=tk.DISABLED)
        UCL_LOW_1_label.config(state=tk.DISABLED)
        LCL_LOW_1_label.config(state=tk.DISABLED)
        UCL_LOW_2_label.config(state=tk.DISABLED)
        LCL_LOW_2_label.config(state=tk.DISABLED)
        messagebox.showerror("Error", "Incorrect password. Settings not enabled.")
import winsound  # Import winsound module
def check_code_before_close():
    user_input = simpledialog.askstring("Exit", "Enter code to close:")
    # Add your code verification logic here
    if user_input == "1a2b3d4e":
        window.destroy()
        save_values()
    else:
        # Play a notification sound if the code is incorrect
        messagebox.showerror("Close","ไม่อนุญาติ ให้ปิด")
 

# Function to handle the close button event
def on_close_button():
    check_code_before_close()


loaded_values = load_values()




    

# Create main window
window = tk.Tk()
window.title("Data Processing App")
window.geometry("458x195")
window.resizable(False, False)

# Frame
frame = ttk.Frame(window, padding="10")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Label
label = ttk.Label(frame, text="Select Folder:")
label.grid(column=0, row=0, sticky=tk.W)

# Entry for Folder
folder_var = tk.StringVar()
folder_var.set(load_path())
entry_folder = ttk.Entry(frame, textvariable=folder_var, state=tk.DISABLED)  # Disabled initially
entry_folder.grid(column=1, row=0, sticky=(tk.W, tk.E))

# Label for Duration
duration_label = ttk.Label(frame, text="Enter Duration (min):")
duration_label.grid(column=0, row=1, sticky=tk.W)

# Entry for Duration
duration_var = tk.StringVar()
duration_var.set(loaded_values[0])  # Set the initial value
duration_entry = ttk.Entry(frame, textvariable=duration_var, state=tk.DISABLED)  # Disabled initially
duration_entry.grid(column=1, row=1, sticky=(tk.W, tk.E))

style = ttk.Style()
style.configure("Green.TButton",foreground="Green")
button_submit = ttk.Button(frame, text="START RUN", command=submit_action ,style ="Green.TButton")
button_submit.grid(column=2, row=1, sticky=tk.W)



button_closeall = ttk.Button(frame, text="Close ALL", command=close_all_warnings)
button_closeall.grid(column=3, row=2, sticky=tk.W)

# Browse Button
browse_button = ttk.Button(frame, text="Browse", command=browse_folder, state=tk.DISABLED)  # Disabled initially
browse_button.grid(column=2, row=0, sticky=tk.W)

# Show Graph Button
show_graph_button = ttk.Button(frame, text="Show Graph", command=show_graph_button)  # Disabled initially
show_graph_button.grid(column=3, row=0, sticky=tk.W)

button_set = ttk.Button(frame, text="Setting", command=settings_action)
button_set.grid(column=3, row=1, sticky=tk.W)

stop_time_label = ttk.Label(frame, text="Last Stop Time:")
stop_time_label.grid(column=0, row=2, sticky=tk.W)

stop_time_var = tk.StringVar()
stop_time_entry = ttk.Entry(frame, textvariable=stop_time_var, state=tk.DISABLED)
stop_time_entry.grid(column=1, row=2, sticky=(tk.W, tk.E))

style = ttk.Style()
style.configure("Red.TButton", foreground="red")

button_stoprun = ttk.Button(frame, text="STOP RUN", command=submit_stop, state=tk.DISABLED, style="Red.TButton")
button_stoprun.grid(column=2, row=2, sticky=tk.W)

duration_label = ttk.Label(frame, text="Control UCL")
duration_label.grid(column=1, row=3, sticky=tk.W)
duration_label = ttk.Label(frame, text="Control LCL")
duration_label.grid(column=2, row=3, sticky=tk.W)

duration_label = ttk.Label(frame, text="Oil UP duration 1")
duration_label.grid(column=0, row=4, sticky=tk.W)

UCL_UP_1 = tk.StringVar()
UCL_UP_1.set(loaded_values[1])  # Set the initial value
UCL_UP_1_label = ttk.Entry(frame, textvariable=UCL_UP_1, state=tk.DISABLED)  # Disabled initially
UCL_UP_1_label.grid(column=1, row=4, sticky=(tk.W, tk.E))

LCL_UP_1 = tk.StringVar()
LCL_UP_1.set(loaded_values[2])  # Set the initial value
LCL_UP_1_label = ttk.Entry(frame, textvariable=LCL_UP_1, state=tk.DISABLED)  # Disabled initially
LCL_UP_1_label.grid(column=2, row=4, sticky=(tk.W, tk.E))

duration_label = ttk.Label(frame, text="Oil UP duration 2")
duration_label.grid(column=0, row=5, sticky=tk.W)

UCL_UP_2 = tk.StringVar()
UCL_UP_2.set(loaded_values[3])  # Set the initial value
UCL_UP_2_label = ttk.Entry(frame, textvariable=UCL_UP_2, state=tk.DISABLED)  # Disabled initially
UCL_UP_2_label.grid(column=1, row=5, sticky=(tk.W, tk.E))

LCL_UP_2 = tk.StringVar()
LCL_UP_2.set(loaded_values[4])  # Set the initial value
LCL_UP_2_label = ttk.Entry(frame, textvariable=LCL_UP_2, state=tk.DISABLED)  # Disabled initially
LCL_UP_2_label.grid(column=2, row=5, sticky=(tk.W, tk.E))

duration_label = ttk.Label(frame, text="Oil Low duration 1")
duration_label.grid(column=0, row=6, sticky=tk.W)

UCL_LOW_1 = tk.StringVar()
UCL_LOW_1.set(loaded_values[5])  # Set the initial value
UCL_LOW_1_label = ttk.Entry(frame, textvariable=UCL_LOW_1, state=tk.DISABLED)  # Disabled initially
UCL_LOW_1_label.grid(column=1, row=6, sticky=(tk.W, tk.E))

LCL_LOW_1 = tk.StringVar()
LCL_LOW_1.set(loaded_values[6])  # Set the initial value
LCL_LOW_1_label = ttk.Entry(frame, textvariable=LCL_LOW_1, state=tk.DISABLED)  # Disabled initially
LCL_LOW_1_label.grid(column=2, row=6, sticky=(tk.W, tk.E))

duration_label = ttk.Label(frame, text="Oil Low duration 2")
duration_label.grid(column=0, row=7, sticky=tk.W)

UCL_LOW_2 = tk.StringVar()
UCL_LOW_2.set(loaded_values[7])  # Set the initial value
UCL_LOW_2_label = ttk.Entry(frame, textvariable=UCL_LOW_2, state=tk.DISABLED)  # Disabled initially
UCL_LOW_2_label.grid(column=1, row=7, sticky=(tk.W, tk.E))

LCL_LOW_2 = tk.StringVar()
LCL_LOW_2.set(loaded_values[8])  # Set the initial value
LCL_LOW_2_label = ttk.Entry(frame, textvariable=LCL_LOW_2, state=tk.DISABLED)  # Disabled initially
LCL_LOW_2_label.grid(column=2, row=7, sticky=(tk.W, tk.E))

version_label = ttk.Label(frame, text="V.1.2.7")
version_label.grid(column=3, row=7, sticky=tk.W)
# Bind the close button event to the check_code_before_close function
window.protocol("WM_DELETE_WINDOW", on_close_button)

if all(value == "" for value in loaded_values):
    messagebox.showwarning("Warning", "(กรุณา setting ก่อน START RUN) \n Please set the initial values before START RUN")
else:
    # Call the submit_action() function if there are loaded values
    submit_action()
# Run the Tkinter main loop
window.mainloop()






# pyinstaller  Run_auto_Fec2.py
# pyinstaller.exe --noconsole Run_auto_Fec2.py   ใช้อันนี้ เพื่อไม่โชว์ console
#pyinstaller --noconsole Run_auto_Fec2_1.2.4.py 