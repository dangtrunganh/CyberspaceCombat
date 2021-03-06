import json
import os
import pandas as pd

current_dir = os.path.abspath(os.path.dirname(__file__))


def read_config_file():
    with open(os.path.join(current_dir, 'config.json'), 'r') as f_:
        config_content = f_.read()
        return json.loads(config_content)


json_content = read_config_file()


def get_path_model():
    return os.path.abspath(
        os.path.join(current_dir, os.pardir, 'model', 'model_classify', json_content['model_classify']))


def get_path_vectorizer():
    return os.path.abspath(
        os.path.join(current_dir, os.pardir, 'model', 'model_vectorizer', json_content['model_vectorizer']))


def get_path_bow_rule_classification():
    return os.path.abspath(
        os.path.join(current_dir, os.pardir, 'model', 'rule_classification', json_content['model_bow_classify']))


def get_path_tree_rule_classification():
    return os.path.abspath(
        os.path.join(current_dir, os.pardir, 'config', 'keyword_label.csv'))


def read_dict_IID_label():
    with open(os.path.join(current_dir, 'dict_IID_label.json'), 'r') as f_:
        dict_content = f_.read()
        return json.loads(dict_content)


def read_dict_IID_threshold():
    df_tree = pd.read_csv(get_path_tree_rule_classification(), delimiter='|')
    dict_id_prob = {}
    for row in df_tree.itertuples():
        dict_id_prob[row.id] = row.threshold_proba
    return dict_id_prob
    # with open(os.path.join(current_dir, 'dict_IID_label.json'), 'r') as f_:
    #     dict_content = f_.read()
    #     return json.loads(dict_content)


json_dict = read_dict_IID_label()
dict_tree_id_threshold_proba = read_dict_IID_threshold()


def get_label_by_IID(IID):
    return json_dict[IID]


def get_max_label_each_post():
    return json_content['max_label_each_post']


def get_path_fig_output(child_last_folder, filename):
    '''
    :param filename:
    :return: Path of image single predicted file
    '''
    return os.path.join(current_dir, os.pardir, os.pardir, 'app', 'static', 'output_chart', child_last_folder, filename)


def get_path_dir_fig_single_name(folder_last_child):
    '''
    :param foldername:
    :return: Path of image single predict folder
    '''
    return os.path.join(current_dir, os.pardir, os.pardir, 'app', 'static', 'output_chart', folder_last_child)


def get_path_saved_folder():
    '''
    :return: Path of folder upload file
    '''
    return os.path.join(current_dir, os.pardir, os.pardir, 'app', 'static', 'upload_file')


def get_path_saved_result_file(path_input_file):
    '''
    :param path_input_file:
    :return: Path of file name predicted dataframe result (csv)
    '''
    file_input_name = os.path.basename(path_input_file)
    file_output_name = 'output_predict_' + file_input_name
    return os.path.join(current_dir, os.pardir, os.pardir, 'app', 'static', 'output_result', file_output_name)


def get_path_result_from_filename(filename):
    return os.path.join(current_dir, os.pardir, os.pardir, 'app', 'static', 'output_result', filename)
