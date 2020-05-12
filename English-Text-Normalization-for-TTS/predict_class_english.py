import numpy as np
import xgboost as xgb
import gc
import random
import os

random.seed(827)


_DEFAULT_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models/xgb_modelV3')


def context_window_transform(data, pad_size):
    max_num_features = 25
    boundary_letter = -1
    
    pre = np.zeros(max_num_features)
    pre = [pre for x in np.arange(pad_size)]
    data = pre + data + pre
    neo_data = []
    for i in np.arange(len(data) - pad_size * 2):
        row = []
        for x in data[i : i + pad_size * 2 + 1]:
            row.append([boundary_letter])
            row.append(x)
        row.append([boundary_letter])
        neo_data.append([int(x) for y in row for x in y])
    
    return neo_data


def predict_class_(word_list, path=_DEFAULT_MODEL_PATH):
    max_num_features = 25
    pad_size = 1
    space_letter = 0
    x_data = []
    
    for x in word_list:
        x_row = np.ones(max_num_features, dtype=int) * space_letter
        for xi, i in zip(list(str(x)), np.arange(max_num_features)):
            x_row[i] = ord(xi)
        x_data.append(x_row)
    
    x_data = np.array(context_window_transform(x_data, pad_size))
    gc.collect()
    x_data = np.array(x_data)
    
    dtest=xgb.DMatrix(x_data)
    
    #############  2. LOAD PRE-TRAINED MODEL  #############
    
    bst = xgb.Booster({'nthread':4})
    bst.load_model(path)
    
    ##############  3. PREDICT CLASSES  ###############
    
    #print("Predicting....")
    pred = bst.predict(dtest)
    labels = ['PLAIN', 'PUNCT', 'DATE', 'LETTERS', 'CARDINAL', 'VERBATIM', 'DECIMAL', 'MEASURE', 'MONEY', 
              'ORDINAL', 'TIME', 'ELECTRONIC', 'DIGIT', 'FRACTION', 'TELEPHONE', 'ADDRESS']
    pred = [labels[int(x)] for x in pred]
    #print(pred)
    return pred
