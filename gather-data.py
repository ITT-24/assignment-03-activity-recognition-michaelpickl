# this program gathers sensor data

from DIPPID import SensorUDP
import time
import os
import re
import pandas as pd
import sys

#connect phone 
PORT = 5700
sensor = SensorUDP(PORT)

#variables
ACTIVITIES = ['running', 'rowing', 'lifting', 'jumpingjacks']
COLUMNS = ['timestamp','acc_x','acc_y','acc_z','gyro_x','gyro_y','gyro_z']
MAX_TIME = 10000
# AS: hard coded :(
NAME = 'tina'
start_logging = False
acc_x = acc_y = acc_z = 0
gyro_x = gyro_y = gyro_z = 0
data_set = []


#get activity
print('showing the possible activites')
print('--------------------')
for i in range(0, len(ACTIVITIES)):
    print(f'{ACTIVITIES[i]} with the ID {i}')

print('--------------------')

print('choose activity by pressing the number and enter afterwards')
activity = ACTIVITIES[int(input())]

#check and create folder
# https://stackoverflow.com/questions/273192/how-do-i-create-a-directory-and-any-missing-parent-directories
if not os.path.exists(NAME):
    os.makedirs(NAME)

#function generated by chatgpt
folder_path = f'{NAME}'
def get_next_filename(folder_path, name, activity):
    # Regular expression to match the files in the desired format
    pattern = re.compile(rf'^{re.escape(name)}-{re.escape(activity)}-(\d+)\.csv$')
    
    max_number = 0
    
    for filename in os.listdir(folder_path):
        match = pattern.match(filename)
        if match:
            number = int(match.group(1))
            if number > max_number:
                max_number = number
    
    # The new file will have the next higher number
    new_number = max_number + 1
    new_filename = f"{name}-{activity}-{new_number}.csv"
    
    return new_filename

#creating filename
filename = get_next_filename(folder_path, NAME, activity)

#create csv
def save_data_to_csv(folder_path, filename, df):
    # write data in CSV
    df.to_csv(os.path.join(folder_path, filename), index=False)
    print(f"Data saved the folder")

#get data
#data: id, timestamp, acc_x, acc_y, acc_z, gyro_x, gyro_y,gyro_z
def handle_accelerometer(data): 
    global acc_x, acc_y, acc_z
    acc_x = data.get("x")
    acc_y = data.get("y")
    acc_z = data.get("z")

def handle_gyroscope(data):
    global gyro_x, gyro_y, gyro_z
    gyro_x = data.get("x")
    gyro_y = data.get("y")
    gyro_z = data.get("z")

def get_data():
    sensor.register_callback('gyroscope', handle_accelerometer)
    sensor.register_callback('gyroscope', handle_gyroscope)
    timer = time.time()
    return[timer, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z]

#buttons to start getting data and to stop
def handle_button_press(data):
    global start_logging
    if int(data) == 1:
        print('button one pressed')
        start_logging = True

# button 1 for starting the logging
print(f'press Button 1 zu start {activity}')
sensor.register_callback('button_1', handle_button_press)

while True:
    if(start_logging):
        df = pd.DataFrame(columns=COLUMNS)
        for i in range(0, MAX_TIME):
            data_row = get_data()
            if(data_row):
                df.loc[len(df)] = data_row
            print(i)
            time.sleep(0.001)
        save_data_to_csv(folder_path, filename, df)
        sys.exit()
  


