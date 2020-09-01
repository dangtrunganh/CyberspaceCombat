import json
import os

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


# model_filename = os.path.abspath(os.path.join(current_dir, os.pardir, 'app_model', 'model_classify', 'vi-model_v1_final_page.pkl'))
#
# vectorizer_filename = os.path.abspath(os.path.join(current_dir, os.pardir, 'app_model', 'model_vectorizer', 'vi-vectorizer_v1_final_page.pkl'))

# if __name__ == '__main__':
#     print(get_path_model())
#     print(get_path_vectorizer())


def read_dict_IID_label():
    with open(os.path.join(current_dir, 'dict_IID_label.json'), 'r') as f_:
        dict_content = f_.read()
        return json.loads(dict_content)


json_dict = read_dict_IID_label()


def get_label_by_IID(IID):
    return json_dict[IID]


def get_path_fig_output(child_last_folder, filename):
    '''
    :param filename:
    :return: Path of image single predict FILE
    '''
    return os.path.join(current_dir, os.pardir, os.pardir, 'app', 'static', 'output_chart', child_last_folder, filename)


def get_path_dir_fig_single_name(folder_last_child):
    '''
    :param foldername:
    :return: Path of image single predict FOLDER
    '''
    return os.path.join(current_dir, os.pardir, os.pardir, 'app', 'static', 'output_chart', folder_last_child)


def get_path_saved_folder():
    '''
    :return: Path of FOLDER upload file
    '''
    return os.path.join(current_dir, os.pardir, os.pardir, 'app', 'static', 'upload_file')


def get_path_saved_result_file(path_input_file):
    '''
    :param path_input_file:
    :return: Path of FILE NAME predicted dataframe result (csv)
    '''
    file_input_name = os.path.basename(path_input_file)
    file_output_name = 'output_predict_' + file_input_name
    return os.path.join(current_dir, os.pardir, os.pardir, 'app', 'static', 'output_result', file_output_name)


def get_path_result_from_filename(filename):
    return os.path.join(current_dir, os.pardir, os.pardir, 'app', 'static', 'output_result', filename)
