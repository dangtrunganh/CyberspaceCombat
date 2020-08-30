# -*- coding: utf-8 -*-

from nlp_core.utils.general_util import _load_model, _load_vectorizer, _convert_ndarray_data
from nlp_core.config.conf_params import *
from nlp_core.utils.general_normalize import _clean_text
import pandas as pd


class PoliticClassification:
    def __init__(self):
        self.vectorizer = _load_vectorizer(get_path_vectorizer())
        self.model = _load_model(get_path_model())

    def predict_single_post(self, x_text):
        x_clean = _clean_text(x_text)
        x_np = _convert_ndarray_data(self.vectorizer, x_clean)
        x_predict = self.model.predict(x_np).squeeze().tolist()
        prob = self.model.predict_proba(x_np)[0].tolist()
        result = {get_label_by_IID(str(index)): prob[index] for index in range(0, len(x_predict)) if x_predict[index] == 1}
        # print(x_predict)
        # print(prob)
        # print(result)
        return x_clean, result

    def predict_file(self, path_file):
        df_raw = pd.read_csv(path_file, delimiter='|')
        # 1. preprocess data
        # 2. predict all data
        # write result to file

