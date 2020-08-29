# -*- coding: UTF-8 -*-
import os
import re
import unicodedata
from typing import List, Dict, Any
from pyvi import ViTokenizer

__current_dir = os.path.abspath(os.path.dirname(__file__))

__word_comma_under_score = "àáảãạăằắẳẵặâầấẩẫậđđèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬĐĐÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴaaaaaaaaaaaaaaaaaddeeeeeeeeeeeiiiiiooooooooooooooooouuuuuuuuuuuyyyyyAAAAAAAAAAAAAAAAADDEEEEEEEEEEEIIIIIOOOOOOOOOOOOOOOOOUUUUUUUUUUUYYYYYa-zA-Z_\\s\\."
__word_comma_under_score_regex = "[^" + __word_comma_under_score + "]"
__word_and_comma = "àáảãạăằắẳẵặâầấẩẫậđđèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬĐĐÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴaaaaaaaaaaaaaaaaaddeeeeeeeeeeeiiiiiooooooooooooooooouuuuuuuuuuuyyyyyAAAAAAAAAAAAAAAAADDEEEEEEEEEEEIIIIIOOOOOOOOOOOOOOOOOUUUUUUUUUUUYYYYY\\w\\d!\\%\\&\\(\\)\\[\\]\\{\\}\\$#@\\-*^\\\"<\\>\\.,;`\\“\\”…'\\s\\:\\/\\\\"
__word_and_comma_regex = "[^" + __word_and_comma + "]"

__WEB_URL_REGEX = r'https?://\S+'
__REGEX_GIGABYTE = "(?i)\\b\\d+\\s*kg\\b"
__REGEX_CURRENCY = "(?i)\\b(\\d{3,}\\s*(d|đ|₫|vnd)|\\d+\\s*(k|tr))\\b|\\b#\\d+\\s*k\\b"
__REGEX_EMAIL = "[\\w\\.-]+@[\\w\\.-]+"
__REGEX_PHONE_NUMBER = "0[0-9\s.-]{9,13}"
__REGEX_HASHTAG = r'\#\S*'

__unikey_accents: List[
    str] = "à,á,ả,ã,ạ,ă,ằ,ắ,ẳ,ẵ,ặ,â,ầ,ấ,ẩ,ẫ,ậ,đ,đ,è,é,ẻ,ẽ,ẹ,ê,ề,ế,ể,ễ,ệ,ì,í,ỉ,ĩ,ị,ò,ó,ỏ,õ,ọ,ô,ồ,ố,ổ,ỗ,ộ,ơ,ờ,ớ,ở,ỡ,ợ,ù,ú,ủ,ũ,ụ,ư,ừ,ứ,ử,ữ,ự,ỳ,ý,ỷ,ỹ,ỵ,À,Á,Ả,Ã,Ạ,Ă,Ằ,Ắ,Ẳ,Ẵ,Ặ,Â,Ầ,Ấ,Ẩ,Ẫ,Ậ,Đ,Đ,È,É,Ẻ,Ẽ,Ẹ,Ê,Ề,Ế,Ể,Ễ,Ệ,Ì,Í,Ỉ,Ĩ,Ị,Ò,Ó,Ỏ,Õ,Ọ,Ô,Ồ,Ố,Ổ,Ỗ,Ộ,Ơ,Ờ,Ớ,Ở,Ỡ,Ợ,Ù,Ú,Ủ,Ũ,Ụ,Ư,Ừ,Ứ,Ử,Ữ,Ự,Ỳ,Ý,Ỷ,Ỹ,Ỵ".split(
    ",")
__non_unikey_accents: List[
    str] = "à,á,ả,ã,ạ,ă,ằ,ắ,ẳ,ẵ,ặ,â,ầ,ấ,ẩ,ẫ,ậ,đ,ð,è,é,ẻ,ẽ,ẹ,ê,ề,ế,ể,ễ,ệ,ì,í,ỉ,ĩ,ị,ò,ó,ỏ,õ,ọ,ô,ồ,ố,ổ,ỗ,ộ,ơ,ờ,ớ,ở,ỡ,ợ,ù,ú,ủ,ũ,ụ,ư,ừ,ứ,ử,ữ,ự,ỳ,ý,ỷ,ỹ,ỵ,À,Á,Ả,Ã,Ạ,Ă,Ằ,Ắ,Ẳ,Ẵ,Ặ̣,Â,Ầ,Ấ,Ẩ,Ẫ,Ậ,Đ,Ð,È,É,Ẻ,Ẽ,Ẹ,Ê,Ề,Ế,Ể,Ễ,Ệ,Ì,Í,Ỉ,Ĩ,Ị,Ò,Ó,Ỏ,Õ,Ọ,Ô,Ồ,Ố,Ổ,Ỗ,Ộ,Ơ,Ờ,Ớ,Ở,Ỡ,Ợ,Ù,Ú,Ủ,Ũ,Ụ,Ư,Ừ,Ứ,Ử,Ữ,Ự,Ỳ,Ý,Ỷ,Ỹ,Ỵ".split(
    ",")
__str_unikey_accents: str = "àáảãạăằắẳẵặâầấẩẫậđđèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬĐĐÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴ"

__map_non_unikey_to_unikey: Dict[Any, Any] = {}

__path_stopwords = os.path.abspath(os.path.join(__current_dir, os.pardir, 'config', 'stopwords-vi.txt'))


def __create_map_non_unikey_to_unikey():
    for i in range(len(__unikey_accents)):
        __map_non_unikey_to_unikey[__non_unikey_accents[i]] = __unikey_accents[i]


