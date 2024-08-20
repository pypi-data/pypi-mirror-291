from konlpy.tag import Mecab
import pandas as pd
from filter_list import *
from cleaning import *
from handler import *

# Attribute call Func
def get_product_type(attributes, product_type_dict):
    def classify_type(attribute):
        if attribute in product_type_dict:
            return product_type_dict[attribute]
        else:
            return 'ETC'

    return attributes.map(classify_type)


# ETC 제목 추출 함수
def title_ETC(description):
    name = description
    return name


# IT 제목 추출 함수
def process_text(morphs, title_list):
    if not isinstance(morphs, list):
        raise TypeError("Input 'morphs' must be a list")
    if not isinstance(title_list, list):
        raise TypeError("Input 'title_list' must be a list")

    title = []
    i = 0
    plus_used = False
    while i < len(morphs):
        if morphs[i] in title_list:
            title.append(morphs[i])
            i += 1
            if i < len(morphs) and morphs[i].isdigit():
                title.append(morphs[i])
                i += 1
            if i < len(morphs) and morphs[i] == '+' and not plus_used:
                title.append(morphs[i])
                plus_used = True
                i += 1
        else:
            i += 1

    return ''.join(title).strip()

def create_dataframe_advanced(df, title, product_type_dict, stopwords, color_list, attribute):
    filtered_text = advanced_cleaning(title, stopwords, color_list)  # Data Cleaning

    extracted_title = []
    extracted_color = []
    extracted_storage = []
    mecab = Mecab()

    # Get product types for all items at once
    product_types = get_product_type(attribute, product_type_dict)

    for text, product_type in zip(filtered_text, product_types):
        if product_type == 'IT':
            mecabmorphs = mecab.morphs(text['cleaned_text'])  # 형태소 추출
            # 제목 형태소 추출
            extracted_title_temp = process_text(mecabmorphs, product_title)
            if len(extracted_title_temp.split()) <= 2:  # 추출된 제목이 2단어 이하인 경우
                extracted_title.append(text['cleaned_text'])  # 정제된 텍스트 사용
            else:
                extracted_title.append(extracted_title_temp)
            extracted_color.append(text['color'])
            extracted_storage.append(text['storage'])
        else:
            extracted_title.append(title_ETC(text['cleaned_text']))
            extracted_color.append(text['color'])
            extracted_storage.append('N/A')

    # 제목에서 색상과 용량 정보 제거
    for i in range(len(extracted_title)):
        if extracted_color[i] != 'N/A':
            extracted_title[i] = extracted_title[i].replace(extracted_color[i], '').strip()
        if extracted_storage[i] != 'N/A':
            extracted_title[i] = extracted_title[i].replace(extracted_storage[i], '').strip()

    # Convert lists to Series
    extracted_title = pd.Series(extracted_title)
    extracted_color = pd.Series(extracted_color)
    extracted_storage = pd.Series(extracted_storage)
    extracted_type = pd.Series(product_types)
    original_title = pd.Series(df["DESCRIPTION"])
    dfattributes = pd.Series(attribute)

    cleaned_df = pd.DataFrame({
        'COLOR': extracted_color,
        'STORAGE': extracted_storage,
        'Type': extracted_type,
        'Classification' : dfattributes,
        'Original': original_title,
        'TITLE': extracted_title
        })

    return cleaned_df