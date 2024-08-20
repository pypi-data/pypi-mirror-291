from rapidfuzz import fuzz, process

def custom_ratio(s1, s2, score_cutoff=0):
    # 공백을 제거한 문자열로 비교하되, 원본 문자열은 변경하지 않음
    return fuzz.ratio(s1.replace(" ", ""), s2.replace(" ", ""), score_cutoff=score_cutoff)

def group_products(df, it_threshold=96, etc_threshold=95):
    # IT / ETC 제품간 임계값 설정
    product_names = df['TITLE'].tolist()
    grouped_names = []
    scores = []

    for index, row in df.iterrows():
        threshold = it_threshold if row['Type'] == 'IT' else etc_threshold

        product_name = row['TITLE']
        best_match = None
        best_score = 0

        for grouped_name in grouped_names:
            score = custom_ratio(product_name, grouped_name)
            if score >= threshold and score > best_score:
                best_match = grouped_name
                best_score = score

        if best_match:
            grouped_names.append(best_match)
            scores.append(best_score)
        else:
            grouped_names.append(product_name)
            scores.append(100)

    df['Grouped Name'] = grouped_names
    df['Score'] = scores
    return df

def update_grouped_titles(df):
    # Get unique group names
    unique_group_names = df['Grouped Name'].unique()

    # Create a dictionary to store representative names for each group
    representative_names = {}

    for group_name in unique_group_names:
        # Get rows belonging to the current group
        group = df[df['Grouped Name'] == group_name]

        # Count the frequency of each title within the group
        title_counts = group['TITLE'].value_counts()

        # Select the most frequent title as the representative name
        representative_name = title_counts.index[0]

        # Store the representative name for the current group
        representative_names[group_name] = representative_name

    # Update the 'Grouped Name' column with representative names
    df['Grouped Name'] = df['Grouped Name'].map(representative_names)

    # Calculate the score between original title and representative name
    df['Score'] = df.apply(lambda row: custom_ratio(row['TITLE'], row['Grouped Name']), axis=1)

    # Check if the title has been modified
    df['Modified'] = df['TITLE'] != df['Grouped Name']

    return df
