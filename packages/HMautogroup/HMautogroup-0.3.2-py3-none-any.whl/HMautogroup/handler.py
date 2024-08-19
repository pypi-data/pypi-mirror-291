def handle_process_text_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AttributeError:
            print("MeCab object 'mecab' is not defined or doesn't have 'morphs' method")
            return "", ""
        except Exception as e:
            print(f"An error occurred in process_text: {str(e)}")
            return "", ""
    return wrapper

def handle_find_storage_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred in find_storage: {str(e)}")
            return 'N/A', 'N/A'
    return wrapper