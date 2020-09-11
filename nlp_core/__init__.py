# -*- coding: utf-8 -*-

from nlp_core.utils.general_util import _load_model, _load_vectorizer, _convert_ndarray_data, \
    _load_bow_rule_classification, _load_tree_rule_classification
from nlp_core.config.conf_params import *
from nlp_core.utils.general_normalize import _clean_text
import numpy as np
import pandas as pd
import pickle


class PoliticClassification:
    def __init__(self):
        self.vectorizer = _load_vectorizer(get_path_vectorizer())
        self.model = _load_model(get_path_model())
        self.rule_classifier = RuleClassification()
        self.max_label = get_max_label_each_post()

    def keep_top_value_in_dict(self, input_dict, remain_label_count):
        # remain_label_count always >= 1
        # input_dict: {'0': 0,9, '1': 0,8,...}
        # output: {'0': 0,9, '4': 0,8,...} # keep each items by rule after
        # keep only label which accept threshold_proba
        dict_sorted_top5 = {k: v for k, v in
                            sorted(list(input_dict.items()), key=lambda x: x[1], reverse=True)[:remain_label_count]}
        dict_temp = {}
        for k, v in dict_sorted_top5.items():
            if v >= dict_tree_id_threshold_proba[k]:
                dict_temp[k] = v
        if remain_label_count == self.max_label and len(dict_temp) == 0:
            # There is not any label classified by rule
            # no id accept -> return empty dict
            # return top items in dict
            return {list(input_dict)[0]: input_dict[list(input_dict)[0]]}
            # There is at least 1 label classified by rule
        return dict_temp

    def predict_single_post(self, x_text):
        # result = {'category': 'Tham nhũng', 'prob': 0.96, 'content_clean': 'truong_hoc cua toi dag co nan tham_nhung'}
        if type(x_text) != str:
            return '', {}
        x_clean = _clean_text(x_text)

        # 1. classify by rule
        dict_result_rule = self.rule_classifier.predict_rule(x_clean)
        if len(dict_result_rule) >= self.max_label:
            # if catch 5 iid by rule --> return
            return dict_result_rule

        # 2. classify by ml - if result classified by rule < max_label
        remain_label = self.max_label - len(dict_result_rule)  # always >= 1

        x_np = _convert_ndarray_data(self.vectorizer, x_clean)
        # x_predict = self.model.predict(x_np).squeeze().tolist()
        prob = self.model.predict_proba(x_np)[0].tolist()
        # print(prob)
        # result = {get_label_by_IID(str(index)): prob[index] for index in range(0, len(x_predict)) if
        #           x_predict[index] == 1}
        # 1. sort dict
        dict_prob = {i: v for i, v in enumerate(prob) if
                     i not in dict_result_rule}  # filtering label which is in dict_result_rule

        print('before filter: {}'.format(dict_prob))
        dict_result_ml = self.keep_top_value_in_dict(dict_prob, remain_label)

        # merge 2 dict
        dict_result_rule.update(dict_result_ml)
        result = {get_label_by_IID(str(k)): v for k, v in dict_result_rule.items()}
        return x_clean, result

    def predict_file(self, df_raw, path_result):
        # 1. preprocess data
        # 2. predict all data
        # write result to file
        return pd.DataFrame()


class RuleClassification:
    def __init__(self):
        self.vectorizer = _load_bow_rule_classification(get_path_bow_rule_classification())
        # self.full_tree = _load_tree_rule_classification(get_path_tree_rule_classification())

    def filter_except_single(self, dictionary, bow, df_col_content, except_keywords):
        word_idx = []
        for word in except_keywords:
            try:
                word_idx.append(dictionary[word])
            except:
                pass
        keyword_matched = bow[:, word_idx]
        number_of_matches = np.sum(keyword_matched.todense(), axis=1)
        mask = np.atleast_1d(np.array(number_of_matches >= 1).squeeze())
        res = df_col_content[~mask], bow[~mask]
        return res

    def filtering_single(self, keywords, dictionary, bow, df_col_content, threshold=2, except_keywords=[]):
        word_idx = []
        if len(except_keywords) > 0:
            df_col_content, bow = self.filter_except_single(dictionary, bow, df_col_content, except_keywords)
        for word in keywords:
            try:
                word_idx.append(dictionary[word])
            except:
                pass
        keyword_matched = bow[:, word_idx]
        number_of_matches = np.sum(keyword_matched.todense(), axis=1)
        mask = np.atleast_1d(np.array(number_of_matches >= threshold).squeeze())
        res = df_col_content[mask]
        return res

    def predict_rule(self, clean_content):
        # result = []
        dict_result = {}
        # preprocess content
        # clean_content = _clean_text(content)
        df_in = pd.DataFrame([{'clean_content': clean_content}])
        # ===================
        # vectorizer = pickle.load(open(output_bow, 'rb'))
        dictionary = self.vectorizer.vocabulary_
        bow = self.vectorizer.transform(df_in["clean_content"])
        full_tree = _load_tree_rule_classification(get_path_tree_rule_classification())
        for itr_branch in full_tree:
            itr_branch.df_content = self.filtering_single(itr_branch.keywords, dictionary, bow,
                                                          df_in['clean_content'], itr_branch.pass_threshold,
                                                          itr_branch.except_keywords)
            print('id_itr = {}, len - number of posts = {}'.format(itr_branch.id, len(itr_branch.df_content)))
            if itr_branch.df_content is not None:
                if len(itr_branch.df_content) > 0:
                    # result.append(itr_branch.id)
                    dict_result[itr_branch.id] = 1
        return dict_result


if __name__ == '__main__':
    # text = 'donald trump,trump,tập_cận_bình,đảng dân_chủ,đảng cộng_hoà,biểu_tình hồng_kông,. 4 ca này điều trị tại Bệnh viện đa khoa khu vực Quảng Nam là BN 644 (SN 1985), BN 645 (SN 1953, cùng trú xã Điện Hồng, thị xã Điện Bàn), BN 859 (SN 1973, trú khối phố 1, phường Phước Hòa, TP Tam Kỳ) và BN 934 (SN 1985, trú khối Tân Lập, phường Tân An, TP Hội An). Trong đó, BN 645 là mẹ của BN 644. Còn BN 859 là mẹ của BN 841 (được công bố xuất viện vào hôm qua 7/9). vườn rau lộc_hưng,thu_hồi đất,bồi_thường đất_đai,tranh_chấp đất_đai,khiếu_kiện đất_đai,thu_hồi đất,vụ án đồng_tâm,vườn rau lộc_hưng,thủ thiêm,phú_lương,đất_đai,tái_định_cư'
    text = ' donald trump,trump Hôm nay tôi đi học nhưng tham nhũng đang xảy ra khá lớn'
    # rc = RuleClassification()
    # print(rc.predict_rule(text))

    pc = PoliticClassification()
    clean_, value_ = pc.predict_single_post(text)
    print(clean_)
    print(value_)