def __replace_special_token(input):
    if input == ".":
        return input
    # replace all special token: **&*_*_&, example: )_anh --> _anh; anh_(_to_) --> anh__to_
    input = re.sub(__word_comma_under_score_regex, '', input)

    # replace all > 1 times "_", example: __anh___to_ --> _anh_to_
    input = re.sub('[_]+', '_', input)

    # replace "_" in first word, example: _anh_to_ --> anh_to_
    input = re.sub('^[_]+', '', input)

    # replace "_" in last word, example: anh_to_ -> anh_to
    input = re.sub('[_]+$', '', input)
    return input


def __replace_str(input):
    for key, value in __map_non_unikey_to_unikey.items():
        input = input.replace(key, value)
    return input


def __reformat_content(input):
    clean_text = unicodedata.normalize('NFKC', input)
    clean_text = __replace_str(clean_text)
    clean_text = __replace_multi_space(clean_text)
    return clean_text


def __replace_multi_space(input):
    return re.sub('\\s+', ' ', input)


def __replace_currency(input):
    return re.sub(__REGEX_CURRENCY, ' numberd ', input)


def __make_boundary_punctuation(input):
    return re.sub('\\b', ' ', input)


def __replace_number_token(input):
    input = re.sub(r'\b\d+\b', ' numbertoken ', input)
    input = re.sub('(?=(?:\\S*\\d))\\S+', ' ', input)
    return input


# replace all emoji, NOT word, digit and punctuation
def replace_emoji(input):
    return re.sub(__word_and_comma_regex, '', input)


# def remove_url_email_phone_currency(input):
#     list_regex = [REGEX_EMAIL, REGEX_GIGABYTE, WEB_URL_REGEX, REGEX_HASHTAG]
#     regex_new = '|'.join(list_regex)
#     return re.sub(regex_new, '', input)

def __replace_email(input):
    return re.sub(__REGEX_EMAIL, ' emailtoken ', input)


def __replace_gigabyte(input):
    return re.sub(__REGEX_GIGABYTE, ' gigabytetoken ', input)


def __replace_url(input):
    return re.sub(__WEB_URL_REGEX, ' urltoken ', input)


def __remove_hashtag(input):
    return re.sub(__REGEX_HASHTAG, ' ', input)


def __replace_phone_number(input):
    return re.sub(__REGEX_PHONE_NUMBER, ' phonenumber ', input)


def __replace_url_email_gigabyte_phone_number_hashtag(input):
    input = __replace_email(input)
    input = __replace_url(input)
    input = __replace_phone_number(input)
    input = __remove_hashtag(input)
    input = __replace_gigabyte(input)
    return input


# replace all multi '...' --> '.'
def __replace_multi_period(input):
    # return input.replaceAll("\\.{2,}", ".")
    return re.sub('\\.{2,}', '.', input)


def __normalize(input):
    input = __reformat_content(input)
    input = __replace_currency(input)
    input = __replace_url_email_gigabyte_phone_number_hashtag(input)
    input = __replace_number_token(input)
    input = __replace_multi_period(input)
    input = __make_boundary_punctuation(input)
    input = replace_emoji(input)
    input = __replace_multi_space(input)
    input = input.strip()
    input = input.lower()
    return input


def __tokenize_sentence(input, keep_price, keep_dot, keep_number,
                        keep_url, keep_gigabyte, keep_email, keep_phone_number):
    input = '. '.join([ViTokenizer.tokenize(input_) for input_ in input.split('.')]).strip()
    input = __replace_special_token(input)
    if not keep_dot:
        input = re.sub('[.]+', '', input)
    if not keep_price:
        input = input.replace('numberd', '')
    if not keep_url:
        input = input.replace('urltoken', '')
    if not keep_gigabyte:
        input = input.replace('gigabytetoken', '')
    if not keep_email:
        input = input.replace('emailtoken', '')
    if not keep_phone_number:
        input = input.replace('phonenumber', '')
    if not keep_number:
        input = input.replace('numbertoken', '')
    input = __replace_multi_space(input)
    return input


def _clean_text(input, thres_hold=-1, keep_price=False, keep_dot=False, keep_number=True,
                keep_url=False, keep_gigabyte=False, keep_email=False, keep_phone_number=False):
    if input is not None:
        split_input = input.split(' ')
        if thres_hold != -1 and len(split_input) > thres_hold:
            input = ' '.join(split_input[:thres_hold])
        input = __normalize(input)
        result = __tokenize_sentence(input, keep_price, keep_dot, keep_number,
                                     keep_url, keep_gigabyte, keep_email, keep_phone_number)
        return result


def __read_stopwords(path_sw):
    with open(path_sw, encoding='utf-8') as f:
        return [line.strip() for line in f.readlines()]


__stop_words = __read_stopwords(__path_stopwords)


def __remove_sw(sentence):
    return ' '.join([word for word in sentence.split() if (word not in __stop_words) and len(word) < 30])


def __remove_token(in_text):
    in_text = in_text.replace('numberd', '')
    in_text = in_text.replace('urltoken', '')
    in_text = in_text.replace('gigabytetoken', '')
    in_text = in_text.replace('emailtoken', '')
    in_text = in_text.replace('phonenumber', '')
    in_text = in_text.replace('numbertoken', '')
    in_text = __remove_sw(in_text)
    in_text = re.sub('\\s+', ' ', in_text)
    in_text = in_text.strip()
    return in_text


if __name__ == '__main__':
    s = '______________________Chiều_________________ 24/8, tại Trụ__________ sở Chính phủ, Phó Thủ tướng Chính phủ Vũ Đức Đam, Trưởng Ban Chỉ đạo Quốc gia phòng, chống dịch COVID-19 chủ trì cuộc họp triển khai các biện pháp phòng, chống dịch trong giai đoạn hiện nay.'
    print(_clean_text(s))
