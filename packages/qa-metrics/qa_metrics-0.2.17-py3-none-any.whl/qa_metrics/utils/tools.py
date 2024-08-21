import string
import contractions
import requests
import os
import regex
from datetime import datetime

def fix_answer(s):
        def remove_articles(text):
            return regex.sub(r'\b(a|an|the)\b', ' ', text)

        def white_space_fix(text):
            return ' '.join(text.split())

        def remove_punc(text):
            exclude = set(string.punctuation)
            return ''.join(ch for ch in text if ch not in exclude)

        def lower(text):
            return text.lower()

        return white_space_fix(remove_articles(remove_punc(lower(s))))

def normalize_answer(text, lower=True):
    if isinstance(text, list):
        result = []
        for ele in text:
            ele = str(ele)
            if lower:
                ele = ele.lower()
            translator = str.maketrans('', '', string.punctuation)
            ele = ele.translate(translator)
            result.append(fix_answer(' '.join(ele.split())))
        return result
    else:
        text = str(text)
        if lower:
            text = text.lower()
        translator = str.maketrans('', '', string.punctuation)
        text = text.translate(translator)
        return fix_answer(' '.join(text.split()))

def calculate_f1_score_with_precision(str1, str2):
    # Split the strings into sets of words
    str1 = fix_answer(contractions.fix(normalize_answer(str1)))
    str2 = fix_answer(contractions.fix(normalize_answer(str2)))
    words_str1 = set(str1.split())
    words_str2 = set(str2.split())

    # Calculate true positives, false positives, and false negatives
    tp = len(words_str1.intersection(words_str2))
    fp = len(words_str1 - words_str2)
    fn = len(words_str2 - words_str1)

    # Calculate precision and recall
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0

    # Calculate F1 score
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return f1_score, precision, recall

def remove_punctuation(text):
    def remove_articles(text):
        return regex.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        try:
            return text.lower()
        except:
            return ''

    return white_space_fix(remove_articles(remove_punc(lower(text))))

def download_link(file, url, name):
    # if not os.path.isfile(file):
    # print("Downloading {}...".format(name))
    try:
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            with open(file, 'wb') as f:
                f.write(response.content)
                # print("Download {} complete.".format(name))
        else:
            print("Failed to download the model. Status code:", response.status_code)
    except:
        if not os.path.isfile(file):
            print("Failed to download the model. Check your internet connection.")


def file_needs_update(url, file_path):
    """
    Check if the file at the given path needs to be updated based on the
    Last-Modified header from the file URL.
    """
    try:
        response = requests.head(url)
        if response.status_code == 200 and 'Last-Modified' in response.headers:
            remote_last_modified = requests.utils.parsedate_to_datetime(response.headers['Last-Modified'])
            if not os.path.exists(file_path):
                return True  # File does not exist, needs download.
            local_last_modified = datetime.fromtimestamp(os.path.getmtime(file_path), tz=remote_last_modified.tzinfo)
            return remote_last_modified > local_last_modified
    except requests.RequestException as e:
        # print(f"Error checking if file needs update: {e}")
        pass
    return False  # Default to not updating if we can't determine.