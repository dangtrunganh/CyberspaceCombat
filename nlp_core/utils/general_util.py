# -*- encoding: utf-8 -*-
import pandas as pd
import os
import joblib
import pickle
import matplotlib.pyplot as plt
import shutil
from matplotlib.ticker import MaxNLocator
from nlp_core.config.conf_params import get_path_fig_output, get_path_dir_fig_single_name
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
    '''
    :param dict_result:
    :param filename:
    :return: Chart in single predict - by category
    '''
    # draw chart and save
    remove_all_files_folder(get_path_dir_fig_single_name('image_single_predict'))
    labels = []
    probs = []
    for key, value in dict_result.items():
        labels.append(key)
        probs.append(value)

    fig1, ax1 = plt.subplots()
    ax1.pie(probs, labels=labels, autopct='%1.1f%%')
    ax1.axis('equal')

    plt.ylabel(None)
    plt.xlabel(None)
    plt.pie(probs, labels=labels)
    # remove_all_files_folder(os)
    plt.savefig(get_path_fig_output('image_single_predict', filename))


def draw_prob_number_posts(df_result, filename):
    '''
    :param df_result:
    :param filename:
    :return: Chart in files predict - by number of posts
    '''
    # draw chart and save
    remove_all_files_folder(get_path_dir_fig_single_name('output_prob_post'))
    labels = []
    count_ = []
    df_group = df_result.groupby(['category']).nunique().reset_index()
    for row in df_group.itertuples():
        labels.append(row.category)
        count_.append(row.post_id)
    # plt.figure()
    fig1, ax1 = plt.subplots()
    ax1.pie(count_, labels=labels, autopct='%1.1f%%')
    ax1.axis('equal')

    plt.ylabel(None)
    plt.xlabel(None)
    plt.pie(count_, labels=labels)
    # remove_all_files_folder(os)
    plt.savefig(get_path_fig_output('output_prob_post', filename))


def draw_prob_number_users(df_result, filename):
    '''
    :param df_result:
    :param filename:
    :return: Chart in files predict - by number of posts
    '''
    # draw chart and save
    remove_all_files_folder(get_path_dir_fig_single_name('output_prob_user'))
    labels = []
    count_ = []
    df_group = df_result.groupby(['category']).nunique().reset_index()
    for row in df_group.itertuples():
        labels.append(row.category)
        count_.append(row.author_id)

    fig1, ax1 = plt.subplots()
    ax1.pie(count_, labels=labels, autopct='%1.1f%%')
    ax1.axis('equal')

    plt.ylabel(None)
    plt.xlabel(None)
    plt.pie(count_, labels=labels)
    # remove_all_files_folder(os)
    plt.savefig(get_path_fig_output('output_prob_user', filename))


def draw_prob_number_access(df_result, filename):
    '''
    :param df_result:
    :param filename:
    :return: Chart in files predict - by number of access
    '''
    # draw chart and save
    remove_all_files_folder(get_path_dir_fig_single_name('output_prob_access'))
    df_f = df_result.groupby(['author_id']).nunique().reset_index().groupby(['post_id']).nunique().reset_index()
    df_f.rename(columns={'post_id': 'number_of_posts',
                         'author_id': 'number_of_users'}, inplace=True)
    labels = []
    x_ = []
    for row in df_f.itertuples():
        labels.append(row.number_of_posts)
        x_.append(row.number_of_users)
    print(df_f.head())
    print('----------------------')
    print('labels = {}'.format(labels))
    print('x_ = {}'.format(x_))
    ax = plt.figure().gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.ylabel('number of posts')
    plt.xlabel('number of users')
    plt.grid(True)
    plt.plot(labels, x_)
    plt.savefig(get_path_fig_output('output_prob_access', filename))


def draw_prob_each_user(df_result, filename):
    remove_all_files_folder(get_path_dir_fig_single_name('output_prob_each_user'))
    labels = []
    count_ = []
    df_group = df_result.groupby(['category']).nunique().reset_index()
    for row in df_group.itertuples():
        labels.append(row.category)
        count_.append(row.post_id)
    # plt.figure()
    fig1, ax1 = plt.subplots()
    ax1.pie(count_, labels=labels, autopct='%1.1f%%')
    ax1.axis('equal')

    plt.ylabel(None)
    plt.xlabel(None)
    plt.pie(count_, labels=labels)
    # remove_all_files_folder(os)
    print(os.path.abspath(get_path_fig_output('output_prob_each_user', filename)))
    plt.savefig(get_path_fig_output('output_prob_each_user', filename))
