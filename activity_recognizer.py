# this program recognizes activities

import pandas as pd
from sklearn import svm
from sklearn.preprocessing import scale, StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split






#variables
PERSONS = ['michael'] #add names if there are more folders
ACTIVITIES = ['running', 'rowing', 'lifting', 'jumpingjacks']
test_size = 0.2



def data_set():
    df = pd.DataFrame()
    for i in range(0, len(PERSONS)):
        person = PERSONS[i]
        for j in range(0, len(ACTIVITIES)):
            activity = ACTIVITIES[j]
            for k in range(1, 6):
                data = pd.read_csv(f'{person}/{person}-{activity}-{k}.csv')
                data['activity'] = activity
                df = pd.concat([df, data], ignore_index=True)
    
    df.to_csv('combined_data.csv', index=False)



def transform_data(data):
    #removes columns and set activty to int
    data = data.drop(['id', 'timestamp'], axis='columns')
    data = data.replace('running', 0)
    data = data.replace('rowing', 1)
    data = data.replace('lifting', 2)
    data = data.replace('jumpingjacks', 3)

    #standardization
    standardization_data = data.drop(['activity'], axis = 1)
    scaled_data = scale(standardization_data)
    data_mean = standardization_data.copy()
    data_mean = scaled_data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data_mean)
    normalized_data = data_mean.copy()
    normalized_data = scaled_data

    return normalized_data


def model():
    #creates data with all collected datasets
    data_set()

    #open csv
    data = pd.read_csv('combined_data.csv')
    #dropping NaN
    data = data.dropna()

    #standardization
    normalized_data = transform_data(data)
    #test and train dataset 
    X = normalized_data
    y = data.activity
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.2)

    #classifier
    model = svm.SVC(kernel='rbf')
    model.fit(X_train, y_train)

    #model accuracy
    accuracy = model.score(X_test, y_test)
    print('-----------------------')
    print(f'The Accuracy of the Model with the test data is {accuracy}')
    print('-----------------------')

    return model

def estimated(model, data):
    estimated = model.predict([data])
    return estimated



    






