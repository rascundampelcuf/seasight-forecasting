
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

def NewPrediction(data, model):
    ndf = pd.DataFrame(columns=['lat','lon','sst'])
    df = data.groupby(['lat','lon'])['sst'].apply(list)
    for lat, lon, sst_list in df:
        if len(sst_list) >= 2:
            pred = model.predict(sst_list[:2])
            ndf.append({'lat': lat, 'lon': lon, 'sst': pred}, ignore_index = True)
    return ndf