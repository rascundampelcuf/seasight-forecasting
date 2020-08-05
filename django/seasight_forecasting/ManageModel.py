
import pickle
import numpy as np
import pandas as pd
from tensorflow.keras.models import model_from_json

def LoadRNNModel():
    json_file = open('../model/model2.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("../model/model2.h5")
    loaded_model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
    return loaded_model

def LoadLRModel():
    # load the model from disk
    loaded_model = pickle.load(open('../model/lr_model.pkl', 'rb'))
    return loaded_model

def NewPrediction(data, model):
    ndf = pd.DataFrame(columns=['lat','lon','sst'])
    df = data.groupby(['lat','lon'])['sst'].apply(list).reset_index()
    for _, row in df.iterrows():
        if len(row.sst) >= 2:
            val = np.array([[row.sst[:2]]])
            print(val)
            pred = model.predict(val)
            print(pred)
            ndf.append({'lat': row.lat, 'lon': row.lon, 'sst': pred}, ignore_index = True)
    return ndf

def LRPrediction(data, model):
    ndf = pd.DataFrame(columns=['lat','lon','sst'])
    df = data.groupby(['lat','lon'])['sst'].apply(list).reset_index()
    for _, row in df.iterrows():
        a = np.array(row.sst).reshape(-1,1)
        pred = model.predict(a)
        nr = pd.DataFrame({'lat': row.lat, 'lon': row.lon, 'sst': pred})
        ndf = ndf.append(nr, ignore_index = True)
    return ndf