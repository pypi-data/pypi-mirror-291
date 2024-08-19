import re

def advanced_cleaning(descriptions, stopwords, color_list):
    if isinstance(descriptions, str):
        descriptions = [descriptions]

    stopwords_set = set(stopwords)
    stopwords_pattern = re.compile(r'\b(' + '|'.join(re.escape(sw) for sw in stopwords_set) + r')\b', re.IGNORECASE)

    cleaned_descriptions = []

    for description in descriptions:
        if '점]' in description:
            description = description.split('점]')[-1]

        # 모든 알파벳을 대문자로 변환
        description = description.upper()

        # 괄호 내용 처리
        description, bracket_storage, bracket_color = process_brackets(description, color_list)

        # 일반 텍스트에서 용량 및 색상 추출
        general_storage = find_storage1(description)
        general_color = color_extraction1(description, color_list)

        # 최종 용량 및 색상 결정
        storage = bracket_storage if bracket_storage != 'N/A' else general_storage
        color = bracket_color if bracket_color != 'N/A' else general_color

        # 불용어 및 특수 문자 제거
        description = re.sub(r'[^A-Z0-9ㄱ-ㅎㅏ-ㅣ가-힣+\s²-]', ' ', description)
        description = stopwords_pattern.sub('', description)

        # 추가 정제: 연속된 공백 제거
        description = re.sub(r'\s+', ' ', description).strip()

        cleaned_descriptions.append({
            'cleaned_text': description,
            'storage': storage,
            'color': color
        })

    return cleaned_descriptions if len(cleaned_descriptions) > 1 else cleaned_descriptions[0]

def process_brackets(text, color_list):
    storage = 'N/A'
    color = 'N/A'

    def extract_from_bracket(match):
        nonlocal storage, color
        content = match.group(0)  # 괄호 내용 전체 캡처
        bracket_storage = find_storage1(content)
        bracket_color = color_extraction1(content, color_list)
        if bracket_storage != 'N/A':
            storage = bracket_storage
        if bracket_color != 'N/A':
            color = bracket_color
        return ''  # 괄호 내용과 괄호 기호 제거

    # 괄호 내용 처리
    bracket_pattern = r'[\(\[\{][^\)\]\}]+[\)\]\}]'
    text = re.sub(bracket_pattern, extract_from_bracket, text)

    return text, storage, color

def find_storage1(text):
    if not isinstance(text, str):
        raise TypeError("Input 'text' must be a string")
    storage_patterns = [
        r'(?:\d+\s*[GT]B\s*\+\s*)*(\d+)\s*([GT]B)',
        r'(\d+)\s*([GT]B)',
        r'(\d+)\s*(G)'
    ]
    for pattern in storage_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            storage_value = int(match.group(1))
            storage_unit = match.group(2).upper()
            if storage_unit == 'TB':
                storage_value *= 1024
            if storage_value < 64:
                return 'N/A'
            else:
                return f'{storage_value}GB'
    return 'N/A'

def color_extraction1(text, color_list):
    color_pattern = r'\b(' + '|'.join(re.escape(color) for color in color_list) + r')\b'
    match = re.search(color_pattern, text, re.IGNORECASE)
    if match:
        return match.group(1)
    else:
        return 'N/A'
