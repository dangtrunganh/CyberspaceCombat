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


def get_path_fig_single_predict(filename):
    return os.path.join(current_dir, os.pardir, os.pardir, 'app', 'static', 'output_chart', filename)


def get_path_dir_fig_single_name(foldername):
    return os.path.join(current_dir, os.pardir, os.pardir, 'app', 'static', 'output_chart')
