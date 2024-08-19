from .text_processing import create_dataframe_advanced
from .similarity import group_products, update_grouped_titles

def main(df, title, product_type_dict, stopwords, color_list, attributes):
    Filtered_DF = create_dataframe_advanced(df, title, product_type_dict, stopwords, color_list, attributes)
    grouped_df = group_products(Filtered_DF)
    updated_df = update_grouped_titles(grouped_df)
    return updated_df
