# -*- encoding: utf-8 -*-
import pandas as pd
import os
import joblib
import pickle
import matplotlib.pyplot as plt
import shutil
from nlp_core.config.conf_params import get_path_fig_single_predict
from sklearn.feature_extraction.text import TfidfVectorizer


# def read_dict_IID_label_file(path_dict):
#     df_IID_to_label = pd.read_csv(path_dict, delimiter='|')
#     dict_label_to_IID = {}
#     dict_IID_to_label = {}
#     for index, row in df_IID_to_label.iterrows():
#         dict_IID_to_label[row['IID']] = row['label']
#         dict_label_to_IID[row['label']] = row['IID']
#     return dict_label_to_IID, dict_IID_to_label

def _read_dict_IID_label_file_single(path_dict):
    df_IID_to_label = pd.read_csv(path_dict, delimiter='|')
    dict_label_to_IID = {}
    for index, row in df_IID_to_label.iterrows():
        dict_label_to_IID[row['label']] = row['IID']
    return dict_label_to_IID


def _read_dict_IID_path_file(path_dict):
    df_IID_to_label = pd.read_csv(path_dict, delimiter='|')
    dict_IID_to_label = {}
    for index, row in df_IID_to_label.iterrows():
        dict_IID_to_label[row['IID']] = row['path']
    return dict_IID_to_label


def _load_vectorizer(path_vectorizer):
    print('Loading app_model vectorizer at...')
    result_vectorizer = None
    if os.path.isfile(path_vectorizer):
        # result_vectorizer = joblib.load(path_vectorizer)
        result_vectorizer = pickle.load(open(path_vectorizer, 'rb'))
    return result_vectorizer


def _load_model(path_model):
    print('Loading app_model classification app_model...')
    if os.path.isfile(path_model):
        # return joblib.load(path_model)
        return pickle.load(open(path_model, 'rb'))
    else:
        return None


def _convert_ndarray_data(vectorizer_nd, data_set):
    x_train = [data_set]
    if vectorizer_nd == None:
        print('vectorizer_nd')
        vectorizer_nd = TfidfVectorizer()
        vectorizer_nd.fit(x_train)
        vectorizer_nd.stop_words_ = None
    x_train_vec = vectorizer_nd.transform(x_train)
    return x_train_vec


def remove_all_files_folder(path_folder):
    for filename in os.listdir(path_folder):
        file_path = os.path.join(path_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def draw_pie_chart_single_predict(dict_result, filename):
    # draw chart and save
    labels = []
    probs = []
    for key, value in dict_result.items():
        labels.append(key)
        probs.append(value)
    plt.pie(probs, labels=labels)
    remove_all_files_folder(os)
    plt.savefig(get_path_fig_single_predict(filename))
