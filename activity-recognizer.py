# this program recognizes activities
from DIPPID import SensorUDP
from sklearn import svm
import pandas as pd # for loading the data from csv
import numpy as np
from sklearn.preprocessing import scale, StandardScaler, MinMaxScaler


#connect phone
PORT = 5700
sensor = SensorUDP(PORT)

#variables
PERSONS = ['michael']
ACTIVITIES = ['running', 'rowing', 'lifting', 'jumpingjacks']


def data_set():
    df = pd.DataFrame()
    for i in range(0, len(PERSONS)):
        person = PERSONS[i]
        print(person)
        for j in range(0, len(ACTIVITIES)):
            activity = ACTIVITIES[j]
            print(activity)
            for k in range(1, 6):
                data = pd.read_csv(f'{person}/{person}-{activity}-{k}.csv')
                data['activity'] = activity
                df = pd.concat([df, data], ignore_index=True)
    
    df.to_csv('combined_data.csv', index=False)


data_set()





